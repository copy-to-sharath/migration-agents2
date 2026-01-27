from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import ctypes

from tree_sitter import Language, Parser


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


def load_language(library_path: Path, name: str) -> LanguageBundle:
    lib = _load_library(library_path)
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
