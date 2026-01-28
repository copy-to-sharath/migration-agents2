#!/usr/bin/env bash
#
# Build tree-sitter language grammars
#
# Features:
#   - Structured JSON logging with timestamps
#   - Comprehensive error capture and reporting
#   - Memory-safe resource cleanup via trap handlers
#   - Configurable log levels
#
# Usage:
#   ./scripts/build_treesitter.sh [OPTIONS] [config_file]
#
# Options:
#   -l, --log-level   Log level: debug, info, warning, error (default: info)
#   -f, --log-file    Write logs to file (JSON format)
#   -c, --clean       Clean build artifacts before building
#   -h, --help        Show this help message
#
# Examples:
#   ./scripts/build_treesitter.sh
#   ./scripts/build_treesitter.sh config/custom_parser.json
#   ./scripts/build_treesitter.sh --log-level debug --log-file build.log
#   ./scripts/build_treesitter.sh --clean
#

set -euo pipefail

#=============================================================================
# Configuration
#=============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Defaults
CONFIG="config/tree_sitter_build.json"
LOG_LEVEL="info"
LOG_FILE=""
CLEAN=false

# Script state
START_TIME=$(date +%s.%N)
ORIGINAL_DIR=$(pwd)
ERROR_COUNT=0
TEMP_FILES=()

# Log level values
declare -A LOG_LEVELS=(
    [debug]=0
    [info]=1
    [warning]=2
    [error]=3
)

#=============================================================================
# Cleanup and Signal Handling
#=============================================================================

cleanup() {
    local exit_code=$?
    
    # Remove temporary files
    for temp_file in "${TEMP_FILES[@]}"; do
        if [[ -f "$temp_file" ]]; then
            rm -f "$temp_file" 2>/dev/null || true
        fi
    done
    
    # Restore original directory
    cd "$ORIGINAL_DIR" 2>/dev/null || true
    
    # Close log file descriptor if open
    if [[ -n "$LOG_FILE" ]] && { true >&3; } 2>/dev/null; then
        exec 3>&-
    fi
    
    exit $exit_code
}

trap cleanup EXIT
trap 'log error "Interrupted by signal"; exit 130' INT TERM

#=============================================================================
# Logging Functions
#=============================================================================

# Get current timestamp in ISO 8601 format
get_timestamp() {
    date -u +"%Y-%m-%dT%H:%M:%S.%3NZ" 2>/dev/null || date -u +"%Y-%m-%dT%H:%M:%SZ"
}

# Get elapsed time in seconds
get_elapsed() {
    local now
    now=$(date +%s.%N)
    echo "$now - $START_TIME" | bc 2>/dev/null || echo "0"
}

# Check if log level should be output
should_log() {
    local level=$1
    local configured_level=${LOG_LEVELS[$LOG_LEVEL]:-1}
    local message_level=${LOG_LEVELS[$level]:-1}
    [[ $message_level -ge $configured_level ]]
}

# Main logging function with structured output
log() {
    local level="${1:-info}"
    local message="${2:-}"
    shift 2 || true
    
    # Check if we should log this level
    if ! should_log "$level"; then
        return 0
    fi
    
    local timestamp
    timestamp=$(get_timestamp)
    local elapsed
    elapsed=$(get_elapsed)
    
    # Build context from remaining arguments (key=value pairs)
    local context=""
    local json_context=""
    while [[ $# -gt 0 ]]; do
        local pair="$1"
        if [[ "$pair" == *"="* ]]; then
            local key="${pair%%=*}"
            local value="${pair#*=}"
            context="${context:+$context }$key=$value"
            json_context="${json_context:+$json_context, }\"$key\": \"$value\""
        fi
        shift
    done
    
    # Console output with colors
    local color=""
    local prefix=""
    case "$level" in
        debug)   color="\033[0;90m"; prefix="[DBG]" ;;
        info)    color="\033[0;37m"; prefix="[INF]" ;;
        warning) color="\033[0;33m"; prefix="[WRN]"; ((ERROR_COUNT++)) || true ;;
        error)   color="\033[0;31m"; prefix="[ERR]"; ((ERROR_COUNT++)) || true ;;
    esac
    local reset="\033[0m"
    
    local console_msg="$prefix $message"
    if [[ -n "$context" ]]; then
        console_msg="$console_msg | $context"
    fi
    
    echo -e "${color}${console_msg}${reset}" >&2
    
    # JSON log file output
    if [[ -n "$LOG_FILE" ]]; then
        local json_entry
        json_entry=$(cat <<EOF
{"timestamp": "$timestamp", "elapsed_s": $elapsed, "level": "${level^^}", "message": "$message"${json_context:+, $json_context}}
EOF
)
        echo "$json_entry" >> "$LOG_FILE"
    fi
}

log_header() {
    local title="$1"
    local separator="============================================================"
    echo "" >&2
    echo -e "\033[0;36m$separator\033[0m" >&2
    echo -e "\033[0;36m $title\033[0m" >&2
    echo -e "\033[0;36m$separator\033[0m" >&2
    echo "" >&2
}

