#!/usr/bin/env python3
"""apple-hig-live: read Apple's Human Interface Guidelines from Apple's own JSON endpoints.

Apple's design pages are rendered with JavaScript, so a normal web fetch returns an empty
shell. The same content is served as DocC JSON. This tool downloads it and prints compact,
citable Markdown (raw JSON is ~10x larger and full of image/reference noise).

Commands
  index   [--group G] [--refresh] [--json]     list every HIG page: slug, title, abstract
  search  <terms...>                            find pages by keyword
  page    <slug...> [--platform ios,macos] [--section TEXT] [--outline] [--full] [--raw]

Examples
  python3 hig.py search "tab bar navigation"
  python3 hig.py page layout typography color --platform ios
  python3 hig.py page layout --section "Size classes"

Stdlib only, Python 3.8+. Environment: HIG_BASE (endpoint override), HIG_CACHE_DIR.
Content is fetched at runtime from Apple and cached locally; it is never redistributed.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import difflib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE = os.environ.get(
    "HIG_BASE",
    "https://developer.apple.com/tutorials/data/design/human-interface-guidelines",
).rstrip("/")
SITE = "https://developer.apple.com/design/human-interface-guidelines"
CACHE = Path(os.environ.get("HIG_CACHE_DIR", str(Path.home() / ".cache" / "apple-hig-live")))
PAGE_TTL = 24 * 3600
INDEX_TTL = 7 * 24 * 3600
UA = "Mozilla/5.0 (compatible; apple-hig-live/1.0)"
PLATFORMS = ("ios", "ipados", "macos", "tvos", "visionos", "watchos")
SLUG_OK = re.compile(r"^[a-z0-9][a-z0-9-]*$")
SLUG_IN_ID = re.compile(r"/(?:design|documentation|tutorials)/human-interface-guidelines/([^#/]+)", re.I)


class HigError(Exception):
    pass


class NotFound(HigError):
    pass


def resolve_slug(s: str | None) -> str:
    """Normalize any slug, URL, or .json endpoint path to a pure HIG page slug."""
    if not s:
        return ""
    s = s.strip()
    if "#" in s:
        s = s.split("#", 1)[0]
    m = SLUG_IN_ID.search(s)
    if m:
        s = m.group(1)
    s = s.strip().rstrip("/")
    if s.endswith(".json"):
        s = s[:-5]
    if "/" in s:
        s = s.rsplit("/", 1)[-1]
    return s.strip().lower()


# --------------------------------------------------------------------------- network

def _get(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise NotFound(url)
        raise HigError(f"HTTP {e.code} for {url}")
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise HigError(f"network error for {url}: {e}")


def fetch(slug=None, cache=True) -> dict:
    """Fetch the table of contents (slug=None) or one page as parsed JSON."""
    if slug is not None:
        slug = resolve_slug(slug)
        if not SLUG_OK.match(slug):
            raise NotFound(slug)
    key = "_toc" if slug is None else slug
    f = CACHE / "pages" / f"{key}.json"
    if cache and f.exists() and time.time() - f.stat().st_mtime < PAGE_TTL:
        try:
            return json.loads(f.read_text("utf-8"))
        except ValueError:
            pass
    url = f"{BASE}.json" if slug is None else f"{BASE}/{slug}.json"
    try:
        raw = _get(url)
    except HigError as e:
        if f.exists():
            try:
                print(f"warning: network failed ({e}); serving cached copy for {key}", file=sys.stderr)
                return json.loads(f.read_text("utf-8"))
            except ValueError:
                pass
        raise
    try:
        doc = json.loads(raw)
    except ValueError:
        raise NotFound(url)  # an HTML error page instead of JSON
    try:
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(raw, "utf-8")
    except OSError:
        pass
    return doc


# --------------------------------------------------------------------------- helpers

def plain(nodes) -> str:
    out = []
    for n in nodes or []:
        if isinstance(n, dict):
            if "text" in n:
                out.append(n["text"])
            elif "inlineContent" in n:
                out.append(plain(n["inlineContent"]))
            elif "code" in n:
                out.append(n["code"])
    return "".join(out).replace("\n", " ").strip()


def slug_of(identifier: str):
    m = SLUG_IN_ID.search(identifier or "")
    if not m:
        return None
    val = m.group(1).lower()
    if val.endswith(".json"):
        val = val[:-5]
    return val


def trim(s: str, n: int) -> str:
    s = (s or "").strip()
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def children(doc: dict):
    refs = doc.get("references", {})
    out = []
    for sec in doc.get("topicSections", []):
        for ident in sec.get("identifiers", []):
            ref, slug = refs.get(ident), slug_of(ident)
            if ref and slug:
                out.append((slug, ref))
    return out


# --------------------------------------------------------------------------- index

def build_index(refresh=False) -> dict:
    f = CACHE / "index.json"
    if not refresh and f.exists() and time.time() - f.stat().st_mtime < INDEX_TTL:
        try:
            return json.loads(f.read_text("utf-8"))
        except ValueError:
            pass
    toc = fetch(None, cache=not refresh)
    entries, failed = {}, []
    frontier = [(s, r, None, s) for s, r in children(toc)]  # slug, ref, parent, top group
    while frontier:
        collections = []
        for s, r, parent, group in frontier:
            if s in entries:
                continue
            is_coll = r.get("role") == "collectionGroup"
            entries[s] = {
                "title": r.get("title", s),
                "abstract": plain(r.get("abstract")),
                "group": group,
                "parent": parent,
                "collection": is_coll,
            }
            if is_coll:
                collections.append(s)

        def get(s):
            try:
                return s, fetch(s, cache=not refresh)
            except HigError as e:
                failed.append(f"{s}: {e}")
                return s, None

        frontier = []
        with cf.ThreadPoolExecutor(max_workers=8) as ex:
            for s, doc in ex.map(get, collections):
                if doc:
                    for cs, cr in children(doc):
                        frontier.append((cs, cr, s, entries[s]["group"]))
    idx = {"generated": int(time.time()), "entries": entries, "failed": failed}
    try:
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps(idx, ensure_ascii=False), "utf-8")
    except OSError:
        pass
    return idx


def cmd_index(a) -> int:
    idx = build_index(a.refresh)
    E = idx["entries"]
    if idx.get("failed"):
        print("warning: some collections failed: " + "; ".join(idx["failed"][:5]), file=sys.stderr)
    if a.json:
        print(json.dumps(E, indent=1, ensure_ascii=False))
        return 0
    g = a.group.lower() if a.group else None
    by_parent: dict = {}
    for s, e in E.items():
        if g and g not in (e["group"], e["parent"] or "", s):
            continue
        by_parent.setdefault(e["parent"] or "(top)", []).append((s, e))
    print(f"# HIG index ({len(E)} pages). Page URL: {SITE}/<slug>")
    for parent in sorted(by_parent):
        print(f"\n## {parent}")
        for s, e in sorted(by_parent[parent]):
            print(f"- {s} -- {e['title']}: {trim(e['abstract'], 100)}")
    return 0


def cmd_search(a) -> int:
    E = build_index(False)["entries"]
    terms = [t.lower() for t in " ".join(a.terms).split() if t.strip()]
    scored = []
    for s, e in E.items():
        title, abstract = e["title"].lower(), e["abstract"].lower()
        score = 0
        for t in terms:
            if t == s:
                score += 100
            if t in title:
                score += 10
            if t in s:
                score += 8
            if t in abstract:
                score += 3
        if score:
            scored.append((score, s, e))
    scored.sort(key=lambda x: (-x[0], x[1]))
    if not scored:
        print("No match. Try fewer or different words, or run: hig.py index")
        return 1
    for score, s, e in scored[: a.limit]:
        print(f"- {s} -- {e['title']} [{e['group']}/{e['parent'] or '-'}]: {trim(e['abstract'], 110)}")
    return 0


# --------------------------------------------------------------------------- rendering

class Renderer:
    def __init__(self, doc: dict):
        self.refs = doc.get("references", {})

    # inline -----------------------------------------------------------------
    def inline(self, nodes) -> str:
        out = []
        for n in nodes or []:
            t = n.get("type")
            if t == "text":
                out.append(n.get("text", ""))
            elif t == "codeVoice":
                out.append(f"`{n.get('code', '')}`")
            elif t in ("strong", "inlineHead"):
                out.append("**" + self.inline(n.get("inlineContent")).strip() + "**")
            elif t in ("emphasis", "newTerm"):
                out.append("*" + self.inline(n.get("inlineContent")).strip() + "*")
            elif t == "reference":
                out.append(self.ref(n))
            elif t == "image":
                continue
            elif "inlineContent" in n:
                out.append(self.inline(n["inlineContent"]))
            elif "text" in n:
                out.append(n["text"])
        return "".join(out)

    def ref(self, n: dict) -> str:
        ident = n.get("identifier", "")
        r = self.refs.get(ident, {})
        title = n.get("overridingTitle") or r.get("title") or ident
        slug = slug_of(ident)
        if ident.startswith("doc://com.apple.HIG") and slug:
            frag = "#" + ident.split("#", 1)[1] if "#" in ident else ""
            return f"{title} (-> {slug}{frag})"
        url = r.get("url", "") or (ident if ident.startswith("http") else "")
        if url.startswith("/"):
            url = "https://developer.apple.com" + url
        if r.get("kind") == "symbol":
            return f"`{title}`"
        return f"[{title}]({url})" if url else title

    # blocks -----------------------------------------------------------------
    def blocks(self, blocks) -> str:
        parts = []
        for b in blocks or []:
            s = self.block(b)
            if s:
                parts.append(s)
        return "\n\n".join(parts)

    def block(self, b: dict) -> str:
        t = b.get("type")
        if t == "heading":
            anchor = b.get("anchor")
            tag = f"  {{#{anchor}}}" if anchor else ""
            return f"{'#' * min(b.get('level', 2), 6)} {b.get('text', '')}{tag}"
        if t in ("paragraph", "small"):
            return self.inline(b.get("inlineContent")).strip()
        if t in ("unorderedList", "orderedList"):
            lines = []
            for i, item in enumerate(b.get("items", []), 1):
                body = self.blocks(item.get("content")).split("\n")
                mark = "- " if t == "unorderedList" else f"{i}. "
                lines.append(mark + body[0])
                lines += ["  " + ln for ln in body[1:]]
            return "\n".join(lines)
        if t == "table":
            return self.table(b)
        if t == "aside":
            label = b.get("name") or b.get("style", "note").title()
            body = self.blocks(b.get("content")).replace("\n", "\n> ")
            return f"> **{label}:** {body}"
        if t == "row":
            return self.blocks([blk for col in b.get("columns", []) for blk in col.get("content", [])])
        if t == "tabNavigator":
            return "\n\n".join(f"**{tab.get('title', '')}**\n\n{self.blocks(tab.get('content'))}"
                               for tab in b.get("tabs", []))
        if t == "links":
            lines = []
            for ident in b.get("items", []):
                r = self.refs.get(ident, {})
                s = slug_of(ident)
                if s:
                    lines.append(f"- {r.get('title', s)} (-> {s})")
                elif r.get("url"):
                    u = r["url"] if r["url"].startswith("http") else "https://developer.apple.com" + r["url"]
                    lines.append(f"- [{r.get('title', u)}]({u})")
            return "\n".join(lines)
        if t == "codeListing":
            return "```" + (b.get("syntax") or "") + "\n" + "\n".join(b.get("code", [])) + "\n```"
        if t == "thematicBreak":
            return "---"
        return ""  # images, video, etc.

    def table(self, b: dict) -> str:
        rows = []
        for row in b.get("rows", []):
            rows.append([self.blocks(cell).replace("\n", " ").replace("|", "/") for cell in row])
        if not rows:
            return ""
        width = max(len(r) for r in rows)
        rows = [r + [""] * (width - len(r)) for r in rows]
        out = ["| " + " | ".join(rows[0]) + " |", "|" + "---|" * width]
        out += ["| " + " | ".join(r) + " |" for r in rows[1:]]
        return "\n".join(out)


def select_blocks(blocks, platforms, full):
    """Drop Change log / Videos and platform sections the caller didn't ask for."""
    out, drop, in_plat = [], None, False
    for b in blocks:
        if b.get("type") == "heading":
            lvl, low = b.get("level", 2), b.get("text", "").lower()
            if drop is not None and lvl <= drop:
                drop = None
            if lvl == 2:
                in_plat = low == "platform considerations"
            if drop is None:
                if not full and ((lvl == 2 and low == "change log") or (lvl == 4 and low == "videos")):
                    drop = lvl
                elif in_plat and lvl == 3 and platforms:
                    if not any(re.search(rf"\b{p}\b", low) for p in platforms):
                        drop = 3
        if drop is None:
            out.append(b)
    return out


