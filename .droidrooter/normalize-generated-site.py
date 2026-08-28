#!/usr/bin/env python3
"""Normalize the checked-in static export without rewriting ranking content."""

from __future__ import annotations

import argparse
import datetime as dt
import html
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://www.droidrooter.com"
CUTOFF = dt.date(2026, 8, 28)
EARLIEST_REPOSITORY_DATE = "2026-08-28"
DEFAULT_EXISTING_LASTMOD = "2026-05-04"

ISO_DATE = re.compile(r"2026-(?:0[1-9]|1[0-2])-[0-3][0-9]")
VISIBLE_DATE = re.compile(
    r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) "
    r"([0-3]?[0-9]), (2026)\b"
)
CANONICAL = re.compile(r'<link rel="canonical" href="([^"]+)">')
ROBOTS_NOINDEX = re.compile(
    r'<meta name="robots" content="[^"]*noindex[^"]*">', re.IGNORECASE
)
META_REFRESH = re.compile(r'<meta[^>]+http-equiv="refresh"', re.IGNORECASE)
SITEMAP_URL = re.compile(
    r"<url>\s*<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>.*?</url>",
    re.DOTALL,
)


def replace_future_dates(text: str) -> tuple[str, int]:
    replacements = 0

    def replace_iso(match: re.Match[str]) -> str:
        nonlocal replacements
        value = dt.date.fromisoformat(match.group(0))
        if value > CUTOFF:
            replacements += 1
            return CUTOFF.isoformat()
        return match.group(0)

    def replace_visible(match: re.Match[str]) -> str:
        nonlocal replacements
        value = dt.datetime.strptime(match.group(0), "%b %d, %Y").date()
        if value > CUTOFF:
            replacements += 1
            return "Aug 28, 2026"
        return match.group(0)

    text = ISO_DATE.sub(replace_iso, text)
    text = VISIBLE_DATE.sub(replace_visible, text)
    return text, replacements


def canonical_route_for_file(path: Path) -> str:
    relative = path.relative_to(ROOT).as_posix()
    if relative == "index.html":
        return "/"
    if not relative.endswith("/index.html"):
        raise ValueError(f"Not a canonical directory route: {relative}")
    return "/" + relative[: -len("/index.html")]


def normalized_url(url: str) -> str:
    if url == BASE_URL + "/":
        return url
    return url.rstrip("/")


def collect_expected_sitemap(
    changed_pages: set[Path], existing_lastmods: dict[str, str]
) -> list[tuple[str, str]]:
    entries: dict[str, str] = {}
    for path in sorted(ROOT.rglob("*.html")):
        relative = path.relative_to(ROOT)
        if relative.parts[0] in {"docs", ".droidrooter"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if ROBOTS_NOINDEX.search(text) or META_REFRESH.search(text):
            continue
        canonicals = CANONICAL.findall(text)
        if len(canonicals) != 1:
            raise ValueError(f"{relative}: expected one canonical, found {len(canonicals)}")
        canonical = normalized_url(html.unescape(canonicals[0]))
        parsed = urlparse(canonical)
        if parsed.scheme != "https" or parsed.netloc != "www.droidrooter.com":
            raise ValueError(f"{relative}: invalid canonical {canonical}")
        expected_route = canonical_route_for_file(path)
        if parsed.path != expected_route:
            raise ValueError(
                f"{relative}: canonical path {parsed.path} does not match {expected_route}"
            )
        lastmod = (
            EARLIEST_REPOSITORY_DATE
            if path in changed_pages
            else existing_lastmods.get(canonical, DEFAULT_EXISTING_LASTMOD)
        )
        entries[canonical] = lastmod
    return sorted(entries.items())


def render_sitemap(entries: list[tuple[str, str]]) -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for url, lastmod in entries:
        lines.append(f"  <url><loc>{url}</loc><lastmod>{lastmod}</lastmod></url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def run(write: bool) -> int:
    current_sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    existing_lastmods = {
        normalized_url(url): lastmod
        for url, lastmod in SITEMAP_URL.findall(current_sitemap)
    }

    changed_pages: set[Path] = set()
    replacement_count = 0
    for path in sorted(ROOT.rglob("*.html")):
        relative = path.relative_to(ROOT)
        if relative.parts[0] in {"docs", ".droidrooter"}:
            continue
        original = path.read_text(encoding="utf-8", errors="ignore")
        updated, count = replace_future_dates(original)
        if relative.as_posix() == "404.html":
            updated = CANONICAL.sub("", updated)
        if updated != original:
            changed_pages.add(path)
            replacement_count += count
            if write:
                path.write_text(updated, encoding="utf-8")

    entries = collect_expected_sitemap(changed_pages, existing_lastmods)
    sitemap = render_sitemap(entries)
    sitemap_changed = sitemap != current_sitemap
    if write and sitemap_changed:
        (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")

    mode = "updated" if write else "would update"
    print(f"{mode} {len(changed_pages)} HTML files")
    print(f"{mode} {replacement_count} future-date tokens")
    print(f"sitemap entries: {len(entries)}")
    print(f"sitemap changed: {sitemap_changed}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write", action="store_true", help="Apply deterministic normalization"
    )
    args = parser.parse_args()
    raise SystemExit(run(args.write))