from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "docs" / "alumni-data"
OUTPUT_DIR = ROOT / "docs" / "alumni"
TEMPLATE_FILE = "TEMPLATE.md"

NAME_FIELD_RE = re.compile(
    r"^\s*[-*]\s*\*\*Name\*\*\s*:\s*(?P<name>.+?)\s*$",
    re.IGNORECASE,
)


# -----------------------------
# Utilities
# -----------------------------
def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "profile"


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


# -----------------------------
# 🔥 FIX: Image Path Handler
# -----------------------------
def fix_image_paths(content: str) -> str:
    """
    Convert relative image paths to absolute paths compatible with GitHub Pages.
    Example:
        ../images/photo.jpg  →  /alumni-network/images/photo.jpg
    """
    return re.sub(
        r"\.\./images/",
        "/alumni-network/images/",
        content
    )


# -----------------------------
# Index Builder
# -----------------------------
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


# -----------------------------
# Main Generator
# -----------------------------
def generate_alumni_docs() -> list[tuple[str, str]]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Clean old generated files
    for path in OUTPUT_DIR.glob("*.md"):
        if path.name != "template.md":  # preserve template
            path.unlink()

    entries: list[tuple[str, str]] = []

    for source_path in sorted(SOURCE_DIR.glob("*.md")):
        is_template = source_path.name.casefold() == TEMPLATE_FILE.casefold()

        content = source_path.read_text(encoding="utf-8")
        content = fix_image_paths(content)  # 🔥 key fix

        if is_template:
            destination_name = "template.md"
        else:
            title = extract_profile_name(content, source_path)
            slug = slugify(title)  # 🔥 better than filename-based slug
            destination_name = f"{slug}.md"
            entries.append((title, slug))

        # Write processed content
        (OUTPUT_DIR / destination_name).write_text(content, encoding="utf-8")

    # Sort entries alphabetically
    entries.sort(key=lambda item: item[0].lower())

    # Generate index page
    (OUTPUT_DIR / "index.md").write_text(
        build_index(entries),
        encoding="utf-8"
    )

    return entries


# -----------------------------
# MkDocs Hook
# -----------------------------
def on_config(config, **kwargs):
    entries = generate_alumni_docs()

    alumni_nav = [
        {"Overview": "alumni/index.md"},
        {"Profile Template": "alumni/template.md"},
    ]

    alumni_nav.extend({title: f"alumni/{slug}.md"} for title, slug in entries)

    # 🔥 Define nav explicitly (no leftovers)
    config["nav"] = [
        {"Home": "index.md"},
        {"Events": "events.md"},
        {"News": "news.md"},
        {"Resources": "resources.md"},
        {"Documents": "documents.md"},
        {"Contact": "contact.md"},
        {"Alumni Profiles": alumni_nav},
    ]

    return config

# -----------------------------
# Local Run
# -----------------------------
if __name__ == "__main__":
    generate_alumni_docs()
