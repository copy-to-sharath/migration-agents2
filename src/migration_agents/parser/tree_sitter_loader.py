from __future__ import annotations

import platform
from dataclasses import dataclass
from pathlib import Path
import ctypes

from tree_sitter import Language, Parser


# Platform detection
IS_WINDOWS = platform.system() == "Windows"
IS_MACOS = platform.system() == "Darwin"

# Library extension by platform
LIB_EXT = ".dll" if IS_WINDOWS else (".dylib" if IS_MACOS else ".so")


# Mapping from our language names to actual tree-sitter symbol names
# when they don't match the standard pattern tree_sitter_{name}
LANGUAGE_SYMBOL_MAP = {
    "cobol": "COBOL",      # tree_sitter_COBOL (uppercase)
    "vbnet": "vb",         # tree_sitter_vb (shorter name)
}


@dataclass(frozen=True)
class LanguageBundle:
    name: str
    language: Language


def find_library(library_path: Path) -> Path:
    """
    Find the language library, trying platform-specific extensions.
    This allows configs to specify a base path and have it work cross-platform.
    """
    if library_path.exists():
        return library_path
    
    # Try with platform-specific extension
    base = library_path.parent / library_path.stem
    for ext in [LIB_EXT, ".so", ".dll", ".dylib"]:
        candidate = base.parent / f"{base.name}{ext}"
        if candidate.exists():
            return candidate
    
    # Return original path (will fail with clear error message)
    return library_path


def load_language(library_path: Path, name: str) -> LanguageBundle:
    actual_path = find_library(library_path)
    lib = _load_library(actual_path)
    # Use symbol map for languages with non-standard names
    symbol_name = LANGUAGE_SYMBOL_MAP.get(name, name)
    symbol = f"tree_sitter_{symbol_name}"
    try:
        fn = getattr(lib, symbol)
    except AttributeError as exc:
        raise RuntimeError(f"Missing language symbol: {symbol}") from exc
    fn.restype = ctypes.c_void_p
    ptr = fn()
    return LanguageBundle(name=name, language=Language(ptr))


def build_parser(bundle: LanguageBundle) -> Parser:
    parser = Parser()
    parser.language = bundle.language
    return parser


_LIB_CACHE: dict[str, ctypes.CDLL] = {}


def _load_library(library_path: Path) -> ctypes.CDLL:
    key = str(library_path)
    if key not in _LIB_CACHE:
        _LIB_CACHE[key] = ctypes.CDLL(key)
    return _LIB_CACHE[key]
