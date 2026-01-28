from __future__ import annotations

import logging
import platform
from dataclasses import dataclass
from pathlib import Path
import ctypes
from typing import Callable

from tree_sitter import Language, Parser


LOGGER = logging.getLogger("migration_agents.parser.tree_sitter_loader")

# Platform detection
IS_WINDOWS = platform.system() == "Windows"
IS_MACOS = platform.system() == "Darwin"
IS_LINUX = platform.system() == "Linux"

# Library extension by platform
LIB_EXT = ".dll" if IS_WINDOWS else (".dylib" if IS_MACOS else ".so")

# Platform identifier for library paths
PLATFORM_ID = f"{platform.system().lower()}_{platform.machine().lower()}"


# Mapping from our language names to actual tree-sitter symbol names
# when they don't match the standard pattern tree_sitter_{name}
LANGUAGE_SYMBOL_MAP = {
    "cobol": "COBOL",      # tree_sitter_COBOL (uppercase)
    "vbnet": "vb",         # tree_sitter_vb (shorter name)
}

# Languages available as pip-installable packages (tree-sitter-{name})
# These provide cross-platform wheels with pre-built binaries
WHEEL_AVAILABLE_LANGUAGES = {
    "python",
    "javascript", 
    "typescript",
    "c_sharp",
    "html",
    "css",
    "sql",
    "xml",
    "php",
    "java",
}

# Languages that require compilation (no wheel packages available)
# These are mainframe and custom languages
COMPILED_ONLY_LANGUAGES = {
    "vbnet",       # VB.NET
    "cobol",       # COBOL
    "jcl",         # JCL (Job Control Language)
    "hlasm",       # IBM High Level Assembler
    "cics",        # CICS (custom grammar)
    "bms",         # BMS (Basic Mapping Support, custom grammar)
    "easytrieve",  # Easytrieve (custom grammar)
}


@dataclass(frozen=True)
class LanguageBundle:
    name: str
    language: Language
    source: str  # "wheel" or "compiled"


def try_load_from_wheel(name: str) -> LanguageBundle | None:
    """
    Try to load a language from its pip-installed wheel package.
    
    These packages (tree-sitter-python, tree-sitter-javascript, etc.)
    provide cross-platform pre-built binaries.
    """
    if name not in WHEEL_AVAILABLE_LANGUAGES:
        return None
    
    # Map language names to package module names
    module_map = {
        "c_sharp": "tree_sitter_c_sharp",
        "javascript": "tree_sitter_javascript",
        "typescript": "tree_sitter_typescript",
        "python": "tree_sitter_python",
        "html": "tree_sitter_html",
        "css": "tree_sitter_css",
        "sql": "tree_sitter_sql",
        "xml": "tree_sitter_xml",
        "php": "tree_sitter_php",
        "java": "tree_sitter_java",
    }
    
    module_name = module_map.get(name, f"tree_sitter_{name}")
    
    try:
        import importlib
        module = importlib.import_module(module_name)
        
        # The wheel packages export a language() function
        if hasattr(module, "language"):
            lang = module.language()
            LOGGER.debug("load_from_wheel success name=%s module=%s", name, module_name)
            return LanguageBundle(name=name, language=lang, source="wheel")
        
        # Some packages use LANGUAGE constant
        if hasattr(module, "LANGUAGE"):
            LOGGER.debug("load_from_wheel success name=%s module=%s", name, module_name)
            return LanguageBundle(name=name, language=module.LANGUAGE, source="wheel")
            
    except ImportError:
        LOGGER.debug("load_from_wheel unavailable name=%s module=%s", name, module_name)
    except Exception as e:
        LOGGER.warning("load_from_wheel failed name=%s error=%s", name, str(e))
    
    return None


