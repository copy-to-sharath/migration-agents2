from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import sys
import subprocess
import logging
import tempfile
import gc
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Generator

LOGGER = logging.getLogger("migration_agents.parser.build_languages")

# Platform detection
IS_WINDOWS = platform.system() == "Windows"
IS_MACOS = platform.system() == "Darwin"
IS_LINUX = platform.system() == "Linux"

# File extensions by platform
OBJ_EXT = ".obj" if IS_WINDOWS else ".o"
LIB_EXT = ".dll" if IS_WINDOWS else (".dylib" if IS_MACOS else ".so")


class BuildError(Exception):
    """Custom exception for build errors with structured context."""
    
    def __init__(self, message: str, context: dict[str, Any] | None = None):
        super().__init__(message)
        self.context = context or {}
    
    def __str__(self) -> str:
        if self.context:
            ctx_str = " ".join(f"{k}={v}" for k, v in self.context.items())
            return f"{super().__str__()} | {ctx_str}"
        return super().__str__()


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


@dataclass
class BuildStats:
    """Track build statistics for reporting."""
    languages_processed: int = 0
    objects_compiled: int = 0
    warnings_count: int = 0
    errors_count: int = 0
    source_files: list[str] = field(default_factory=list)
    failed_languages: list[str] = field(default_factory=list)


def load_config(path: Path) -> BuildConfig:
    """Load build configuration from JSON file with validation."""
    LOGGER.info("load_config start path=%s", path)
    
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise BuildError("Invalid JSON in config file", {"path": str(path), "error": str(e)})
    except FileNotFoundError:
        raise BuildError("Config file not found", {"path": str(path)})
    
    # Validate required fields
    required_fields = ["output_path", "vendor_dir", "build_dir", "languages"]
    missing = [f for f in required_fields if f not in raw]
    if missing:
        raise BuildError("Missing required config fields", {"fields": ", ".join(missing)})
    
    # Parse languages, skipping comment entries (those with _comment or missing required fields)
    languages = []
    for lang in raw["languages"]:
        # Skip comment/metadata entries
        if "_comment" in lang or "_note" in lang and "name" not in lang:
            continue
        # Skip entries without required fields
        if not all(k in lang for k in ["name", "repo", "path"]):
            continue
        languages.append(LanguageSpec(
            name=lang["name"],
            repo=lang["repo"],
            path=lang["path"],
        ))
    
    # Get output path and adjust extension for platform
    output_path = Path(raw["output_path"]).expanduser().resolve()
    output_path = _adjust_lib_extension(output_path)
    
    config = BuildConfig(
        output_path=output_path,
        vendor_dir=Path(raw["vendor_dir"]).expanduser().resolve(),
        build_dir=Path(raw["build_dir"]).expanduser().resolve(),
        core_repo=raw.get("core_repo"),
        core_dir=Path(raw["core_dir"]).expanduser().resolve()
        if raw.get("core_dir")
        else None,
        languages=languages,
    )
    
    LOGGER.info(
        "load_config complete languages=%d output=%s",
        len(languages),
        config.output_path,
    )
    return config


def _adjust_lib_extension(path: Path) -> Path:
    """Adjust library extension based on platform."""
    stem = path.stem
    # Remove any existing library extension
    for ext in [".so", ".dll", ".dylib"]:
        if stem.endswith(ext.replace(".", "")):
            stem = stem[:-len(ext) + 1]
    return path.parent / f"{stem}{LIB_EXT}"


@contextmanager
def _temp_file_context() -> Generator[Path, None, None]:
    """Context manager for temporary file with guaranteed cleanup."""
    temp_path = Path(tempfile.mktemp())
    try:
        yield temp_path
    finally:
        if temp_path.exists():
            try:
                temp_path.unlink()
            except OSError:
                pass


