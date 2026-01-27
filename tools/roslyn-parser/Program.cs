using System.Collections.Concurrent;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using System.Xml.Linq;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.CodeAnalysis;
using Microsoft.Build.Locator;
using Microsoft.Build.Evaluation;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.VisualBasic;
using CS = Microsoft.CodeAnalysis.CSharp.Syntax;
using VB = Microsoft.CodeAnalysis.VisualBasic.Syntax;
using Parquet;
using Parquet.Data;
using Parquet.Serialization;

namespace RoslynParser;

// Basic ORM/ADO patterns to classify data access
public record DataAccessPattern(string Name, string[] TypePrefixes, string[] MemberNames, bool IsStoredProc);

public static class Program
{
    private static readonly bool VerboseLog =
        string.Equals(Environment.GetEnvironmentVariable("ROSLYN_VERBOSE_LOG"), "1", StringComparison.OrdinalIgnoreCase);

    private static readonly HashSet<string> SourceExtensions = new(StringComparer.OrdinalIgnoreCase)
    {
        ".cs",
        ".csx",
        ".vb",
        ".vbx",
        ".bas",
    };

    private static readonly HashSet<string> DefaultExcludedDirectories = new(StringComparer.OrdinalIgnoreCase)
    {
        "bin",
        "obj",
    };

    private static void Log(string message)
    {
        if (!VerboseLog) return;
        WriteError(message);
    }

    private static void WriteError(string message)
    {
        Console.Error.WriteLine(message);
        Console.Error.Flush();
    }

    private static readonly DataAccessPattern[] DataAccessPatterns =
    [
        // ADO.NET
        new DataAccessPattern("ado:command", ["System.Data.SqlClient.SqlCommand", "Microsoft.Data.SqlClient.SqlCommand"], ["ExecuteNonQuery", "ExecuteReader", "ExecuteScalar", "ExecuteXmlReader"], false),
        new DataAccessPattern("ado:proc", ["System.Data.SqlClient.SqlCommand", "Microsoft.Data.SqlClient.SqlCommand"], ["ExecuteNonQuery", "ExecuteReader", "ExecuteScalar", "ExecuteXmlReader"], true),
        // Entity Framework Core
        new DataAccessPattern("ef:fromsql", ["Microsoft.EntityFrameworkCore.DbSet", "Microsoft.EntityFrameworkCore.RelationalQueryableExtensions"], ["FromSql", "FromSqlInterpolated", "FromSqlRaw"], false),
        new DataAccessPattern("ef:exec", ["Microsoft.EntityFrameworkCore.DatabaseFacade"], ["ExecuteSql", "ExecuteSqlRaw", "ExecuteSqlInterpolated"], false),
        // Dapper
        new DataAccessPattern("dapper:query", ["System.Data.IDbConnection"], ["Query", "QueryAsync", "QueryFirst", "QueryFirstAsync", "QuerySingle", "QuerySingleAsync", "QueryMultiple"], false),
        new DataAccessPattern("dapper:execute", ["System.Data.IDbConnection"], ["Execute", "ExecuteAsync"], false),
        // NHibernate
        new DataAccessPattern("nhibernate:sql", ["NHibernate.ISession"], ["CreateSQLQuery", "GetNamedQuery"], false),
    ];

    public static int Main(string[] args)
    {
        var options = ParseArgs(args);
        var ingestionConfigPath = options.IngestionConfigPath;
        var outputPath = options.OutputPath;
        var targetPaths = options.TargetPaths;
        var format = NormalizeFormat(options.OutputFormat);
        if (targetPaths.Count == 0)
        {
            WriteError("Usage: roslyn-parser [--ingestion-config <path>] <file-or-dir> [more files/dirs]");
            return 1;
        }

        var ingestionConfig = LoadIngestionConfig(ingestionConfigPath);
        var resolvedTargets = ResolvePaths(targetPaths, ingestionConfig);
        if (resolvedTargets.Count == 0)
        {
            WriteError("No valid targets to parse.");
            return 1;
        }

        var results = new List<TargetParseResult>();
        foreach (var target in resolvedTargets)
        {
            if (Directory.Exists(target))
            {
                var solutions = FindSolutions(target, ingestionConfig);
                if (solutions.Count == 0)
                {
                    Log($"directory_no_solutions path={target}");
                    continue;
                }
                foreach (var sln in solutions)
                {
                    results.Add(new TargetParseResult(sln, ParseSingle(sln, ingestionConfig)));
                }
                continue;
            }

            results.Add(new TargetParseResult(target, ParseSingle(target, ingestionConfig)));
        }

        if (results.Count == 0)
        {
            WriteError("No parse results generated.");
            return 1;
        }

        if (format is "parquet" or "pq")
        {
            var ok = WriteParquetResults(results, outputPath, ingestionConfig);
            return ok ? 0 : 1;
        }

        WriteResult(results, outputPath);
        return 0;
    }

    private static string NormalizeFormat(string? format)
    {
        if (string.IsNullOrWhiteSpace(format))
        {
            return "json";
        }
        return format.Trim().ToLowerInvariant();
    }

    private static void WriteResult(List<TargetParseResult> results, string? outputPath)
    {
        var options = new JsonSerializerOptions
        {
            WriteIndented = false
        };
        if (results.Count == 1)
        {
            WriteSingleResult(results[0].Result, outputPath, options);
            return;
        }

        WriteMultipleResults(results, outputPath, options);
    }

    private static void WriteSingleResult(ParseResult aggregate, string? outputPath, JsonSerializerOptions options)
    {
        if (string.IsNullOrWhiteSpace(outputPath))
        {
            var stdout = Console.OpenStandardOutput();
            JsonSerializer.Serialize(stdout, aggregate, options);
            stdout.Flush();
            Console.Out.WriteLine();
            Console.Out.Flush();
            return;
        }

        try
        {
            var fullPath = Path.GetFullPath(outputPath);
            var dir = Path.GetDirectoryName(fullPath);
            if (!string.IsNullOrEmpty(dir) && !Directory.Exists(dir))
            {
                Directory.CreateDirectory(dir);
            }

            using var file = File.Create(fullPath);
            JsonSerializer.Serialize(file, aggregate, options);
            file.Flush(true);
            Log($"write_output file={fullPath} bytes={file.Length}");
        }
        catch (Exception ex)
        {
            WriteError($"write_output_failed path={outputPath} error={ex.Message}");
            var stdout = Console.OpenStandardOutput();
            JsonSerializer.Serialize(stdout, aggregate, options);
            stdout.Flush();
            Console.Out.WriteLine();
            Console.Out.Flush();
        }
    }

    private static void WriteMultipleResults(
        List<TargetParseResult> results,
        string? outputPath,
        JsonSerializerOptions options)
    {
        var writeToStdout = string.IsNullOrWhiteSpace(outputPath);
        Stream? stream = null;
        try
        {
            if (writeToStdout)
            {
                stream = Console.OpenStandardOutput();
            }
            else
            {
                var fullPath = Path.GetFullPath(outputPath!);
                var dir = Path.GetDirectoryName(fullPath);
                if (!string.IsNullOrEmpty(dir) && !Directory.Exists(dir))
                {
                    Directory.CreateDirectory(dir);
                }

                stream = File.Create(fullPath);
            }

            foreach (var result in results)
            {
                JsonSerializer.Serialize(
                    stream,
                    TargetParseResult.Flatten(result),
                    options);
                stream.WriteByte((byte)'\n');
            }
            stream.Flush();
            Log($"write_output count={results.Count} path={outputPath ?? "stdout"}");
        }
        catch (Exception ex)
        {
            WriteError($"write_output_failed path={outputPath} error={ex.Message}");
            if (!writeToStdout && stream is FileStream fileStream)
            {
                try { fileStream.Dispose(); } catch { /* ignore */ }
                stream = null;
            }
            var stdout = Console.OpenStandardOutput();
            foreach (var result in results)
            {
                JsonSerializer.Serialize(stdout, TargetParseResult.Flatten(result), options);
                stdout.WriteByte((byte)'\n');
            }
            stdout.Flush();
        }
        finally
        {
            if (!writeToStdout && stream is FileStream fileStream)
            {
                fileStream.Dispose();
            }
            else if (writeToStdout)
            {
                stream?.Flush();
            }
        }
    }

