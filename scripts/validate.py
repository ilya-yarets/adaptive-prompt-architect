#!/usr/bin/env python3
"""Validate the public plugin package with Python's standard library."""

from __future__ import annotations

import json
import re
import struct
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / ".codex-plugin" / "plugin.json"
SKILL_ROOT = ROOT / "skills" / "prompt-architect"
SKILL_PATH = SKILL_ROOT / "SKILL.md"
AGENT_PATH = SKILL_ROOT / "agents" / "openai.yaml"
EVALS_PATH = ROOT / "evals" / "evals.json"
TRIGGERS_PATH = ROOT / "evals" / "trigger-queries.json"
README_PATH = ROOT / "README.md"
README_RU_PATH = ROOT / "README.ru.md"
ICON_SVG_PATH = SKILL_ROOT / "assets" / "icon.svg"
ICON_PNG_PATH = SKILL_ROOT / "assets" / "icon.png"
HERO_SVG_PATH = ROOT / "assets" / "brand" / "hero.svg"
SOCIAL_SVG_PATH = ROOT / "assets" / "brand" / "social-preview.svg"
SOCIAL_PNG_PATH = ROOT / "assets" / "brand" / "social-preview.png"
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:[-+][0-9A-Za-z.-]+)?$")
CYRILLIC = re.compile(r"[\u0400-\u04FF]")


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing {path.relative_to(ROOT)}")
    except json.JSONDecodeError as error:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {error}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def fail(message: str) -> None:
    print(f"validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate_manifest() -> None:
    manifest = load_json(MANIFEST_PATH)
    require(isinstance(manifest, dict), "plugin manifest must be an object")
    require(manifest.get("name") == "adaptive-prompt-architect", "unexpected plugin name")
    require(bool(SEMVER.fullmatch(manifest.get("version", ""))), "version must be semver")
    require(manifest.get("skills") == "./skills/", "skills path must be ./skills/")
    require(manifest.get("license") == "MIT", "license must be MIT")
    require(isinstance(manifest.get("keywords"), list) and manifest["keywords"], "keywords are required")
    author = manifest.get("author")
    require(isinstance(author, dict) and author.get("name"), "author.name is required")
    interface = manifest.get("interface")
    require(isinstance(interface, dict), "interface is required")
    for field in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
        require(isinstance(interface.get(field), str) and interface[field].strip(), f"interface.{field} is required")
    prompts = interface.get("defaultPrompt")
    require(isinstance(prompts, list) and 1 <= len(prompts) <= 3, "defaultPrompt must contain 1-3 prompts")
    require(all(isinstance(item, str) and 0 < len(item) <= 128 for item in prompts), "default prompts must be 1-128 characters")
    expected_icon = "./skills/prompt-architect/assets/icon.png"
    for field in ("composerIcon", "logo", "logoDark"):
        require(interface.get(field) == expected_icon, f"interface.{field} must use the packaged icon")


def validate_skill() -> None:
    require(SKILL_PATH.is_file(), "missing skills/prompt-architect/SKILL.md")
    text = SKILL_PATH.read_text(encoding="utf-8")
    require(text.startswith("---\n"), "SKILL.md must start with YAML frontmatter")
    parts = text.split("---", 2)
    require(len(parts) == 3, "SKILL.md frontmatter is not closed")
    frontmatter = parts[1]
    require(re.search(r"(?m)^name:\s*prompt-architect\s*$", frontmatter) is not None, "skill name is missing or mismatched")
    require(re.search(r"(?m)^description:\s*.+$", frontmatter) is not None, "skill description is required")
    require("молча улучши запрос и сразу выполни задачу" in text, "silent execution default is missing")
    require("не даёт новых полномочий" in text, "authorization boundary is missing")
    require(AGENT_PATH.is_file(), "missing agents/openai.yaml")
    agent = AGENT_PATH.read_text(encoding="utf-8")
    for key in (
        "display_name:",
        "short_description:",
        "icon_small:",
        "icon_large:",
        "brand_color:",
        "default_prompt:",
        "allow_implicit_invocation:",
    ):
        require(key in agent, f"agents/openai.yaml is missing {key}")


def validate_png(path: Path, expected_size: tuple[int, int]) -> None:
    require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    header = path.read_bytes()[:24]
    require(header[:8] == b"\x89PNG\r\n\x1a\n", f"{path.relative_to(ROOT)} is not a PNG")
    require(len(header) == 24 and header[12:16] == b"IHDR", f"{path.relative_to(ROOT)} has an invalid PNG header")
    dimensions = struct.unpack(">II", header[16:24])
    require(dimensions == expected_size, f"{path.relative_to(ROOT)} must be {expected_size[0]}x{expected_size[1]}")


def validate_svg(path: Path, expected_viewbox: str) -> None:
    require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as error:
        fail(f"invalid SVG in {path.relative_to(ROOT)}: {error}")
    require(root.tag.endswith("svg"), f"{path.relative_to(ROOT)} must contain an SVG root")
    require(root.attrib.get("viewBox") == expected_viewbox, f"{path.relative_to(ROOT)} has an unexpected viewBox")


def validate_brand_assets() -> None:
    validate_svg(ICON_SVG_PATH, "0 0 512 512")
    validate_svg(HERO_SVG_PATH, "0 0 1280 480")
    validate_svg(SOCIAL_SVG_PATH, "0 0 1280 640")
    validate_png(ICON_PNG_PATH, (512, 512))
    validate_png(SOCIAL_PNG_PATH, (1280, 640))


def validate_readmes() -> None:
    require(README_PATH.is_file(), "missing README.md")
    require(README_RU_PATH.is_file(), "missing README.ru.md")
    english = README_PATH.read_text(encoding="utf-8")
    russian = README_RU_PATH.read_text(encoding="utf-8")
    require('<h1 align="center" aria-label="Adaptive Prompt Architect">' in english, "README.md must have an accessible H1")
    require('<h1 align="center" aria-label="Adaptive Prompt Architect">' in russian, "README.ru.md must have an accessible H1")
    require('src="assets/brand/hero.svg"' in english, "README.md must display the brand hero")
    require("README.ru.md" in english, "README.md must link to the Russian version")
    require("README.md" in russian, "README.ru.md must link to the English version")
    require(CYRILLIC.search(english) is None, "README.md must remain English-only")
    for path, text in ((README_PATH, english), (README_RU_PATH, russian)):
        markdown_links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
        html_links = re.findall(r"(?:href|src)=[\"']([^\"']+)[\"']", text)
        links = markdown_links + html_links
        for target in links:
            if re.match(r"(?:https?://|#|mailto:)", target):
                continue
            require((ROOT / target).exists(), f"{path.name} links to missing {target}")


def validate_evals() -> None:
    payload = load_json(EVALS_PATH)
    require(isinstance(payload, dict) and payload.get("skill_name") == "prompt-architect", "eval skill_name is invalid")
    evals = payload.get("evals")
    require(isinstance(evals, list) and len(evals) >= 8, "at least eight behavior evals are required")
    ids = []
    for case in evals:
        require(isinstance(case, dict), "each eval must be an object")
        for field in ("id", "prompt", "expected_output"):
            require(isinstance(case.get(field), str) and case[field].strip(), f"eval is missing {field}")
        assertions = case.get("assertions")
        require(isinstance(assertions, list) and assertions, f"eval {case['id']} needs assertions")
        require(all(isinstance(item, str) and item.strip() for item in assertions), f"eval {case['id']} has an invalid assertion")
        ids.append(case["id"])
    require(len(ids) == len(set(ids)), "eval ids must be unique")

    triggers = load_json(TRIGGERS_PATH)
    require(isinstance(triggers, list) and len(triggers) >= 10, "trigger query set is too small")
    require(any(item.get("should_trigger") is True for item in triggers), "positive trigger cases are required")
    require(any(item.get("should_trigger") is False for item in triggers), "negative trigger cases are required")
    for item in triggers:
        require(isinstance(item, dict), "each trigger case must be an object")
        require(isinstance(item.get("query"), str) and item["query"].strip(), "trigger query is required")
        require(isinstance(item.get("should_trigger"), bool), "should_trigger must be boolean")


def validate_public_content() -> None:
    forbidden = {
        "/" + "Users/": "absolute macOS user path",
        "Second" + " Brain": "private workspace name",
        "gho" + "_": "GitHub OAuth token prefix",
        "BEGIN " + "PRIVATE KEY": "private key material",
        "[" + "TODO:": "unfinished scaffold placeholder",
    }
    extensions = {".md", ".json", ".yaml", ".yml", ".py", ".svg"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix not in extensions:
            continue
        content = path.read_text(encoding="utf-8")
        for needle, label in forbidden.items():
            require(needle not in content, f"{path.relative_to(ROOT)} contains {label}")


def main() -> None:
    validate_manifest()
    validate_skill()
    validate_brand_assets()
    validate_readmes()
    validate_evals()
    validate_public_content()
    print("validation passed")


if __name__ == "__main__":
    main()
