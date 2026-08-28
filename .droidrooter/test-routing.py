#!/usr/bin/env python3
"""Static and optional live regression checks for DroidRooter routing."""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://www.droidrooter.com"
CUTOFF = dt.date(2026, 8, 28)
CANONICAL = re.compile(r'<link rel="canonical" href="([^"]+)">')
ROBOTS_NOINDEX = re.compile(
    r'<meta name="robots" content="[^"]*noindex[^"]*">', re.IGNORECASE
)
META_REFRESH = re.compile(r'<meta[^>]+http-equiv="refresh"', re.IGNORECASE)
JSON_LD = re.compile(
    r'<script type="application/ld\+json">(.*?)</script>', re.DOTALL | re.IGNORECASE
)
ISO_DATE = re.compile(r"2026-(?:0[1-9]|1[0-2])-[0-3][0-9]")
VISIBLE_DATE = re.compile(
    r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) "
    r"([0-3]?[0-9]), (2026)\b"
)

HIGH_RISK_SOURCES = {
    "/blog/rootable-android-devices-complete-list-2025.html",
    "/blog/rootable-android-devices-complete-list-2025",
    "/blog/android-custom-kernel-guide-2025",
    "/blog/unlock-bootloader-android-guide",
}

SERVICE_CLUSTER = {
    "/services/android-rooting",
    "/services/bootloader-unlock",
    "/services/magisk-installation",
    "/services/custom-rom-installation",
    "/services/advanced-mods",
}


def route_for(path: Path) -> str:
    relative = path.relative_to(ROOT).as_posix()
    if relative == "index.html":
        return "/"
    return "/" + relative[: -len("/index.html")]


