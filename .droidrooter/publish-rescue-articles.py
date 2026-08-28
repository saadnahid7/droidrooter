#!/usr/bin/env python3
"""Integrate the twelve approved rescue articles into the generated DroidRooter site."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT.parent / "attached_assets"
ARTICLE_TEMPLATE = ROOT / "blog/android-custom-kernel-guide-2026/index.html"
AUTHOR_TEMPLATE = ROOT / "team/naz-n/index.html"

ARTICLE_SPECS = [
    ("B01-android-bootloop-fix-without-losing-data", "2026-08-18"),
    ("B02-phone-stuck-on-boot-screen", "2026-08-20"),
    ("B03-soft-brick-vs-hard-brick", "2026-08-22"),
    ("B04-magisk-flash-failed-recovery", "2026-08-24"),
    ("B05-stuck-in-recovery-mode-android", "2026-08-26"),
    ("B06-fastboot-device-not-detected", "2026-08-28"),
    ("B07-edl-mode-explained", "2026-08-17"),
    ("B08-failed-ota-update-rooted-phone", "2026-08-19"),
    ("B09-odin-fail-errors-samsung", "2026-08-21"),
    ("B10-bootloop-after-custom-rom", "2026-08-23"),
    ("B11-android-wont-turn-on-diagnosis", "2026-08-25"),
    ("B12-recover-data-from-bricked-phone", "2026-08-27"),
]

HERO_IMAGES = {
    "android-bootloop-fix-without-losing-data": "broken-phone-fix.webp",
    "phone-stuck-on-boot-screen": "broken-phone-fix.webp",
    "soft-brick-vs-hard-brick": "bootloader-recovery.webp",
    "magisk-flash-failed-recovery": "magisk-modules.webp",
    "stuck-in-recovery-mode-android": "bootloader-recovery.webp",
    "fastboot-device-not-detected": "bootloader-recovery.webp",
    "edl-mode-explained": "bootloader-recovery.webp",
    "failed-ota-update-rooted-phone": "android-features.webp",
    "odin-fail-errors-samsung": "samsung-root.webp",
    "bootloop-after-custom-rom": "custom-roms.webp",
    "android-wont-turn-on-diagnosis": "broken-phone-fix.webp",
    "recover-data-from-bricked-phone": "storage-recovery.webp",
}

RELATED_GUIDES = {
    "android-bootloop-fix-without-losing-data": [
        "phone-stuck-on-boot-screen",
        "soft-brick-vs-hard-brick",
        "magisk-flash-failed-recovery",
    ],
    "phone-stuck-on-boot-screen": [
        "android-bootloop-fix-without-losing-data",
        "android-wont-turn-on-diagnosis",
        "stuck-in-recovery-mode-android",
    ],
    "soft-brick-vs-hard-brick": [
        "edl-mode-explained",
        "magisk-flash-failed-recovery",
        "bootloop-after-custom-rom",
    ],
    "magisk-flash-failed-recovery": [
        "failed-ota-update-rooted-phone",
        "soft-brick-vs-hard-brick",
        "stuck-in-recovery-mode-android",
    ],
    "stuck-in-recovery-mode-android": [
        "android-bootloop-fix-without-losing-data",
        "phone-stuck-on-boot-screen",
        "fastboot-device-not-detected",
    ],
    "fastboot-device-not-detected": [
        "soft-brick-vs-hard-brick",
        "android-bootloop-fix-without-losing-data",
        "edl-mode-explained",
    ],
    "edl-mode-explained": [
        "soft-brick-vs-hard-brick",
        "fastboot-device-not-detected",
        "recover-data-from-bricked-phone",
    ],
    "failed-ota-update-rooted-phone": [
        "magisk-flash-failed-recovery",
        "odin-fail-errors-samsung",
        "bootloop-after-custom-rom",
    ],
    "odin-fail-errors-samsung": [
        "failed-ota-update-rooted-phone",
        "magisk-flash-failed-recovery",
        "soft-brick-vs-hard-brick",
    ],
    "bootloop-after-custom-rom": [
        "soft-brick-vs-hard-brick",
        "android-bootloop-fix-without-losing-data",
        "magisk-flash-failed-recovery",
    ],
    "android-wont-turn-on-diagnosis": [
        "phone-stuck-on-boot-screen",
        "android-bootloop-fix-without-losing-data",
        "recover-data-from-bricked-phone",
    ],
    "recover-data-from-bricked-phone": [
        "android-wont-turn-on-diagnosis",
        "android-bootloop-fix-without-losing-data",
        "edl-mode-explained",
    ],
}

AUTHORS = {
    "Saad Bin Abdul Hai": {
        "slug": "saad-nahid",
        "role": "Android IT Expert & Founder, Droid Rooter",
        "bio": (
            "Saad Bin Abdul Hai is the founder of Droid Rooter and a hands-on "
            "Android IT specialist with over three years of remote-support "
            "experience across more than 160 client devices. He focuses on "
            "rooting, custom ROM installs, FRP bypass, IMEI repair and recovery "
            "work for bricked phones, and writes every guide on this site from "
            "his own field experience."
        ),
    },
    "Imran R.": {
        "slug": "imran-r",
        "role": "Rescue & Recovery Diagnostics",
        "location": "Virginia, United States",
        "coverage": (
            "Bootloop triage, boot-screen symptom diagnosis, Magisk and "
            "boot-image failures, fastboot and USB connectivity, data-preserving "
            "recovery paths"
        ),
        "hours": "US Eastern business hours",
        "bio": (
            "Imran R. handles rescue and recovery diagnosis at Droid Rooter, "
            "working from Virginia in the United States. He covers bootloops, "
            "failed flashes, boot-image mismatches and fastboot connectivity "
            "problems, with a focus on working out what a device is actually "
            "doing before anything destructive gets run on it. He writes the "
            "diagnostic tables and decision trees used across the rescue guides "
            "on this site."
        ),
        "short_bio": (
            "Rescue and recovery diagnostics at Droid Rooter, based in Virginia, "
            "USA. Covers bootloops, failed flashes and fastboot connectivity."
        ),
    },
    "Ontor Zubair": {
        "slug": "ontor-zubair",
        "role": "Firmware & Brick Recovery",
        "location": "Dubai, United Arab Emirates",
        "coverage": (
            "Soft and hard brick classification, stock firmware restores, vendor "
            "flash tooling, recovery-mode and A/B slot issues, GCC device variants"
        ),
        "hours": "Gulf Standard Time",
        "bio": (
            "Ontor Zubair covers firmware and brick recovery at Droid Rooter from "
            "Dubai, United Arab Emirates. His work is the boundary between what "
            "software can still reach and what it cannot: classifying brick "
            "states, restoring stock firmware, and handling recovery-mode and "
            "slot problems on devices that will not boot. He handles a large "
            "share of the GCC caseload and the regional firmware variants that "
            "come with it."
        ),
        "short_bio": (
            "Firmware and brick recovery at Droid Rooter, based in Dubai, UAE. "
            "Covers brick classification, stock firmware restores and "
            "recovery-mode faults."
        ),
    },
}


def latest_asset(prefix: str) -> Path:
    candidates = sorted(ASSETS.glob(prefix + "_*.md"))
    if not candidates:
        raise FileNotFoundError(f"missing attached article for {prefix}")
    return candidates[-1]


def scalar(frontmatter: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.*)$", frontmatter, re.MULTILINE)
    if not match:
        raise ValueError(f"missing frontmatter field: {key}")
    value = match.group(1).strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1]
    return value


def read_article(prefix: str) -> dict:
    path = latest_asset(prefix)
    raw = path.read_text(encoding="utf-8")
    parts = raw.split("---", 2)
    if len(parts) != 3:
        raise ValueError(f"invalid frontmatter in {path}")
    frontmatter, body = parts[1], parts[2].lstrip()
    fields = {
        key: scalar(frontmatter, key)
        for key in (
            "slug",
            "url",
            "canonical",
            "title",
            "meta_title",
            "meta_description",
            "excerpt",
            "category",
            "difficulty",
            "author",
            "datePublished",
            "dateModified",
            "last_verified",
            "image_alt",
            "schema",
        )
    }
    fields["body"] = body
    fields["source"] = path
    fields["body"] = re.sub(
        r"<!--\s*AFFILIATE SLOT:.*?-->\s*",
        "",
        fields["body"],
        flags=re.DOTALL,
    )
    return fields


def normalize_internal_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.netloc == "www.droidrooter.com":
        path = parsed.path.rstrip("/") or "/"
        return path + (f"#{parsed.fragment}" if parsed.fragment else "")
    return url


def inline(text: str) -> str:
    text = re.sub(
        r"https://www\.droidrooter\.com/[^\s)>\"]+",
        lambda m: normalize_internal_url(m.group(0)),
        text,
    )
    escaped = html.escape(text, quote=False)
    code_tokens: list[str] = []

    def save_code(match: re.Match[str]) -> str:
        code_tokens.append(f"<code>{html.escape(match.group(1), quote=False)}</code>")
        return f"\x00CODE{len(code_tokens) - 1}\x00"

    escaped = re.sub(r"`([^`]+)`", save_code, escaped)

    def link(match: re.Match[str]) -> str:
        label = match.group(1)
        href = normalize_internal_url(match.group(2))
        return f'<a href="{html.escape(href, quote=True)}">{label}</a>'

    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", escaped)
    for index, token in enumerate(code_tokens):
        escaped = escaped.replace(f"\x00CODE{index}\x00", token)
    return escaped


def cells(line: str) -> list[str]:
    value = line.strip()
    if value.startswith("|"):
        value = value[1:]
    if value.endswith("|"):
        value = value[:-1]
    return [part.strip() for part in value.split("|")]


def slugify(text: str) -> str:
    text = re.sub(r"[`*_]", "", text).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text


def scoped(markup: str, scope_id: str) -> str:
    tags = (
        "a",
        "aside",
        "article",
        "blockquote",
        "code",
        "div",
        "figure",
        "h1",
        "h2",
        "h3",
        "img",
        "li",
        "main",
        "nav",
        "ol",
        "p",
        "pre",
        "section",
        "span",
        "summary",
        "strong",
        "table",
        "tbody",
        "td",
        "th",
        "thead",
        "tr",
        "ul",
        "time",
    )
    for tag in tags:
        markup = re.sub(
            rf"<{tag}(?![^>]*data-astro-cid-)(?=[\s>])",
            f'<{tag} data-astro-cid-{scope_id}',
            markup,
        )
    return markup


def markdown_to_html(body: str, title: str) -> tuple[str, list[tuple[str, str]]]:
    lines = body.replace("\r\n", "\n").splitlines()
    output: list[str] = []
    headings: list[tuple[str, str]] = []
    i = 0
    first_h1_skipped = False

    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("```"):
            language = line[3:].strip()
            code_lines: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            language_attr = f' class="language-{html.escape(language)}"' if language else ""
            output.append(
                f"<pre><code{language_attr}>{html.escape(chr(10).join(code_lines), quote=False)}</code></pre>"
            )
            continue
        heading = re.match(r"^(#{1,3})\s+(.+?)\s*#*\s*$", line)
        if heading:
            level, text = len(heading.group(1)), heading.group(2)
            if level == 1 and not first_h1_skipped and text == title:
                first_h1_skipped = True
                i += 1
                continue
            if level == 1:
                raise ValueError(f"unexpected second H1 in {title}")
            anchor = slugify(text)
            headings.append((f"h{level}", text))
            output.append(f'<h{level} id="{anchor}">{inline(text)}</h{level}>')
            i += 1
            continue
        if line.strip() == "---":
            output.append("<hr>")
            i += 1
            continue
        if line.startswith(">"):
            quote_lines: list[str] = []
            while i < len(lines) and (lines[i].startswith(">") or not lines[i].strip()):
                if lines[i].startswith(">"):
                    quote_lines.append(lines[i][1:].lstrip())
                else:
                    quote_lines.append("")
                i += 1
            quote = "\n".join(quote_lines).strip()
            output.append(
                scoped(
                    '<aside class="dr-callout dr-callout--warning" '
                    'aria-label="Important note" role="note">'
                    '<span class="dr-callout-icon" aria-hidden="true">⚠</span>'
                    '<div class="dr-callout-body">'
                    f'<div class="dr-callout-content"><p>{inline(quote)}</p></div>'
                    "</div></aside>",
                    "x2ep4vyf",
                )
            )
            continue
        if (
            line.strip().startswith("|")
            and i + 1 < len(lines)
            and re.match(r"^\s*\|?\s*:?-{3,}", lines[i + 1])
        ):
            header = cells(line)
            i += 2
            rows: list[list[str]] = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(cells(lines[i]))
                i += 1
            table = [
                '<div class="dr-table-wrap"><table class="dr-table"><thead><tr>'
            ]
            table.extend(f"<th scope=\"col\">{inline(cell)}</th>" for cell in header)
            table.append("</tr></thead><tbody>")
            for row in rows:
                table.append("<tr>")
                table.extend(f'<td class="dr-cell-text">{inline(cell)}</td>' for cell in row)
                table.append("</tr>")
            table.append("</tbody></table></div>")
            output.append(scoped("".join(table), "yc4hcm2d"))
            continue
        list_match = re.match(r"^\s*([-*])\s+(.+)$", line)
        ordered_match = re.match(r"^\s*\d+[.)]\s+(.+)$", line)
        if list_match or ordered_match:
            ordered = bool(ordered_match)
            items: list[str] = []
            while i < len(lines):
                match = (
                    re.match(r"^\s*\d+[.)]\s+(.+)$", lines[i])
                    if ordered
                    else re.match(r"^\s*[-*]\s+(.+)$", lines[i])
                )
                if not match:
                    break
                items.append(f"<li>{inline(match.group(1))}</li>")
                i += 1
            tag = "ol" if ordered else "ul"
            output.append(f"<{tag}>" + "".join(items) + f"</{tag}>")
            continue

        paragraph = [line.strip()]
        i += 1
        while i < len(lines):
            candidate = lines[i]
            if (
                not candidate.strip()
                or candidate.startswith(("```", ">", "#"))
                or re.match(r"^\s*[-*]\s+", candidate)
                or re.match(r"^\s*\d+[.)]\s+", candidate)
                or candidate.strip().startswith("|")
                or candidate.strip() == "---"
            ):
                break
            paragraph.append(candidate.strip())
            i += 1
        output.append(f"<p>{inline(' '.join(paragraph))}</p>")

    return scoped("\n".join(output), "bvzihdzo"), headings


def jsonld_scripts(article: dict, canonical: str, author_url: str) -> str:
    image = "https://www.droidrooter.com/assets/og-default.webp"
    article_schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": article["title"],
        "description": article["meta_description"],
        "image": image,
        "datePublished": f'{article["datePublished"]}T00:00:00.000Z',
        "dateModified": f'{article["dateModified"]}T00:00:00.000Z',
        "author": {
            "@type": "Person",
            "name": article["author"],
            "url": f"https://www.droidrooter.com{author_url}",
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
    }
    breadcrumb_names = ["Home", "Blog", article["category"].title(), article["title"]]
    breadcrumb_paths = [
        "/",
        "/blog",
        f'/blog/category/{article["category"]}',
        f'/{article["slug"]}' if article["slug"].startswith("blog/") else f'/blog/{article["slug"]}',
    ]
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index,
                "name": name,
                "item": f"https://www.droidrooter.com{path}",
            }
            for index, (name, path) in enumerate(zip(breadcrumb_names, breadcrumb_paths), 1)
        ],
    }
    return "\n".join(
        f'<script type="application/ld+json">{json.dumps(data, separators=(",", ":"))}</script>'
        for data in (article_schema, breadcrumb)
    )


def replace_meta(prefix: str, article: dict, canonical: str) -> str:
    def replace(pattern: str, value: str, text: str, count: int = 1) -> str:
        return re.sub(pattern, value, text, count=count, flags=re.DOTALL)

    title = html.escape(article["meta_title"], quote=False)
    description = html.escape(article["meta_description"], quote=True)
    prefix = replace(r"<title>.*?</title>", f"<title>{title}</title>", prefix)
    prefix = replace(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{description}">',
        prefix,
    )
    prefix = replace(
        r'<link rel="canonical" href="[^"]*">',
        f'<link rel="canonical" href="{canonical}">',
        prefix,
    )
    for property_name, value in (
        ("og:title", title),
        ("og:description", description),
        ("og:url", canonical),
        ("og:image", "https://www.droidrooter.com/assets/og-default.webp"),
        ("article:published_time", f'{article["datePublished"]}T00:00:00.000Z'),
        ("article:modified_time", f'{article["dateModified"]}T00:00:00.000Z'),
    ):
        prefix = replace(
            rf'<meta property="{re.escape(property_name)}"[^>]*>',
            f'<meta property="{property_name}" content="{html.escape(value, quote=True)}">',
            prefix,
        )
    prefix = replace(
        r'<meta name="twitter:title"[^>]*>',
        f'<meta name="twitter:title" content="{title}">',
        prefix,
    )
    prefix = replace(
        r'<meta name="twitter:description"[^>]*>',
        f'<meta name="twitter:description" content="{description}">',
        prefix,
    )
    prefix = replace(
        r'<meta name="twitter:image"[^>]*>',
        '<meta name="twitter:image" content="https://www.droidrooter.com/assets/og-default.webp">',
        prefix,
    )
    prefix = re.sub(
        r'<script[^>]*type="application/ld\+json"[^>]*>.*?</script>',
        "",
        prefix,
        flags=re.DOTALL,
    )
    return prefix


def toc_html(headings: list[tuple[str, str]], mobile: bool = False) -> str:
    cid = "ymbpksfa"
    classes = "dr-toc dr-toc--mobile" if mobile else "dr-toc dr-toc--desktop"
    inner = "" if mobile else '<p class="dr-toc-heading">On this page</p>'
    if mobile:
        inner = "<summary>Table of Contents</summary>"
    inner += '<ol class="dr-toc-list">'
    for level, text in headings:
        cls = "dr-toc-d2" if level == "h2" else "dr-toc-d3"
        anchor = slugify(text)
        inner += (
            f'<li class="{cls}"><a data-toc-link="{anchor}" '
            f'href="#{anchor}">{html.escape(text)}</a></li>'
        )
    inner += "</ol>"
    markup = f'<details class="{classes}" data-astro-cid-{cid}>{inner}</details>' if mobile else (
        f'<aside class="{classes}" aria-label="Table of contents" data-astro-cid-{cid}>{inner}</aside>'
    )
    return scoped(markup, cid)


def author_bio(author: str) -> str:
    record = AUTHORS[author]
    bio = record["bio"]
    author_url = f'/team/{record["slug"]}'
    stats = ""
    if author == "Saad Bin Abdul Hai":
        stats = (
            '<p class="dr-bio-stats"><span><strong>3+</strong> years experience</span>'
            '<span class="dr-bio-sep" aria-hidden="true">|</span>'
            '<span><strong>160+</strong> devices serviced</span></p>'
        )
    return scoped(
        f'''<aside class="dr-bio" aria-label="About the author">
 <div class="dr-bio-avatar" aria-hidden="true"><svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg"><rect width="80" height="80" rx="40" fill="#0E141A"></rect><circle cx="40" cy="32" r="14" fill="#00FF88"></circle><path d="M16 72c0-13 11-22 24-22s24 9 24 22" fill="#00FF88"></path></svg></div>
 <div class="dr-bio-body">
  <p class="dr-bio-eyebrow">About the Author</p>
  <h3 class="dr-bio-name">{html.escape(author)}</h3>
  <p class="dr-bio-title">{html.escape(record["role"])}</p>
  <p class="dr-bio-text">{html.escape(bio)}</p>
  {stats}
  <a class="dr-bio-link" href="{author_url}">View all articles by {html.escape(author.split()[0])} &rarr;</a>
 </div>
</aside>''',
        "a2z3okge",
    )


def more_guides(article: dict, articles: list[dict]) -> str:
    articles_by_slug = {item["slug"]: item for item in articles}
    related = [articles_by_slug[slug] for slug in RELATED_GUIDES[article["slug"]]]
    return scoped(
        '<section class="dr-related" aria-labelledby="dr-related-heading">'
        '<h2 id="dr-related-heading">More Android Guides</h2>'
        '<div class="dr-related-grid">'
        + "".join(card(item) for item in related)
        + "</div></section>",
        "xj4yj4fu",
    )


def render_article(article: dict, articles: list[dict]) -> str:
    template = ARTICLE_TEMPLATE.read_text(encoding="utf-8")
    prefix, tail = template.split("<main>", 1)[0], template.split("</main>", 1)[1]
    canonical = f'https://www.droidrooter.com/blog/{article["slug"]}'
    prefix = replace_meta(prefix, article, canonical)
    prefix = prefix.replace("</head>", jsonld_scripts(article, canonical, f'/team/{AUTHORS[article["author"]]["slug"]}') + "</head>")
    body, headings = markdown_to_html(article["body"], article["title"])
    category = article["category"].title()
    breadcrumb = (
        '<nav class="dr-crumbs" aria-label="Breadcrumb"><ol>'
        '<li><a href="/">Home</a><span class="dr-crumb-sep" aria-hidden="true">›</span></li>'
        '<li><a href="/blog">Blog</a><span class="dr-crumb-sep" aria-hidden="true">›</span></li>'
        f'<li><a href="/blog/category/{article["category"]}">{category}</a><span class="dr-crumb-sep" aria-hidden="true">›</span></li>'
        f'<li><span aria-current="page">{html.escape(article["title"])}</span></li>'
        "</ol></nav>"
    )
    read_time = max(1, round(len(re.sub(r"<[^>]+>", " ", body).split()) / 200))
    hero_image = HERO_IMAGES.get(article["slug"], "bootloader-recovery.webp")
    hero = scoped(
        f'''<header class="dr-bhero">
 {breadcrumb}
 <div class="dr-bhero-badges"><span class="dr-bhero-badge dr-bhero-badge--cat">{category}</span><span class="dr-bhero-badge dr-bhero-badge--diff">{html.escape(article["difficulty"])}</span><span class="dr-bhero-badge dr-bhero-badge--time">{read_time} min read</span></div>
 <h1 class="dr-bhero-title">{html.escape(article["title"])}</h1>
 <p class="dr-bhero-desc">{html.escape(article["excerpt"])}</p>
 <p class="dr-bhero-byline">By <a class="dr-bhero-author" href="/team/{AUTHORS[article["author"]]["slug"]}"><strong>{html.escape(article["author"])}</strong></a> <span class="dr-bhero-sep">|</span> Published <time datetime="{article["datePublished"]}T00:00:00.000Z">{human_date(article["datePublished"])}</time></p>
 <figure class="dr-bhero-figure"><img src="/assets/blog/{hero_image}" alt="{html.escape(article["image_alt"], quote=True)}" width="1200" height="630" loading="eager" fetchpriority="high" decoding="async"></figure>
</header>''',
        "k2pn77o4",
    )
    main = f'''<main><article class="dr-article" data-astro-cid-bvzihdzo><div class="dr-article-inner" data-astro-cid-bvzihdzo><div class="dr-article-main" data-astro-cid-bvzihdzo>{hero}{toc_html(headings, mobile=True)}<div class="dr-prose prose prose-invert" data-astro-cid-bvzihdzo>{body}</div>{author_bio(article["author"])}{more_guides(article, articles)}</div><aside class="dr-article-side" aria-label="Article navigation" data-astro-cid-bvzihdzo>{toc_html(headings)}</aside></div></article></main>'''
    return prefix + main + tail


def human_date(value: str) -> str:
    months = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
    return f"{months[int(value[5:7]) - 1]} {int(value[8:10])}, {value[:4]}"


def render_author(name: str) -> str:
    record = AUTHORS[name]
    template = AUTHOR_TEMPLATE.read_text(encoding="utf-8")
    prefix, tail = template.split("<main>", 1)[0], template.split("</main>", 1)[1]
    canonical = f'https://www.droidrooter.com/team/{record["slug"]}'
    title = f'{name} — {record["role"]}, Droid Rooter'
    description = record["bio"]
    prefix = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)}</title>", prefix, count=1, flags=re.DOTALL)
    prefix = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(description, quote=True)}">', prefix, count=1)
    prefix = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{canonical}">', prefix, count=1)
    prefix = re.sub(r'<script[^>]*type="application/ld\+json"[^>]*>.*?</script>', "", prefix, flags=re.DOTALL)
    person = {
        "@context": "https://schema.org",
        "@type": "Person",
        "@id": canonical + "#person",
        "name": name,
        "jobTitle": record["role"],
        "description": description,
        "url": canonical,
        "worksFor": {"@type": "Organization", "name": "Droid Rooter"},
    }
    crumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.droidrooter.com"},
            {"@type": "ListItem", "position": 2, "name": "Team", "item": "https://www.droidrooter.com/team"},
            {"@type": "ListItem", "position": 3, "name": name, "item": canonical},
        ],
    }
    prefix = prefix.replace(
        "</head>",
        "\n".join(
            f'<script type="application/ld+json">{json.dumps(data, separators=(",", ":"))}</script>'
            for data in (crumbs, person)
        ) + "</head>",
    )
    initials = "".join(part[0] for part in name.replace(".", "").split())
    fields = [
        ("Based in", record.get("location", "Remote")),
        ("Coverage", record.get("coverage", "")),
        ("Hours", record.get("hours", "Worldwide remote support")),
    ]
    meta = "".join(f"<li><span>{label}</span><strong>{html.escape(value)}</strong></li>" for label, value in fields)
    posts = []
    for source_prefix, _date in ARTICLE_SPECS:
        article = read_article(source_prefix)
        if article["author"] == name:
            posts.append(
                f'<li class="dr-au-post"><a class="dr-au-post-link" href="/blog/{article["slug"]}"><span class="dr-au-post-date">{human_date(article["datePublished"])}</span><span class="dr-au-post-title">{html.escape(article["title"])}</span></a></li>'
            )
    main = scoped(
        f'''<main><section class="dr-au-hero"><div class="dr-au-inner dr-au-hero-grid"><div class="dr-au-hero-copy"><p class="dr-au-eyebrow mono">// {html.escape(record["role"].lower())}</p><h1 class="dr-au-h1">{html.escape(title)}</h1><p class="dr-au-lead">{html.escape(record["bio"])}</p><div class="dr-au-actions"><a class="btn-primary" href="https://wa.me/8801748788939" rel="noopener" target="_blank">Message {html.escape(name.split()[0])}</a><a class="btn-secondary" href="https://t.me/DroidRooter" rel="noopener" target="_blank">Open Telegram</a></div></div><aside class="dr-au-card" aria-label="{html.escape(name)} profile card"><div class="dr-au-photo dr-au-photo-fallback" aria-hidden="true"><span>{initials}</span></div><p class="dr-au-card-name">{html.escape(name)}</p><p class="dr-au-card-role mono">{html.escape(record["role"])}</p><ul class="dr-au-card-meta">{meta}</ul></aside></div></section><section class="dr-au-expertise"><div class="dr-au-inner"><p class="dr-au-eyebrow mono">// coverage</p><h2 class="dr-au-h2">Areas of Hands-On Expertise</h2><p class="dr-au-text">{html.escape(record.get("short_bio", record["bio"]))}</p></div></section><section class="dr-au-posts"><div class="dr-au-inner"><p class="dr-au-eyebrow mono">// articles by {html.escape(name.split()[0].lower())}</p><h2 class="dr-au-h2">Guides Written by {html.escape(name.split()[0])}</h2><ul class="dr-au-post-list">{"".join(posts)}</ul></div></section></main>''',
        "pevjtjxq",
    )
    return prefix + main + tail


def card(article: dict) -> str:
    category = article["category"].title()
    markup = f'''<a href="/blog/{article["slug"]}" class="dr-bcard" aria-label="{html.escape(article["title"], quote=True)}"><div class="dr-bcard-img"><img src="/assets/blog/{HERO_IMAGES.get(article["slug"], "bootloader-recovery.webp")}" alt="{html.escape(article["image_alt"], quote=True)}" width="800" height="450" loading="lazy" decoding="async"></div><div class="dr-bcard-body"><div class="dr-bcard-badges"><span class="dr-bcard-badge dr-bcard-badge--cat">{category}</span><span class="dr-bcard-badge dr-bcard-badge--diff">{html.escape(article["difficulty"])}</span><span class="dr-bcard-badge dr-bcard-badge--time">{max(1, round(len(article["body"].split()) / 200))} min read</span></div><h3 class="dr-bcard-title">{html.escape(article["title"])}</h3><p class="dr-bcard-excerpt">{html.escape(article["excerpt"])}</p><div class="dr-bcard-meta"><span class="dr-bcard-avatar" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"></circle><path d="M4 21c0-4 4-7 8-7s8 3 8 7"></path></svg></span><span class="dr-bcard-author">{html.escape(article["author"])}</span><span class="dr-bcard-dot" aria-hidden="true">&middot;</span><time datetime="{article["datePublished"]}T00:00:00.000Z">{human_date(article["datePublished"])}</time></div><span class="dr-bcard-cta">Read More &rarr;</span></div></a>'''
    return scoped(markup, "fkyubztb")


def add_cards(path: Path, articles: list[dict]) -> None:
    text = path.read_text(encoding="utf-8")
    for article in articles:
        text = re.sub(
            rf'<a(?=[^>]*href="/blog/{re.escape(article["slug"])}")'
            rf'(?=[^>]*class="dr-bcard")[^>]*>.*?</a>',
            "",
            text,
            flags=re.DOTALL,
        )
    marker = re.search(r'<a href="/blog/[^"]+" class="dr-bcard"', text)
    if not marker:
        marker = re.search(
            r'<a(?=[^>]*href="/blog/[^"]+")(?=[^>]*class="dr-bcard")',
            text,
        )
    if not marker:
        raise ValueError(f"no blog card insertion point in {path}")
    additions = "".join(card(article) for article in articles)
    text = text[: marker.start()] + additions + text[marker.start() :]
    path.write_text(text, encoding="utf-8")


def remove_alex_success_rate() -> list[str]:
    changed: list[str] = []
    pattern = re.compile(
        r'\s*<span class="dr-bio-sep"[^>]*>\|</span>\s*'
        r'<span[^>]*><strong[^>]*>95%</strong>\s*success rate</span>'
    )
    for path in ROOT.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        updated, count = pattern.subn("", text)
        if count:
            path.write_text(updated, encoding="utf-8")
            changed.append(str(path.relative_to(ROOT)))
    return changed


def add_reciprocal_links() -> None:
    bootloop = ROOT / "blog/android-boot-loop-fix/index.html"
    text = bootloop.read_text(encoding="utf-8")
    if "/blog/android-bootloop-fix-without-losing-data" not in text:
        addition = (
            '<p class="dr-svp-text">Related reading: '
            '<a href="/blog/android-bootloop-fix-without-losing-data">Fix a bootloop without losing your data</a> · '
            '<a href="/blog/phone-stuck-on-boot-screen">What each boot-screen symptom means</a></p>'
        )
        related_start = text.find('<section class="dr-related"')
        related_end = text.find("</section>", related_start)
        if related_start < 0 or related_end < 0:
            raise ValueError("could not find Related Reading block on boot-loop article")
        text = text[:related_end] + addition + text[related_end:]
        bootloop.write_text(text, encoding="utf-8")

    firmware = ROOT / "services/firmware/index.html"
    text = firmware.read_text(encoding="utf-8")
    if "/blog/soft-brick-vs-hard-brick" not in text:
        addition = (
            '<p class="dr-svp-text">Related reading: '
            '<a href="/blog/soft-brick-vs-hard-brick">Soft brick vs hard brick: how to tell</a> · '
            '<a href="/blog/android-bootloop-fix-without-losing-data">Fix a bootloop without losing your data</a></p>'
        )
        text = text.replace("</main>", addition + "</main>", 1)
        firmware.write_text(text, encoding="utf-8")


def add_author_links_to_about() -> None:
    path = ROOT / "about/index.html"
    text = path.read_text(encoding="utf-8")
    if "/team/imran-r" not in text:
        match = re.search(r'<a\b[^>]*href="/team/saad-nahid"[^>]*>', text)
        if not match:
            raise ValueError("could not find the existing team link on about page")
        index = match.start()
        close = text.find("</a>", index)
        insert_at = close + len("</a>")
        text = (
            text[:insert_at]
            + ' <a href="/team/imran-r" class="btn-secondary">Meet Imran R.</a>'
            + ' <a href="/team/ontor-zubair" class="btn-secondary">Meet Ontor Zubair</a>'
            + text[insert_at:]
        )
        path.write_text(text, encoding="utf-8")


def update_sitemap(articles: list[dict]) -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    additions = []
    for article in articles:
        url = f'https://www.droidrooter.com/blog/{article["slug"]}'
        entry = f'<url><loc>{url}</loc><lastmod>{article["dateModified"]}</lastmod></url>'
        if f"<loc>{url}</loc>" not in text:
            additions.append(entry)
    for name in ("Imran R.", "Ontor Zubair"):
        url = f'https://www.droidrooter.com/team/{AUTHORS[name]["slug"]}'
        if f"<loc>{url}</loc>" not in text:
            additions.append(f"<url><loc>{url}</loc><lastmod>2026-08-28</lastmod></url>")
    if additions:
        text = text.replace("</urlset>", "".join(additions) + "</urlset>")
        path.write_text(text, encoding="utf-8")


def main() -> None:
    articles = [read_article(prefix) for prefix, _date in ARTICLE_SPECS]
    for article in articles:
        destination = ROOT / "blog" / article["slug"] / "index.html"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(render_article(article, articles), encoding="utf-8")

    for name in ("Imran R.", "Ontor Zubair"):
        destination = ROOT / "team" / AUTHORS[name]["slug"] / "index.html"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(render_author(name), encoding="utf-8")

    # Newest first, matching the current blog index convention.
    index_articles = sorted(articles, key=lambda article: article["datePublished"], reverse=True)
    add_cards(ROOT / "blog/index.html", index_articles)
    add_cards(
        ROOT / "blog/category/troubleshooting/index.html",
        [article for article in index_articles if article["category"] == "troubleshooting"],
    )
    add_cards(
        ROOT / "blog/category/guide/index.html",
        [article for article in index_articles if article["category"] == "guide"],
    )
    remove_alex_success_rate()
    add_reciprocal_links()
    add_author_links_to_about()
    update_sitemap(articles)
    print("published:", ", ".join(article["slug"] for article in articles))
    print("author archives: team/imran-r, team/ontor-zubair")


if __name__ == "__main__":
    main()