def pick_section(blocks, query):
    q = query.strip().lstrip("#").lower()
    q_norm = q.replace(" ", "-").replace("_", "-")
    out, keep, lvl = [], False, 0
    for b in blocks:
        if b.get("type") == "heading":
            b_text = b.get("text", "").lower()
            b_anchor = (b.get("anchor") or "").lower()
            b_norm = b_anchor.replace("_", "-")
            b_text_norm = b_text.replace(" ", "-").replace("_", "-")
            if keep and b.get("level", 2) <= lvl:
                keep = False
            if not keep and (
                q in b_text
                or q_norm == b_norm
                or q_norm == b_text_norm
                or (b_norm and b_norm.replace("-", " ") in q)
            ):
                keep, lvl = True, b.get("level", 2)
        if keep:
            out.append(b)
    return out


def render_page(doc: dict, slug: str, a) -> str:
    meta = doc.get("metadata", {})
    custom = meta.get("customMetadata", {})
    r = Renderer(doc)
    blocks = [b for sec in doc.get("primaryContentSections", [])
              if sec.get("kind") == "content" for b in sec.get("content", [])]
    platforms = [p.strip().lower() for p in (a.platform or "").split(",") if p.strip() and p.strip() != "all"]
    for p in platforms:
        if p not in PLATFORMS:
            raise HigError(f"unknown platform '{p}' (use: {', '.join(PLATFORMS)})")
    blocks = select_blocks(blocks, platforms, a.full)

    head = [f"# {meta.get('title', slug)}", f"Source: {SITE}/{slug}"]
    info = []
    if custom.get("supported-platforms"):
        info.append("Platforms: " + custom["supported-platforms"])
    if custom.get("alert-date"):
        info.append("Last updated: " + custom["alert-date"])
    if info:
        head.append(" | ".join(info))
    if doc.get("abstract"):
        head.append("> " + plain(doc["abstract"]))

    if a.outline:
        lines = [f"{'  ' * (b['level'] - 2)}- {b['text']}  #{b.get('anchor', '')}"
                 for b in blocks if b.get("type") == "heading" and b.get("level", 2) <= 4]
        return "\n".join(head + [""] + lines)

    if a.section:
        blocks = pick_section(blocks, a.section)
        if not blocks:
            raise HigError(f"section '{a.section}' not found in {slug} (try --outline)")

    body = r.blocks(blocks)
    kids = children(doc)
    tail = ""
    if kids:
        tail = "\n\n## In this section\n" + "\n".join(
            f"- {s} -- {c.get('title', s)}: {trim(plain(c.get('abstract')), 100)}" for s, c in kids)
    return "\n".join(head) + "\n\n" + body + tail