def _run_subprocess(
    args: list[str],
    description: str,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    capture_output: bool = True,
) -> subprocess.CompletedProcess[str]:
    """
    Run subprocess with comprehensive error handling and logging.
    
    Memory-safe: Uses communicate() with timeout to prevent hangs.
    """
    LOGGER.debug("subprocess_start cmd=%s", " ".join(args[:3]) + ("..." if len(args) > 3 else ""))
    
    try:
        result = subprocess.run(
            args,
            check=False,  # We handle errors ourselves
            capture_output=capture_output,
            text=True,
            cwd=cwd,
            env=env,
            timeout=300,  # 5 minute timeout per command
        )
        
        if result.returncode != 0:
            error_output = result.stderr or result.stdout or "No output"
            LOGGER.error(
                "subprocess_failed cmd=%s exit_code=%d error=%s",
                args[0],
                result.returncode,
                error_output[:200],
            )
            raise BuildError(
                f"{description} failed",
                {
                    "command": args[0],
                    "exit_code": result.returncode,
                    "stderr": error_output[:500],
                },
            )
        
        # Log warnings from successful builds
        if result.stderr and ("warning" in result.stderr.lower()):
            warning_count = result.stderr.lower().count("warning")
            LOGGER.warning(
                "subprocess_warnings cmd=%s count=%d",
                args[0],
                warning_count,
            )
        
        return result
        
    except subprocess.TimeoutExpired as e:
        LOGGER.error("subprocess_timeout cmd=%s", args[0])
        raise BuildError(f"{description} timed out", {"command": args[0]})
    except FileNotFoundError:
        LOGGER.error("subprocess_not_found cmd=%s", args[0])
        raise BuildError(f"Command not found: {args[0]}", {"command": args[0]})


def _find_compiler() -> tuple[str, str, bool]:
    """
    Find available C/C++ compiler on the system.
    
    Returns: (cc_path, cxx_path, is_msvc)
    Raises: BuildError if no compiler found
    """
    LOGGER.debug("find_compiler start platform=%s", platform.system())
    
    if IS_WINDOWS:
        # Try to find MSVC cl.exe
        cl_path = shutil.which("cl")
        if cl_path:
            LOGGER.info("find_compiler found=MSVC path=%s", cl_path)
            return cl_path, cl_path, True
        
        # Try clang on Windows
        clang_path = shutil.which("clang")
        clangpp_path = shutil.which("clang++")
        if clang_path and clangpp_path:
            LOGGER.info("find_compiler found=Clang path=%s", clang_path)
            return clang_path, clangpp_path, False
        
        # Try MinGW gcc
        gcc_path = shutil.which("gcc")
        gpp_path = shutil.which("g++")
        if gcc_path and gpp_path:
            LOGGER.info("find_compiler found=MinGW path=%s", gcc_path)
            return gcc_path, gpp_path, False
        
        raise BuildError(
            "No C compiler found on Windows",
            {"tried": "cl.exe, clang, gcc"},
        )
    else:
        # Unix-like systems
        cc = os.environ.get("CC", "cc")
        cxx = os.environ.get("CXX", "c++")
        
        # Verify compiler exists
        if not shutil.which(cc):
            cc_alternatives = ["gcc", "clang", "cc"]
            for alt in cc_alternatives:
                if shutil.which(alt):
                    cc = alt
                    break
            else:
                raise BuildError(
                    "No C compiler found",
                    {"tried": ", ".join(cc_alternatives)},
                )
        
        LOGGER.info("find_compiler found=%s", cc)
        return cc, cxx, False


def ensure_repo(spec: LanguageSpec, vendor_dir: Path) -> Path:
    """Clone grammar repository if not present, or use local grammar."""
    target = vendor_dir / spec.name
    
    # For local grammars (empty repo), just check if directory exists
    if not spec.repo:
        if target.exists():
            LOGGER.debug("ensure_repo local name=%s path=%s", spec.name, target)
            return target
        else:
            raise BuildError(
                f"Local grammar not found: {spec.name}",
                {"path": str(target), "hint": "Create grammar in vendor directory"},
            )
    
    # For remote grammars, clone if not present
    if target.exists():
        LOGGER.debug("ensure_repo exists name=%s path=%s", spec.name, target)
        return target
    
    LOGGER.info("ensure_repo clone name=%s repo=%s", spec.name, spec.repo)
    target.parent.mkdir(parents=True, exist_ok=True)
    
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["GIT_ASKPASS"] = "/usr/bin/true" if not IS_WINDOWS else ""
    env["GIT_CONFIG_COUNT"] = "1"
    env["GIT_CONFIG_KEY_0"] = "credential.helper"
    env["GIT_CONFIG_VALUE_0"] = ""
    
    _run_subprocess(
        ["git", "clone", "--depth", "1", spec.repo, str(target)],
        f"Clone {spec.name}",
        env=env,
    )
    
    return target


