from __future__ import annotations

import re
from pathlib import Path
from typing import Optional, Tuple, List


def split_frontmatter(text: str) -> Tuple[Optional[str], str]:
    """
    Split Obsidian-style YAML frontmatter from the rest of the file.

    Returns:
        (frontmatter, body)
        - frontmatter: string without the surrounding --- lines, or None
        - body: remaining markdown body
    """
    if not text.startswith("---\n"):
        return None, text

    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not match:
        return None, text

    frontmatter = match.group(1).strip()
    body = match.group(2).lstrip("\n")
    return frontmatter, body


def extract_title_from_body(body: str) -> Optional[str]:
    """
    Try to find the first H1 heading in the note body.
    """
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return None


def extract_date_from_filename(filename: str) -> Optional[str]:
    """
    Extract YYYY-MM-DD from filenames like:
    2026-03-26 - Doors of Shadebarrow.md
    """
    match = re.match(r"(\d{4}-\d{2}-\d{2})", filename)
    return match.group(1) if match else None


def build_index_entry(filename: str, body: str) -> str:
    """
    Build a simple session index entry.
    """
    date = extract_date_from_filename(filename)
    title = extract_title_from_body(body)

    if title:
        title = re.sub(r'^\d{4}-\d{2}-\d{2}\s*-\s*', '', title).strip()

    if date and title:
        return f"- {date} — {title}"
    if date:
        return f"- {date} — {filename}"
    if title:
        return f"- {title}"
    return f"- {filename}"


def build_session_block(file_path: Path) -> Tuple[str, str]:
    """
    Build one archive block for a single session note.

    Returns:
        (index_entry, session_block)
    """
    text = file_path.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(text)

    index_entry = build_index_entry(file_path.name, body)

    parts: List[str] = []
    parts.append(f"## Session File: {file_path.name}")

    if frontmatter:
        parts.append("```yaml")
        parts.append(frontmatter)
        parts.append("```")

    parts.append(body.rstrip())
    parts.append("\n---\n---\n---")

    return index_entry, "\n\n".join(parts)


def generate_sessions_archive(
    sessions_dir: Path,
    output_file: Path,
    archive_title: str = "Sessions Archive — Whispers of the Umbral Abyss",
) -> None:
    """
    Generate a combined markdown archive from all session notes in a folder.
    """
    if not sessions_dir.exists():
        raise FileNotFoundError(f"Sessions folder does not exist: {sessions_dir}")

    if not sessions_dir.is_dir():
        raise NotADirectoryError(f"Not a folder: {sessions_dir}")

    session_files = sorted(
        [p for p in sessions_dir.iterdir() if p.is_file() and p.suffix.lower() == ".md"],
        key=lambda p: p.name.lower(),
    )

    if not session_files:
        raise ValueError(f"No markdown files found in: {sessions_dir}")

    index_entries: List[str] = []
    session_blocks: List[str] = []

    for file_path in session_files:
        index_entry, block = build_session_block(file_path)
        index_entries.append(index_entry)
        session_blocks.append(block)

    output_parts = [
        f"# {archive_title}",
        "",
        "## Session Index",
        *index_entries,
        "",
        "---",
        "",
        *session_blocks,
        "",
    ]

    output_file.write_text("\n".join(output_parts), encoding="utf-8")


if __name__ == "__main__":
    # Change these paths to match your vault
    sessions_folder = Path(r"./Whispers of the Umbral Abyss/Sessions")
    output_archive = Path(r"./Whispers of the Umbral Abyss/Sessions Archive.md")

    generate_sessions_archive(sessions_folder, output_archive)
    print(f"Archive created: {output_archive.resolve()}")