log_section() {
    local title="$1"
    echo "" >&2
    echo -e "\033[0;36m--- $title ---\033[0m" >&2
}

#=============================================================================
# Utility Functions
#=============================================================================

show_help() {
    cat << 'EOF'
Build tree-sitter language grammars

Usage:
    ./scripts/build_treesitter.sh [OPTIONS] [config_file]

Options:
    -l, --log-level LEVEL   Log level: debug, info, warning, error (default: info)
    -f, --log-file FILE     Write logs to file (JSON format)
    -c, --clean             Clean build artifacts before building
    -h, --help              Show this help message

Arguments:
    config_file             Path to build configuration (default: config/parser.json)

Examples:
    ./scripts/build_treesitter.sh
    ./scripts/build_treesitter.sh config/custom_parser.json
    ./scripts/build_treesitter.sh --log-level debug --log-file build.log
    ./scripts/build_treesitter.sh --clean -l debug

EOF
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -l|--log-level)
                if [[ -z "${2:-}" ]]; then
                    log error "Missing value for --log-level"
                    exit 1
                fi
                LOG_LEVEL="${2,,}"  # lowercase
                if [[ ! "${LOG_LEVELS[$LOG_LEVEL]+isset}" ]]; then
                    log error "Invalid log level: $LOG_LEVEL" "valid=debug,info,warning,error"
                    exit 1
                fi
                shift 2
                ;;
            -f|--log-file)
                if [[ -z "${2:-}" ]]; then
                    log error "Missing value for --log-file"
                    exit 1
                fi
                LOG_FILE="$2"
                shift 2
                ;;
            -c|--clean)
                CLEAN=true
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            -*)
                log error "Unknown option: $1"
                show_help
                exit 1
                ;;
            *)
                if [[ -z "$CONFIG" ]]; then
                    CONFIG="$1"
                else
                    log error "Unexpected argument: $1"
                    exit 1
                fi
                shift
                ;;
        esac
    done
    
    # Set default config if not specified
    CONFIG="${CONFIG:-config/tree_sitter_build.json}"
}

init_log_file() {
    if [[ -n "$LOG_FILE" ]]; then
        local log_dir
        log_dir=$(dirname "$LOG_FILE")
        if [[ -n "$log_dir" ]] && [[ ! -d "$log_dir" ]]; then
            mkdir -p "$log_dir"
        fi
        # Create/truncate log file
        : > "$LOG_FILE"
        log debug "Log file initialized" "path=$LOG_FILE"
    fi
}

#=============================================================================
# Compiler Detection
#=============================================================================

find_compiler() {
    log_section "Compiler Detection"
    
    local cc=""
    local cxx=""
    local version=""
    
    # Check CC environment variable first
    if [[ -n "${CC:-}" ]] && command -v "$CC" &>/dev/null; then
        cc="$CC"
        cxx="${CXX:-c++}"
        version=$("$cc" --version 2>/dev/null | head -n1 || echo "Unknown")
        log info "Using compiler from CC environment variable" "cc=$cc" "version=$version"
        export CC="$cc"
        export CXX="$cxx"
        return 0
    fi
    
    # Try to find cc (default system compiler)
    if command -v cc &>/dev/null; then
        version=$(cc --version 2>/dev/null | head -n1 || echo "Unknown")
        log info "Found system compiler (cc)" "version=$version"
        return 0
    fi
    
    # Try gcc
    if command -v gcc &>/dev/null; then
        version=$(gcc --version 2>/dev/null | head -n1 || echo "Unknown")
        log info "Found GCC" "version=$version"
        export CC=gcc
        export CXX=g++
        return 0
    fi
    
    # Try clang
    if command -v clang &>/dev/null; then
        version=$(clang --version 2>/dev/null | head -n1 || echo "Unknown")
        log info "Found Clang" "version=$version"
        export CC=clang
        export CXX=clang++
        return 0
    fi
    
    log error "No C compiler found"
    return 1
}

show_compiler_help() {
    echo "" >&2
    echo -e "\033[0;31mNo C compiler found!\033[0m" >&2
    echo "" >&2
    echo -e "\033[0;33mPlease install a C compiler:\033[0m" >&2
    echo "" >&2
    echo "  Ubuntu/Debian: sudo apt install build-essential" >&2
    echo "  macOS:         xcode-select --install" >&2
    echo "  Fedora:        sudo dnf install gcc gcc-c++" >&2
    echo "  Arch:          sudo pacman -S base-devel" >&2
    echo "" >&2
}

#=============================================================================
# Prerequisite Checks
#=============================================================================