    private static bool WriteParquetResults(List<TargetParseResult> results, string? outputPath, IngestionConfig? ingestionConfig)
    {
        var outputRoot = ResolveOutputRoot(outputPath, ingestionConfig);
        var runId = ResolveRunId(ingestionConfig?.RunId, outputRoot);
        var artifactVersion = ingestionConfig?.ArtifactVersion ?? 1;
        var createdAt = DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ss'Z'");
        var stageRoot = Path.Combine(outputRoot, runId, "stage_1");
        var symbolsDir = Path.Combine(stageRoot, "symbols", $"run_id={runId}", $"artifact_version={artifactVersion}");
        var callsDir = Path.Combine(stageRoot, "calls", $"run_id={runId}", $"artifact_version={artifactVersion}");
        Directory.CreateDirectory(symbolsDir);
        Directory.CreateDirectory(callsDir);
        var symbolsPath = Path.Combine(symbolsDir, "symbols-0.parquet");
        var callsPath = Path.Combine(callsDir, "calls-0.parquet");

        var symbolRows = new List<SymbolGraphRow>();
        var callRows = new List<CallGraphRow>();

        foreach (var result in results)
        {
            foreach (var sym in result.Result.Symbols)
            {
                symbolRows.Add(new SymbolGraphRow
                {
                    SymbolId = sym.SymbolId,
                    Name = sym.Name,
                    Kind = sym.Kind,
                    Signature = sym.Signature,
                    FilePath = sym.FilePath,
                    Line = sym.Line,
                    SourceRef = sym.SourceRef,
                    RunId = runId,
                    ArtifactVersion = artifactVersion,
                    CreatedAt = createdAt,
                    SliceId = null,
                    SupersedesVersion = null
                });
            }

            foreach (var call in result.Result.Calls)
            {
                callRows.Add(new CallGraphRow
                {
                    CallerId = call.CallerId,
                    CalleeId = call.CalleeId,
                    FilePath = call.FilePath,
                    Line = call.Line,
                    SourceRef = call.SourceRef,
                    RunId = runId,
                    ArtifactVersion = artifactVersion,
                    CreatedAt = createdAt,
                    SliceId = null,
                    SupersedesVersion = null
                });
            }
        }

        try
        {
            using (var symStream = File.Create(symbolsPath))
            {
                ParquetSerializer.SerializeAsync(symbolRows, symStream).GetAwaiter().GetResult();
            }

            using (var callStream = File.Create(callsPath))
            {
                ParquetSerializer.SerializeAsync(callRows, callStream).GetAwaiter().GetResult();
            }

            CallRow.PrintCallStats();
            Log($"write_parquet root={outputRoot} run_id={runId} symbols={symbolRows.Count} calls={callRows.Count}");
            return true;
        }
        catch (Exception ex)
        {
            WriteError($"write_parquet_failed root={outputRoot} error={ex.Message}");
            return false;
        }
    }

    private static string ResolveOutputRoot(string? outputPath, IngestionConfig? ingestionConfig)
    {
        if (!string.IsNullOrWhiteSpace(outputPath))
        {
            var full = Path.GetFullPath(outputPath);
            if (full.EndsWith(".parquet", StringComparison.OrdinalIgnoreCase))
            {
                var dir = Path.GetDirectoryName(full);
                return string.IsNullOrEmpty(dir) ? Directory.GetCurrentDirectory() : dir;
            }
            return full;
        }

        if (!string.IsNullOrWhiteSpace(ingestionConfig?.OutputRoot))
        {
            return Path.GetFullPath(ingestionConfig.OutputRoot);
        }

        return Path.GetFullPath(Path.Combine(Directory.GetCurrentDirectory(), "data", "parquet"));
    }

    private static string ResolveRunId(string? requestedRunId, string outputRoot)
    {
        Directory.CreateDirectory(outputRoot);
        if (!string.IsNullOrWhiteSpace(requestedRunId)
            && !string.Equals(requestedRunId, "auto", StringComparison.OrdinalIgnoreCase))
        {
            var explicitDir = Path.Combine(outputRoot, requestedRunId);
            Directory.CreateDirectory(explicitDir);
            PersistLatestRun(outputRoot, requestedRunId);
            return requestedRunId;
        }

        var latestFile = Path.Combine(outputRoot, "LATEST_RUN");
        try
        {
            if (File.Exists(latestFile))
            {
                var value = File.ReadAllText(latestFile).Trim();
                if (!string.IsNullOrWhiteSpace(value))
                {
                    return value;
                }
            }
        }
        catch (Exception ex)
        {
            Log($"read_latest_run_failed root={outputRoot} error={ex.Message}");
        }

        var runId = $"run_{DateTime.UtcNow:yyyyMMddHHmmss}";
        var runDir = Path.Combine(outputRoot, runId);
        Directory.CreateDirectory(runDir);
        PersistLatestRun(outputRoot, runId);
        return runId;
    }

    private static void PersistLatestRun(string outputRoot, string runId)
    {
        try
        {
            var latestFile = Path.Combine(outputRoot, "LATEST_RUN");
            File.WriteAllText(latestFile, runId);
        }
        catch (Exception ex)
        {
            Log($"persist_latest_run_failed root={outputRoot} error={ex.Message}");
        }
    }

    private static ParseOptions ParseArgs(string[] args)
    {
        string? ingestionConfigPath = Environment.GetEnvironmentVariable("ROSLYN_INGESTION_CONFIG");
        string? outputPath = Environment.GetEnvironmentVariable("ROSLYN_OUTPUT_PATH");
        string? outputFormat = Environment.GetEnvironmentVariable("ROSLYN_OUTPUT_FORMAT");
        var targetPaths = new List<string>();
        for (var i = 0; i < args.Length; i++)
        {
            var arg = args[i];
            if (arg is "--ingestion-config" or "--config")
            {
                if (i + 1 < args.Length)
                {
                    ingestionConfigPath = args[i + 1];
                    i++;
                    continue;
                }
                WriteError("--ingestion-config requires a path");
                return new ParseOptions(ingestionConfigPath, outputPath, outputFormat, new List<string>());
            }

            if (arg is "--output" or "--out")
            {
                if (i + 1 < args.Length)
                {
                    outputPath = args[i + 1];
                    i++;
                    continue;
                }
                WriteError("--output requires a path");
                return new ParseOptions(ingestionConfigPath, outputPath, outputFormat, new List<string>());
            }

            if (arg is "--format" or "--output-format" or "--out-format")
            {
                if (i + 1 < args.Length)
                {
                    outputFormat = args[i + 1];
                    i++;
                    continue;
                }
                WriteError("--format requires a value (json|parquet)");
                return new ParseOptions(ingestionConfigPath, outputPath, outputFormat, new List<string>());
            }

            targetPaths.Add(arg);
        }

        return new ParseOptions(ingestionConfigPath, outputPath, outputFormat, targetPaths);
    }

    private sealed record ParseOptions(string? IngestionConfigPath, string? OutputPath, string? OutputFormat, List<string> TargetPaths);

    private static List<string> ResolvePaths(IEnumerable<string> paths, IngestionConfig? config)
    {
        var resolved = new List<string>();
        foreach (var path in paths)
        {
            var full = ResolvePath(path, config);
            if (File.Exists(full) || Directory.Exists(full))
            {
                resolved.Add(full);
            }
            else
            {
                Log($"target_missing path={path} resolved={full}");
            }
        }
        return resolved;
    }

    private static string ResolvePath(string path, IngestionConfig? config)
    {
        if (Path.IsPathRooted(path))
        {
            return path;
        }

        if (!string.IsNullOrWhiteSpace(config?.InputRoot))
        {
            var candidate = Path.Combine(config.InputRoot, path);
            if (File.Exists(candidate) || Directory.Exists(candidate))
            {
                return Path.GetFullPath(candidate);
            }
        }

        return Path.GetFullPath(path);
    }

    private static IngestionConfig? LoadIngestionConfig(string? path)
    {
        var configPath = path;
        if (string.IsNullOrWhiteSpace(configPath))
        {
            configPath = "config/ingestion.json";
        }
        var resolved = Path.GetFullPath(configPath);
        if (!File.Exists(resolved))
        {
            Log($"ingestion_config missing path={resolved}");
            return null;
        }

        try
        {
            var json = File.ReadAllText(resolved);
            var config = JsonSerializer.Deserialize<IngestionConfig>(
                json,
                new JsonSerializerOptions { PropertyNameCaseInsensitive = true }
            );
            if (config == null)
            {
                Log($"ingestion_config parse_failed path={resolved}");
                return null;
            }
            if (!string.IsNullOrWhiteSpace(config.InputRoot))
            {
                config.InputRoot = Path.GetFullPath(config.InputRoot);
            }
            if (!string.IsNullOrWhiteSpace(config.OutputRoot))
            {
                config.OutputRoot = Path.GetFullPath(config.OutputRoot);
            }
            Log($"ingestion_config loaded path={resolved}");
            return config;
        }
        catch (Exception ex)
        {
            Log($"ingestion_config error path={resolved} error={ex.Message}");
            return null;
        }
    }