def cmd_page(a) -> int:
    code, shown = 0, []
    for raw_slug in a.slugs:
        slug = resolve_slug(raw_slug)
        if not slug:
            print(f"error: invalid page slug '{raw_slug}'", file=sys.stderr)
            code = 2
            continue
        try:
            doc = fetch(slug, cache=not a.no_cache)
        except NotFound:
            hint = ""
            try:
                names = list(build_index(False)["entries"])
                close = difflib.get_close_matches(slug, names, n=5, cutoff=0.5)
                hint = f" Did you mean: {', '.join(close)}?" if close else ""
            except HigError:
                pass
            print(f"error: no HIG page '{slug}'.{hint} Run: hig.py search <words>", file=sys.stderr)
            code = 2
            continue
        except HigError as e:
            print(f"error: {e}", file=sys.stderr)
            code = 3
            continue
        try:
            shown.append(json.dumps(doc, ensure_ascii=False) if a.raw else render_page(doc, slug, a))
        except HigError as e:
            print(f"error: {e}", file=sys.stderr)
            code = 2
    if shown:
        print("\n\n---\n\n".join(shown))
    return code


# --------------------------------------------------------------------------- symbols & prompt & verify

def get_verified_symbols() -> dict[str, list[str]]:
    """Parse common symbols from references/sf-symbols.md or return curated dictionary."""
    ref_file = Path(__file__).resolve().parent.parent / "references" / "sf-symbols.md"
    symbols_by_cat: dict[str, list[str]] = {}
    if ref_file.exists():
        try:
            content = ref_file.read_text(encoding="utf-8")
            table_started = False
            for line in content.splitlines():
                if "## Common symbols" in line:
                    table_started = True
                    continue
                if table_started and line.startswith("|") and not line.startswith("| Area") and not line.startswith("|---"):
                    parts = [p.strip() for p in line.split("|") if p.strip()]
                    if len(parts) >= 2:
                        cat = parts[0]
                        syms = [s.strip("` ") for s in parts[1].split() if s.strip("` ")]
                        symbols_by_cat[cat] = syms
        except Exception:
            pass
    if not symbols_by_cat:
        symbols_by_cat = {
            "Navigation": ["house", "house.fill", "magnifyingglass", "gearshape", "gearshape.fill", "sidebar.left", "line.3.horizontal", "list.bullet", "square.grid.2x2", "slider.horizontal.3"],
            "Directions": ["chevron.left", "chevron.right", "chevron.up", "chevron.down", "arrow.left", "arrow.right", "arrow.up", "arrow.down", "arrow.clockwise", "arrow.counterclockwise"],
            "Actions": ["plus", "plus.circle.fill", "minus", "xmark", "xmark.circle.fill", "checkmark", "checkmark.circle.fill", "trash", "pencil", "square.and.pencil", "square.and.arrow.up", "square.and.arrow.down", "doc.on.doc", "ellipsis", "ellipsis.circle"],
            "Status": ["info.circle", "exclamationmark.triangle", "questionmark.circle", "bell", "bell.fill", "lock", "lock.open", "eye", "eye.slash"],
            "People": ["person", "person.fill", "person.crop.circle", "person.2"],
            "Content": ["folder", "doc", "doc.text", "photo", "camera", "mic", "calendar", "clock", "envelope", "paperplane", "link", "globe", "tag", "flag", "bookmark", "bookmark.fill", "tray"],
            "Media": ["play.fill", "pause.fill", "forward.fill", "backward.fill", "speaker.wave.2", "music.note"],
            "Social": ["heart", "heart.fill", "star", "star.fill", "hand.thumbsup", "message", "phone"],
            "Commerce": ["cart", "bag", "creditcard"],
            "Data": ["chart.bar", "chart.line.uptrend.xyaxis"],
            "Misc": ["bolt.fill", "flame.fill", "sparkles", "map", "location", "wifi", "gamecontroller", "terminal", "wrench.and.screwdriver"],
        }
    return symbols_by_cat