def ensure_core_repo(core_repo: str | None, core_dir: Path | None) -> Path | None:
    """Clone tree-sitter core repository if not present."""
    if not core_repo or not core_dir:
        return None
    
    if core_dir.exists():
        LOGGER.debug("ensure_core_repo exists path=%s", core_dir)
        return core_dir
    
    LOGGER.info("ensure_core_repo clone repo=%s", core_repo)
    core_dir.parent.mkdir(parents=True, exist_ok=True)
    
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["GIT_ASKPASS"] = "/usr/bin/true" if not IS_WINDOWS else ""
    env["GIT_CONFIG_COUNT"] = "1"
    env["GIT_CONFIG_KEY_0"] = "credential.helper"
    env["GIT_CONFIG_VALUE_0"] = ""
    
    _run_subprocess(
        ["git", "clone", "--depth", "1", core_repo, str(core_dir)],
        "Clone tree-sitter core",
        env=env,
    )
    
    return core_dir


def collect_sources(grammar_dir: Path) -> tuple[list[Path], list[Path]]:
    """Collect C and C++ source files from grammar directory."""
    src_dir = grammar_dir / "src"
    if not src_dir.exists():
        LOGGER.warning("collect_sources missing_src=%s", src_dir)
        return [], []
    
    c_files = [path for path in src_dir.glob("*.c") if path.name != "lib.c"]
    cc_files = list(src_dir.glob("*.cc"))
    
    LOGGER.debug(
        "collect_sources dir=%s c_files=%d cc_files=%d",
        grammar_dir.name,
        len(c_files),
        len(cc_files),
    )
    
    return c_files, cc_files


def compile_objects(
    build_dir: Path,
    grammar_dir: Path,
    c_files: list[Path],
    cc_files: list[Path],
    core_includes: list[Path] | None,
    stats: BuildStats | None = None,
) -> tuple[list[Path], bool]:
    """
    Compile source files to object files.
    
    Memory-safe: Cleans up partial builds on failure.
    """
    build_dir.mkdir(parents=True, exist_ok=True)
    objects: list[Path] = []
    uses_cxx = bool(cc_files)
    compiled_objects: list[Path] = []  # Track for cleanup on failure
    
    try:
        cc, cxx, is_msvc = _find_compiler()
        include_dir = grammar_dir / "src"
        
        LOGGER.info(
            "compile_objects start grammar=%s c_files=%d cc_files=%d",
            grammar_dir.name,
            len(c_files),
            len(cc_files),
        )
        
        if is_msvc:
            # MSVC compiler flags
            include_flags = [f"/I{include_dir}", f"/I{include_dir / 'tree_sitter'}"]
            if core_includes:
                include_flags.extend([f"/I{path}" for path in core_includes])
            
            for file_path in c_files:
                obj = build_dir / f"{file_path.stem}{OBJ_EXT}"
                args = [cc, "/nologo", "/c", "/O2", "/W3", str(file_path), f"/Fo{obj}"]
                args.extend(include_flags)
                _run_subprocess(args, f"Compile {file_path.name}")
                compiled_objects.append(obj)
                objects.append(obj)
                if stats:
                    stats.objects_compiled += 1
            
            for file_path in cc_files:
                obj = build_dir / f"{file_path.stem}{OBJ_EXT}"
                args = [cxx, "/nologo", "/c", "/O2", "/W3", "/EHsc", str(file_path), f"/Fo{obj}"]
                args.extend(include_flags)
                _run_subprocess(args, f"Compile {file_path.name}")
                compiled_objects.append(obj)
                objects.append(obj)
                if stats:
                    stats.objects_compiled += 1
        else:
            # GCC/Clang compiler flags
            include_flag = f"-I{include_dir}"
            include_tree_sitter = f"-I{include_dir / 'tree_sitter'}"
            core_flags = [f"-I{path}" for path in core_includes] if core_includes else []
            
            for file_path in c_files:
                obj = build_dir / f"{file_path.stem}{OBJ_EXT}"
                args = [cc, "-fPIC", "-c", "-Wall", "-Wextra", "-O2", 
                        str(file_path), "-o", str(obj), include_flag, include_tree_sitter]
                args.extend(core_flags)
                _run_subprocess(args, f"Compile {file_path.name}")
                compiled_objects.append(obj)
                objects.append(obj)
                if stats:
                    stats.objects_compiled += 1
            
            for file_path in cc_files:
                obj = build_dir / f"{file_path.stem}{OBJ_EXT}"
                args = [cxx, "-fPIC", "-c", "-Wall", "-Wextra", "-O2",
                        str(file_path), "-o", str(obj), include_flag, include_tree_sitter]
                args.extend(core_flags)
                _run_subprocess(args, f"Compile {file_path.name}")
                compiled_objects.append(obj)
                objects.append(obj)
                if stats:
                    stats.objects_compiled += 1
        
        LOGGER.info(
            "compile_objects complete grammar=%s objects=%d",
            grammar_dir.name,
            len(objects),
        )
        
        return objects, uses_cxx
        
    except BuildError:
        # Clean up partial build on failure
        LOGGER.warning(
            "compile_objects cleanup grammar=%s partial_objects=%d",
            grammar_dir.name,
            len(compiled_objects),
        )
        for obj in compiled_objects:
            if obj.exists():
                try:
                    obj.unlink()
                except OSError:
                    pass
        raise