    private static ParseResult ParseSingle(string filePath, IngestionConfig? ingestionConfig)
    {
        if (!File.Exists(filePath))
        {
            Log($"file_missing path={filePath}");
            return EmptyResult();
        }

        var extension = Path.GetExtension(filePath).ToLowerInvariant();
        var text = File.ReadAllText(filePath);
        Log($"roslyn_start file={filePath}");

        var result = extension switch
        {
            ".cs" => ParseCSharp(filePath, text),
            ".vb" => ParseVisualBasic(filePath, text),
            ".sln" => ParseSolution(filePath, text, ingestionConfig),
            ".csproj" => ParseProject(filePath, text, parseCompileItems: true, ingestionConfig),
            ".vbproj" => ParseProject(filePath, text, parseCompileItems: true, ingestionConfig),
            ".vsproj" => ParseProject(filePath, text, parseCompileItems: true, ingestionConfig),
            ".slnf" => ParseSolution(filePath, text, ingestionConfig),
            _ => EmptyResult()
        };
        Log($"roslyn_done file={filePath}");
        return result;
    }

    private static List<string> FindSolutions(string root, IngestionConfig? ingestionConfig)
    {
        var solutions = new List<string>();
        if (!Directory.Exists(root))
        {
            return solutions;
        }

        var excludedDirs = BuildExcludedDirSet(ingestionConfig);
        var stack = new Stack<string>();
        stack.Push(root);

        while (stack.Count > 0)
        {
            var current = stack.Pop();
            IEnumerable<string> subDirs;
            try
            {
                subDirs = Directory.EnumerateDirectories(current);
            }
            catch (Exception ex)
            {
                Log($"solution_scan skip_dir path={current} error={ex.Message}");
                continue;
            }

            foreach (var dir in subDirs)
            {
                var name = Path.GetFileName(dir);
                if (string.IsNullOrEmpty(name)) continue;
                if (excludedDirs.Contains(name)) continue;
                stack.Push(dir);
            }

            IEnumerable<string> files;
            try
            {
                files = Directory.EnumerateFiles(current);
            }
            catch (Exception ex)
            {
                Log($"solution_scan skip_files path={current} error={ex.Message}");
                continue;
            }

            foreach (var file in files)
            {
                var ext = Path.GetExtension(file);
                if (ext.Equals(".sln", StringComparison.OrdinalIgnoreCase)
                    || ext.Equals(".slnf", StringComparison.OrdinalIgnoreCase))
                {
                    solutions.Add(file);
                }
            }
        }

        Log($"solution_scan done root={root} count={solutions.Count}");
        return solutions;
    }

    private static ParseResult EmptyResult()
    {
        return new ParseResult();
    }

    private static ParseResult ParseCSharp(string filePath, string text)
    {
        var tree = CSharpSyntaxTree.ParseText(text);
        var root = tree.GetRoot();
        var compilation = BuildCSharpCompilation(tree);
        var semanticModel = compilation.GetSemanticModel(tree, ignoreAccessibility: true);
        var ctx = new ParseContext(filePath, tree);
        var parallelTagsSeen = new HashSet<string>();

        foreach (var node in root.DescendantNodes())
        {
            switch (node)
            {
                case CS.ClassDeclarationSyntax cls:
                    ctx.Symbols.Add(SymbolRow.FromSymbol(filePath, cls, semanticModel, "class", ctx));
                    ctx.Constants.AddRange(AttributeRows.FromAttributes(filePath, tree, cls.AttributeLists));
                    break;
                case CS.StructDeclarationSyntax str:
                    ctx.Symbols.Add(SymbolRow.FromSymbol(filePath, str, semanticModel, "struct", ctx));
                    ctx.Constants.AddRange(AttributeRows.FromAttributes(filePath, tree, str.AttributeLists));
                    break;
                case CS.InterfaceDeclarationSyntax iface:
                    ctx.Symbols.Add(SymbolRow.FromSymbol(filePath, iface, semanticModel, "interface", ctx));
                    ctx.Constants.AddRange(AttributeRows.FromAttributes(filePath, tree, iface.AttributeLists));
                    break;
                case CS.RecordDeclarationSyntax record:
                    ctx.Symbols.Add(SymbolRow.FromSymbol(filePath, record, semanticModel, "record", ctx));
                    ctx.Constants.AddRange(AttributeRows.FromAttributes(filePath, tree, record.AttributeLists));
                    break;
                case CS.MethodDeclarationSyntax method:
                    ctx.Symbols.Add(SymbolRow.FromSymbol(filePath, method, semanticModel, "method", ctx));
                    ctx.Constants.AddRange(AttributeRows.FromAttributes(filePath, tree, method.AttributeLists));
                    break;
                case CS.ConstructorDeclarationSyntax ctor:
                    ctx.Symbols.Add(SymbolRow.FromSymbol(filePath, ctor, semanticModel, "ctor", ctx));
                    ctx.Constants.AddRange(AttributeRows.FromAttributes(filePath, tree, ctor.AttributeLists));
                    break;
                case CS.InvocationExpressionSyntax invocation:
                    var invSymbol = semanticModel.GetSymbolInfo(invocation).Symbol;
                    var callerSymbol = GetCallerSymbol(semanticModel, invocation.SpanStart);
                    RecordCall(
                        ctx,
                        filePath,
                        tree,
                        semanticModel,
                        invocation.GetLocation(),
                        invSymbol,
                        callerSymbol,
                        invocation.Expression.ToString()
                    );
                    if (TryExtractDataAccess(invocation, semanticModel, invSymbol, out var dataAccess))
                    {
                        ctx.DataAccess.Add(DataAccessRow.FromSymbol(filePath, tree, dataAccess, invocation.GetLocation()));
                    }
                    if (IsParallelCall(invSymbol, out var parallelTag))
                    {
                        RecordParallelTag(ctx, filePath, tree, invocation.GetLocation(), callerSymbol, parallelTag, parallelTagsSeen);
                    }
                    if (invocation.Expression is CS.MemberAccessExpressionSyntax member
                        && member.Name.Identifier.Text is "Where" or "Select" or "Join" or "GroupBy")
                    {
                        ctx.Conditions.Add(ConditionRow.FromNode(filePath, tree, $"linq:{member.Name.Identifier.Text}"));
                    }
                    break;
                case CS.ObjectCreationExpressionSyntax objCreate:
                    RecordCall(
                        ctx,
                        filePath,
                        tree,
                        semanticModel,
                        objCreate.GetLocation(),
                        semanticModel.GetSymbolInfo(objCreate).Symbol,
                        GetCallerSymbol(semanticModel, objCreate.SpanStart),
                        objCreate.Type.ToString()
                    );
                    break;
                case CS.ConstructorInitializerSyntax ctorInit:
                    RecordCall(
                        ctx,
                        filePath,
                        tree,
                        semanticModel,
                        ctorInit.GetLocation(),
                        semanticModel.GetSymbolInfo(ctorInit).Symbol,
                        GetCallerSymbol(semanticModel, ctorInit.SpanStart),
                        ctorInit.ToString()
                    );
                    break;
                case CS.MemberAccessExpressionSyntax memberAccess:
                    RecordSymbolAccess(
                        ctx,
                        filePath,
                        tree,
                        semanticModel,
                        memberAccess.GetLocation(),
                        semanticModel.GetSymbolInfo(memberAccess).Symbol,
                        memberAccess.Name.Identifier.Text
                    );
                    if (memberAccess.Expression is CS.BaseExpressionSyntax)
                    {
                        RecordBaseCall(
                            ctx,
                            filePath,
                            tree,
                            semanticModel,
                            memberAccess.GetLocation(),
                            semanticModel.GetSymbolInfo(memberAccess).Symbol,
                            GetCallerSymbol(semanticModel, memberAccess.SpanStart)
                        );
                    }
                    break;
                case CS.IdentifierNameSyntax identifier:
                    RecordSymbolAccess(
                        ctx,
                        filePath,
                        tree,
                        semanticModel,
                        identifier.GetLocation(),
                        semanticModel.GetSymbolInfo(identifier).Symbol,
                        identifier.Identifier.Text
                    );
                    break;
                case CS.AwaitExpressionSyntax awaitExpr:
                    var awaitType = semanticModel.GetTypeInfo(awaitExpr.Expression).Type;
                    RecordCall(
                        ctx,
                        filePath,
                        tree,
                        semanticModel,
                        awaitExpr.GetLocation(),
                        semanticModel.GetSymbolInfo(awaitExpr.Expression).Symbol,
                        GetCallerSymbol(semanticModel, awaitExpr.SpanStart),
                        $"await:{awaitType?.ToDisplayString(SymbolDisplayFormat.FullyQualifiedFormat) ?? awaitExpr.Expression.ToString()}"
                    );
                    break;
                case CS.QueryExpressionSyntax queryExpr:
                    RecordCall(
                        ctx,
                        filePath,
                        tree,
                        semanticModel,
                        queryExpr.GetLocation(),
                        semanticModel.GetSymbolInfo(queryExpr).Symbol,
                        GetCallerSymbol(semanticModel, queryExpr.SpanStart),
                        "linq:query"
                    );
                    break;
                case CS.IfStatementSyntax ifStmt:
                    ctx.Conditions.Add(ConditionRow.FromNode(filePath, tree, ifStmt.Condition.ToString()));
                    break;
                case CS.ElseClauseSyntax elseClause:
                    ctx.Conditions.Add(ConditionRow.FromNode(filePath, tree, "else"));
                    break;
                case CS.WhileStatementSyntax whileStmt:
                    ctx.Conditions.Add(ConditionRow.FromNode(filePath, tree, whileStmt.Condition.ToString()));
                    break;
                case CS.ForStatementSyntax forStmt when forStmt.Condition is not null:
                    ctx.Conditions.Add(ConditionRow.FromNode(filePath, tree, forStmt.Condition.ToString()));
                    break;
                case CS.SwitchStatementSyntax switchStmt:
                    ctx.Conditions.Add(ConditionRow.FromNode(filePath, tree, $"switch({switchStmt.Expression})"));
                    break;
                case CS.CatchClauseSyntax catchClause:
                    ctx.Conditions.Add(ConditionRow.FromNode(filePath, tree, $"catch({catchClause.Declaration?.Type})"));
                    break;
                case CS.TryStatementSyntax:
                    ctx.Conditions.Add(ConditionRow.FromNode(filePath, tree, "try"));
                    break;
                case CS.UsingStatementSyntax:
                    ctx.Conditions.Add(ConditionRow.FromNode(filePath, tree, "using"));
                    break;
                case CS.ForEachStatementSyntax foreachStmt:
                    ctx.Conditions.Add(ConditionRow.FromNode(filePath, tree, $"foreach({foreachStmt.Expression})"));
                    break;
                case CS.ForEachVariableStatementSyntax foreachVarStmt:
                    ctx.Conditions.Add(ConditionRow.FromNode(filePath, tree, $"foreach({foreachVarStmt.Expression})"));
                    break;
                case CS.ConditionalExpressionSyntax conditionalExpr:
                    ctx.Conditions.Add(ConditionRow.FromNode(filePath, tree, conditionalExpr.Condition.ToString()));
                    break;
                // LINQ handled in invocation case above.
                case CS.LiteralExpressionSyntax literal:
                    var value = literal.Token.ValueText;
                    if (!string.IsNullOrEmpty(value))
                    {
                        ctx.Constants.Add(ConstantRow.FromNode(filePath, tree, value));
                        if (LooksLikeSql(value))
                        {
                            ctx.DataAccess.Add(DataAccessRow.FromNode(filePath, tree, value));
                        }
                    }
                    break;
            }
        }

        return ctx.ToResult();
    }

