from __future__ import annotations

import argparse
import json
import os
import sys
import subprocess
import logging
from dataclasses import dataclass
from pathlib import Path

LOGGER = logging.getLogger("migration_agents.parser.build_languages")


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
    return BuildConfig(
        output_path=Path(raw["output_path"]).expanduser().resolve(),
        vendor_dir=Path(raw["vendor_dir"]).expanduser().resolve(),
        build_dir=Path(raw["build_dir"]).expanduser().resolve(),
        core_repo=raw.get("core_repo"),
        core_dir=Path(raw["core_dir"]).expanduser().resolve()
        if raw.get("core_dir")
        else None,
        languages=languages,
    )


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
    cc = os.environ.get("CC", "cc")
    cxx = os.environ.get("CXX", "c++")
    include_dir = grammar_dir / "src"
    include_flag = f"-I{include_dir}"
    include_tree_sitter = f"-I{include_dir / 'tree_sitter'}"
    core_flags = [f"-I{path}" for path in core_includes] if core_includes else []
    for file_path in c_files:
        obj = build_dir / f"{file_path.stem}.o"
        args = [
            cc,
            "-fPIC",
            "-c",
            str(file_path),
            "-o",
            str(obj),
            include_flag,
            include_tree_sitter,
        ]
        args.extend(core_flags)
        subprocess.run(args, check=True)
        objects.append(obj)
    for file_path in cc_files:
        obj = build_dir / f"{file_path.stem}.o"
        args = [
            cxx,
            "-fPIC",
            "-c",
            str(file_path),
            "-o",
            str(obj),
            include_flag,
            include_tree_sitter,
        ]
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
    linker = os.environ.get("CXX", "c++") if uses_cxx else os.environ.get("CC", "cc")
    link_flag = "-dynamiclib" if sys.platform == "darwin" else "-shared"
    subprocess.run(
        [linker, link_flag, "-o", str(config.output_path), *map(str, core_objects + all_objects)],
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
    cc = os.environ.get("CC", "cc")
    include_flag = f"-I{src_dir}"
    include_flags = [include_flag]
    if core_includes:
        include_flags.extend([f"-I{path}" for path in core_includes])
    objects: list[Path] = []
    for file_path in c_files:
        obj = core_build / f"{file_path.stem}.o"
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