def find_library(library_path: Path) -> Path:
    """
    Find the language library, trying platform-specific paths and extensions.
    
    Supports cross-platform library organization:
      - tree-sitter/languages.so          (single platform)
      - tree-sitter/linux_x86_64/languages.so    (multi-platform)
      - tree-sitter/windows_amd64/languages.dll
      - tree-sitter/darwin_arm64/languages.dylib
    """
    if library_path.exists():
        return library_path
    
    base_dir = library_path.parent
    stem = library_path.stem
    
    # Try platform-specific subdirectory first
    platform_paths = [
        base_dir / PLATFORM_ID / f"{stem}{LIB_EXT}",
        base_dir / platform.system().lower() / f"{stem}{LIB_EXT}",
    ]
    
    for candidate in platform_paths:
        if candidate.exists():
            LOGGER.debug("find_library platform_specific path=%s", candidate)
            return candidate
    
    # Try with platform-specific extension in same directory
    for ext in [LIB_EXT, ".so", ".dll", ".dylib"]:
        candidate = base_dir / f"{stem}{ext}"
        if candidate.exists():
            LOGGER.debug("find_library fallback path=%s", candidate)
            return candidate
    
    # Return original path (will fail with clear error message)
    return library_path


def load_language(
    library_path: Path,
    name: str,
    prefer_wheel: bool = True,
) -> LanguageBundle:
    """
    Load a tree-sitter language, trying multiple sources.
    
    Args:
        library_path: Path to compiled language library
        name: Language name (e.g., "python", "c_sharp")
        prefer_wheel: If True, try wheel packages before compiled library
    
    Returns:
        LanguageBundle with loaded language
    
    The loading order (when prefer_wheel=True):
        1. Pip-installed wheel package (cross-platform)
        2. Compiled library from library_path
    """
    # Try wheel first if preferred and available
    if prefer_wheel:
        bundle = try_load_from_wheel(name)
        if bundle:
            return bundle
    
    # Fall back to compiled library
    return load_language_from_library(library_path, name)


def load_language_from_library(library_path: Path, name: str) -> LanguageBundle:
    """Load a language from a compiled shared library."""
    actual_path = find_library(library_path)
    
    if not actual_path.exists():
        raise FileNotFoundError(
            f"Language library not found: {library_path}\n"
            f"Searched: {actual_path}\n"
            f"Platform: {PLATFORM_ID}\n"
            f"Run 'scripts/build_treesitter.ps1' (Windows) or "
            f"'scripts/build_treesitter.sh' (Linux/macOS) to build."
        )
    
    lib = _load_library(actual_path)
    
    # Use symbol map for languages with non-standard names
    symbol_name = LANGUAGE_SYMBOL_MAP.get(name, name)
    symbol = f"tree_sitter_{symbol_name}"
    
    try:
        fn = getattr(lib, symbol)
    except AttributeError as exc:
        raise RuntimeError(
            f"Missing language symbol: {symbol} in {actual_path}\n"
            f"Available symbols may differ. Check the grammar's export name."
        ) from exc
    
    fn.restype = ctypes.c_void_p
    ptr = fn()
    
    LOGGER.debug(
        "load_language_from_library success name=%s path=%s",
        name,
        actual_path,
    )
    
    return LanguageBundle(name=name, language=Language(ptr), source="compiled")


def build_parser(bundle: LanguageBundle) -> Parser:
    """Create a parser for a language bundle.
    
    Raises:
        RuntimeError: If parser creation fails (e.g., invalid language bundle).
    """
    try:
        parser = Parser()
        parser.language = bundle.language
        return parser
    except Exception as exc:
        raise RuntimeError(
            f"Failed to create parser for language '{bundle.name}' "
            f"(source: {bundle.source}): {exc}"
        ) from exc


def get_available_wheel_languages() -> list[str]:
    """
    Get list of languages that can be loaded from wheel packages.
    
    Useful for determining which languages don't need compilation.
    """
    available = []
    for name in WHEEL_AVAILABLE_LANGUAGES:
        bundle = try_load_from_wheel(name)
        if bundle:
            available.append(name)
    return available


_LIB_CACHE: dict[str, ctypes.CDLL] = {}


def _load_library(library_path: Path) -> ctypes.CDLL:
    """Load a shared library with caching."""
    key = str(library_path)
    if key not in _LIB_CACHE:
        try:
            _LIB_CACHE[key] = ctypes.CDLL(key)
        except OSError as e:
            raise RuntimeError(
                f"Failed to load library: {library_path}\n"
                f"Platform: {PLATFORM_ID}\n"
                f"Error: {e}\n"
                f"Make sure the library was compiled for this platform."
            ) from e
    return _LIB_CACHE[key]


def clear_library_cache() -> None:
    """Clear the library cache. Useful for testing."""
    _LIB_CACHE.clear()