    private static ParseResult ParseVisualBasic(string filePath, string text)
    {
        var tree = VisualBasicSyntaxTree.ParseText(text);
        var root = tree.GetRoot();
        var compilation = BuildVisualBasicCompilation(tree);
        var semanticModel = compilation.GetSemanticModel(tree, ignoreAccessibility: true);
        var ctx = new ParseContext(filePath, tree);
        var parallelTagsSeen = new HashSet<string>();

        foreach (var node in root.DescendantNodes())
        {
            switch (node)
            {
                case VB.ClassBlockSyntax cls:
                    ctx.Symbols.Add(SymbolRow.FromSymbol(filePath, cls.ClassStatement, semanticModel, "class", ctx));
                    ctx.Constants.AddRange(AttributeRows.FromAttributes(filePath, tree, cls.ClassStatement.AttributeLists));
                    break;
                case VB.ModuleBlockSyntax mod:
                    ctx.Symbols.Add(SymbolRow.FromSymbol(filePath, mod.ModuleStatement, semanticModel, "module", ctx));
                    ctx.Constants.AddRange(AttributeRows.FromAttributes(filePath, tree, mod.ModuleStatement.AttributeLists));
                    break;
                case VB.MethodBlockSyntax method:
                    ctx.Symbols.Add(SymbolRow.FromSymbol(filePath, method.SubOrFunctionStatement, semanticModel, "method", ctx));
                    ctx.Constants.AddRange(AttributeRows.FromAttributes(filePath, tree, method.SubOrFunctionStatement.AttributeLists));
                    break;
                case VB.InvocationExpressionSyntax invocation:
                    var invSymbol = semanticModel.GetSymbolInfo(invocation).Symbol;
                    var callerSymbol = GetCallerSymbol(semanticModel, invocation.SpanStart);
                    RecordCall(
                        ctx,
                        filePath,
                        tree,
                        semanticModel,
                        invocation.GetLocation(),
                        invSymbol,
                        callerSymbol,
                        invocation.Expression.ToString()
                    );
                    if (TryExtractDataAccess(invocation, semanticModel, invSymbol, out var dataAccess))
                    {
                        ctx.DataAccess.Add(DataAccessRow.FromSymbol(filePath, tree, dataAccess, invocation.GetLocation()));
                    }
                    if (IsParallelCall(invSymbol, out var parallelTag))
                    {
                        RecordParallelTag(ctx, filePath, tree, invocation.GetLocation(), callerSymbol, parallelTag, parallelTagsSeen);
                    }
                    if (invocation.Expression is VB.MemberAccessExpressionSyntax member
                        && member.Name.Identifier.Text is "Where" or "Select" or "Join" or "GroupBy")
                    {
                        ctx.Conditions.Add(ConditionRow.FromNode(filePath, tree, $"linq:{member.Name.Identifier.Text}"));
                    }
                    break;
                case VB.ObjectCreationExpressionSyntax objCreate:
                    RecordCall(
                        ctx,
                        filePath,
                        tree,
                        semanticModel,
                        objCreate.GetLocation(),
                        semanticModel.GetSymbolInfo(objCreate).Symbol,
                        GetCallerSymbol(semanticModel, objCreate.SpanStart),
                        objCreate.Type.ToString()
                    );
                    break;
                case VB.MemberAccessExpressionSyntax memberAccess:
                    RecordSymbolAccess(
                        ctx,
                        filePath,
                        tree,
                        semanticModel,
                        memberAccess.GetLocation(),
                        semanticModel.GetSymbolInfo(memberAccess).Symbol,
                        memberAccess.Name.Identifier.Text
                    );
                    break;
                case VB.IdentifierNameSyntax identifier:
                    RecordSymbolAccess(
                        ctx,
                        filePath,
                        tree,
                        semanticModel,
                        identifier.GetLocation(),
                        semanticModel.GetSymbolInfo(identifier).Symbol,
                        identifier.Identifier.Text
                    );
                    break;
                case VB.AwaitExpressionSyntax awaitExpr:
                    var awaitType = semanticModel.GetTypeInfo(awaitExpr.Expression).Type;
                    RecordCall(
                        ctx,
                        filePath,
                        tree,
                        semanticModel,
                        awaitExpr.GetLocation(),
                        semanticModel.GetSymbolInfo(awaitExpr.Expression).Symbol,
                        GetCallerSymbol(semanticModel, awaitExpr.SpanStart),
                        $"await:{awaitType?.ToDisplayString(SymbolDisplayFormat.FullyQualifiedFormat) ?? awaitExpr.Expression.ToString()}"
                    );
                    break;
                case VB.QueryExpressionSyntax queryExpr:
                    RecordCall(
                        ctx,
                        filePath,
                        tree,
                        semanticModel,
                        queryExpr.GetLocation(),
                        semanticModel.GetSymbolInfo(queryExpr).Symbol,
                        GetCallerSymbol(semanticModel, queryExpr.SpanStart),
                        "linq:query"
                    );
                    break;
                case VB.IfStatementSyntax ifStmt:
                    ctx.Conditions.Add(ConditionRow.FromNode(filePath, tree, ifStmt.Condition.ToString()));
                    break;
                case VB.ElseStatementSyntax:
                    ctx.Conditions.Add(ConditionRow.FromNode(filePath, tree, "Else"));
                    break;
                case VB.WhileStatementSyntax whileStmt:
                    ctx.Conditions.Add(ConditionRow.FromNode(filePath, tree, whileStmt.Condition.ToString()));
                    break;
                case VB.ForStatementSyntax forStmt:
                    ctx.Conditions.Add(ConditionRow.FromNode(filePath, tree, forStmt.ControlVariable.ToString()));
                    break;
                case VB.SelectBlockSyntax selectBlock:
                    ctx.Conditions.Add(ConditionRow.FromNode(filePath, tree, $"Select({selectBlock.SelectStatement.Expression})"));
                    break;
                case VB.CatchBlockSyntax:
                    ctx.Conditions.Add(ConditionRow.FromNode(filePath, tree, "Catch"));
                    break;
                case VB.TryBlockSyntax:
                    ctx.Conditions.Add(ConditionRow.FromNode(filePath, tree, "Try"));
                    break;
                case VB.UsingBlockSyntax:
                    ctx.Conditions.Add(ConditionRow.FromNode(filePath, tree, "Using"));
                    break;
                case VB.ForEachBlockSyntax foreachBlock:
                    ctx.Conditions.Add(ConditionRow.FromNode(filePath, tree, $"ForEach({foreachBlock.ForEachStatement.Expression})"));
                    break;
                case VB.MultiLineLambdaExpressionSyntax:
                case VB.SingleLineLambdaExpressionSyntax:
                    ctx.Conditions.Add(ConditionRow.FromNode(filePath, tree, "Lambda"));
                    break;
                // LINQ handled in invocation case above.
                case VB.LiteralExpressionSyntax literal:
                    var value = literal.Token.Value?.ToString() ?? "";
                    if (!string.IsNullOrEmpty(value))
                    {
                        ctx.Constants.Add(ConstantRow.FromNode(filePath, tree, value));
                        if (LooksLikeSql(value))
                        {
                            ctx.DataAccess.Add(DataAccessRow.FromNode(filePath, tree, value));
                        }
                    }
                    break;
            }
        }

        return ctx.ToResult();
    }

