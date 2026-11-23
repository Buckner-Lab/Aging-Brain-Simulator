#!/usr/bin/env python3
"""Write an index.html file listing the contents of each top-level folder.

GitHub Pages never shows a folder's contents, so a link to a folder would
otherwise give a 404. This script writes one index.html per top-level folder,
listing every file git tracks there, with its size. Markdown files link to
their formatted view on github.com; every other file links to itself.

The output depends only on the files in the repository, so running it twice
gives identical files. The GitHub Action in .github/workflows/ runs it on
every push and commits any listing that changed.

Run it from anywhere inside the repository:

    python3 .github/scripts/make_folder_indexes.py
"""

import html
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

# Where .md files open, formatted. Change this if the repository moves.
GITHUB_BLOB_URL = "https://github.com/Buckner-Lab/Aging-Brain-Simulator/blob/main/"

LISTING_NAME = "index.html"

FOLDER_ICON = (
    '<svg class="fi" width="18" height="15" viewBox="0 0 18 15" aria-hidden="true">'
    '<path d="M1 2.5A1.5 1.5 0 0 1 2.5 1h4l1.6 2h7.4A1.5 1.5 0 0 1 17 4.5v8a1.5 1.5 0 0 1-1.5 1.5h-13'
    'A1.5 1.5 0 0 1 1 12.5z"/></svg>'
)
FILE_ICON = (
    '<svg class="fl" width="13" height="15" viewBox="0 0 13 15" aria-hidden="true">'
    '<path d="M1.5 1h6.5l3.5 3.5v8.5a1 1 0 0 1-1 1h-9a1 1 0 0 1-1-1v-11a1 1 0 0 1 1-1z M8 1v3.5h3.5"/></svg>'
)

# The same colour tokens as the version list, so the listings follow the
# reader's light or dark setting the same way that page does.
STYLE = """\
:root { --bg: #fcfbf8; --surface: #ffffff; --ink: #1c1c1e; --ink-2: #55534f; --muted: #85827b; --line: #e3e1da; --band: #f4f3ee; --accent: #b4521f; color-scheme: light dark; }
@media (prefers-color-scheme: dark) { :root { --bg: #131312; --surface: #1a1a18; --ink: #f1f0eb; --ink-2: #c4c2ba; --muted: #8f8c85; --line: #34322e; --band: #1f1f1c; --accent: #e2733d; } }
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink); font: 14px/1.5 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }
main { max-width: 960px; margin: 0 auto; padding: 28px 16px 56px; }
a { color: var(--accent); }
nav.back { font-size: 13px; margin: 0 0 18px; }
nav.back a { font-weight: 600; text-decoration: none; }
nav.back a:hover { text-decoration: underline; }
.kicker { margin: 0 0 2px; font-size: 12px; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); }
h1 { display: flex; align-items: center; gap: 10px; margin: 0 0 6px; font: 600 22px/1.25 ui-monospace, Menlo, Consolas, monospace; overflow-wrap: anywhere; }
.fi { flex: none; } .fi path { fill: color-mix(in srgb, var(--accent) 22%, transparent); stroke: var(--accent); stroke-width: 1.3; }
.count { margin: 0 0 18px; color: var(--ink-2); }
table { width: 100%; border-collapse: separate; border-spacing: 0; background: var(--surface); border: 1px solid var(--line); border-radius: 10px; overflow: hidden; }
th { text-align: left; font-weight: 600; font-size: 12px; color: var(--muted); padding: 9px 12px; border-bottom: 1px solid var(--line); background: var(--band); }
th.size, td.size { text-align: right; }
td { padding: 7px 12px; border-bottom: 1px solid var(--line); vertical-align: baseline; }
tr:last-child td { border-bottom: 0; }
tbody tr:hover td { background: color-mix(in srgb, var(--accent) 5%, var(--surface)); }
td.name a { display: inline-flex; align-items: baseline; gap: 8px; color: var(--ink); text-decoration: none; font: 13px ui-monospace, Menlo, Consolas, monospace; overflow-wrap: anywhere; }
td.name a:hover { color: var(--accent); text-decoration: underline; }
.fl { flex: none; position: relative; top: 2px; } .fl path { fill: none; stroke: var(--muted); stroke-width: 1.2; }
.ext { font: 11.5px system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; color: var(--muted); white-space: nowrap; }
td.size { white-space: nowrap; color: var(--ink-2); font: 12px ui-monospace, Menlo, Consolas, monospace; }
.note { margin: 14px 0 0; font-size: 12.5px; color: var(--muted); }
@media (max-width: 600px) { h1 { font-size: 17px; } td, th { padding: 7px 9px; } }
"""


