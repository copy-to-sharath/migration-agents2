#!/usr/bin/env bash
#
# Build tree-sitter language grammars
#
# Usage:
#   ./scripts/build_treesitter.sh [config_file]
#
# Example:
#   ./scripts/build_treesitter.sh
#   ./scripts/build_treesitter.sh config/custom_parser.json
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR"

CONFIG="${1:-config/parser.json}"

echo "=== Tree-sitter Build Script ==="
echo ""

# Check for C compiler
if command -v cc &> /dev/null; then
    echo "Found compiler: $(cc --version | head -n1)"
elif command -v gcc &> /dev/null; then
    export CC=gcc
    export CXX=g++
    echo "Found compiler: $(gcc --version | head -n1)"
elif command -v clang &> /dev/null; then
    export CC=clang
    export CXX=clang++
    echo "Found compiler: $(clang --version | head -n1)"
else
    echo "ERROR: No C compiler found!"
    echo ""
    echo "Please install a C compiler:"
    echo "  Ubuntu/Debian: sudo apt install build-essential"
    echo "  macOS: xcode-select --install"
    echo "  Fedora: sudo dnf install gcc gcc-c++"
    exit 1
fi

echo ""
echo "Building tree-sitter grammars..."
echo "Config: $CONFIG"
echo ""

export PYTHONPATH="${PYTHONPATH:-}:src"

uv run python -m migration_agents.parser.build_languages --config "$CONFIG"

echo ""
echo "Build completed successfully!"
