from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
PATTERNS = {
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    "Generic API key assignment": re.compile(
        r"(?i)\b(api[_-]?key|secret|token)\b\s*[:=]\s*['\"][^'\"]{12,}['\"]"
    ),
    "Private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}
SKIP = {".git", "site", "node_modules", ".venv", "venv"}
TEXT_EXTENSIONS = {
    ".md", ".txt", ".yml", ".yaml", ".json", ".py",
    ".js", ".css", ".html", ".toml", ".ini", ".env"
}


def main() -> int:
    findings: list[str] = []

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP for part in path.parts):
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS and path.name != ".env":
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        for label, pattern in PATTERNS.items():
            if pattern.search(text):
                findings.append(f"{label}: {path.relative_to(ROOT)}")

    if findings:
        print("Possíveis segredos encontrados:")
        for finding in findings:
            print(f"- {finding}")
        return 1

    print("Nenhum padrão comum de segredo foi encontrado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