    private static void RecordCall(
        ParseContext ctx,
        string filePath,
        SyntaxTree tree,
        SemanticModel semanticModel,
        Location location,
        ISymbol? calleeSymbol,
        ISymbol? callerSymbol,
        string fallbackCallee)
    {
        var calleeName = calleeSymbol?.ToDisplayString(SymbolDisplayFormat.FullyQualifiedFormat)
            ?? fallbackCallee;
        var callerName = callerSymbol?.ToDisplayString(SymbolDisplayFormat.FullyQualifiedFormat) ?? "";
        ctx.Calls.Add(CallRow.FromSymbols(filePath, tree, semanticModel, calleeSymbol, callerSymbol, calleeName, callerName, location, ctx));
    }

    private static ISymbol? GetCallerSymbol(SemanticModel semanticModel, int position) =>
        semanticModel.GetEnclosingSymbol(position, default);

    private static void RecordSymbolAccess(
        ParseContext ctx,
        string filePath,
        SyntaxTree tree,
        SemanticModel semanticModel,
        Location location,
        ISymbol? symbol,
        string fallbackName)
    {
        switch (symbol)
        {
            case IPropertySymbol prop:
                RecordCall(
                    ctx,
                    filePath,
                    tree,
                    semanticModel,
                    location,
                    prop.GetMethod ?? prop.SetMethod,
                    GetCallerSymbol(semanticModel, location.SourceSpan.Start),
                    prop.ToDisplayString(SymbolDisplayFormat.FullyQualifiedFormat)
                );
                break;
            case IEventSymbol evt:
                RecordCall(
                    ctx,
                    filePath,
                    tree,
                    semanticModel,
                    location,
                    evt.AddMethod ?? evt.RemoveMethod ?? evt.RaiseMethod,
                    GetCallerSymbol(semanticModel, location.SourceSpan.Start),
                    evt.ToDisplayString(SymbolDisplayFormat.FullyQualifiedFormat)
                );
                break;
            case IMethodSymbol method when method.MethodKind == MethodKind.DelegateInvoke:
                RecordCall(
                    ctx,
                    filePath,
                    tree,
                    semanticModel,
                    location,
                    method,
                    GetCallerSymbol(semanticModel, location.SourceSpan.Start),
                    method.ToDisplayString(SymbolDisplayFormat.FullyQualifiedFormat)
                );
                break;
            case IMethodSymbol method when method.MethodKind is MethodKind.PropertyGet or MethodKind.PropertySet:
                RecordCall(
                    ctx,
                    filePath,
                    tree,
                    semanticModel,
                    location,
                    method,
                    GetCallerSymbol(semanticModel, location.SourceSpan.Start),
                    method.ToDisplayString(SymbolDisplayFormat.FullyQualifiedFormat)
                );
                break;
            default:
                if (symbol != null)
                {
                    RecordCall(
                        ctx,
                        filePath,
                        tree,
                        semanticModel,
                        location,
                        symbol,
                        GetCallerSymbol(semanticModel, location.SourceSpan.Start),
                        fallbackName
                    );
                }
                break;
        }
    }

    private static void RecordBaseCall(
        ParseContext ctx,
        string filePath,
        SyntaxTree tree,
        SemanticModel semanticModel,
        Location location,
        ISymbol? symbol,
        ISymbol? callerSymbol)
    {
        if (symbol == null)
        {
            return;
        }
        RecordCall(
            ctx,
            filePath,
            tree,
            semanticModel,
            location,
            symbol,
            callerSymbol,
            symbol.ToDisplayString(SymbolDisplayFormat.FullyQualifiedFormat)
        );
    }

    private static bool IsParallelCall(ISymbol? symbol, out string tag)
    {
        tag = string.Empty;
        if (symbol is not IMethodSymbol method) return false;
        var typeName = method.ContainingType?.ToDisplayString(SymbolDisplayFormat.FullyQualifiedFormat) ?? "";
        var name = method.Name;

        // Task-based parallelism
        if (typeName.StartsWith("System.Threading.Tasks.Task", StringComparison.Ordinal))
        {
            if (name is "Run" or "RunAsync" or "Factory" or "StartNew" or "WhenAll" or "WhenAny" or "WaitAll")
            {
                tag = $"parallel:task:{name.ToLowerInvariant()}";
                return true;
            }
        }

        // Parallel class
        if (typeName.StartsWith("System.Threading.Tasks.Parallel", StringComparison.Ordinal))
        {
            if (name is "For" or "ForEach" or "Invoke")
            {
                tag = $"parallel:parallel:{name.ToLowerInvariant()}";
                return true;
            }
        }

        // ThreadPool / Thread
        if (typeName.StartsWith("System.Threading.ThreadPool", StringComparison.Ordinal))
        {
            if (name is "QueueUserWorkItem")
            {
                tag = "parallel:threadpool:queue";
                return true;
            }
        }

        if (typeName.StartsWith("System.Threading.Thread", StringComparison.Ordinal))
        {
            if (name is "Start")
            {
                tag = "parallel:thread:start";
                return true;
            }
        }

        // Dataflow (simple hint)
        if (typeName.Contains("System.Threading.Tasks.Dataflow", StringComparison.Ordinal))
        {
            tag = "parallel:dataflow";
            return true;
        }

        return false;
    }

    private static void RecordParallelTag(
        ParseContext ctx,
        string filePath,
        SyntaxTree tree,
        Location location,
        ISymbol? callerSymbol,
        string tag,
        HashSet<string> seenTags)
    {
        var callerName = callerSymbol?.ToDisplayString(SymbolDisplayFormat.FullyQualifiedFormat) ?? "";
        var key = $"{callerName}|{tag}";
        if (seenTags.Contains(key))
        {
            return;
        }
        seenTags.Add(key);
        ctx.Conditions.Add(ConditionRow.FromNode(filePath, tree, tag));
    }

    private static bool LooksLikeSql(string value)
    {
        var trimmed = value.TrimStart();
        if (trimmed.Length < 6) return false;
        var head = trimmed.Length > 32 ? trimmed[..32] : trimmed;
        return StartsWithAny(head,
            "select ",
            "insert ",
            "update ",
            "delete ",
            "merge ",
            "with ",
            "exec ",
            "execute ",
            "call ",
            "declare ",
            "create ",
            "alter ",
            "drop ",
            "truncate ");
    }

