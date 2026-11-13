---
name: apple-hig-live
description: Design, mock up and audit native-feeling Apple-platform UI (iOS, iPadOS, macOS, watchOS, tvOS, visionOS) from the live, current Apple Human Interface Guidelines and SF Symbols. Apple's design pages are JavaScript-rendered and look blank to a normal web fetch, so this skill reads them through Apple's JSON endpoints with a bundled script and cites the HIG page behind every decision. Use whenever the user mentions HIG, Human Interface Guidelines, Apple design, SwiftUI/UIKit/AppKit screens, Liquid Glass, SF Symbols, SF Pro, Dynamic Type, safe areas, tab bars, sidebars, toolbars, or asks for an "iOS-style", "native" or "Apple-like" UI or a design review, even if they never say "HIG".
---

# Apple HIG Live

Design from the real, current HIG instead of memory. Apple's design site renders with JavaScript, so a plain fetch of `developer.apple.com/design/...` returns an empty page. The same content is served as JSON; `scripts/hig.py` downloads it and prints compact Markdown.

`<SKILL_DIR>` below means the folder that contains this SKILL.md. Use `python3` (Windows: `python`).

## Rules

1. **Never browse or web-fetch the HIG HTML pages.** They come back blank. Use `hig.py`.
2. **No HIG rule or number from memory.** Point sizes, margins, contrast ratios and behaviors must come from a page you fetched in this session.
3. **Every design decision carries a source** (page slug + section anchor). See "Output".
4. **System first:** SF Symbols for icons, system colors, system font with text styles. Custom only with a stated reason.
5. **Never invent SF Symbol names.** Use names from `references/sf-symbols.md` or ones the user supplied; mark anything else `verify in SF Symbols app`.
6. If HIG access fails, say so and mark the affected decisions `UNVERIFIED`. Never fabricate a citation.

## Workflow

**1. Scope.** Decide platform(s), screens, and framework (SwiftUI / UIKit / AppKit / HTML mockup / non-Apple target). Infer from the repo when possible; otherwise assume iOS + SwiftUI and say so in one line.

**2. Find pages & symbols.**
```
python3 <SKILL_DIR>/scripts/hig.py search "tab bar navigation"
python3 <SKILL_DIR>/scripts/hig.py index --group components
python3 <SKILL_DIR>/scripts/hig.py symbols "gear"                # search verified SF Symbols
```
`references/page-map.md` maps common tasks to slugs. Always read the core set: `layout typography color materials sf-symbols dark-mode accessibility`.

**3. Read.**
```
python3 <SKILL_DIR>/scripts/hig.py page layout typography color --platform ios
python3 <SKILL_DIR>/scripts/hig.py page tab-bars --outline          # headings only
python3 <SKILL_DIR>/scripts/hig.py page layout --section "Size classes"
```
- `--platform` takes `ios,ipados,macos,tvos,visionos,watchos` and trims unrelated platform sections.
- On large pages run `--outline` first, then `--section`, to save context.
- Pages end with "Related" links shown as `(-> slug)`; follow them when a component depends on another.
- Output starts with `Last updated:` when Apple provides it. Prefer newer guidance (e.g. Liquid Glass) over anything you remember.

**4. Design / implement.** Start from system components; deviate only where the HIG allows. For non-Apple targets (WPF, Electron, web) read `references/non-apple-targets.md` first.

**5. Cite and self-check.**
Verify citations with `python3 <SKILL_DIR>/scripts/hig.py verify <slug>#<Anchor>` to guarantee 100% verified anchors without hallucinations.

## Output

End every design or review with a decision log:

| Decision | Rule applied | Source |
|---|---|---|
| Bottom tab bar, 4 items | Top-level navigation uses a tab bar | `tab-bars` |
| Body uses `.body` text style | Support Dynamic Type | `typography#Supporting-Dynamic-Type` |

- Source format: `slug` or `slug#Anchor`. Full URL = `https://developer.apple.com/design/human-interface-guidelines/<slug>`.
- Quote at most a short phrase from the page; paraphrase the rest.
- Code gets the same treatment: add a short comment such as `// HIG: layout#Guides-and-safe-areas` next to the line it justifies.

### Self-check before finishing
Verify each against the fetched pages, not memory:
- Content respects safe areas and layout guides; controls are not placed where the page says to avoid.
- Text uses system text styles and survives larger Dynamic Type sizes.
- Light and dark appearance both work; color is never the only signal.
- Standard system components are used before custom ones.
- Icons are SF Symbols with consistent weight and rendering mode.
- Touch / pointer target sizes match the numbers on the fetched page.
- Platform-specific considerations for each target platform were read.

## Failure handling

| Symptom | Action |
|---|---|
| `python3` missing | `curl -s -A "Mozilla/5.0" https://developer.apple.com/tutorials/data/design/human-interface-guidelines/<slug>.json`, then read `primaryContentSections` (schema: `references/json-schema.md`) |
| `no HIG page '<slug>'` | Use the suggestion it prints, or `hig.py search` / `hig.py index --refresh` |
| Network blocked | Tell the user; continue with general principles labeled `UNVERIFIED (no HIG access)` |

## References (read when needed)

- `references/page-map.md` — task → HIG slugs
- `references/sf-symbols.md` — naming, variants, rendering modes, common symbol names, usage snippets
- `references/non-apple-targets.md` — adapting HIG principles to WPF / Electron / web, plus licensing notes
- `references/json-schema.md` — DocC JSON shape, for the curl fallback
