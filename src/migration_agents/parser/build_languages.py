from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import sys
import subprocess
import logging
from dataclasses import dataclass
from pathlib import Path

LOGGER = logging.getLogger("migration_agents.parser.build_languages")

# Platform detection
IS_WINDOWS = platform.system() == "Windows"
IS_MACOS = platform.system() == "Darwin"
IS_LINUX = platform.system() == "Linux"

# File extensions by platform
OBJ_EXT = ".obj" if IS_WINDOWS else ".o"
LIB_EXT = ".dll" if IS_WINDOWS else (".dylib" if IS_MACOS else ".so")


@dataclass(frozen=True)
class LanguageSpec:
    name: str
    repo: str
    path: str


@dataclass(frozen=True)
class BuildConfig:
    output_path: Path
    vendor_dir: Path
    build_dir: Path
    core_repo: str | None
    core_dir: Path | None
    languages: list[LanguageSpec]


def load_config(path: Path) -> BuildConfig:
    raw = json.loads(path.read_text(encoding="utf-8"))
    languages = [LanguageSpec(**lang) for lang in raw["languages"]]
    
    # Get output path and adjust extension for platform
    output_path = Path(raw["output_path"]).expanduser().resolve()
    output_path = _adjust_lib_extension(output_path)
    
    return BuildConfig(
        output_path=output_path,
        vendor_dir=Path(raw["vendor_dir"]).expanduser().resolve(),
        build_dir=Path(raw["build_dir"]).expanduser().resolve(),
        core_repo=raw.get("core_repo"),
        core_dir=Path(raw["core_dir"]).expanduser().resolve()
        if raw.get("core_dir")
        else None,
        languages=languages,
    )


def _adjust_lib_extension(path: Path) -> Path:
    """Adjust library extension based on platform."""
    stem = path.stem
    # Remove any existing library extension
    for ext in [".so", ".dll", ".dylib"]:
        if stem.endswith(ext.replace(".", "")):
            stem = stem[:-len(ext) + 1]
    return path.parent / f"{stem}{LIB_EXT}"


def _find_compiler() -> tuple[str, str, bool]:
    """
    Find available C/C++ compiler on the system.
    Returns: (cc_path, cxx_path, is_msvc)
    """
    if IS_WINDOWS:
        # Try to find MSVC cl.exe
        cl_path = shutil.which("cl")
        if cl_path:
            return cl_path, cl_path, True
        
        # Try clang on Windows
        clang_path = shutil.which("clang")
        clangpp_path = shutil.which("clang++")
        if clang_path and clangpp_path:
            return clang_path, clangpp_path, False
        
        # Try MinGW gcc
        gcc_path = shutil.which("gcc")
        gpp_path = shutil.which("g++")
        if gcc_path and gpp_path:
            return gcc_path, gpp_path, False
        
        raise RuntimeError(
            "No C compiler found on Windows. Install one of:\n"
            "  - Visual Studio Build Tools (cl.exe)\n"
            "  - LLVM/Clang\n"
            "  - MinGW-w64"
        )
    else:
        # Unix-like systems
        cc = os.environ.get("CC", "cc")
        cxx = os.environ.get("CXX", "c++")
        return cc, cxx, False


def ensure_repo(spec: LanguageSpec, vendor_dir: Path) -> Path:
    target = vendor_dir / spec.name
    if target.exists():
        return target
    target.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["GIT_ASKPASS"] = "/usr/bin/true"
    env["GIT_CONFIG_COUNT"] = "1"
    env["GIT_CONFIG_KEY_0"] = "credential.helper"
    env["GIT_CONFIG_VALUE_0"] = ""
    subprocess.run(
        ["git", "clone", "--depth", "1", spec.repo, str(target)],
        check=True,
        env=env,
    )
    return target


def ensure_core_repo(core_repo: str | None, core_dir: Path | None) -> Path | None:
    if not core_repo or not core_dir:
        return None
    if core_dir.exists():
        return core_dir
    core_dir.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["GIT_ASKPASS"] = "/usr/bin/true"
    env["GIT_CONFIG_COUNT"] = "1"
    env["GIT_CONFIG_KEY_0"] = "credential.helper"
    env["GIT_CONFIG_VALUE_0"] = ""
    subprocess.run(
        ["git", "clone", "--depth", "1", core_repo, str(core_dir)],
        check=True,
        env=env,
    )
    return core_dir


def collect_sources(grammar_dir: Path) -> tuple[list[Path], list[Path]]:
    src_dir = grammar_dir / "src"
    if not src_dir.exists():
        LOGGER.warning("build_languages_skip missing_src=%s", src_dir)
        return [], []
    c_files = [path for path in src_dir.glob("*.c") if path.name != "lib.c"]
    cc_files = list(src_dir.glob("*.cc"))
    return c_files, cc_files


