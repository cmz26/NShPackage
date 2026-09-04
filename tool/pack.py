#!/usr/bin/env python3
"""pack.py - neosh 包打包工具（纯标准库，跨平台）

把一个包目录（含 __init__.py，暴露 info() / main(args)）打包成
neosh 可安装的 <name>.neopackage.<ext> 归档，归档内统一带顶层目录
<name>.neopackage/，与 shell 端 pkg_manager 的解压规则对应。

用法:
    python pack.py <包目录> [--out DIR] [--type tar-gz|zip]
                           [--register URL] [--index PATH]

示例:
    python pack.py ../code/echo
    python pack.py ../code/echo --type zip
    python pack.py ../code/echo --register https://example.com/echo.neopackage.tar.gz
"""

import argparse
import json
import sys
import tarfile
import zipfile
from pathlib import Path

PACKAGE_SUFFIX = ".neopackage"
SKIP_DIRS = {"__pycache__", ".git", ".vscode"}
SKIP_SUFFIXES = {".pyc", ".pyo"}

# pkgs/tool/pack.py -> pkgs
PKGS_DIR = Path(__file__).resolve().parent.parent
DEFAULT_OUT_DIR = PKGS_DIR / "dist"
DEFAULT_INDEX = PKGS_DIR / "__index__.json"

ARCHIVE_TYPES = {
    "tar-gz": ".tar.gz",
    "zip": ".zip",
}


def iter_package_files(pkg_dir: Path):
    """Yield (absolute_path, archive_relative_posix_path) for files to pack."""
    for path in sorted(pkg_dir.rglob("*")):
        if path.is_dir():
            continue
        rel_parts = path.relative_to(pkg_dir).parts
        if any(part in SKIP_DIRS for part in rel_parts):
            continue
        if path.suffix in SKIP_SUFFIXES:
            continue
        yield path, "/".join(rel_parts)


def make_targz(pkg_dir: Path, arc_root: str, dest: Path) -> None:
    with tarfile.open(dest, "w:gz") as tf:
        for path, rel in iter_package_files(pkg_dir):
            tf.add(path, arcname=f"{arc_root}/{rel}")


def make_zip(pkg_dir: Path, arc_root: str, dest: Path) -> None:
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as zf:
        for path, rel in iter_package_files(pkg_dir):
            zf.write(path, arcname=f"{arc_root}/{rel}")


def register(index_path: Path, name: str, url: str, pkg_type: str) -> None:
    """Insert/update an entry in __index__.json (registry list)."""
    if index_path.exists():
        with open(index_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError(f"{index_path} is not a registry list")
    else:
        data = []

    entry = {"name": name, "url": url, "type": pkg_type}
    for i, item in enumerate(data):
        if item.get("name") == name:
            data[i] = entry
            break
    else:
        data.append(entry)

    index_path.parent.mkdir(parents=True, exist_ok=True)
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.write("\n")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Pack a neosh package folder into a .neopackage archive.",
    )
    parser.add_argument("package_dir", type=Path, help="package folder (must contain __init__.py)")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT_DIR,
                        help=f"output directory (default: {DEFAULT_OUT_DIR})")
    parser.add_argument("--type", choices=sorted(ARCHIVE_TYPES), default="tar-gz",
                        help="archive type (default: tar-gz)")
    parser.add_argument("--register", metavar="URL",
                        help="also register/update the package in the index with this URL")
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX,
                        help=f"index file for --register (default: {DEFAULT_INDEX})")
    args = parser.parse_args(argv)

    pkg_dir = args.package_dir.resolve()
    if not pkg_dir.is_dir():
        print(f"[x] package directory not found: {pkg_dir}", file=sys.stderr)
        return 1
    if not (pkg_dir / "__init__.py").is_file():
        print(f"[x] not a package: {pkg_dir} has no __init__.py", file=sys.stderr)
        return 1

    name = pkg_dir.name
    arc_root = f"{name}{PACKAGE_SUFFIX}"
    ext = ARCHIVE_TYPES[args.type]
    args.out.mkdir(parents=True, exist_ok=True)
    dest = (args.out / f"{arc_root}{ext}").resolve()

    files = list(iter_package_files(pkg_dir))
    if args.type == "tar-gz":
        make_targz(pkg_dir, arc_root, dest)
    else:
        make_zip(pkg_dir, arc_root, dest)

    print(f"[ok] packed {name} -> {dest}")
    print(f"     {len(files)} file(s), type={args.type}, arc root={arc_root}/")

    if args.register:
        index_path = args.index.resolve()
        register(index_path, arc_root, args.register, args.type)
        print(f"[ok] registered {arc_root} in {index_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