    private static ParseResult ParseSolution(string filePath, string text, IngestionConfig? ingestionConfig)
    {
        var aggregate = new ParseResult();
        var projects = new List<string>();
        var extensions = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        foreach (var line in text.Split('\n'))
        {
            var trimmed = line.Trim();
            if (!trimmed.StartsWith("Project(", StringComparison.OrdinalIgnoreCase)) continue;
            var parts = trimmed.Split(',');
            if (parts.Length < 2) continue;
            var projPath = parts[1].Trim().Trim('"');
            var normalized = projPath.Replace('\\', Path.DirectorySeparatorChar);
            var resolved = Path.GetFullPath(Path.Combine(Path.GetDirectoryName(filePath) ?? "", normalized));
            var ext = Path.GetExtension(resolved);
            if (string.IsNullOrEmpty(ext) ||
                !(ext.Equals(".csproj", StringComparison.OrdinalIgnoreCase)
                  || ext.Equals(".vbproj", StringComparison.OrdinalIgnoreCase)
                  || ext.Equals(".vsproj", StringComparison.OrdinalIgnoreCase)))
            {
                continue; // skip solution folders / non-project entries
            }
            projects.Add(resolved);
            extensions.Add(ext);
        }
        Log($"solution_parse start file={filePath} projects={projects.Count}");

        for (var i = 0; i < projects.Count; i++)
        {
            var proj = projects[i];
            if (!File.Exists(proj))
            {
                Log($"solution_project_missing index={i + 1}/{projects.Count} path={proj}");
                continue;
            }
            Log($"solution_project start index={i + 1}/{projects.Count} path={proj}");
            var projText = File.ReadAllText(proj);
            var projResult = ParseProject(proj, projText, parseCompileItems: true, ingestionConfig);
            AppendResult(aggregate, projResult);
            Log($"solution_project done index={i + 1}/{projects.Count} path={proj} symbols={projResult.Symbols.Count} calls={projResult.Calls.Count}");
        }

        aggregate.Constants.Add(ConstantRow.FromProject(filePath, 1, $"Projects:{projects.Count}"));
        aggregate.Constants.Add(
            ConstantRow.FromProject(filePath, 1, $"Extensions:{string.Join('|', extensions.OrderBy(x => x))}")
        );
        Log($"solution_parse done file={filePath} projects={projects.Count}");
        return aggregate;
    }

    private static ParseResult ParseProject(
        string filePath,
        string text,
        bool parseCompileItems = false,
        IngestionConfig? ingestionConfig = null)
    {
        var extensions = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        var dir = Path.GetDirectoryName(filePath) ?? Directory.GetCurrentDirectory();
        var compileItems = CollectCompileItems(dir, ingestionConfig);
        foreach (var full in compileItems)
        {
            var ext = Path.GetExtension(full);
            if (!string.IsNullOrEmpty(ext))
            {
                extensions.Add(ext);
            }
        }

        Log($"project_parse start file={filePath} compile_items={compileItems.Count} extensions={string.Join('|', extensions.OrderBy(x => x))}");

        var result = new ParseResult
        {
            Constants = new List<ConstantRow>
            {
                ConstantRow.FromProject(filePath, 1, $"CompileItems:{compileItems.Count}"),
                ConstantRow.FromProject(filePath, 1, $"Extensions:{string.Join('|', extensions.OrderBy(x => x))}")
            }
        };

        if (!parseCompileItems || compileItems.Count == 0)
        {
            Log($"project_parse done file={filePath} parsed=0");
            return result;
        }

        var symbols = new ConcurrentBag<SymbolRow>();
        var calls = new ConcurrentBag<CallRow>();
        var conditions = new ConcurrentBag<ConditionRow>();
        var constants = new ConcurrentBag<ConstantRow>(result.Constants);
        var dataAccess = new ConcurrentBag<DataAccessRow>();
        var processed = 0;

        Parallel.ForEach(compileItems, file =>
        {
            if (!File.Exists(file)) return;
            var ext = Path.GetExtension(file).ToLowerInvariant();
            var content = File.ReadAllText(file);
            ParseResult sub = ext switch
            {
                ".cs" or ".csx" => ParseCSharp(file, content),
                ".vb" or ".vbx" or ".bas" => ParseVisualBasic(file, content),
                _ => EmptyResult()
            };
            foreach (var s in sub.Symbols) symbols.Add(s);
            foreach (var c in sub.Calls) calls.Add(c);
            foreach (var cond in sub.Conditions) conditions.Add(cond);
            foreach (var con in sub.Constants) constants.Add(con);
            foreach (var da in sub.DataAccess) dataAccess.Add(da);
            var current = Interlocked.Increment(ref processed);
            if (current % 100 == 0)
            {
                Log($"project_parse progress file={filePath} processed={current}/{compileItems.Count}");
            }
        });

        Log($"project_parse done file={filePath} processed={processed} symbols={symbols.Count} calls={calls.Count}");
        return new ParseResult
        {
            Symbols = symbols.ToList(),
            Calls = calls.ToList(),
            Conditions = conditions.ToList(),
            Constants = constants.ToList(),
            DataAccess = dataAccess.ToList(),
        };
    }

    private static List<string> CollectCompileItems(string root, IngestionConfig? ingestionConfig)
    {
        var compileItems = new List<string>();
        if (!Directory.Exists(root))
        {
            Log($"project_parse root_missing path={root}");
            return compileItems;
        }

        var includeExts = NormalizeExtensions(ingestionConfig?.IncludeExtensions);
        var excludeExts = NormalizeExtensions(ingestionConfig?.ExcludeExtensions);
        var includeAll = includeExts.Count == 0 || includeExts.Contains("*");
        var allowedExts = includeAll
            ? SourceExtensions
            : new HashSet<string>(SourceExtensions.Where(includeExts.Contains), StringComparer.OrdinalIgnoreCase);
        if (allowedExts.Count == 0)
        {
            Log($"project_parse allowed_exts_empty root={root}");
            return compileItems;
        }

        var excludedDirs = BuildExcludedDirSet(ingestionConfig);
        var stack = new Stack<string>();
        var seen = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        stack.Push(root);

        while (stack.Count > 0)
        {
            var current = stack.Pop();
            IEnumerable<string> subDirs;
            try
            {
                subDirs = Directory.EnumerateDirectories(current);
            }
            catch (Exception ex)
            {
                Log($"project_parse skip_dir path={current} error={ex.Message}");
                continue;
            }

            foreach (var sub in subDirs)
            {
                var name = Path.GetFileName(sub);
                if (string.IsNullOrEmpty(name)) continue;
                if (excludedDirs.Contains(name)) continue;
                stack.Push(sub);
            }

            IEnumerable<string> files;
            try
            {
                files = Directory.EnumerateFiles(current);
            }
            catch (Exception ex)
            {
                Log($"project_parse skip_files path={current} error={ex.Message}");
                continue;
            }

            foreach (var file in files)
            {
                var ext = Path.GetExtension(file);
                if (!allowedExts.Contains(ext)) continue;
                if (excludeExts.Contains(ext)) continue;
                if (seen.Add(file))
                {
                    compileItems.Add(file);
                }
            }
        }

        return compileItems;
    }

    private static HashSet<string> NormalizeExtensions(IEnumerable<string>? extensions)
    {
        var set = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        if (extensions == null)
        {
            return set;
        }

        foreach (var ext in extensions)
        {
            if (string.IsNullOrWhiteSpace(ext))
            {
                continue;
            }
            if (ext == "*")
            {
                set.Add("*");
                continue;
            }
            set.Add(ext.StartsWith(".") ? ext : $".{ext}");
        }

        return set;
    }

    private static HashSet<string> BuildExcludedDirSet(IngestionConfig? ingestionConfig)
    {
        var set = new HashSet<string>(DefaultExcludedDirectories, StringComparer.OrdinalIgnoreCase);
        if (ingestionConfig?.ExcludeDirs == null)
        {
            return set;
        }

        foreach (var dir in ingestionConfig.ExcludeDirs)
        {
            if (string.IsNullOrWhiteSpace(dir))
            {
                continue;
            }
            set.Add(dir.Trim());
        }

        return set;
    }

    private static bool StartsWithAny(string input, params string[] prefixes)
    {
        foreach (var prefix in prefixes)
        {
            if (input.StartsWith(prefix, StringComparison.OrdinalIgnoreCase))
            {
                return true;
            }
        }
        return false;
    }

    private sealed class IngestionConfig
    {
        public string? InputRoot { get; set; }
        public string? OutputRoot { get; set; }
        public string RunId { get; set; } = "auto";
        public int ArtifactVersion { get; set; } = 1;
        public string[] IncludeExtensions { get; set; } = Array.Empty<string>();
        public string[] ExcludeExtensions { get; set; } = Array.Empty<string>();
        public string[] ExcludeDirs { get; set; } = Array.Empty<string>();
    }

    private sealed class ParseContext
    {
        public ParseContext(string filePath, SyntaxTree? tree)
        {
            FilePath = filePath;
            Tree = tree;
        }

        public string FilePath { get; }
        public SyntaxTree? Tree { get; }
        public List<SymbolRow> Symbols { get; } = new();
        public List<CallRow> Calls { get; } = new();
        public List<ConditionRow> Conditions { get; } = new();
        public List<ConstantRow> Constants { get; } = new();
        public List<DataAccessRow> DataAccess { get; } = new();
        