def compile_objects(
    build_dir: Path,
    grammar_dir: Path,
    c_files: list[Path],
    cc_files: list[Path],
    core_includes: list[Path] | None,
) -> tuple[list[Path], bool]:
    build_dir.mkdir(parents=True, exist_ok=True)
    objects: list[Path] = []
    uses_cxx = bool(cc_files)
    
    cc, cxx, is_msvc = _find_compiler()
    include_dir = grammar_dir / "src"
    
    if is_msvc:
        # MSVC compiler flags
        include_flags = [f"/I{include_dir}", f"/I{include_dir / 'tree_sitter'}"]
        if core_includes:
            include_flags.extend([f"/I{path}" for path in core_includes])
        
        for file_path in c_files:
            obj = build_dir / f"{file_path.stem}{OBJ_EXT}"
            args = [cc, "/nologo", "/c", "/O2", str(file_path), f"/Fo{obj}"]
            args.extend(include_flags)
            subprocess.run(args, check=True)
            objects.append(obj)
        
        for file_path in cc_files:
            obj = build_dir / f"{file_path.stem}{OBJ_EXT}"
            args = [cxx, "/nologo", "/c", "/O2", "/EHsc", str(file_path), f"/Fo{obj}"]
            args.extend(include_flags)
            subprocess.run(args, check=True)
            objects.append(obj)
    else:
        # GCC/Clang compiler flags
        include_flag = f"-I{include_dir}"
        include_tree_sitter = f"-I{include_dir / 'tree_sitter'}"
        core_flags = [f"-I{path}" for path in core_includes] if core_includes else []
        
        for file_path in c_files:
            obj = build_dir / f"{file_path.stem}{OBJ_EXT}"
            args = [cc, "-fPIC", "-c", str(file_path), "-o", str(obj), include_flag, include_tree_sitter]
            args.extend(core_flags)
            subprocess.run(args, check=True)
            objects.append(obj)
        
        for file_path in cc_files:
            obj = build_dir / f"{file_path.stem}{OBJ_EXT}"
            args = [cxx, "-fPIC", "-c", str(file_path), "-o", str(obj), include_flag, include_tree_sitter]
            args.extend(core_flags)
            subprocess.run(args, check=True)
            objects.append(obj)
    
    return objects, uses_cxx


def build_languages(config: BuildConfig) -> None:
    core_repo_dir = ensure_core_repo(config.core_repo, config.core_dir)
    core_includes: list[Path] | None = None
    if core_repo_dir:
        core_includes = _prepare_core_include(config.build_dir, core_repo_dir)
    core_objects: list[Path] = []
    if core_repo_dir:
        core_objects = _compile_core_runtime(config.build_dir, core_repo_dir, core_includes)
    all_objects: list[Path] = []
    uses_cxx = False
    for spec in config.languages:
        repo_dir = ensure_repo(spec, config.vendor_dir)
        grammar_dir = repo_dir / spec.path
        if not grammar_dir.exists():
            LOGGER.warning("build_languages_skip missing_grammar_dir=%s", grammar_dir)
            continue
        c_files, cc_files = collect_sources(grammar_dir)
        if not c_files and not cc_files:
            LOGGER.warning("build_languages_skip no_sources=%s", grammar_dir)
            continue
        build_subdir = config.build_dir / spec.name
        objects, needs_cxx = compile_objects(
            build_subdir, grammar_dir, c_files, cc_files, core_includes
        )
        uses_cxx = uses_cxx or needs_cxx
        all_objects.extend(objects)

    config.output_path.parent.mkdir(parents=True, exist_ok=True)
    
    cc, cxx, is_msvc = _find_compiler()
    linker = cxx if uses_cxx else cc
    all_objs = [str(o) for o in core_objects + all_objects]
    
    if is_msvc:
        # MSVC linker
        subprocess.run(
            [linker, "/nologo", "/LD", f"/Fe{config.output_path}", *all_objs],
            check=True,
        )
    elif IS_MACOS:
        # macOS dynamic library
        subprocess.run(
            [linker, "-dynamiclib", "-o", str(config.output_path), *all_objs],
            check=True,
        )
    elif IS_WINDOWS:
        # MinGW/Clang on Windows - create DLL
        subprocess.run(
            [linker, "-shared", "-o", str(config.output_path), *all_objs],
            check=True,
        )
    else:
        # Linux shared library
        subprocess.run(
            [linker, "-shared", "-o", str(config.output_path), *all_objs],
            check=True,
        )


def _prepare_core_include(build_dir: Path, core_repo_dir: Path) -> list[Path]:
    include_root = build_dir / "tree_sitter_include"
    include_tree_sitter = include_root / "tree_sitter"
    include_tree_sitter.mkdir(parents=True, exist_ok=True)
    core_src = core_repo_dir / "lib" / "src"
    for header in core_src.glob("*.h"):
        target = include_tree_sitter / header.name
        target.write_text(header.read_text(encoding="utf-8"), encoding="utf-8")
    return [include_root, core_repo_dir / "lib" / "include"]


def _compile_core_runtime(
    build_dir: Path,
    core_repo_dir: Path,
    core_includes: list[Path] | None,
) -> list[Path]:
    src_dir = core_repo_dir / "lib" / "src"
    c_files = [path for path in src_dir.glob("*.c") if path.name != "lib.c"]
    if not c_files:
        return []
    core_build = build_dir / "core"
    core_build.mkdir(parents=True, exist_ok=True)
    
    cc, _, is_msvc = _find_compiler()
    objects: list[Path] = []
    
    if is_msvc:
        include_flags = [f"/I{src_dir}"]
        if core_includes:
            include_flags.extend([f"/I{path}" for path in core_includes])
        
        for file_path in c_files:
            obj = core_build / f"{file_path.stem}{OBJ_EXT}"
            subprocess.run(
                [cc, "/nologo", "/c", "/O2", str(file_path), f"/Fo{obj}", *include_flags],
                check=True,
            )
            objects.append(obj)
    else:
        include_flag = f"-I{src_dir}"
        include_flags = [include_flag]
        if core_includes:
            include_flags.extend([f"-I{path}" for path in core_includes])
        
        for file_path in c_files:
            obj = core_build / f"{file_path.stem}{OBJ_EXT}"
            subprocess.run(
                [cc, "-fPIC", "-c", str(file_path), "-o", str(obj), *include_flags],
                check=True,
            )
            objects.append(obj)
    
    return objects


def main() -> None:
    parser = argparse.ArgumentParser(description="Build tree-sitter languages.so")
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    config = load_config(args.config)
    build_languages(config)


if __name__ == "__main__":
    main()
