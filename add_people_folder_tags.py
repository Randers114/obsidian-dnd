from __future__ import annotations

from pathlib import Path
import re
from typing import Optional, Tuple, List


PEOPLE_ROOT = Path("Whispers of the Umbral Abyss") / "People"


def to_snake_case(value: str) -> str:
    """
    Convert a folder name like 'Faction Figures' to 'faction_figures'.
    """
    value = value.strip().lower()
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"[\s-]+", "_", value)
    value = re.sub(r"_+", "_", value)
    return value.strip("_")


def split_frontmatter(text: str) -> Tuple[Optional[str], str]:
    """
    Return (frontmatter_without_markers, body).
    If no valid YAML frontmatter exists, returns (None, original_text).
    """
    if not text.startswith("---\n"):
        return None, text

    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not match:
        return None, text

    frontmatter = match.group(1)
    body = match.group(2)
    return frontmatter, body


def extract_tags(frontmatter: str) -> Tuple[List[str], bool]:
    """
    Extract tags from a YAML list like:

    tags:
      - person
      - allies

    Returns:
        (tags, found_tags_block)
    """
    lines = frontmatter.splitlines()
    tags: List[str] = []
    found_tags_block = False
    in_tags_block = False

    for line in lines:
        if re.match(r"^tags:\s*$", line):
            found_tags_block = True
            in_tags_block = True
            continue

        if in_tags_block:
            tag_match = re.match(r"^\s*-\s*(.+?)\s*$", line)
            if tag_match:
                tag_value = tag_match.group(1).strip().strip('"').strip("'")
                tags.append(tag_value)
                continue
            else:
                in_tags_block = False

    return tags, found_tags_block


def replace_or_add_tags_block(frontmatter: str, new_tags: List[str]) -> str:
    """
    Replace existing tags block or add a new one.
    """
    lines = frontmatter.splitlines()
    tag_block_lines = ["tags:"] + [f"  - {tag}" for tag in new_tags]

    start_idx = None
    end_idx = None

    for i, line in enumerate(lines):
        if re.match(r"^tags:\s*$", line):
            start_idx = i
            end_idx = i + 1

            while end_idx < len(lines):
                if re.match(r"^\s*-\s+.+$", lines[end_idx]):
                    end_idx += 1
                else:
                    break
            break

    if start_idx is not None and end_idx is not None:
        new_lines = lines[:start_idx] + tag_block_lines + lines[end_idx:]
    else:
        # Add tags at the end of frontmatter
        if lines and lines[-1].strip() != "":
            new_lines = lines + [""] + tag_block_lines
        else:
            new_lines = lines + tag_block_lines

    return "\n".join(new_lines)


def update_note_tags(file_path: Path) -> bool:
    """
    Add the immediate parent folder as a snake_case tag.
    Returns True if file was changed.
    """
    text = file_path.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(text)

    if frontmatter is None:
        print(f"Skipped (no frontmatter): {file_path}")
        return False

    folder_name = file_path.parent.name
    folder_tag = to_snake_case(folder_name)

    if not folder_tag:
        print(f"Skipped (invalid folder name): {file_path}")
        return False

    existing_tags, _ = extract_tags(frontmatter)

    if folder_tag in existing_tags:
        return False

    updated_tags = existing_tags.copy()
    updated_tags.append(folder_tag)

    new_frontmatter = replace_or_add_tags_block(frontmatter, updated_tags)
    new_text = f"---\n{new_frontmatter}\n---\n{body}"

    file_path.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    if not PEOPLE_ROOT.exists():
        raise FileNotFoundError(
            f"People folder not found: {PEOPLE_ROOT.resolve()}"
        )

    updated = 0
    checked = 0

    for file_path in PEOPLE_ROOT.rglob("*.md"):
        if not file_path.is_file():
            continue

        checked += 1
        if update_note_tags(file_path):
            updated += 1
            print(f"Updated: {file_path}")

    print(f"\nDone. Checked {checked} files. Updated {updated} files.")


if __name__ == "__main__":
    main()