def build_languages(config: BuildConfig) -> BuildStats:
    """
    Build all configured tree-sitter language grammars.
    
    Returns BuildStats with build metrics.
    Raises BuildError on failure.
    """
    stats = BuildStats()
    
    LOGGER.info(
        "build_languages start languages=%d output=%s",
        len(config.languages),
        config.output_path,
    )
    
    try:
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
            try:
                repo_dir = ensure_repo(spec, config.vendor_dir)
                grammar_dir = repo_dir / spec.path
                
                if not grammar_dir.exists():
                    LOGGER.warning("build_languages_skip missing_grammar_dir=%s", grammar_dir)
                    stats.failed_languages.append(spec.name)
                    continue
                
                c_files, cc_files = collect_sources(grammar_dir)
                if not c_files and not cc_files:
                    LOGGER.warning("build_languages_skip no_sources=%s", grammar_dir)
                    stats.failed_languages.append(spec.name)
                    continue
                
                build_subdir = config.build_dir / spec.name
                objects, needs_cxx = compile_objects(
                    build_subdir, grammar_dir, c_files, cc_files, core_includes, stats
                )
                uses_cxx = uses_cxx or needs_cxx
                all_objects.extend(objects)
                stats.languages_processed += 1
                stats.source_files.extend([f.name for f in c_files + cc_files])
                
            except BuildError as e:
                LOGGER.error("build_languages_failed language=%s error=%s", spec.name, str(e))
                stats.failed_languages.append(spec.name)
                stats.errors_count += 1
                # Continue with other languages
                continue
        
        if not all_objects:
            raise BuildError("No objects compiled", {"languages": len(config.languages)})
        
        # Link final library
        config.output_path.parent.mkdir(parents=True, exist_ok=True)
        
        cc, cxx, is_msvc = _find_compiler()
        linker = cxx if uses_cxx else cc
        all_objs = [str(o) for o in core_objects + all_objects]
        
        LOGGER.info(
            "build_languages link objects=%d output=%s",
            len(all_objs),
            config.output_path,
        )
        
        if is_msvc:
            # MSVC linker
            _run_subprocess(
                [linker, "/nologo", "/LD", f"/Fe{config.output_path}", *all_objs],
                "Link library",
            )
        elif IS_MACOS:
            # macOS dynamic library
            _run_subprocess(
                [linker, "-dynamiclib", "-o", str(config.output_path), *all_objs],
                "Link library",
            )
        elif IS_WINDOWS:
            # MinGW/Clang on Windows - create DLL
            _run_subprocess(
                [linker, "-shared", "-o", str(config.output_path), *all_objs],
                "Link library",
            )
        else:
            # Linux shared library
            _run_subprocess(
                [linker, "-shared", "-o", str(config.output_path), *all_objs],
                "Link library",
            )
        
        LOGGER.info(
            "build_languages complete languages=%d objects=%d output=%s",
            stats.languages_processed,
            stats.objects_compiled,
            config.output_path,
        )
        
        return stats
        
    finally:
        # Force garbage collection to free memory
        gc.collect()