def static_checks() -> None:
    expected_urls: set[str] = set()
    json_ld_blocks = 0
    for path in ROOT.rglob("*.html"):
        relative = path.relative_to(ROOT)
        if relative.parts[0] in {"docs", ".droidrooter"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for value in ISO_DATE.findall(text):
            assert dt.date.fromisoformat(value) <= CUTOFF, (
                f"{relative}: future date remains: {value}"
            )
        for month, day, year in VISIBLE_DATE.findall(text):
            value = dt.datetime.strptime(
                f"{month} {day}, {year}", "%b %d, %Y"
            ).date()
            assert value <= CUTOFF, (
                f"{relative}: future visible date remains: {value}"
            )
        for block in JSON_LD.findall(text):
            data = json.loads(html.unescape(block))
            json_ld_blocks += 1
            assert "AggregateRating" not in json.dumps(data), (
                f"{relative}: self-serving AggregateRating remains"
            )
            organization_ids: set[str] = set()

            def collect_organization_ids(value) -> None:
                if isinstance(value, dict):
                    kind = value.get("@type")
                    if kind == "Organization" and value.get("@id"):
                        organization_ids.add(value["@id"])
                    for child in value.values():
                        collect_organization_ids(child)
                elif isinstance(value, list):
                    for child in value:
                        collect_organization_ids(child)

            collect_organization_ids(data)
            assert len(organization_ids) <= 1, (
                f"{relative}: conflicting Organization @ids: "
                f"{sorted(organization_ids)}"
            )

        noindex = bool(ROBOTS_NOINDEX.search(text))
        redirected = bool(META_REFRESH.search(text))
        canonicals = CANONICAL.findall(text)
        if noindex or redirected:
            self_url = BASE_URL + route_for(path)
            assert all(
                html.unescape(canonical).rstrip("/") != self_url.rstrip("/")
                for canonical in canonicals
            ), f"{relative}: redirected/noindex page claims itself as canonical"
            continue
        assert len(canonicals) == 1, (
            f"{relative}: indexable page has {len(canonicals)} canonicals"
        )
        canonical = html.unescape(canonicals[0])
        assert canonical.startswith(BASE_URL + "/"), (
            f"{relative}: canonical is not absolute HTTPS"
        )
        expected = BASE_URL + route_for(path)
        assert canonical == expected, (
            f"{relative}: canonical {canonical} is not self-referencing {expected}"
        )
        expected_urls.add(canonical)

    assert json_ld_blocks > 0, "No JSON-LD blocks were validated"

    # Production redirects live in nginx on the VPS; the reference copy is kept
    # in .droidrooter/nginx-droidrooter.conf and must stay in sync.
    nginx_conf = (ROOT / ".droidrooter" / "nginx-droidrooter.conf").read_text(
        encoding="utf-8"
    )
    redirect_sources = set(re.findall(r"location = (\S+)", nginx_conf))
    assert not (HIGH_RISK_SOURCES & redirect_sources), (
        "High-risk source was added to permanent redirects"
    )

    tree = ET.parse(ROOT / "sitemap.xml")
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    sitemap_urls = {
        node.text for node in tree.findall(".//sm:loc", namespace) if node.text
    }
    assert sitemap_urls == expected_urls, (
        f"Sitemap mismatch: missing={sorted(expected_urls - sitemap_urls)}, "
        f"extra={sorted(sitemap_urls - expected_urls)}"
    )
    assert all(url == BASE_URL + "/" or not url.endswith("/") for url in sitemap_urls)
    assert not any("/index." in url or url.endswith(".html") for url in sitemap_urls)
    assert {BASE_URL + route for route in SERVICE_CLUSTER} <= sitemap_urls

    for route in SERVICE_CLUSTER:
        path = ROOT / route.lstrip("/") / "index.html"
        text = path.read_text(encoding="utf-8")
        assert len(re.findall(r"<h1(?:\s|>)", text)) == 1, (
            f"{route}: expected exactly one H1"
        )
        schema_types = set(re.findall(r'"@type":"([^"]+)"', text))
        assert "FAQPage" not in schema_types
        assert "Service" not in schema_types
        assert "Offer" not in schema_types
        assert "All Major Brands" not in text
        assert "pay only after" not in text.lower()
        assert "banking-safe" not in text.lower()
    print(
        f"Static checks passed: {len(expected_urls)} canonical URLs, "
        f"{json_ld_blocks} valid JSON-LD blocks"
    )


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch_without_redirect(url: str) -> tuple[int, str | None]:
    opener = urllib.request.build_opener(NoRedirect)
    request = urllib.request.Request(url, headers={"User-Agent": "DroidRooterRegression/1.0"})
    try:
        response = opener.open(request, timeout=20)
        return response.status, response.headers.get("Location")
    except urllib.error.HTTPError as error:
        return error.code, error.headers.get("Location")


def fetch_following(url: str) -> tuple[int, str, str]:
    request = urllib.request.Request(url, headers={"User-Agent": "DroidRooterRegression/1.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        body = response.read().decode("utf-8", errors="ignore")
        return response.status, response.geturl(), body


def live_checks(base_url: str) -> None:
    base_url = base_url.rstrip("/")
    aliases = {
        "/index.html": "/",
        "/about/": "/about",
        "/about/index.html": "/about",
        "/contact.html": "/contact",
        "/devices/": "/devices/samsung",
        "/tools/": "/tools/rootability-checker",
    }
    for source, destination in aliases.items():
        status, location = fetch_without_redirect(base_url + source)
        assert status in {301, 308}, f"{source}: expected permanent redirect, got {status}"
        resolved = urllib.parse.urljoin(base_url + source, location or "")
        assert resolved == base_url + destination, (
            f"{source}: expected {destination}, got {location}"
        )
        final_status, final_url, body = fetch_following(base_url + source)
        assert final_status == 200, f"{source}: final status {final_status}"
        assert final_url.rstrip("/") == (base_url + destination).rstrip("/")
        canonical = CANONICAL.search(body)
        assert canonical, f"{destination}: canonical missing"
        assert canonical.group(1).rstrip("/") == final_url.rstrip("/"), (
            f"{destination}: canonical does not match final URL"
        )

    tier_a = "/blog/magisk-modules-guide-2026"
    status, location = fetch_without_redirect(base_url + tier_a)
    assert status == 200 and location is None, (
        f"Tier A route changed: status={status}, location={location}"
    )
    print(f"Live checks passed: {len(aliases)} aliases and Tier A route")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", help="Run live redirect checks against this host")
    args = parser.parse_args()
    static_checks()
    if args.base_url:
        live_checks(args.base_url)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)