check_prerequisites() {
    log_section "Prerequisites Check"
    
    local errors=0
    
    # Check uv
    if ! command -v uv &>/dev/null; then
        log error "uv (Python package manager) not found" "install=https://docs.astral.sh/uv/"
        ((errors++))
    else
        log debug "Found uv" "path=$(command -v uv)"
    fi
    
    # Check git
    if ! command -v git &>/dev/null; then
        log error "git not found (required for cloning grammars)"
        ((errors++))
    else
        log debug "Found git" "path=$(command -v git)"
    fi
    
    # Check config file
    if [[ ! -f "$CONFIG" ]]; then
        log error "Config file not found" "path=$CONFIG"
        ((errors++))
    else
        log debug "Config file validated" "path=$CONFIG"
    fi
    
    if [[ $errors -gt 0 ]]; then
        return 1
    fi
    
    log info "All prerequisites satisfied"
    return 0
}

#=============================================================================
# Build Functions
#=============================================================================

clean_build() {
    log_section "Cleaning Build Artifacts"
    
    if [[ ! -f "$CONFIG" ]]; then
        log warning "Cannot clean: config file not found"
        return 0
    fi
    
    # Parse build_dir and output_path from config
    local build_dir
    local output_path
    
    build_dir=$(python3 -c "import json; print(json.load(open('$CONFIG')).get('build_dir', ''))" 2>/dev/null || echo "")
    output_path=$(python3 -c "import json; print(json.load(open('$CONFIG')).get('output_path', ''))" 2>/dev/null || echo "")
    
    if [[ -n "$build_dir" ]] && [[ -d "$build_dir" ]]; then
        log info "Removing build directory" "path=$build_dir"
        rm -rf "$build_dir"
    fi
    
    if [[ -n "$output_path" ]]; then
        local base_path="${output_path%.*}"
        for ext in .so .dll .dylib; do
            local target="${base_path}${ext}"
            if [[ -f "$target" ]]; then
                log debug "Removing artifact" "path=$target"
                rm -f "$target"
            fi
        done
    fi
    
    log info "Clean completed"
}

run_build() {
    log_section "Building Tree-sitter Grammars"
    
    local full_config
    full_config=$(cd "$ROOT_DIR" && realpath "$CONFIG")
    
    log info "Starting build" "config=$full_config"
    
    # Set up Python path
    export PYTHONPATH="${PYTHONPATH:-}:src"
    
    # Create temp files for output capture
    local stdout_file
    local stderr_file
    stdout_file=$(mktemp)
    stderr_file=$(mktemp)
    TEMP_FILES+=("$stdout_file" "$stderr_file")
    
    local exit_code=0
    
    # Run build with output capture
    # Use tee to show output in real-time while also capturing it
    {
        uv run python -m migration_agents.parser.build_languages --config "$CONFIG" 2>&1 | \
        while IFS= read -r line; do
            echo "$line"
            # Log compiler warnings/errors
            if [[ "$line" =~ [Ee]rror|ERROR|[Ff]atal|FATAL ]]; then
                log error "Compiler: $line"
            elif [[ "$line" =~ [Ww]arning|WARNING ]]; then
                log warning "Compiler: $line"
            fi
        done
    } || exit_code=$?
    
    if [[ $exit_code -ne 0 ]]; then
        log error "Build failed" "exit_code=$exit_code"
        return 1
    fi
    
    log info "Build completed successfully"
    return 0
}

show_summary() {
    local success="$1"
    local end_time
    end_time=$(date +%s.%N)
    local duration
    duration=$(echo "$end_time - $START_TIME" | bc 2>/dev/null || echo "0")
    
    echo "" >&2
    echo "============================================================" >&2
    
    if [[ "$success" == "true" ]]; then
        echo -e "\033[0;32m BUILD SUCCESSFUL\033[0m" >&2
    else
        echo -e "\033[0;31m BUILD FAILED\033[0m" >&2
    fi
    
    echo "============================================================" >&2
    echo "" >&2
    printf "Duration: %.2f seconds\n" "$duration" >&2
    
    if [[ $ERROR_COUNT -gt 0 ]]; then
        echo "" >&2
        echo -e "\033[0;31mErrors/Warnings encountered: $ERROR_COUNT\033[0m" >&2
    fi
    
    if [[ -n "$LOG_FILE" ]]; then
        echo "" >&2
        echo "Full log written to: $LOG_FILE" >&2
    fi
    
    echo "" >&2
}

#=============================================================================
# Main Execution
#=============================================================================

main() {
    parse_args "$@"
    
    cd "$ROOT_DIR"
    
    init_log_file
    
    log_header "Tree-sitter Build Script"
    
    log info "Build started" \
        "config=$CONFIG" \
        "log_level=$LOG_LEVEL" \
        "clean=$CLEAN" \
        "cwd=$ROOT_DIR"
    
    # Check prerequisites
    if ! check_prerequisites; then
        show_summary "false"
        exit 1
    fi
    
    # Find compiler
    if ! find_compiler; then
        show_compiler_help
        show_summary "false"
        exit 1
    fi
    
    # Clean if requested
    if [[ "$CLEAN" == "true" ]]; then
        clean_build
    fi
    
    # Run build
    if run_build; then
        show_summary "true"
        exit 0
    else
        show_summary "false"
        exit 1
    fi
}

main "$@"
