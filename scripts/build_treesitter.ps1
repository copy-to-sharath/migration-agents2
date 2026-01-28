<#
.SYNOPSIS
    Build tree-sitter language grammars on Windows.

.DESCRIPTION
    This script builds the tree-sitter language grammars into a DLL file
    that can be loaded by the migration-agents parser. Features structured
    logging, comprehensive error handling, and memory-safe resource cleanup.

.PARAMETER Config
    Path to the build configuration JSON file.
    Default: config/parser.json

.PARAMETER LogLevel
    Logging verbosity: Debug, Info, Warning, Error
    Default: Info

.PARAMETER LogFile
    Optional path to write logs to file.

.PARAMETER Clean
    Clean build artifacts before building.

.EXAMPLE
    .\scripts\build_treesitter.ps1
    .\scripts\build_treesitter.ps1 -Config config/custom_parser.json -LogLevel Debug
    .\scripts\build_treesitter.ps1 -Clean -LogFile build.log

.NOTES
    Requires one of:
    - Visual Studio Build Tools (cl.exe) - recommended
    - LLVM/Clang
    - MinGW-w64
#>

[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [ValidateScript({ Test-Path $_ -PathType Leaf })]
    [string]$Config = "config/tree_sitter_build.json",

    [Parameter()]
    [ValidateSet("Debug", "Info", "Warning", "Error")]
    [string]$LogLevel = "Info",

    [Parameter()]
    [string]$LogFile,

    [Parameter()]
    [switch]$Clean
)

#region Initialization
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Script-level state (cleaned up in finally block)
$script:LogFileStream = $null
$script:StartTime = [DateTime]::UtcNow
$script:ErrorList = [System.Collections.Generic.List[hashtable]]::new()
$script:OriginalLocation = Get-Location
$script:OriginalEnv = @{}
#endregion

#region Logging Functions
$script:LogLevels = @{
    Debug   = 0
    Info    = 1
    Warning = 2
    Error   = 3
}

function Write-Log {
    <#
    .SYNOPSIS
        Thread-safe structured logging with file and console output.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory, Position = 0)]
        [string]$Message,

        [Parameter()]
        [ValidateSet("Debug", "Info", "Warning", "Error")]
        [string]$Level = "Info",

        [Parameter()]
        [hashtable]$Context = @{},

        [Parameter()]
        [System.Management.Automation.ErrorRecord]$ErrorRecord
    )

    # Skip if below configured log level
    if ($script:LogLevels[$Level] -lt $script:LogLevels[$LogLevel]) {
        return
    }

    $timestamp = [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
    $elapsed = ([DateTime]::UtcNow - $script:StartTime).TotalSeconds

    # Build structured log entry
    $logEntry = [ordered]@{
        timestamp = $timestamp
        elapsed_s = [Math]::Round($elapsed, 3)
        level     = $Level.ToUpper()
        message   = $Message
    }

    # Add context fields
    foreach ($key in $Context.Keys) {
        $logEntry[$key] = $Context[$key]
    }

    # Add error details if present
    if ($ErrorRecord) {
        $logEntry["error_type"] = $ErrorRecord.Exception.GetType().FullName
        $logEntry["error_message"] = $ErrorRecord.Exception.Message
        $logEntry["error_position"] = $ErrorRecord.InvocationInfo.PositionMessage
        if ($ErrorRecord.Exception.InnerException) {
            $logEntry["inner_error"] = $ErrorRecord.Exception.InnerException.Message
        }

        # Track errors for summary
        $script:ErrorList.Add(@{
            Timestamp = $timestamp
            Message   = $Message
            Error     = $ErrorRecord.Exception.Message
        })
    }

    # Format for console
    $consolePrefix = switch ($Level) {
        "Debug"   { "[DBG]" }
        "Info"    { "[INF]" }
        "Warning" { "[WRN]" }
        "Error"   { "[ERR]" }
    }
    $consoleColor = switch ($Level) {
        "Debug"   { "DarkGray" }
        "Info"    { "White" }
        "Warning" { "Yellow" }
        "Error"   { "Red" }
    }

    $consoleMessage = "$consolePrefix $Message"
    if ($Context.Count -gt 0) {
        $contextStr = ($Context.GetEnumerator() | ForEach-Object { "$($_.Key)=$($_.Value)" }) -join " "
        $consoleMessage += " | $contextStr"
    }

    Write-Host $consoleMessage -ForegroundColor $consoleColor

    # Write to file if configured
    if ($script:LogFileStream) {
        try {
            $jsonLine = $logEntry | ConvertTo-Json -Compress -Depth 4
            $script:LogFileStream.WriteLine($jsonLine)
            $script:LogFileStream.Flush()
        }
        catch {
            Write-Host "[WRN] Failed to write to log file: $_" -ForegroundColor Yellow
        }
    }
}

