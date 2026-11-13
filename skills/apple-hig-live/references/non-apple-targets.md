# Using the HIG outside Apple platforms (WPF, Electron, web)

## Port the principles, not the assets

| Port | Do not copy |
|---|---|
| Visual hierarchy, grouping, progressive disclosure | SF Pro and other SF fonts (licensing restricted) |
| Spacing and alignment discipline, adaptive layout | SF Symbols glyphs (proprietary binary format) |
| Type scale and text-style thinking | Apple app icons and trademarks |
| Semantic color roles, light and dark appearance | Apple proprietary logos, hardware frames |
| Authentic Apple component sizing & metrics | Non-system decorative widgets |
| Accessibility: contrast, target size, scalable text | Banned neon glow patterns |

**Licensing:** Apple's licenses for SF Symbols and the SF fonts restrict use to apps for Apple platforms and design mockups. Check the current license before shipping them in WPF, Electron or web products. For cross-platform targets, use high-fidelity open-source SVG equivalents adhering to SF Symbols proportions (see `references/designer-svg-standards.md`).

## Substitutes

| Need | Windows (WPF) | Cross-platform / Electron / Web |
|---|---|---|
| **Font** | `Segoe UI Variable` | `system-ui, -apple-system, "Segoe UI Variable", Roboto, sans-serif` |
| **Icons** | Segoe Fluent Icons or custom SVG | Custom designer-grade SVGs (`references/designer-svg-standards.md`) or Lucide |
| **Colors** | Semantic brush resources (Background, Label, Accent) | CSS custom properties with light/dark adaptive variables |
| **Materials** | Windows 11 Mica Alt / Acrylic | Liquid Glass SVG filter + multi-stop specular CSS (`references/liquid-glass-physics.md`) |
| **Controls** | Custom ControlTemplates matching Apple metrics | CSS components matching `references/components-and-controls.md` |

Treat HIG "points" as device-independent pixels (WPF DIP, CSS px at 1x) when applying spacing and target-size numbers.

---

## Component Adaptations for Web & Electron

When implementing Apple-style interfaces in Electron or Web applications, do not invent hybrid widgets:

1. **Segmented Controls:**
   - Use the exact 28px/32px height, 2px padding, and elevated sliding pill indicator specified in `references/components-and-controls.md`.
   - Animate the indicator with `transform: translateX(...)` using the Apple spring easing `cubic-bezier(0.16, 1, 0.3, 1)`.
2. **Buttons:**
   - Adhere to the 24px/28px height, 6px corner radius, and top-down specular bevel (`inset 0 0.5px 0.5px rgba(255,255,255,0.25)`).
   - Strictly observe the rule of **maximum 1 prominent tinted button per view**.
3. **Switches (Toggles):**
   - On desktop Electron views, render compact 38px × 22px capsule switches with 18px thumbs. Avoid oversized 52x30px mobile switches or Android-style switches.
4. **Sliders:**
   - Maintain a 4px subtle track and 20px circular thumb. Never implement thick 8-14px glowing gradient tracks.

---

## Rules for agents

1. Read the HIG pages as usual, then state which guidance transfers and which is Apple-specific (e.g. Dynamic Island, tab bars on macOS).
2. Consult `references/components-and-controls.md` for exact control sizing, geometry, and forbidden patterns.
3. In the decision log write `adapted from <slug>` and name the non-Apple platform convention you followed where it differs.
4. Do not claim a result "follows the HIG" when it uses non-Apple components; say "HIG-inspired".
5. Never introduce forbidden anti-patterns (neon dispersion tracks, multiple prominent buttons, mixed text/icon segments).
