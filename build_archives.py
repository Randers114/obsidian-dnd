from __future__ import annotations

import re
from pathlib import Path
from typing import Optional, Tuple, List


# =====================================
# CONFIGURATION
# =====================================

VAULT_ROOT = Path(".")
CAMPAIGN_ROOT = VAULT_ROOT / "Whispers of the Umbral Abyss"
ARCHIVE_OUTPUT_DIR = VAULT_ROOT / "_Archives"

ARCHIVE_CONFIG = {
    "sessions": {
        "source_dirs": [CAMPAIGN_ROOT / "Sessions"],
        "output_file": ARCHIVE_OUTPUT_DIR / "Sessions Archive.md",
        "archive_title": "Sessions Archive — Whispers of the Umbral Abyss",
        "item_heading": "Session File",
        "required_type": "session",
    },
    "people": {
        "source_dirs": [CAMPAIGN_ROOT / "People"],
        "output_file": ARCHIVE_OUTPUT_DIR / "People Archive.md",
        "archive_title": "People Archive — Whispers of the Umbral Abyss",
        "item_heading": "Person File",
        "required_type": "person",
    },
    "places": {
        "source_dirs": [CAMPAIGN_ROOT / "Locations"],
        "output_file": ARCHIVE_OUTPUT_DIR / "Places Archive.md",
        "archive_title": "Places Archive — Whispers of the Umbral Abyss",
        "item_heading": "Place File",
        "required_type": "place",
    },
    "organizations": {
        "source_dirs": [CAMPAIGN_ROOT / "Organizations"],
        "output_file": ARCHIVE_OUTPUT_DIR / "Organizations Archive.md",
        "archive_title": "Organizations Archive — Whispers of the Umbral Abyss",
        "item_heading": "Organization File",
        "required_type": "organization",
    },
    "quests": {
        "source_dirs": [
            CAMPAIGN_ROOT / "Quest Log",
            CAMPAIGN_ROOT / "Quests",
        ],
        "output_file": ARCHIVE_OUTPUT_DIR / "Quests Archive.md",
        "archive_title": "Quests Archive — Whispers of the Umbral Abyss",
        "item_heading": "Quest File",
        "required_type": "quest",
    },
}

SKIP_FILENAME_PATTERNS = [
    r".*archive.*\.md$",
    r".*template.*\.md$",
]

SKIP_EXACT_FILENAMES = {
    "Sessions.md",
    "People.md",
    "Places.md",
    "Organizations.md",
    "Quests.md",
    "Quest Log.md",
}


# =====================================
# HELPERS
# =====================================

def should_skip_file(path: Path) -> bool:
    name = path.name.strip()

    if name in SKIP_EXACT_FILENAMES:
        return True

    for pattern in SKIP_FILENAME_PATTERNS:
        if re.match(pattern, name, re.IGNORECASE):
            return True

    try:
        path.relative_to(ARCHIVE_OUTPUT_DIR)
        return True
    except ValueError:
        pass

    return False


def split_frontmatter(text: str) -> Tuple[Optional[str], str]:
    if not text.startswith("---\n"):
        return None, text

    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not match:
        return None, text

    frontmatter = match.group(1).strip()
    body = match.group(2).lstrip("\n")
    return frontmatter, body


def extract_property(frontmatter: Optional[str], key: str) -> Optional[str]:
    if not frontmatter:
        return None

    pattern = rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$"
    match = re.search(pattern, frontmatter)
    if not match:
        return None

    value = match.group(1).strip()
    if value in {"", "[]", "null", "None"}:
        return None

    return value.strip('"').strip("'")


def extract_first_h1(body: str) -> Optional[str]:
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return None


def extract_date_from_filename(filename: str) -> Optional[str]:
    match = re.match(r"(\d{4}-\d{2}-\d{2})", filename)
    return match.group(1) if match else None


def clean_title(title: str) -> str:
    title = re.sub(r'^\d{4}-\d{2}-\d{2}\s*-\s*', '', title).strip()
    return title.strip('"')


def relative_display_path(path: Path, base_dir: Path) -> str:
    try:
        return str(path.relative_to(base_dir))
    except ValueError:
        return path.name