function Write-LogHeader {
    param([string]$Title)
    
    $separator = "=" * 60
    Write-Host ""
    Write-Host $separator -ForegroundColor Cyan
    Write-Host " $Title" -ForegroundColor Cyan
    Write-Host $separator -ForegroundColor Cyan
    Write-Host ""
}

function Write-LogSection {
    param([string]$Title)
    Write-Host ""
    Write-Host "--- $Title ---" -ForegroundColor DarkCyan
}
#endregion

#region Resource Management
function Initialize-LogFile {
    param([string]$Path)
    
    if (-not $Path) { return }
    
    try {
        $fullPath = [System.IO.Path]::GetFullPath($Path)
        $dir = [System.IO.Path]::GetDirectoryName($fullPath)
        if (-not (Test-Path $dir)) {
            New-Item -Path $dir -ItemType Directory -Force | Out-Null
        }
        
        $script:LogFileStream = [System.IO.StreamWriter]::new(
            $fullPath,
            $false,  # append = false
            [System.Text.Encoding]::UTF8
        )
        $script:LogFileStream.AutoFlush = $true
        
        Write-Log "Log file initialized" -Level Debug -Context @{ path = $fullPath }
    }
    catch {
        Write-Host "[WRN] Could not create log file: $_" -ForegroundColor Yellow
    }
}

function Save-EnvironmentVariable {
    param([string]$Name)
    
    $value = [Environment]::GetEnvironmentVariable($Name)
    $script:OriginalEnv[$Name] = $value
}

function Restore-Environment {
    foreach ($kvp in $script:OriginalEnv.GetEnumerator()) {
        [Environment]::SetEnvironmentVariable($kvp.Key, $kvp.Value)
    }
}