        // Symbol location lookup: maps symbol to its source location
        public ConcurrentDictionary<ISymbol, (string FilePath, int Line, string Name)> SymbolLocations { get; } = new(SymbolEqualityComparer.Default);

        public ParseResult ToResult()
        {
            return new ParseResult
            {
                Symbols = Symbols,
                Calls = Calls,
                Conditions = Conditions,
                Constants = Constants,
                DataAccess = DataAccess
            };
        }
    }

    private sealed class ParseResult
    {
        public List<SymbolRow> Symbols { get; init; } = new();
        public List<CallRow> Calls { get; init; } = new();
        public List<ConditionRow> Conditions { get; init; } = new();
        public List<ConstantRow> Constants { get; init; } = new();
        public List<DataAccessRow> DataAccess { get; init; } = new();
    }

    private sealed class TargetParseResult
    {
        public TargetParseResult(string path, ParseResult result)
        {
            Path = path;
            Result = result;
        }

        public string Path { get; }
        public ParseResult Result { get; }

        public static FlattenedTargetParseResult Flatten(TargetParseResult result)
        {
            return new FlattenedTargetParseResult
            {
                TargetPath = result.Path,
                Symbols = result.Result.Symbols,
                Calls = result.Result.Calls,
                Conditions = result.Result.Conditions,
                Constants = result.Result.Constants,
                DataAccess = result.Result.DataAccess
            };
        }
    }

    private sealed class FlattenedTargetParseResult
    {
        public string TargetPath { get; init; } = "";
        public List<SymbolRow> Symbols { get; init; } = new();
        public List<CallRow> Calls { get; init; } = new();
        public List<ConditionRow> Conditions { get; init; } = new();
        public List<ConstantRow> Constants { get; init; } = new();
        public List<DataAccessRow> DataAccess { get; init; } = new();
    }

    private sealed class SymbolGraphRow
    {
        public string SymbolId { get; set; } = "";
        public string Name { get; set; } = "";
        public string Kind { get; set; } = "";
        public string Signature { get; set; } = "";
        public string FilePath { get; set; } = "";
        public int Line { get; set; }
        public string SourceRef { get; set; } = "";
        public string RunId { get; set; } = "";
        public int ArtifactVersion { get; set; }
        public string? SliceId { get; set; }
        public string? CreatedAt { get; set; }
        public string? SupersedesVersion { get; set; }
    }

    private sealed class CallGraphRow
    {
        public string CallerId { get; set; } = "";
        public string CalleeId { get; set; } = "";
        public string FilePath { get; set; } = "";
        public int Line { get; set; }
        public string SourceRef { get; set; } = "";
        public string RunId { get; set; } = "";
        public int ArtifactVersion { get; set; }
        public string? SliceId { get; set; }
        public string? CreatedAt { get; set; }
        public string? SupersedesVersion { get; set; }
    }

    private sealed class SymbolRow
    {
        public string SymbolId { get; init; } = "";
        public string Name { get; init; } = "";
        public string Kind { get; init; } = "";
        public string Signature { get; init; } = "";
        public string FilePath { get; init; } = "";
        public int Line { get; init; }
        public string SourceRef { get; init; } = "";

        public static SymbolRow FromNode(string filePath, SyntaxTree tree, string name, string kind, string signature)
        {
            var line = GetLine(tree, name, filePath, out var sourceRef);
            return new SymbolRow
            {
                SymbolId = Hash($"{filePath}:{line}:{name}"),
                Name = name,
                Kind = kind,
                Signature = signature,
                FilePath = filePath,
                Line = line,
                SourceRef = sourceRef
            };
        }

        public static SymbolRow FromSymbol(string filePath, SyntaxNode node, SemanticModel model, string kind, ParseContext? ctx = null)
        {
            var symbol = model.GetDeclaredSymbol(node);
            var name = symbol?.Name ?? node.ToString();
            var signature = symbol is IMethodSymbol methodSymbol
                ? MethodSignature(methodSymbol)
                : symbol?.ToDisplayString(SymbolDisplayFormat.FullyQualifiedFormat) ?? "";
            var line = GetLine(node.GetLocation(), filePath, out var sourceRef);
            
            // Register symbol location for later lookup
            if (symbol != null && ctx != null)
            {
                ctx.SymbolLocations.TryAdd(symbol, (filePath, line, name));
            }
            
            return new SymbolRow
            {
                SymbolId = Hash($"{filePath}:{line}:{name}"),
                Name = name,
                Kind = kind,
                Signature = signature,
                FilePath = filePath,
                Line = line,
                SourceRef = sourceRef
            };
        }

        public static SymbolRow FromProject(string filePath, int line, string name, string kind)
        {
            return new SymbolRow
            {
                SymbolId = Hash($"{filePath}:{line}:{name}"),
                Name = name,
                Kind = kind,
                Signature = name,
                FilePath = filePath,
                Line = line,
                SourceRef = $"{filePath}:{line}"
            };
        }
    }

    private sealed class CallRow
    {
        public string CallerId { get; init; } = "";
        public string CalleeId { get; init; } = "";
        public string FilePath { get; init; } = "";
        public int Line { get; init; }
        public string SourceRef { get; init; } = "";

        public static CallRow FromNode(string filePath, SyntaxTree tree, string callee)
        {
            var line = GetLine(tree, callee, filePath, out var sourceRef);
            return new CallRow
            {
                CallerId = Hash($"{filePath}:{line}:call"),
                CalleeId = Hash($"{callee}:0:callee"),
                FilePath = filePath,
                Line = line,
                SourceRef = sourceRef
            };
        }

        public static CallRow FromSymbol(
            string filePath,
            SyntaxTree tree,
            string callee,
            string caller,
            Location location)
        {
            var line = GetLine(location, filePath, out var sourceRef);
            var callerId = string.IsNullOrEmpty(caller) ? $"{filePath}:{line}:call" : caller;
            return new CallRow
            {
                CallerId = Hash(callerId),
                CalleeId = Hash(callee),
                FilePath = filePath,
                Line = line,
                SourceRef = sourceRef
            };
        }

        private static int _callsWithSymbol = 0;
        private static int _callsWithoutSymbol = 0;
        private static int _callsExternal = 0;

        public static CallRow FromSymbols(
            string filePath,
            SyntaxTree tree,
            SemanticModel semanticModel,
            ISymbol? calleeSymbol,
            ISymbol? callerSymbol,
            string calleeName,
            string callerName,
            Location location,
            ParseContext ctx)
        {
            var line = GetLine(location, filePath, out var sourceRef);
            
            // For callee: try to find location from our symbol lookup table
            string calleeId;
            if (calleeSymbol != null && ctx.SymbolLocations.TryGetValue(calleeSymbol, out var calleeLoc))
            {
                // Found in our symbol table - use the registered location
                calleeId = Hash($"{calleeLoc.FilePath}:{calleeLoc.Line}:{calleeLoc.Name}");
                System.Threading.Interlocked.Increment(ref _callsWithSymbol);
            }
            else if (calleeSymbol != null)
            {
                // Not in our table - external or metadata symbol
                calleeId = Hash(calleeName);
                System.Threading.Interlocked.Increment(ref _callsExternal);
            }
            else
            {
                // No symbol info, use name
                calleeId = Hash(calleeName);
                System.Threading.Interlocked.Increment(ref _callsWithoutSymbol);
            }

            // For caller: try to use its declaration location from lookup table
            string callerId;
            if (callerSymbol != null && ctx.SymbolLocations.TryGetValue(callerSymbol, out var callerLoc))
            {
                callerId = Hash($"{callerLoc.FilePath}:{callerLoc.Line}:{callerLoc.Name}");
            }
            else if (callerSymbol != null && !IsGlobalOrRootNamespace(callerSymbol))
            {
                // External or metadata symbol, but not global namespace
                callerId = Hash(callerName);
            }
            else
            {
                // No symbol info, or global/root namespace - use file:line for uniqueness
                callerId = Hash($"{filePath}:{line}:call");
            }

            return new CallRow
            {
                CallerId = callerId,
                CalleeId = calleeId,
                FilePath = filePath,
                Line = line,
                SourceRef = sourceRef
            };
        }

        public static void PrintCallStats()
        {
            Console.WriteLine($"\n=== Call Resolution Stats ===");
            Console.WriteLine($"Resolved (in-source): {_callsWithSymbol:N0}");
            Console.WriteLine($"External (library):   {_callsExternal:N0}");
            Console.WriteLine($"Unresolved (null):    {_callsWithoutSymbol:N0}");
            var total = _callsWithSymbol + _callsExternal + _callsWithoutSymbol;
            if (total > 0)
                Console.WriteLine($"In-source match rate: {_callsWithSymbol * 100.0 / total:F2}%");
        }

