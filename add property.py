from pathlib import Path
import re

SESSIONS_DIR = Path("Whispers of the Umbral Abyss") / "Sessions"


def add_type_to_frontmatter(file_path: Path) -> bool:
    text = file_path.read_text(encoding="utf-8")

    if not text.startswith("---\n"):
        return False

    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not match:
        return False

    frontmatter = match.group(1)
    body = match.group(2)

    # Skip if already present
    if re.search(r"(?m)^type:\s*session\s*$", frontmatter):
        return False

    lines = frontmatter.splitlines()

    new_lines = []
    inserted = False

    for line in lines:
        new_lines.append(line)

        # Insert type right after sessionNumber if present
        if re.match(r"^sessionNumber\s*:", line) and not inserted:
            new_lines.append("type: session")
            inserted = True

    # Fallback: if sessionNumber was not found, insert near top
    if not inserted:
        new_lines.insert(0, "type: session")

    new_frontmatter = "\n".join(new_lines)
    new_text = f"---\n{new_frontmatter}\n---\n{body}"

    file_path.write_text(new_text, encoding="utf-8")
    return True


def main():
    updated = 0

    for file_path in SESSIONS_DIR.rglob("*.md"):
        if add_type_to_frontmatter(file_path):
            updated += 1
            print(f"Updated: {file_path}")

    print(f"\nDone. Updated {updated} files.")


if __name__ == "__main__":
    main()