function Close-Resources {
    <#
    .SYNOPSIS
        Memory-safe cleanup of all resources.
    #>
    
    # Close log file stream
    if ($script:LogFileStream) {
        try {
            $script:LogFileStream.Flush()
            $script:LogFileStream.Close()
            $script:LogFileStream.Dispose()
        }
        catch {
            # Ignore cleanup errors
        }
        finally {
            $script:LogFileStream = $null
        }
    }
    
    # Restore original location
    try {
        Set-Location $script:OriginalLocation
    }
    catch {
        # Ignore
    }
    
    # Restore environment variables
    Restore-Environment
    
    # Force garbage collection for memory safety
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
#endregion

#region Compiler Detection
function Find-Compiler {
    <#
    .SYNOPSIS
        Detect available C compiler with detailed logging.
    .OUTPUTS
        Hashtable with Type, Path, Version or $null if not found.
    #>
    
    Write-LogSection "Compiler Detection"
    
    # Check for Visual Studio via vswhere
    $vsWhere = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"
    if (Test-Path $vsWhere) {
        Write-Log "Checking Visual Studio installation" -Level Debug -Context @{ vswhere = $vsWhere }
        
        try {
            $vsPath = & $vsWhere -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath 2>$null
            if ($vsPath -and (Test-Path $vsPath)) {
                $vcVarsAll = Join-Path $vsPath "VC\Auxiliary\Build\vcvarsall.bat"
                if (Test-Path $vcVarsAll) {
                    $vsVersion = & $vsWhere -latest -property catalog_productDisplayVersion 2>$null
                    Write-Log "Found Visual Studio" -Level Info -Context @{
                        path    = $vsPath
                        version = $vsVersion
                    }
                    return @{
                        Type    = "MSVC"
                        Path    = $vcVarsAll
                        Version = $vsVersion
                    }
                }
            }
        }
        catch {
            Write-Log "Visual Studio detection failed" -Level Debug -ErrorRecord $_
        }
    }

    # Check for cl.exe in PATH
    $cl = Get-Command cl.exe -ErrorAction SilentlyContinue
    if ($cl) {
        Write-Log "Found MSVC cl.exe in PATH" -Level Info -Context @{ path = $cl.Source }
        return @{
            Type    = "MSVC_PATH"
            Path    = $cl.Source
            Version = "Unknown"
        }
    }

    # Check for clang
    $clang = Get-Command clang.exe -ErrorAction SilentlyContinue
    if ($clang) {
        $version = "Unknown"
        try {
            $versionOutput = & clang.exe --version 2>&1 | Select-Object -First 1
            if ($versionOutput -match "version\s+([\d.]+)") {
                $version = $Matches[1]
            }
        }
        catch { }
        
        Write-Log "Found Clang" -Level Info -Context @{
            path    = $clang.Source
            version = $version
        }
        return @{
            Type    = "Clang"
            Path    = $clang.Source
            Version = $version
        }
    }

    # Check for gcc (MinGW)
    $gcc = Get-Command gcc.exe -ErrorAction SilentlyContinue
    if ($gcc) {
        $version = "Unknown"
        try {
            $versionOutput = & gcc.exe --version 2>&1 | Select-Object -First 1
            if ($versionOutput -match "(\d+\.\d+\.\d+)") {
                $version = $Matches[1]
            }
        }
        catch { }
        
        Write-Log "Found GCC (MinGW)" -Level Info -Context @{
            path    = $gcc.Source
            version = $version
        }
        return @{
            Type    = "MinGW"
            Path    = $gcc.Source
            Version = $version
        }
    }

    Write-Log "No C compiler found" -Level Error
    return $null
}

function Initialize-MSVCEnvironment {
    <#
    .SYNOPSIS
        Set up Visual Studio build environment safely.
    #>
    param(
        [Parameter(Mandatory)]
        [string]$VcVarsPath
    )
    
    Write-LogSection "MSVC Environment Setup"
    
    $arch = if ([Environment]::Is64BitOperatingSystem) { "x64" } else { "x86" }
    Write-Log "Configuring MSVC environment" -Level Info -Context @{ arch = $arch }
    
    # Save current PATH for restoration
    Save-EnvironmentVariable "PATH"
    Save-EnvironmentVariable "INCLUDE"
    Save-EnvironmentVariable "LIB"
    Save-EnvironmentVariable "LIBPATH"
    
    try {
        $envVars = cmd /c "`"$VcVarsPath`" $arch >nul 2>&1 && set" 2>&1
        if ($LASTEXITCODE -ne 0) {
            throw "vcvarsall.bat failed with exit code $LASTEXITCODE"
        }
        
        $setCount = 0
        $envVars | ForEach-Object {
            if ($_ -match "^([^=]+)=(.*)$") {
                [Environment]::SetEnvironmentVariable($Matches[1], $Matches[2])
                $setCount++
            }
        }
        
        Write-Log "MSVC environment configured" -Level Info -Context @{ variables_set = $setCount }
    }
    catch {
        Write-Log "Failed to configure MSVC environment" -Level Error -ErrorRecord $_
        throw
    }
}

function Show-CompilerHelp {
    Write-Host ""
    Write-Host "No C compiler found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install one of the following:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  1. Visual Studio Build Tools (recommended)" -ForegroundColor White
    Write-Host "     https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  2. LLVM/Clang" -ForegroundColor White
    Write-Host "     winget install LLVM.LLVM" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  3. MinGW-w64" -ForegroundColor White
    Write-Host "     winget install MinGW.MinGW64" -ForegroundColor DarkGray
    Write-Host ""
}
#endregion

#region Build Functions
function Test-Prerequisites {
    <#
    .SYNOPSIS
        Validate all prerequisites before building.
    #>
    
    Write-LogSection "Prerequisites Check"
    $errors = @()
    
    # Check Python/uv
    $uv = Get-Command uv -ErrorAction SilentlyContinue
    if (-not $uv) {
        $errors += "uv (Python package manager) not found. Install from: https://docs.astral.sh/uv/"
    }
    else {
        Write-Log "Found uv" -Level Debug -Context @{ path = $uv.Source }
    }
    
    # Check Git
    $git = Get-Command git -ErrorAction SilentlyContinue
    if (-not $git) {
        $errors += "git not found. Required for cloning grammar repositories."
    }
    else {
        Write-Log "Found git" -Level Debug -Context @{ path = $git.Source }
    }
    
    # Check config file
    $configPath = Resolve-Path $Config -ErrorAction SilentlyContinue
    if (-not $configPath) {
        $errors += "Config file not found: $Config"
    }
    else {
        Write-Log "Config file validated" -Level Debug -Context @{ path = $configPath.Path }
    }
    
    if ($errors.Count -gt 0) {
        foreach ($err in $errors) {
            Write-Log $err -Level Error
        }
        return $false
    }
    
    Write-Log "All prerequisites satisfied" -Level Info
    return $true
}

function Invoke-CleanBuild {
    <#
    .SYNOPSIS
        Clean build artifacts before building.
    #>
    param(
        [Parameter(Mandatory)]
        [string]$ConfigPath
    )
    
    Write-LogSection "Cleaning Build Artifacts"
    
    try {
        $configContent = Get-Content $ConfigPath -Raw | ConvertFrom-Json
        
        if ($configContent.build_dir) {
            $buildDir = [System.IO.Path]::GetFullPath($configContent.build_dir)
            if (Test-Path $buildDir) {
                Write-Log "Removing build directory" -Level Info -Context @{ path = $buildDir }
                Remove-Item -Path $buildDir -Recurse -Force -ErrorAction Stop
            }
        }
        
        if ($configContent.output_path) {
            $outputPath = [System.IO.Path]::GetFullPath($configContent.output_path)
            # Handle different library extensions
            $basePath = [System.IO.Path]::ChangeExtension($outputPath, $null)
            foreach ($ext in @(".dll", ".so", ".dylib", ".lib", ".exp", ".pdb")) {
                $targetPath = "$basePath$ext"
                if (Test-Path $targetPath) {
                    Write-Log "Removing artifact" -Level Debug -Context @{ path = $targetPath }
                    Remove-Item -Path $targetPath -Force -ErrorAction SilentlyContinue
                }
            }
        }
        
        Write-Log "Clean completed" -Level Info
    }
    catch {
        Write-Log "Clean failed" -Level Warning -ErrorRecord $_
        # Continue anyway - clean failure shouldn't stop build
    }
}

function Invoke-Build {
    <#
    .SYNOPSIS
        Execute the tree-sitter build with comprehensive error handling.
    #>
    param(
        [Parameter(Mandatory)]
        [string]$ConfigPath
    )
    
    Write-LogSection "Building Tree-sitter Grammars"
    
    $fullConfigPath = Resolve-Path $ConfigPath
    Write-Log "Starting build" -Level Info -Context @{
        config = $fullConfigPath.Path
    }
    
    # Set up Python environment
    $env:PYTHONPATH = "src"
    
    # Create a temporary file for stderr capture
    $stderrFile = [System.IO.Path]::GetTempFileName()
    $stdoutFile = [System.IO.Path]::GetTempFileName()
    
    try {
        $processInfo = New-Object System.Diagnostics.ProcessStartInfo
        $processInfo.FileName = "uv"
        $processInfo.Arguments = "run python -m migration_agents.parser.build_languages --config `"$fullConfigPath`""
        $processInfo.UseShellExecute = $false
        $processInfo.RedirectStandardOutput = $true
        $processInfo.RedirectStandardError = $true
        $processInfo.CreateNoWindow = $true
        $processInfo.WorkingDirectory = $RootDir
        
        $process = New-Object System.Diagnostics.Process
        $process.StartInfo = $processInfo
        
        # Use StringBuilder for thread-safe output capture
        $stdout = [System.Text.StringBuilder]::new()
        $stderr = [System.Text.StringBuilder]::new()
        
        # Register event handlers for async output reading
        $stdoutEvent = Register-ObjectEvent -InputObject $process -EventName OutputDataReceived -Action {
            if ($EventArgs.Data) {
                $Event.MessageData.AppendLine($EventArgs.Data) | Out-Null
                Write-Host $EventArgs.Data -ForegroundColor Gray
            }
        } -MessageData $stdout
        
        $stderrEvent = Register-ObjectEvent -InputObject $process -EventName ErrorDataReceived -Action {
            if ($EventArgs.Data) {
                $Event.MessageData.AppendLine($EventArgs.Data) | Out-Null
                Write-Host $EventArgs.Data -ForegroundColor DarkYellow
            }
        } -MessageData $stderr
        
        Write-Log "Executing build process" -Level Debug
        
        $started = $process.Start()
        if (-not $started) {
            throw "Failed to start build process"
        }
        
        $process.BeginOutputReadLine()
        $process.BeginErrorReadLine()
        
        # Wait for process with timeout (10 minutes)
        $timeout = 600000  # 10 minutes in milliseconds
        $completed = $process.WaitForExit($timeout)
        
        if (-not $completed) {
            $process.Kill()
            throw "Build process timed out after 10 minutes"
        }
        
        # Give events time to complete
        Start-Sleep -Milliseconds 500
        
        # Unregister events
        Unregister-Event -SourceIdentifier $stdoutEvent.Name
        Unregister-Event -SourceIdentifier $stderrEvent.Name
        
        $exitCode = $process.ExitCode
        $stderrOutput = $stderr.ToString()
        
        Write-Log "Build process completed" -Level Debug -Context @{
            exit_code     = $exitCode
            stderr_length = $stderrOutput.Length
        }
        
        if ($exitCode -ne 0) {
            Write-Log "Build failed with exit code $exitCode" -Level Error -Context @{
                exit_code = $exitCode
            }
            
            if ($stderrOutput) {
                # Parse and log individual errors
                $errorLines = $stderrOutput -split "`n" | Where-Object { $_.Trim() }
                foreach ($line in $errorLines) {
                    if ($line -match "error|Error|ERROR|fatal|Fatal|FATAL") {
                        Write-Log "Compiler error: $line" -Level Error
                    }
                    elseif ($line -match "warning|Warning|WARNING") {
                        Write-Log "Compiler warning: $line" -Level Warning
                    }
                }
            }
            
            return $false
        }
        
        # Check for warnings in successful builds
        if ($stderrOutput -match "warning|Warning|WARNING") {
            $warningCount = ([regex]::Matches($stderrOutput, "warning|Warning|WARNING")).Count
            Write-Log "Build succeeded with warnings" -Level Warning -Context @{
                warning_count = $warningCount
            }
        }
        
        return $true
    }
    catch {
        Write-Log "Build execution failed" -Level Error -ErrorRecord $_
        return $false
    }
    finally {
        # Memory-safe cleanup
        if ($process) {
            try { $process.Dispose() } catch { }
        }
        if (Test-Path $stderrFile) {
            Remove-Item $stderrFile -Force -ErrorAction SilentlyContinue
        }
        if (Test-Path $stdoutFile) {
            Remove-Item $stdoutFile -Force -ErrorAction SilentlyContinue
        }
    }
}

function Show-BuildSummary {
    param(
        [bool]$Success,
        [DateTime]$StartTime
    )
    
    $duration = [DateTime]::UtcNow - $StartTime
    
    Write-Host ""
    Write-Host ("=" * 60) -ForegroundColor Cyan
    
    if ($Success) {
        Write-Host " BUILD SUCCESSFUL" -ForegroundColor Green
    }
    else {
        Write-Host " BUILD FAILED" -ForegroundColor Red
    }
    
    Write-Host ("=" * 60) -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Duration: $($duration.TotalSeconds.ToString('F2')) seconds" -ForegroundColor Gray
    
    if ($script:ErrorList.Count -gt 0) {
        Write-Host ""
        Write-Host "Errors encountered: $($script:ErrorList.Count)" -ForegroundColor Red
        foreach ($err in $script:ErrorList) {
            Write-Host "  - $($err.Message): $($err.Error)" -ForegroundColor DarkRed
        }
    }
    
    if ($LogFile) {
        Write-Host ""
        Write-Host "Full log written to: $LogFile" -ForegroundColor Gray
    }
    
    Write-Host ""
}
#endregion

#region Main Execution
try {
    # Initialize
    $RootDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
    Set-Location $RootDir
    
    Initialize-LogFile -Path $LogFile
    
    Write-LogHeader "Tree-sitter Build Script for Windows"
    
    Write-Log "Build started" -Level Info -Context @{
        config    = $Config
        log_level = $LogLevel
        clean     = $Clean.IsPresent
        cwd       = $RootDir
    }
    
    # Validate prerequisites
    if (-not (Test-Prerequisites)) {
        throw "Prerequisites check failed"
    }
    
    # Find compiler
    $compiler = Find-Compiler
    if (-not $compiler) {
        Show-CompilerHelp
        throw "No C compiler available"
    }
    
    # Set up MSVC environment if needed
    if ($compiler.Type -eq "MSVC") {
        Initialize-MSVCEnvironment -VcVarsPath $compiler.Path
    }
    
    # Clean if requested
    if ($Clean) {
        Invoke-CleanBuild -ConfigPath $Config
    }
    
    # Execute build
    $buildSuccess = Invoke-Build -ConfigPath $Config
    
    # Show summary
    Show-BuildSummary -Success $buildSuccess -StartTime $script:StartTime
    
    if (-not $buildSuccess) {
        exit 1
    }
    
    exit 0
}
catch {
    Write-Log "Fatal error" -Level Error -ErrorRecord $_
    Show-BuildSummary -Success $false -StartTime $script:StartTime
    exit 1
}
finally {
    Close-Resources
}
#endregion
