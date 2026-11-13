# Task → HIG page map

Slugs below are the usual ones. The source of truth is `hig.py index`; if a slug 404s, the script suggests the closest match.
Read with: `python3 <SKILL_DIR>/scripts/hig.py page <slug> [<slug> ...] --platform ios`

## Always read (any screen)

`layout` `typography` `color` `materials` `sf-symbols` `dark-mode` `accessibility`

## By task

| Task | Pages |
|---|---|
| App shell / navigation (tabs, sidebar) | `tab-bars` `sidebars` `navigation-bars` `toolbars` `split-views` |
| Lists, settings, forms | `lists-and-tables` `collections` `settings` `entering-data` `text-fields` `toggles` `pickers` `segmented-controls` `sliders` `steppers` |
| Dialogs and overlays | `alerts` `sheets` `popovers` `action-sheets` `modality` |
| Buttons and menus | `buttons` `menus` `context-menus` `pop-up-buttons` `pull-down-buttons` |
| Search | `search-fields` `searching` |
| Onboarding, launch, empty / loading states | `onboarding` `launching` `loading` `progress-indicators` |
| Dashboards, data | `charts` `widgets` `color` |
| Scrolling content | `scroll-views` `collections` |
| Notifications and permissions | `notifications` `requesting-permission` |
| App icon and iconography | `app-icons` `icons` `sf-symbols` `images` |
| Motion and feedback | `motion` `feedback` `playing-haptics` |
| Writing / microcopy | `writing` |
| Right-to-left, localization | `right-to-left` `layout` |
| Gestures, pointer, keyboard | `gestures` `pointing-devices` `keyboards` |

## By platform

| Platform | Start with |
|---|---|
| iOS | `designing-for-ios` |
| iPadOS | `designing-for-ipados` `multitasking` |
| macOS | `designing-for-macos` `windows` `menus` `toolbars` |
| watchOS | `designing-for-watchos` |
| tvOS | `designing-for-tvos` |
| visionOS | `designing-for-visionos` `spatial-layout` `ornaments` |

## Deep Specifications & References

- `references/components-and-controls.md` — exact Apple specifications for segmented controls, push/tinted buttons, pop-up/pull-down buttons, native switches, native sliders, and forbidden patterns.
- `references/liquid-glass-physics.md` — mathematical optics, Snell's law ($n=1.52$), Abbe dispersion ($V_d=58.6$), Fresnel reflection, regular vs. clear variants, and Web/Electron SVG realization.
- `references/designer-svg-standards.md` — macOS app icon squircle geometry (1024x1024 / 824x824), 4-tier shadow stack, SF Symbols metrics, and designer-grade SVG architecture.
- `references/non-apple-targets.md` — porting HIG principles to Electron, Web, and WPF.

## Efficient reading

1. `hig.py page <slug> --outline` to see headings.
2. `hig.py page <slug> --section "<heading>"` for only what you need.
3. Always pass `--platform` for the target platform(s).