def cmd_symbols(a) -> int:
    syms = get_verified_symbols()
    query = (a.query or "").strip().lower()
    if not query:
        print("# Verified SF Symbols by Category\n")
        print("Note: Apple's SF Symbols contains 7,000+ icons. Use these verified names or verify custom names in the SF Symbols app.\n")
        for cat, items in syms.items():
            print(f"### {cat}")
            print(" ".join(f"`{s}`" for s in items))
            print()
        return 0
    matched = []
    for cat, items in syms.items():
        for s in items:
            if query in s.lower() or query in cat.lower():
                matched.append((cat, s))
    if not matched:
        print(f"No match for '{query}' in verified common symbols.", file=sys.stderr)
        print("Rule: If not listed, verify existence in the official Apple SF Symbols macOS app before finalizing.", file=sys.stderr)
        return 1
    print(f"# Matches for '{query}':")
    for cat, s in matched:
        print(f"- `{s}` ({cat})")
    return 0


def cmd_prompt(a) -> int:
    """Print ready-to-use prompt for Claude Code, ChatGPT, Codex, Antigravity, etc."""
    lang = (a.lang or "tr").lower()
    if lang == "tr":
        print("""Uygulamamın ekranlarını Apple'ın Human Interface Guidelines (HIG) kurallarına göre tasarla.

Sayfaları web sitesinden değil, doğrudan Apple'ın JSON adreslerinden oku:
1. Önce https://developer.apple.com/tutorials/data/design/human-interface-guidelines.json ile içindekileri al.
2. İşine yarayan her sayfayı https://developer.apple.com/tutorials/data/design/human-interface-guidelines/SAYFA.json biçiminde aç (en az layout, typography, color, tab-bars, lists-and-tables, sf-symbols ve materials).
3. İkonlarda SF Symbols, renklerde sistem renkleri (system colors), tipografide sistem fontu (Dynamic Type) kullan.
4. Her tasarım kararının yanına hangi HIG sayfasından ve anchor'dan aldığını yaz (Örnek: `// HIG: layout#Size-classes` veya karar tablosu).
5. Hafızandan veya tahminle kural uydurma; aldığın tüm değer ve prensipleri JSON'dan doğrulayarak aktar.""")
    else:
        print("""Design my app's screens according to Apple's Human Interface Guidelines (HIG).

Read the guidelines directly from Apple's official JSON endpoints, not the web interface:
1. First, fetch https://developer.apple.com/tutorials/data/design/human-interface-guidelines.json for the full index.
2. Fetch each relevant page via https://developer.apple.com/tutorials/data/design/human-interface-guidelines/PAGE.json (at minimum: layout, typography, color, tab-bars, lists-and-tables, sf-symbols, and materials).
3. Use SF Symbols for iconography, system semantic colors for palettes, and system typography with Dynamic Type support.
4. Explicitly cite the source HIG slug and anchor for every single design decision (e.g. `// HIG: layout#Size-classes` or a decision table).
5. Never invent rules or symbol names from memory; strictly verify all measurements, principles, and tokens from the fetched JSON.""")
    return 0