def _prepare_core_include(build_dir: Path, core_repo_dir: Path) -> list[Path]:
    """Prepare tree-sitter core include directories."""
    LOGGER.debug("prepare_core_include start core_dir=%s", core_repo_dir)
    
    include_root = build_dir / "tree_sitter_include"
    include_tree_sitter = include_root / "tree_sitter"
    include_tree_sitter.mkdir(parents=True, exist_ok=True)
    
    core_src = core_repo_dir / "lib" / "src"
    headers_copied = 0
    
    for header in core_src.glob("*.h"):
        target = include_tree_sitter / header.name
        target.write_text(header.read_text(encoding="utf-8"), encoding="utf-8")
        headers_copied += 1
    
    LOGGER.debug("prepare_core_include complete headers=%d", headers_copied)
    
    return [include_root, core_repo_dir / "lib" / "include"]


def _compile_core_runtime(
    build_dir: Path,
    core_repo_dir: Path,
    core_includes: list[Path] | None,
) -> list[Path]:
    """Compile tree-sitter core runtime objects."""
    src_dir = core_repo_dir / "lib" / "src"
    c_files = [path for path in src_dir.glob("*.c") if path.name != "lib.c"]
    
    if not c_files:
        LOGGER.warning("compile_core_runtime no_sources path=%s", src_dir)
        return []
    
    LOGGER.info("compile_core_runtime start files=%d", len(c_files))
    
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
            _run_subprocess(
                [cc, "/nologo", "/c", "/O2", "/W3", str(file_path), f"/Fo{obj}", *include_flags],
                f"Compile core {file_path.name}",
            )
            objects.append(obj)
    else:
        include_flag = f"-I{src_dir}"
        include_flags = [include_flag]
        if core_includes:
            include_flags.extend([f"-I{path}" for path in core_includes])
        
        for file_path in c_files:
            obj = core_build / f"{file_path.stem}{OBJ_EXT}"
            _run_subprocess(
                [cc, "-fPIC", "-c", "-Wall", "-O2", str(file_path), "-o", str(obj), *include_flags],
                f"Compile core {file_path.name}",
            )
            objects.append(obj)
    
    LOGGER.info("compile_core_runtime complete objects=%d", len(objects))
    
    return objects


def main() -> None:
    """CLI entry point with comprehensive error handling."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    
    parser = argparse.ArgumentParser(
        description="Build tree-sitter languages.so",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python -m migration_agents.parser.build_languages --config config/parser.json
    python -m migration_agents.parser.build_languages --config config/parser.json --verbose
        """,
    )
    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to build configuration JSON file",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable debug logging",
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger("migration_agents.parser.build_languages").setLevel(logging.DEBUG)
    
    try:
        config = load_config(args.config)
        stats = build_languages(config)
        
        # Print summary
        print()
        print("=" * 60)
        print(" BUILD SUCCESSFUL")
        print("=" * 60)
        print(f"Languages processed: {stats.languages_processed}")
        print(f"Objects compiled:    {stats.objects_compiled}")
        print(f"Output:              {config.output_path}")
        
        if stats.failed_languages:
            print(f"Failed languages:    {', '.join(stats.failed_languages)}")
        
        print()
        
    except BuildError as e:
        LOGGER.error("build_failed error=%s", str(e))
        print()
        print("=" * 60)
        print(" BUILD FAILED")
        print("=" * 60)
        print(f"Error: {e}")
        if e.context:
            for key, value in e.context.items():
                print(f"  {key}: {value}")
        print()
        sys.exit(1)
    except KeyboardInterrupt:
        LOGGER.warning("build_interrupted")
        print("\nBuild interrupted by user")
        sys.exit(130)
    except Exception as e:
        LOGGER.exception("build_unexpected_error")
        print()
        print("=" * 60)
        print(" BUILD FAILED (Unexpected Error)")
        print("=" * 60)
        print(f"Error: {type(e).__name__}: {e}")
        print()
        sys.exit(1)


if __name__ == "__main__":
    main()
