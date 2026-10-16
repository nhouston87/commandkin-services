"""Dependency-free checks for the documentation bootstrap, not application tests."""
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def check(root, names):
    errors = []
    for name in names:
        path = root / name
        if path.is_symlink():
            errors.append(f"{name}: symlinks are not supported in this baseline")
            continue
        if path.suffix not in {".md", ".py", ".yml", ".yaml"}:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeError, OSError):
            errors.append(f"{name}: must be readable UTF-8")
            continue
        if not content.strip() or not content.endswith("\n"):
            errors.append(f"{name}: must be nonempty with a final newline")
        if any(line.rstrip() != line for line in content.splitlines()):
            errors.append(f"{name}: trailing whitespace")
        if re.search(r"^(<<<<<<< |=======\s*$|>>>>>>> )", content, re.MULTILINE):
            errors.append(f"{name}: unresolved merge conflict")
        if path.suffix == ".md":
            if not re.search(r"^# \S", content, re.MULTILINE):
                errors.append(f"{name}: missing document title")
            # Inline links only; network URLs and heading fragments are not fetched.
            for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", content):
                parsed = urlsplit(target)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                resolved = (path.parent / unquote(parsed.path)).resolve()
                if not resolved.is_relative_to(root.resolve()) or not resolved.exists():
                    errors.append(f"{name}: missing or outside-repository link: {target}")
    if "README.md" not in names:
        errors.append("README.md is required")
    return errors


if __name__ == "__main__":
    names = subprocess.check_output(
        ["git", "ls-files", "-z"], cwd=ROOT
    ).decode("utf-8").strip("\0").split("\0")
    errors = check(ROOT, names)
    for error in errors:
        print(error)
    if errors:
        raise SystemExit(1)
    print(f"Repository checks passed ({len(names)} tracked files).")