def cmd_verify(a) -> int:
    """Verify a citation in the format slug, slug#Anchor, or full HIG URL against the live HIG."""
    target = a.citation.strip()
    if "#" in target:
        raw_slug, anchor = target.split("#", 1)
    else:
        raw_slug, anchor = target, ""
    slug = resolve_slug(raw_slug)
    anchor = anchor.strip().lstrip("#")

    if not slug:
        print("INVALID: citation must include a valid page slug or URL (e.g. layout#Size-classes).", file=sys.stderr)
        return 1

    try:
        doc = fetch(slug, cache=not a.no_cache)
    except NotFound:
        print(f"INVALID: slug '{slug}' not found in Apple HIG.", file=sys.stderr)
        return 1
    except HigError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    title = doc.get("metadata", {}).get("title", slug)
    url = f"{SITE}/{slug}"

    if not anchor:
        print(f"VALID: {title} ({url})")
        return 0

    blocks = [b for sec in doc.get("primaryContentSections", [])
              if sec.get("kind") == "content" for b in sec.get("content", [])]
    found_heading = None
    target_anchor_norm = anchor.lower().replace(" ", "-").replace("_", "-")

    for b in blocks:
        if b.get("type") == "heading":
            b_anchor = (b.get("anchor") or "").lower().replace("_", "-")
            b_text_norm = (b.get("text") or "").lower().replace(" ", "-").replace("_", "-")
            if b_anchor == target_anchor_norm or b_text_norm == target_anchor_norm:
                found_heading = b.get("text")
                break

    if found_heading:
        print(f"VALID: {title} > {found_heading} ({url}#{anchor})")
        return 0
    else:
        anchors = [b.get("anchor") for b in blocks if b.get("type") == "heading" and b.get("anchor")]
        print(f"INVALID: anchor '{anchor}' not found on page '{slug}'.", file=sys.stderr)
        if anchors:
            print(f"Available anchors on '{slug}':", file=sys.stderr)
            for anc in anchors[:8]:
                print(f"  - #{anc}", file=sys.stderr)
        return 1


