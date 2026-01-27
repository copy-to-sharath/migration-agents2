<# 
.SYNOPSIS
    Build tree-sitter language grammars on Windows.

.DESCRIPTION
    This script builds the tree-sitter language grammars into a DLL file
    that can be loaded by the migration-agents parser.

.PARAMETER Config
    Path to the build configuration JSON file.
    Default: config/parser.json

.EXAMPLE
    .\scripts\build_treesitter.ps1
    .\scripts\build_treesitter.ps1 -Config config/custom_parser.json

.NOTES
    Requires one of:
    - Visual Studio Build Tools (cl.exe) - recommended
    - LLVM/Clang
    - MinGW-w64
#>

param(
    [string]$Config = "config/parser.json"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RootDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $RootDir

# Check for available compilers
function Find-Compiler {
    # Check for Visual Studio cl.exe
    $vsWhere = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"
    if (Test-Path $vsWhere) {
        $vsPath = & $vsWhere -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
        if ($vsPath) {
            $vcVarsAll = Join-Path $vsPath "VC\Auxiliary\Build\vcvarsall.bat"
            if (Test-Path $vcVarsAll) {
                Write-Host "Found Visual Studio at: $vsPath" -ForegroundColor Green
                return @{ Type = "MSVC"; Path = $vcVarsAll }
            }
        }
    }

    # Check for cl.exe in PATH
    $cl = Get-Command cl.exe -ErrorAction SilentlyContinue
    if ($cl) {
        Write-Host "Found cl.exe in PATH" -ForegroundColor Green
        return @{ Type = "MSVC_PATH"; Path = $cl.Source }
    }

    # Check for clang
    $clang = Get-Command clang.exe -ErrorAction SilentlyContinue
    if ($clang) {
        Write-Host "Found Clang at: $($clang.Source)" -ForegroundColor Green
        return @{ Type = "Clang"; Path = $clang.Source }
    }

    # Check for gcc (MinGW)
    $gcc = Get-Command gcc.exe -ErrorAction SilentlyContinue
    if ($gcc) {
        Write-Host "Found GCC (MinGW) at: $($gcc.Source)" -ForegroundColor Green
        return @{ Type = "MinGW"; Path = $gcc.Source }
    }

    return $null
}

Write-Host "=== Tree-sitter Build Script for Windows ===" -ForegroundColor Cyan
Write-Host ""

$compiler = Find-Compiler
if (-not $compiler) {
    Write-Host "ERROR: No C compiler found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install one of the following:" -ForegroundColor Yellow
    Write-Host "  1. Visual Studio Build Tools (recommended)" -ForegroundColor White
    Write-Host "     https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  2. LLVM/Clang" -ForegroundColor White
    Write-Host "     winget install LLVM.LLVM" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  3. MinGW-w64" -ForegroundColor White
    Write-Host "     winget install MinGW.MinGW64" -ForegroundColor Gray
    exit 1
}

# If MSVC, set up the environment
if ($compiler.Type -eq "MSVC") {
    Write-Host "Setting up Visual Studio environment..." -ForegroundColor Yellow
    $arch = if ([Environment]::Is64BitOperatingSystem) { "x64" } else { "x86" }
    cmd /c "`"$($compiler.Path)`" $arch && set" | ForEach-Object {
        if ($_ -match "^([^=]+)=(.*)$") {
            [Environment]::SetEnvironmentVariable($matches[1], $matches[2])
        }
    }
}

Write-Host ""
Write-Host "Building tree-sitter grammars..." -ForegroundColor Yellow
Write-Host "Config: $Config" -ForegroundColor Gray
Write-Host ""

$env:PYTHONPATH = "src"

try {
    uv run python -m migration_agents.parser.build_languages --config $Config
    Write-Host ""
    Write-Host "Build completed successfully!" -ForegroundColor Green
} catch {
    Write-Host ""
    Write-Host "Build failed: $_" -ForegroundColor Red
    exit 1
}