def file_matches_type(frontmatter: Optional[str], required_type: Optional[str]) -> bool:
    if required_type is None:
        return True
    actual_type = extract_property(frontmatter, "type")
    return actual_type == required_type


def make_index_entry(
    path: Path,
    frontmatter: Optional[str],
    body: str,
    archive_kind: str,
    source_root: Path,
) -> str:
    rel_name = relative_display_path(path, source_root)
    stem_name = path.stem

    if archive_kind == "sessions":
        date = extract_property(frontmatter, "date") or extract_date_from_filename(path.name)
        title = extract_property(frontmatter, "title") or clean_title(stem_name)

        if date and title:
            return f"- {date} — {title}"
        if date:
            return f"- {date} — {rel_name}"
        return f"- {clean_title(stem_name)}"

    if archive_kind == "quests":
        title = extract_property(frontmatter, "title") or extract_first_h1(body)
        if title:
            return f"- {clean_title(title)}"
        return f"- {clean_title(stem_name)}"

    return f"- {clean_title(stem_name)}"


def build_archive_block(
    path: Path,
    item_heading: str,
    archive_kind: str,
    source_root: Path,
) -> Tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(text)

    index_entry = make_index_entry(path, frontmatter, body, archive_kind, source_root)
    rel_name = relative_display_path(path, source_root)

    parts: List[str] = [f"## {item_heading}: {rel_name}"]

    if frontmatter:
        parts.extend([
            "",
            "```yaml",
            frontmatter,
            "```",
        ])

    cleaned_body = body.rstrip()
    if cleaned_body:
        parts.extend(["", cleaned_body])

    parts.extend([
        "",
        "---",
        "---",
        "---",
    ])

    return index_entry, "\n".join(parts)


def collect_markdown_files(source_dirs: List[Path]) -> List[Tuple[Path, Path]]:
    results: List[Tuple[Path, Path]] = []

    for source_dir in source_dirs:
        if not source_dir.exists():
            continue

        for path in source_dir.rglob("*.md"):
            if not path.is_file():
                continue
            if should_skip_file(path):
                continue
            results.append((path, source_dir))

    results.sort(key=lambda item: str(item[0]).lower())
    return results


def generate_archive(
    source_dirs: List[Path],
    output_file: Path,
    archive_title: str,
    item_heading: str,
    archive_kind: str,
    required_type: Optional[str],
) -> None:
    collected = collect_markdown_files(source_dirs)

    included: List[Tuple[Path, Path]] = []
    for path, source_root in collected:
        text = path.read_text(encoding="utf-8")
        frontmatter, _ = split_frontmatter(text)

        if file_matches_type(frontmatter, required_type):
            included.append((path, source_root))

    output_file.parent.mkdir(parents=True, exist_ok=True)

    if output_file.exists():
        output_file.unlink()

    if not included:
        output_file.write_text(
            f"# {archive_title}\n\n_No matching files found._\n",
            encoding="utf-8",
        )
        return

    index_entries: List[str] = []
    blocks: List[str] = []

    for path, source_root in included:
        index_entry, block = build_archive_block(
            path=path,
            item_heading=item_heading,
            archive_kind=archive_kind,
            source_root=source_root,
        )
        index_entries.append(index_entry)
        blocks.append(block)

    content = "\n".join([
        f"# {archive_title}",
        "",
        "## Index",
        *index_entries,
        "",
        "---",
        "",
        *blocks,
        "",
    ])

    output_file.write_text(content, encoding="utf-8")


def main() -> None:
    if not CAMPAIGN_ROOT.exists():
        raise FileNotFoundError(
            f"Campaign root not found: {CAMPAIGN_ROOT.resolve()}\n"
            f"Update CAMPAIGN_ROOT in the script if needed."
        )

    for archive_kind, cfg in ARCHIVE_CONFIG.items():
        generate_archive(
            source_dirs=cfg["source_dirs"],
            output_file=cfg["output_file"],
            archive_title=cfg["archive_title"],
            item_heading=cfg["item_heading"],
            archive_kind=archive_kind,
            required_type=cfg["required_type"],
        )
        print(f"Built: {cfg['output_file'].resolve()}")


if __name__ == "__main__":
    main()