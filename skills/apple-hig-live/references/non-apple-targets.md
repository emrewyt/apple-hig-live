# Using the HIG outside Apple platforms (WPF, Electron, web)

## Port the principles, not the assets

| Port | Do not copy |
|---|---|
| Visual hierarchy, grouping, progressive disclosure | SF Pro and other SF fonts |
| Spacing and alignment discipline, adaptive layout | SF Symbols glyphs |
| Type scale and text-style thinking | Apple app icons and marks |
| Semantic color roles, light and dark appearance | Apple logos, device frames |
| Accessibility: contrast, target size, scalable text | |

**Licensing:** Apple's licenses for SF Symbols and the SF fonts restrict use to apps for Apple platforms and design mockups. Check the current license before shipping them in WPF, Electron or web products.

## Substitutes

| Need | Windows (WPF) | Cross-platform / web |
|---|---|---|
| Font | `Segoe UI Variable` | `system-ui, -apple-system, "Segoe UI", Roboto, sans-serif` |
| Icons | Segoe Fluent Icons | Lucide or Phosphor (permissive licenses; check version) |
| Colors | Define semantic roles (background, label, separator, accent) with light and dark values | CSS custom properties with `prefers-color-scheme` |

Treat HIG "points" as device-independent pixels (WPF DIP, CSS px at 1x) when applying spacing and target-size numbers.

## Rules for agents

1. Read the HIG pages as usual, then state which guidance transfers and which is Apple-specific (e.g. Dynamic Island, tab bars on macOS).
2. In the decision log write `adapted from <slug>` and name the non-Apple platform convention you followed where it differs.
3. Do not claim a result "follows the HIG" when it uses non-Apple components; say "HIG-inspired".
