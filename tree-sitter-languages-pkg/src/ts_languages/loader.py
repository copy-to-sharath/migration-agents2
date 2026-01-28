"""
Language loader for tree-sitter grammars.

Provides functions to load pre-compiled language grammars from the bundled DLL/SO.
"""

import ctypes
import sys
from pathlib import Path
from typing import Optional

import tree_sitter

# Cache for loaded library
_library: Optional[ctypes.CDLL] = None

# Language name mappings (user-friendly name -> symbol name)
LANGUAGE_MAP = {
    # Mainframe
    "cobol": "COBOL",
    "COBOL": "COBOL",
    "jcl": "jcl",
    "JCL": "jcl",
    "bms": "bms",
    "BMS": "bms",
    "cics": "cics",
    "CICS": "cics",
    "csd": "csd",
    "CSD": "csd",
    "idcams": "idcams",
    "IDCAMS": "idcams",
    "hlasm": "hlasm",
    "HLASM": "hlasm",
    "easytrieve": "easytrieve",
    "Easytrieve": "easytrieve",
    "copybook": "copybook",
    # Modern languages
    "python": "python",
    "javascript": "javascript",
    "js": "javascript",
    "typescript": "typescript",
    "ts": "typescript",
    "c_sharp": "c_sharp",
    "csharp": "c_sharp",
    "cs": "c_sharp",
    "java": "java",
    "vb": "vb",
    "vbnet": "vb",
    "html": "html",
    "css": "css",
    "xml": "xml",
    "php": "php",
    "sql": "sql",
}


def get_library_path() -> Path:
    """Get the path to the language library file."""
    lib_dir = Path(__file__).parent / "lib"
    
    if sys.platform == "win32":
        lib_name = "languages.dll"
    elif sys.platform == "darwin":
        lib_name = "languages.dylib"
    else:
        lib_name = "languages.so"
    
    lib_path = lib_dir / lib_name
    if not lib_path.exists():
        raise FileNotFoundError(
            f"Language library not found at {lib_path}. "
            f"This package may not support your platform ({sys.platform})."
        )
    return lib_path


def _get_library() -> ctypes.CDLL:
    """Get or load the shared library."""
    global _library
    if _library is None:
        lib_path = get_library_path()
        _library = ctypes.cdll.LoadLibrary(str(lib_path))
    return _library


def list_languages() -> list[str]:
    """List all available language names."""
    return sorted(set(LANGUAGE_MAP.keys()))


def load_language(name: str) -> tree_sitter.Language:
    """
    Load a tree-sitter language by name.
    
    Args:
        name: Language name (e.g., 'cobol', 'jcl', 'copybook', 'python')
        
    Returns:
        tree_sitter.Language object ready for use with Parser
        
    Raises:
        ValueError: If language name is not recognized
        AttributeError: If language symbol not found in library
        
    Example:
        >>> lang = load_language('copybook')
        >>> parser = tree_sitter.Parser(lang)
        >>> tree = parser.parse(b'01 MY-FIELD PIC X(10).')
    """
    if name not in LANGUAGE_MAP:
        available = ", ".join(sorted(set(LANGUAGE_MAP.values())))
        raise ValueError(
            f"Unknown language '{name}'. Available: {available}"
        )
    
    symbol_name = LANGUAGE_MAP[name]
    func_name = f"tree_sitter_{symbol_name}"
    
    lib = _get_library()
    try:
        func = getattr(lib, func_name)
    except AttributeError:
        raise AttributeError(
            f"Language function '{func_name}' not found in library. "
            f"The library may need to be rebuilt."
        )
    
    func.restype = ctypes.c_void_p
    lang_ptr = func()
    return tree_sitter.Language(lang_ptr)