# --------------------------------------------------------------------------- main

def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    p = argparse.ArgumentParser(prog="hig.py", description="Read Apple's HIG via its JSON endpoints.")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("index", help="list all HIG pages")
    s.add_argument("--group", help="filter: top group or parent (e.g. components, foundations, patterns)")
    s.add_argument("--refresh", action="store_true", help="ignore cache and re-crawl")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_index)

    s = sub.add_parser("search", help="find pages by keyword")
    s.add_argument("terms", nargs="+")
    s.add_argument("--limit", type=int, default=12)
    s.set_defaults(fn=cmd_search)

    s = sub.add_parser("page", help="print one or more pages as Markdown")
    s.add_argument("slugs", nargs="+", help="e.g. layout typography color tab-bars")
    s.add_argument("--platform", help="comma list: " + ",".join(PLATFORMS) + " (default: all)")
    s.add_argument("--section", help="print only the section whose heading/anchor matches")
    s.add_argument("--outline", action="store_true", help="headings only, to pick a --section")
    s.add_argument("--full", action="store_true", help="keep Change log and Videos")
    s.add_argument("--raw", action="store_true", help="print raw JSON")
    s.add_argument("--no-cache", action="store_true")
    s.set_defaults(fn=cmd_page)

    s = sub.add_parser("symbols", help="search or list verified SF Symbols")
    s.add_argument("query", nargs="?", help="optional keyword e.g. gear, arrow, bell")
    s.set_defaults(fn=cmd_symbols)

    s = sub.add_parser("prompt", help="output ready-to-use prompt for agents")
    s.add_argument("--lang", choices=["tr", "en"], default="tr", help="language (tr or en)")
    s.set_defaults(fn=cmd_prompt)

    s = sub.add_parser("verify", help="verify a citation slug#Anchor against the live HIG")
    s.add_argument("citation", help="e.g. layout#Size-classes or materials#Liquid-Glass")
    s.add_argument("--no-cache", action="store_true")
    s.set_defaults(fn=cmd_verify)

    a = p.parse_args(argv)
    try:
        return a.fn(a)
    except HigError as e:
        print(f"error: {e}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
