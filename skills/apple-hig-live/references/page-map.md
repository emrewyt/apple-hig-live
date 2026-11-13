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
| Buttons and menus | `buttons` `menus` `context-menus` `pull-down-buttons` |
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

## Efficient reading

1. `hig.py page <slug> --outline` to see headings.
2. `hig.py page <slug> --section "<heading>"` for only what you need.
3. Always pass `--platform` for the target platform(s).
