from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
ERRORS: list[str] = []
WARNINGS: list[str] = []

MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HTML_LINK = re.compile(r"(?:href|src)=[\"']([^\"']+)[\"']", re.IGNORECASE)


def report_error(message: str) -> None:
    ERRORS.append(message)


def report_warning(message: str) -> None:
    WARNINGS.append(message)


def validate_json_files() -> None:
    for path in ROOT.rglob("*.json"):
        if any(part in {".git", "site", "node_modules"} for part in path.parts):
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            report_error(f"JSON inválido: {path.relative_to(ROOT)} — {exc}")


def resolve_local_target(source: Path, target: str) -> Path | None:
    target = target.strip()
    if not target or target.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return None

    parsed = urlparse(target)
    if parsed.scheme in {"http", "https"}:
        return None

    clean = target.split("#", 1)[0].split("?", 1)[0]
    if not clean:
        return None

    if clean.startswith("/"):
        candidate = ROOT / clean.lstrip("/")
    else:
        candidate = source.parent / clean

    if candidate.exists():
        return candidate

    if candidate.suffix == "":
        for alternate in (
            candidate.with_suffix(".md"),
            candidate / "index.md",
            candidate / "index.html",
        ):
            if alternate.exists():
                return alternate

    return candidate


def validate_links() -> None:
    patterns = (MARKDOWN_LINK, HTML_LINK)
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".html"}:
            continue
        if any(part in {".git", "site", "node_modules"} for part in path.parts):
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            report_warning(f"Arquivo não UTF-8 ignorado: {path.relative_to(ROOT)}")
            continue

        targets: list[str] = []
        for pattern in patterns:
            targets.extend(pattern.findall(text))

        for target in targets:
            resolved = resolve_local_target(path, target)
            if resolved is not None and not resolved.exists():
                report_error(
                    f"Link local quebrado em {path.relative_to(ROOT)}: {target}"
                )


def validate_required_files() -> None:
    for name in ["README.md", "mkdocs.yml", "LICENSE"]:
        if not (ROOT / name).exists():
            report_warning(f"Arquivo recomendado ausente: {name}")

    if not DOCS.exists():
        report_error("Diretório docs/ ausente.")
    elif not any(DOCS.rglob("*.md")):
        report_error("Nenhuma página Markdown encontrada em docs/.")


def validate_markdown_headings() -> None:
    for path in DOCS.rglob("*.md") if DOCS.exists() else []:
        text = path.read_text(encoding="utf-8")
        headings = [line for line in text.splitlines() if line.startswith("#")]
        has_html_h1 = bool(re.search(r"<h1(?:\s[^>]*)?>.*?</h1>", text, re.IGNORECASE | re.DOTALL))
        if not headings and not has_html_h1:
            report_warning(f"Página sem título H1: {path.relative_to(ROOT)}")
        for line_no, line in enumerate(text.splitlines(), start=1):
            if re.match(r"^#{1,6}[^ #]", line):
                report_error(
                    f"Heading sem espaço em {path.relative_to(ROOT)}:{line_no}"
                )


def main() -> int:
    validate_required_files()
    validate_json_files()
    validate_links()
    validate_markdown_headings()

    print("=== Auditoria Claude Skills Observatory ===")
    print(f"Erros: {len(ERRORS)}")
    print(f"Avisos: {len(WARNINGS)}")

    if WARNINGS:
        print("\nAvisos:")
        for item in WARNINGS:
            print(f"- {item}")

    if ERRORS:
        print("\nErros:")
        for item in ERRORS:
            print(f"- {item}")
        return 1

    print("\nAuditoria concluída sem erros bloqueadores.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
