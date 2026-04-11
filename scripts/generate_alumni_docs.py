from __future__ import annotations

import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "alumni-data"
OUTPUT_DIR = ROOT / "docs" / "alumni"
TEMPLATE_FILE = "TEMPLATE.md"
NAME_FIELD_RE = re.compile(
    r"^\s*[-*]\s*\*\*Name\*\*\s*:\s*(?P<name>.+?)\s*$",
    re.IGNORECASE,
)


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "profile"


def display_name_from_filename(path: Path) -> str:
    return re.sub(r"[-_]+", " ", path.stem).strip() or path.stem


def extract_profile_name(text: str, source_path: Path) -> str:
    fallback = display_name_from_filename(source_path)

    for line in text.splitlines():
        match = NAME_FIELD_RE.match(line)
        if match:
            name = match.group("name").strip()
            if name:
                return name

    return fallback


def build_index(entries: list[tuple[str, str]]) -> str:
    lines = [
        "# Alumni Profiles",
        "",
        "This section is generated automatically from the Markdown files in `alumni-data/`.",
        "",
        "## Available Profiles",
        "",
    ]

    if entries:
        lines.extend(f"- [{title}]({slug}.md)" for title, slug in entries)
    else:
        lines.append("- No alumni profiles have been added yet.")

    lines.extend(
        [
            "",
            "## Template",
            "",
            "- [Profile Template](template.md)",
        ]
    )
    return "\n".join(lines) + "\n"


def generate_alumni_docs() -> list[tuple[str, str]]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for path in OUTPUT_DIR.glob("*.md"):
        path.unlink()

    entries: list[tuple[str, str]] = []

    for source_path in sorted(SOURCE_DIR.glob("*.md")):
        is_template = source_path.name.casefold() == TEMPLATE_FILE.casefold()
        destination_name = "template.md" if is_template else None
        content = source_path.read_text(encoding="utf-8")

        if destination_name is None:
            title = extract_profile_name(content, source_path)
            slug = slugify(source_path.stem)
            destination_name = f"{slug}.md"
            entries.append((title, slug))

        shutil.copyfile(source_path, OUTPUT_DIR / destination_name)

    entries.sort(key=lambda item: item[0].lower())
    (OUTPUT_DIR / "index.md").write_text(build_index(entries), encoding="utf-8")
    return entries


def on_config(config, **kwargs):
    entries = generate_alumni_docs()
    alumni_nav = [
        {"Overview": "alumni/index.md"},
        {"Profile Template": "alumni/template.md"},
    ]
    alumni_nav.extend({title: f"alumni/{slug}.md"} for title, slug in entries)

    updated_nav = []
    for item in config["nav"]:
        if isinstance(item, dict) and "Alumni Profiles" in item:
            updated_nav.append({"Alumni Profiles": alumni_nav})
        else:
            updated_nav.append(item)

    config["nav"] = updated_nav
    return config


if __name__ == "__main__":
    generate_alumni_docs()