def repo_root() -> Path:
    out = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, check=True,
        cwd=Path(__file__).resolve().parent,
    )
    return Path(out.stdout.strip())


def tracked_files(root: Path) -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "-z"], capture_output=True, check=True, cwd=root,
    )
    return [p for p in out.stdout.decode("utf-8").split("\0") if p]


def natural_key(name: str):
    """Sort v9 before v10, ignoring case."""
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", name)]


def human_size(n: int) -> str:
    """Sizes in decimal units, as browsers and Finder show them."""
    if n < 1000:
        return f"{n} B"
    for unit in ("kB", "MB", "GB"):
        n /= 1000
        if n < 1000 or unit == "GB":
            return f"{n:.3g} {unit}" if n < 100 else f"{n:.0f} {unit}"
    raise AssertionError


def render(folder: str, entries: list[tuple[str, int]]) -> str:
    rows = []
    for name, size in entries:
        if name.lower().endswith(".md"):
            href = GITHUB_BLOB_URL + quote(f"{folder}/{name}")
            extra = ' <span class="ext">opens on GitHub</span>'
        else:
            href = quote(name)
            extra = ""
        rows.append(
            f'<tr><td class="name"><a href="{html.escape(href)}">{FILE_ICON}'
            f"<span>{html.escape(name)}</span></a>{extra}</td>"
            f'<td class="size">{human_size(size)}</td></tr>'
        )
    count = len(entries)
    noun = "file" if count == 1 else "files"
    title = html.escape(folder)
    return (
        "<!doctype html>\n"
        '<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{title}: AgingBrain Simulator</title>\n"
        '<meta name="color-scheme" content="light dark">\n'
        f"<style>\n{STYLE}</style></head><body><main>\n"
        "<!-- Written by .github/scripts/make_folder_indexes.py. Edits by hand are overwritten on the next push. -->\n"
        '<nav class="back"><a href="../index.html">&larr; AgingBrain Simulator: all versions</a></nav>\n'
        '<p class="kicker">Folder</p>\n'
        f"<h1>{FOLDER_ICON}<span>{title}</span></h1>\n"
        f'<p class="count">{count} {noun}</p>\n'
        '<table><thead><tr><th>Name</th><th class="size">Size</th></tr></thead><tbody>\n'
        + "\n".join(rows)
        + "\n</tbody></table>\n"
        "</main></body></html>\n"
    )


def main() -> int:
    root = repo_root()
    by_folder: dict[str, list[str]] = {}
    for path in tracked_files(root):
        parts = path.split("/")
        if len(parts) < 2 or parts[0].startswith("."):
            continue  # files at the root, and hidden folders such as .github
        folder, rest = parts[0], "/".join(parts[1:])
        if "/" in rest:
            continue  # files in sub-folders are not listed
        if rest == LISTING_NAME or rest.startswith("."):
            continue  # the listing itself, and hidden files such as .gitkeep
        by_folder.setdefault(folder, []).append(rest)

    changed = 0
    for folder, names in sorted(by_folder.items()):
        names.sort(key=natural_key)
        entries = []
        for name in names:
            p = root / folder / name
            if p.is_file():  # skip files deleted but not yet committed
                entries.append((name, p.stat().st_size))
        text = render(folder, entries)
        out = root / folder / LISTING_NAME
        old = out.read_text(encoding="utf-8") if out.exists() else None
        if old != text:
            out.write_text(text, encoding="utf-8")
            changed += 1
            print(f"wrote {folder}/{LISTING_NAME} ({len(entries)} files)")
    if not changed:
        print("All folder listings are up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
