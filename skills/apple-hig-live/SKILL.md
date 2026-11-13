---
name: apple-hig-live
description: Design, mock up and audit native-feeling Apple-platform UI (iOS, iPadOS, macOS, watchOS, tvOS, visionOS) from the live, current Apple Human Interface Guidelines, authentic Liquid Glass optical physics, and SF Symbols. Apple's design pages are JavaScript-rendered and look blank to a normal web fetch, so this skill reads them through Apple's JSON endpoints with a bundled script and cites the HIG page behind every decision. Mandates genuine Liquid Glass physics (Snell refraction, Abbe dispersion, Fresnel specular rims) over flat CSS blur, authentic native Apple components (segmented controls, standard push/pop-up buttons), and professional designer-grade SVGs.
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
7. **Authentic Liquid Glass Optical Physics:** Never accept flat CSS blur as Liquid Glass. When specifying or implementing Liquid Glass, enforce genuine optical physics:
   - Snell's Law refraction ($n = 1.520$) with perimeter coordinate displacement.
   - Abbe chromatic dispersion ($V_d = 58.6$) with subtle spectral fringing.
   - Schlick Fresnel reflectivity ($R_0 \approx 4.3\%$, $R_{90^\circ} \approx 98.5\%$) via multi-stop specular rims.
   - System variants: `regular` (for navigation/sidebars) vs `clear` (for media HUDs with mandatory 35% dimming layer `rgba(0,0,0,0.35)`).
   - Strict functional layer placement: NEVER use Liquid Glass in the content layer or app backgrounds.
   - *Reference:* `references/liquid-glass-physics.md`.
8. **Strict Apple Component Architecture:**
   - Use native segmented controls (monolithic container with sliding elevated pill indicator, 2px padding, equal-width segments), standard push buttons, tinted prominent buttons (max 1 per view), and pop-up/pull-down buttons.
   - Strictly forbid non-Apple patterns: custom slider dispersion bars, unrounded rectangular tabs, non-Apple toggles, and arbitrary saturated gradients.
   - *Reference:* `references/components-and-controls.md`.
9. **Designer-Grade Vector Iconography:**
   - Vector SVGs must adhere to SF Symbols geometric proportions, standard `viewBox="0 0 24 24"`, semantic `<g id="...">` layers, cubic Bézier curvature, and Apple spring transitions (`cubic-bezier(0.16, 1, 0.3, 1)`).
   - *Reference:* `references/designer-svg-standards.md`.
10. **Layer Separation:** Never apply Liquid Glass to the content layer; reserve it strictly for functional floating navigation layers (tab bars, sidebars, floating HUD decks).

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

**4. Design / implement.** Start from system components; deviate only where the HIG allows.
- **Controls & Navigation:** Consult `references/components-and-controls.md`. Use native segmented controls (28px/32px, equal width, sliding card indicator), push buttons (24px/28px, 6px radius), max 1 prominent button, native switches (38x22px in rows), and native sliders (4px track).
- **Materials:** Consult `references/liquid-glass-physics.md`. Apply Liquid Glass to functional navigation layers only.
- **Icons & Graphics:** Consult `references/designer-svg-standards.md` for SF Symbols alignment, squircle math, and SVG architecture.
For non-Apple targets (WPF, Electron, web) read `references/non-apple-targets.md` first.

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
- Liquid Glass components use authentic optical physics (refraction, dispersion, Fresnel specular borders) and appear only in the functional navigation layer.
- Clear Liquid Glass includes the mandatory 35% dark dimming layer over rich media.
- Controls adhere strictly to native Apple patterns (segmented controls, standard push/pop-up buttons) with zero forbidden custom slider/toggle shapes.
- Icons are professional designer-grade SVGs adhering to SF Symbols proportions and cubic Béziers.

## Failure handling

| Symptom | Action |
|---|---|
| `python3` missing | `curl -s -A "Mozilla/5.0" https://developer.apple.com/tutorials/data/design/human-interface-guidelines/<slug>.json`, then read `primaryContentSections` (schema: `references/json-schema.md`) |
| `no HIG page '<slug>'` | Use the suggestion it prints, or `hig.py search` / `hig.py index --refresh` |
| Network blocked | Tell the user; continue with general principles labeled `UNVERIFIED (no HIG access)` |

## References (read when needed)

- `references/page-map.md` — task → HIG slugs
- `references/sf-symbols.md` — naming, variants, rendering modes, common symbol names, usage snippets
- `references/liquid-glass-physics.md` — optical physics (Snell, Abbe, Fresnel, Beer-Lambert), regular vs clear variants, 35% dimming scrim, SVG/CSS implementation
- `references/components-and-controls.md` — native Apple segmented controls, push/tinted buttons, pop-up buttons, native switches, forbidden patterns
- `references/designer-svg-standards.md` — Figma/Illustrator tier SVG standards, squircle math, SF Symbols alignment, Apple spring motion curves
- `references/non-apple-targets.md` — adapting HIG principles to WPF / Electron / web, plus licensing notes
- `references/json-schema.md` — DocC JSON shape, for the curl fallback
