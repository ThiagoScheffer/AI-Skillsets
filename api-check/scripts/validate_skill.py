#!/usr/bin/env python3
"""Small local validator for this standalone skill bundle."""
from __future__ import annotations
import re
import sys
from pathlib import Path
import yaml

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parents[1])
    skill = root / "SKILL.md"
    if not skill.exists():
        print("ERROR: SKILL.md missing")
        return 1
    text = skill.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        print("ERROR: invalid YAML frontmatter")
        return 1
    data = yaml.safe_load(m.group(1))
    if not isinstance(data, dict) or set(data) != {"name", "description"}:
        print("ERROR: frontmatter must contain exactly name and description")
        return 1
    name = data.get("name")
    desc = data.get("description")
    if not isinstance(name, str) or not NAME_RE.fullmatch(name) or len(name) > 64:
        print("ERROR: invalid skill name")
        return 1
    if not isinstance(desc, str) or not desc.strip():
        print("ERROR: description missing")
        return 1
    openai_yaml = root / "agents" / "openai.yaml"
    if not openai_yaml.exists():
        print("ERROR: agents/openai.yaml missing")
        return 1
    interface = yaml.safe_load(openai_yaml.read_text(encoding="utf-8"))
    if not isinstance(interface, dict) or "interface" not in interface:
        print("ERROR: agents/openai.yaml missing interface")
        return 1
    ui = interface["interface"]
    short = ui.get("short_description", "") if isinstance(ui, dict) else ""
    prompt = ui.get("default_prompt", "") if isinstance(ui, dict) else ""
    if not (25 <= len(short) <= 64):
        print("ERROR: short_description must be 25-64 characters")
        return 1
    if f"${name}" not in prompt:
        print("ERROR: default_prompt must explicitly mention the skill")
        return 1
    print(f"OK: {name} skill structure is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
