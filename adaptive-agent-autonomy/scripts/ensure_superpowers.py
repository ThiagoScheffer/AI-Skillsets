#!/usr/bin/env python3
"""Check for Superpowers and optionally install a portable copy if missing.

Portable mode clones the official OpenAI plugins repository sparsely, copies
plugins/superpowers under ~/.agents/plugins/superpowers, then exposes each skill
under ~/.agents/skills. Runtime-native plugin installation is still preferred
when available.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

OFFICIAL_REPO = "https://github.com/openai/plugins.git"


def candidates() -> list[Path]:
    return [
        Path.home()/".agents"/"skills"/"using-superpowers"/"SKILL.md",
        Path.home()/".claude"/"skills"/"using-superpowers"/"SKILL.md",
        Path.home()/".agents"/"plugins"/"superpowers"/"skills"/"using-superpowers"/"SKILL.md",
        Path.cwd()/"plugins"/"superpowers"/"skills"/"using-superpowers"/"SKILL.md",
    ]


def found() -> list[Path]:
    return [p for p in candidates() if p.exists()]


def copy_or_link_skills(plugin_dir: Path, skills_dir: Path, force: bool) -> None:
    source_skills = plugin_dir / "skills"
    if not source_skills.exists():
        raise RuntimeError(f"No skills directory found in {plugin_dir}")
    skills_dir.mkdir(parents=True, exist_ok=True)
    for src in source_skills.iterdir():
        if not src.is_dir() or not (src / "SKILL.md").exists():
            continue
        dst = skills_dir / src.name
        if dst.exists() or dst.is_symlink():
            if not force:
                continue
            if dst.is_symlink() or dst.is_file():
                dst.unlink()
            else:
                shutil.rmtree(dst)
        try:
            dst.symlink_to(src, target_is_directory=True)
        except OSError:
            shutil.copytree(src, dst)


def install(plugin_dir: Path, skills_dir: Path, force: bool) -> None:
    if shutil.which("git") is None:
        raise RuntimeError("git is required for portable Superpowers installation")
    if plugin_dir.exists():
        if not force:
            raise RuntimeError(f"Target already exists: {plugin_dir}. Use --force to replace it.")
        shutil.rmtree(plugin_dir)
    plugin_dir.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="superpowers-install-") as td:
        repo = Path(td) / "plugins"
        subprocess.run([
            "git", "clone", "--depth", "1", "--filter=blob:none", "--sparse",
            OFFICIAL_REPO, str(repo)
        ], check=True)
        subprocess.run(["git", "-C", str(repo), "sparse-checkout", "set", "plugins/superpowers"], check=True)
        src = repo / "plugins" / "superpowers"
        if not (src / "skills" / "using-superpowers" / "SKILL.md").exists():
            raise RuntimeError("Official repository layout did not contain Superpowers where expected")
        shutil.copytree(src, plugin_dir)
    copy_or_link_skills(plugin_dir, skills_dir, force=force)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--install", action="store_true", help="install portable Superpowers if it is missing")
    p.add_argument("--force", action="store_true")
    p.add_argument("--plugin-dir", default=str(Path.home()/".agents"/"plugins"/"superpowers"))
    p.add_argument("--skills-dir", default=str(Path.home()/".agents"/"skills"))
    a = p.parse_args()

    hits = found()
    if hits:
        print("Superpowers found:")
        for item in hits:
            print(" -", item)
        return 0

    if not a.install:
        print("Superpowers not found in common portable locations.")
        print("To add it portably: python scripts/ensure_superpowers.py --install")
        print("Official curated source:", OFFICIAL_REPO.replace(".git", "/tree/main/plugins/superpowers"))
        return 1

    plugin_dir = Path(a.plugin_dir).expanduser()
    skills_dir = Path(a.skills_dir).expanduser()
    install(plugin_dir, skills_dir, a.force)
    expected = skills_dir / "using-superpowers" / "SKILL.md"
    plugin_expected = plugin_dir / "skills" / "using-superpowers" / "SKILL.md"
    print("Portable Superpowers installation complete.")
    if expected.exists():
        print(" -", expected)
    if plugin_expected.exists():
        print(" -", plugin_expected)
    return 0 if (expected.exists() or plugin_expected.exists()) else 2


if __name__ == "__main__":
    raise SystemExit(main())