        private static bool IsGlobalOrRootNamespace(ISymbol symbol)
        {
            // Check if the symbol is the global namespace or a root namespace
            // These have names like "<global namespace>" and shouldn't be used as caller IDs
            if (symbol is INamespaceSymbol ns)
            {
                return ns.IsGlobalNamespace || 
                       ns.Name == "" || 
                       ns.ToDisplayString().Contains("<global namespace>");
            }
            return false;
        }
    }

    private sealed class ConditionRow
    {
        public string SymbolId { get; init; } = "";
        public string Predicate { get; init; } = "";
        public string FilePath { get; init; } = "";
        public int Line { get; init; }
        public string SourceRef { get; init; } = "";

        public static ConditionRow FromNode(string filePath, SyntaxTree tree, string predicate)
        {
            var line = GetLine(tree, predicate, filePath, out var sourceRef);
            return new ConditionRow
            {
                SymbolId = Hash($"{filePath}:{line}:cond"),
                Predicate = predicate,
                FilePath = filePath,
                Line = line,
                SourceRef = sourceRef
            };
        }
    }

    private sealed class ConstantRow
    {
        public string Name { get; init; } = "";
        public string Value { get; init; } = "";
        public string FilePath { get; init; } = "";
        public int Line { get; init; }
        public string SourceRef { get; init; } = "";

        public static ConstantRow FromNode(string filePath, SyntaxTree tree, string value)
        {
            var line = GetLine(tree, value, filePath, out var sourceRef);
            return new ConstantRow
            {
                Name = "",
                Value = value,
                FilePath = filePath,
                Line = line,
                SourceRef = sourceRef
            };
        }

        public static ConstantRow FromProject(string filePath, int line, string value)
        {
            return new ConstantRow
            {
                Name = "",
                Value = value,
                FilePath = filePath,
                Line = line,
                SourceRef = $"{filePath}:{line}"
            };
        }
    }

    private static class AttributeRows
    {
        public static IEnumerable<ConstantRow> FromAttributes(
            string filePath,
            SyntaxTree tree,
            IEnumerable<CS.AttributeListSyntax> lists)
        {
            foreach (var list in lists)
            {
                foreach (var attr in list.Attributes)
                {
                    yield return ConstantRow.FromNode(filePath, tree, attr.Name.ToString());
                }
            }
        }

        public static IEnumerable<ConstantRow> FromAttributes(
            string filePath,
            SyntaxTree tree,
            IEnumerable<VB.AttributeListSyntax> lists)
        {
            foreach (var list in lists)
            {
                foreach (var attr in list.Attributes)
                {
                    yield return ConstantRow.FromNode(filePath, tree, attr.Name.ToString());
                }
            }
        }
    }

    private sealed class DataAccessRow
    {
        public string SymbolId { get; init; } = "";
        public string TableName { get; init; } = "";
        public string Op { get; init; } = "";
        public string SqlText { get; init; } = "";
        public string FilePath { get; init; } = "";
        public int Line { get; init; }
        public string SourceRef { get; init; } = "";

        public static DataAccessRow FromNode(string filePath, SyntaxTree tree, string sql)
        {
            var line = GetLine(tree, sql, filePath, out var sourceRef);
            return new DataAccessRow
            {
                SymbolId = Hash($"{filePath}:{line}:sql"),
                TableName = "",
                Op = SqlOp(sql),
                SqlText = sql,
                FilePath = filePath,
                Line = line,
                SourceRef = sourceRef
            };
        }

        public static DataAccessRow FromSymbol(string filePath, SyntaxTree tree, string sql, Location location)
        {
            var line = GetLine(location, filePath, out var sourceRef);
            return new DataAccessRow
            {
                SymbolId = Hash($"{filePath}:{line}:sql"),
                TableName = "",
                Op = SqlOp(sql),
                SqlText = sql,
                FilePath = filePath,
                Line = line,
                SourceRef = sourceRef
            };
        }
    }

    private static int GetLine(SyntaxTree tree, string text, string filePath, out string sourceRef)
    {
        var span = tree.GetText().ToString().IndexOf(text, StringComparison.Ordinal);
        var line = 1;
        if (span >= 0)
        {
            var lineSpan = tree.GetText().Lines.GetLinePosition(span);
            line = lineSpan.Line + 1;
        }
        sourceRef = $"{filePath}:{line}";
        return line;
    }

    private static int GetLine(Location location, string filePath, out string sourceRef)
    {
        var line = 1;
        if (location != Location.None)
        {
            var span = location.GetLineSpan();
            line = span.StartLinePosition.Line + 1;
        }
        sourceRef = $"{filePath}:{line}";
        return line;
    }

    private static CSharpCompilation BuildCSharpCompilation(SyntaxTree tree)
    {
        return CSharpCompilation.Create(
            "RoslynParser",
            new[] { tree },
            GetReferences(),
            new CSharpCompilationOptions(OutputKind.DynamicallyLinkedLibrary));
    }

    private static VisualBasicCompilation BuildVisualBasicCompilation(SyntaxTree tree)
    {
        return VisualBasicCompilation.Create(
            "RoslynParser",
            new[] { tree },
            GetReferences(),
            new VisualBasicCompilationOptions(OutputKind.DynamicallyLinkedLibrary));
    }

    private static IEnumerable<MetadataReference> GetReferences()
    {
        var references = new List<MetadataReference>();
        foreach (var assembly in AppDomain.CurrentDomain.GetAssemblies())
        {
            if (assembly.IsDynamic) continue;
            if (string.IsNullOrEmpty(assembly.Location)) continue;
            references.Add(MetadataReference.CreateFromFile(assembly.Location));
        }
        return references;
    }

    private static string SqlOp(string sql)
    {
        var trimmed = sql.TrimStart();
        if (trimmed.StartsWith("select ", StringComparison.OrdinalIgnoreCase)) return "select";
        if (trimmed.StartsWith("insert ", StringComparison.OrdinalIgnoreCase)) return "insert";
        if (trimmed.StartsWith("update ", StringComparison.OrdinalIgnoreCase)) return "update";
        if (trimmed.StartsWith("delete ", StringComparison.OrdinalIgnoreCase)) return "delete";
        if (trimmed.StartsWith("merge ", StringComparison.OrdinalIgnoreCase)) return "merge";
        return "";
    }

    private static string Hash(string value)
    {
        var bytes = Encoding.UTF8.GetBytes(value);
        var hash = SHA256.HashData(bytes);
        return Convert.ToHexString(hash).ToLowerInvariant();
    }

    private static string MethodSignature(IMethodSymbol method)
    {
        var returnType = method.ReturnType.ToDisplayString(SymbolDisplayFormat.FullyQualifiedFormat);
        var parameters = string.Join(
            ", ",
            method.Parameters.Select(p =>
                $"{p.Type.ToDisplayString(SymbolDisplayFormat.FullyQualifiedFormat)} {p.Name}"));
        var containing = method.ContainingType.ToDisplayString(SymbolDisplayFormat.FullyQualifiedFormat);
        return $"{containing}.{method.Name}({parameters}) -> {returnType}";
    }

    private static void AppendResult(ParseResult target, ParseResult add)
    {
        target.Symbols.AddRange(add.Symbols);
        target.Calls.AddRange(add.Calls);
        target.Conditions.AddRange(add.Conditions);
        target.Constants.AddRange(add.Constants);
        target.DataAccess.AddRange(add.DataAccess);
    }

    private static bool TryExtractDataAccess(SyntaxNode node, SemanticModel model, ISymbol? symbol, out string kind)
    {
        kind = string.Empty;

        // Literal SQL
        if (node is CS.InvocationExpressionSyntax csInvoc && LooksLikeSql(csInvoc.ToString()))
        {
            kind = "sql:literal";
            return true;
        }
        if (node is VB.InvocationExpressionSyntax vbInvoc && LooksLikeSql(vbInvoc.ToString()))
        {
            kind = "sql:literal";
            return true;
        }

        // Method-based patterns (ADO/ORM)
        if (symbol is IMethodSymbol methodSymbol)
        {
            var methodName = methodSymbol.Name;
            var containingType = methodSymbol.ContainingType?.ToDisplayString(SymbolDisplayFormat.FullyQualifiedFormat) ?? "";
            foreach (var pattern in DataAccessPatterns)
            {
                if (!pattern.MemberNames.Contains(methodName))
                {
                    continue;
                }
                if (!pattern.TypePrefixes.Any(prefix => containingType.StartsWith(prefix, StringComparison.Ordinal)))
                {
                    continue;
                }
                kind = pattern.IsStoredProc ? "sql:proc" : "sql:orm";
                return true;
            }
        }

        return false;
    }
}
