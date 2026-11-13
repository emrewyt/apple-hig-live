# Apple HIG Components, Controls & Interaction Architecture

Official specifications for authentic Apple system controls across macOS, iOS, iPadOS, visionOS, and adapted cross-platform runtimes (Electron, Web, WPF).

Citations in this document are verified against live Apple DocC endpoints using `scripts/hig.py verify`.

---

## 1. Native Segmented Controls

> **HIG Citation:** `segmented-controls#Best-practices`, `segmented-controls#Content`, `segmented-controls#macOS`  
> *"Use a segmented control to provide closely related choices that affect an object, state, or view... When all segments have equal width, a segmented control feels balanced... Prefer using either text or images — not a mix of both — in a single segmented control."*

### 1.1 Dimensional & Visual Geometry

| Attribute | macOS Toolbar / Desktop | iOS Standard / Mobile |
|---|---|---|
| **Height** | `28px` (regular) / `32px` (large) | `32px` |
| **Outer Container Padding** | `2px` | `3px` |
| **Outer Border Radius** | `8px` (`--radius-sm`) or Capsule (`9999px`) | Capsule (`9999px`) or `8px` |
| **Container Background (Dark)** | `rgba(118, 118, 128, 0.16)` | `rgba(118, 118, 128, 0.24)` |
| **Container Background (Light)** | `rgba(118, 118, 128, 0.12)` | `rgba(118, 118, 128, 0.12)` |
| **Container Border** | `0.5px solid rgba(255, 255, 255, 0.08)` (Dark) | `0.5px solid rgba(0, 0, 0, 0.04)` |
| **Active Pill Fill (Dark)** | `rgba(255, 255, 255, 0.22)` | `rgba(255, 255, 255, 0.25)` |
| **Active Pill Fill (Light)** | `#FFFFFF` | `#FFFFFF` |
| **Active Pill Shadow** | `0 3px 8px 0 rgba(0,0,0,0.16), 0 3px 1px 0 rgba(0,0,0,0.06), inset 0 0.5px 0.5px rgba(255,255,255,0.35)` | `0 3px 8px rgba(0,0,0,0.12)` |
| **Pill Radius** | `calc(var(--radius) - 2px)` (e.g. `6px`) | `calc(var(--radius) - 3px)` |
| **Sliding Easing Curve** | `cubic-bezier(0.16, 1, 0.3, 1)` (Apple Spring) | `cubic-bezier(0.16, 1, 0.3, 1)` |
| **Sliding Duration** | `260ms` | `280ms` |
| **Max Recommended Segments** | 5 to 7 segments | 5 segments |
| **Segment Width** | Strictly equal width (`flex: 1 1 0`) | Strictly equal width |

### 1.2 Typography & Segment State Discipline
- **Inactive Segments:** San Francisco, size `13px`, weight `500` (Medium), color `var(--label-secondary)` (`rgba(235, 235, 245, 0.68)` in dark mode, `rgba(60, 60, 67, 0.60)` in light mode).
- **Active Segment:** San Francisco, size `13px`, weight `600` (Semibold), color `var(--label-primary)` (`#FFFFFF` in dark mode, `#000000` in light mode).
- **Inter-Segment Dividers:** `1px` wide, `12px` tall vertical lines centered vertically (`background: rgba(255, 255, 255, 0.14)` in dark mode). Dividers are hidden adjacent to the active sliding pill indicator.
- **Content Homogeneity:** Strictly all text labels OR all icons/symbols. Never mix text and glyphs in the same segmented control (`segmented-controls#Content`).
- **Semantic ARIA Markup:** Container has `role="tablist"`, segments have `role="tab"`, `aria-selected="true|false"`, and support ArrowLeft/ArrowRight keyboard navigation.

### 1.3 Production CSS Implementation
```css
/* Monolithic Apple Segmented Control */
.apple-segmented-control {
  position: relative;
  display: inline-flex;
  align-items: center;
  height: 28px;
  padding: 2px;
  background: rgba(118, 118, 128, 0.16);
  border: 0.5px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  user-select: none;
  box-sizing: border-box;
}

/* Sliding Elevated Pill Indicator */
.apple-segment-indicator {
  position: absolute;
  top: 2px;
  left: 2px;
  height: calc(100% - 4px);
  background: rgba(255, 255, 255, 0.22);
  border-radius: 6px;
  box-shadow: 
    0 3px 8px 0 rgba(0, 0, 0, 0.16),
    0 3px 1px 0 rgba(0, 0, 0, 0.06),
    inset 0 0.5px 0.5px 0 rgba(255, 255, 255, 0.35);
  transition: transform 260ms cubic-bezier(0.16, 1, 0.3, 1), width 260ms cubic-bezier(0.16, 1, 0.3, 1);
  pointer-events: none;
  z-index: 1;
}

/* Individual Segment Items */
.apple-segment-item {
  position: relative;
  z-index: 2;
  flex: 1 1 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0 12px;
  height: 100%;
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui, sans-serif;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: -0.08px;
  color: rgba(235, 235, 245, 0.68);
  background: transparent;
  border: none;
  cursor: pointer;
  white-space: nowrap;
  transition: color 180ms ease;
}

.apple-segment-item.active {
  font-weight: 600;
  color: #FFFFFF;
}

/* Subtle Inactive Segment Dividers */
.apple-segment-divider {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 1px;
  height: 12px;
  background: rgba(255, 255, 255, 0.14);
  pointer-events: none;
  transition: opacity 160ms ease;
}

.apple-segment-item.active .apple-segment-divider,
.apple-segment-item.prev-active .apple-segment-divider {
  opacity: 0;
}
```

---

## 2. Standard Apple Buttons & Action Hierarchy

> **HIG Citation:** `buttons#Style`, `buttons#Push-buttons`, `pop-up-buttons#Best-practices`, `pull-down-buttons#Best-practices`  
> *"In general, use a button that has a prominent visual style for the most likely action in a view... Keep the number of prominent buttons to one or two per view... The standard button type in macOS is known as a push button... Pop-up buttons present a flat list of mutually exclusive options... Pull-down buttons present commands or items directly related to the action."*

### 2.1 Button Taxonomy & Specifications

| Button Type | Purpose | Dimensions & Styling | Indicator / Icon | HIG Constraints |
|---|---|---|---|---|
| **Standard Push Button** (`.apple-button-push`, `.apple-btn-push`) | Secondary, modal, or standard dialog actions | Height: `24px` (regular) or `28px` (large). Corner radius: `6px`. Background: `rgba(255, 255, 255, 0.09)`. Border: `0.5px solid rgba(255, 255, 255, 0.14)`. Inset specular highlight. | None, or leading SF Symbol. Trailing ellipsis (`…`) if opening another view. | Default styling for secondary actions. |
| **Prominent / Tinted Button** (`.apple-button-prominent`, `.apple-btn-prominent`) | Primary call to action (Done, Save, Send, Connect) | Height: `24px` / `28px`. Radius: `6px`. Fill: `var(--accent-blue)` (`#0A84FF` dark / `#007AFF` light). Text: `#FFFFFF`, weight `600`. Glow shadow: `0 2px 8px rgba(10, 132, 255, 0.35)`. | Optional leading glyph | **Strictly max 1 (or at most 2) per view.** Never place multiple prominent buttons together. |
| **Pop-Up Button** (`.apple-button-popup`, `.apple-btn-popup`) | Select one mutually exclusive option from a flat list | Height & radius match push button. Displays currently active selection. | Trailing double chevron (`chevron.up.chevron.down` or `▲▼`) | Updates title to reflect selected option. |
| **Pull-Down Button** (`.apple-button-pulldown`, `.apple-btn-pulldown`) | Trigger contextual commands or menu actions | Height & radius match push button. Persistent action title (e.g. "Action", "Sort"). | Trailing single chevron (`chevron.down` or `▼`) | Minimum 3 items. Never hides primary view actions. |

### 2.2 Button Production CSS
```css
/* Standard macOS Push Button (Contract: .apple-button-push | Alias: .apple-btn-push) */
.apple-button-push,
.apple-btn-push {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  height: 24px;
  padding: 0 12px;
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui, sans-serif;
  font-size: 13px;
  font-weight: 500;
  color: #FFFFFF;
  background: rgba(255, 255, 255, 0.09);
  border: 0.5px solid rgba(255, 255, 255, 0.14);
  border-radius: 6px;
  box-shadow: 
    0 1px 2px rgba(0, 0, 0, 0.20),
    inset 0 0.5px 0.5px rgba(255, 255, 255, 0.25);
  cursor: pointer;
  user-select: none;
  transition: background 150ms ease, transform 80ms ease;
}

.apple-button-push:hover,
.apple-btn-push:hover {
  background: rgba(255, 255, 255, 0.15);
}

.apple-button-push:active,
.apple-btn-push:active {
  background: rgba(255, 255, 255, 0.22);
  transform: scale(0.98);
}

/* Prominent Accent Button (Contract: .apple-button-prominent | Alias: .apple-btn-prominent) */
.apple-button-prominent,
.apple-btn-prominent {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  height: 24px;
  padding: 0 14px;
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui, sans-serif;
  font-size: 13px;
  font-weight: 600;
  color: #FFFFFF;
  background: var(--accent-blue, #0A84FF);
  border: 0.5px solid rgba(255, 255, 255, 0.20);
  border-radius: 6px;
  box-shadow: 
    0 2px 8px rgba(10, 132, 255, 0.35),
    inset 0 0.5px 1px rgba(255, 255, 255, 0.35);
  cursor: pointer;
  user-select: none;
  transition: filter 150ms ease, transform 80ms ease;
}

.apple-button-prominent:hover,
.apple-btn-prominent:hover {
  filter: brightness(1.10);
}

.apple-button-prominent:active,
.apple-btn-prominent:active {
  filter: brightness(0.92);
  transform: scale(0.98);
}

/* Pop-Up Button (Contract: .apple-button-popup | Alias: .apple-btn-popup) */
.apple-button-popup,
.apple-btn-popup {
  display: inline-flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  height: 24px;
  padding: 0 8px 0 12px;
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui, sans-serif;
  font-size: 13px;
  font-weight: 500;
  color: #FFFFFF;
  background: rgba(255, 255, 255, 0.09);
  border: 0.5px solid rgba(255, 255, 255, 0.14);
  border-radius: 6px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.20), inset 0 0.5px 0.5px rgba(255, 255, 255, 0.25);
  cursor: pointer;
}

.apple-button-popup .chevron-indicator,
.apple-btn-popup .chevron-indicator {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  opacity: 0.65;
}
```

---

## 3. macOS Native Switch (Toggle)

> **HIG Citation:** `toggles#Switches`  
> *"Within a grouped form, consider using a mini switch to control the setting in a single row. The height of a mini switch is similar to the height of buttons and other controls, resulting in rows that have a consistent height... Prefer a switch for settings that you want to emphasize."*

### 3.1 Dimensional Geometry & Styling
- **Role & Placement:** Strictly in settings rows, inspector tables, and grouped list rows. Never float as a hero control.
- **Track Geometry:** Width `38px`, height `22px`, corner radius `11px` (capsule). Inset padding: `2px`.
- **Thumb Geometry:** Diameter `18px`, circular (`border-radius: 50%`), solid `#FFFFFF`.
- **Thumb Elevation:** `box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.25), 0 0 1px rgba(0, 0, 0, 0.15)`.
- **Off State Track:** `background: rgba(120, 120, 128, 0.32)`.
- **On State Track:** `background: var(--accent-green, #30D158)` (or system accent).
- **Thumb Travel Distance:** `transform: translateX(16px)` on active state.
- **Spring Transition:** `all 250ms cubic-bezier(0.16, 1, 0.3, 1)`.

### 3.2 Production CSS
```css
/* Authentic macOS Switch */
.apple-switch {
  position: relative;
  width: 38px;
  height: 22px;
  background: rgba(120, 120, 128, 0.32);
  border-radius: 11px;
  padding: 2px;
  box-sizing: border-box;
  cursor: pointer;
  transition: background 250ms cubic-bezier(0.16, 1, 0.3, 1);
  user-select: none;
}

.apple-switch.active {
  background: #30D158;
}

.apple-switch-thumb {
  width: 18px;
  height: 18px;
  background: #FFFFFF;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.25), 0 0 1px rgba(0, 0, 0, 0.15);
  transition: transform 250ms cubic-bezier(0.16, 1, 0.3, 1);
}

.apple-switch.active .apple-switch-thumb {
  transform: translateX(16px);
}
```

---

## 4. macOS Native Slider

> **HIG Citation:** `sliders#Best-practices`, `sliders#macOS`  
> *"People expect the minimum and maximum sides of sliders to be consistent in all apps, with minimum values on the leading side and maximum values on the trailing side... In a linear slider either with or without tick marks, the thumb is a narrow lozenge shape, and the portion of track between the minimum value and the thumb is filled with color."*

### 4.1 Dimensional Geometry & Styling
- **Track Height:** Strictly `4px` (never thick 8-12px decorative bars). Corner radius: `2px`.
- **Inactive Track Background:** `rgba(255, 255, 255, 0.16)` (dark mode) / `rgba(0, 0, 0, 0.10)` (light mode).
- **Active Track Fill:** `var(--accent-blue, #0A84FF)`.
- **Thumb Geometry:** Diameter `20px`, circular, `#FFFFFF`.
- **Thumb Elevation:** `box-shadow: 0 2px 6px rgba(0, 0, 0, 0.35), 0 0 1px rgba(0, 0, 0, 0.20)`. No oversized neon outer halos.
- **Directionality:** Minimum values on leading side (left), maximum values on trailing side (right).

### 4.2 Production CSS
```css
/* Authentic macOS Native Slider */
.apple-slider-container {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
}

.apple-slider {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 4px;
  border-radius: 2px;
  background: rgba(255, 255, 255, 0.16);
  outline: none;
  cursor: pointer;
  position: relative;
}

.apple-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #FFFFFF;
  border: 0.5px solid rgba(0, 0, 0, 0.04);
  box-shadow: 
    0 2px 6px rgba(0, 0, 0, 0.35),
    0 0 1px rgba(0, 0, 0, 0.20);
  cursor: pointer;
  transition: transform 120ms ease;
}

.apple-slider::-webkit-slider-thumb:active {
  transform: scale(1.08);
}
```

---

## 5. Strictly Forbidden Non-Apple Control Patterns

The following patterns violate Apple HIG and must be rejected during audits and refactoring:

| # | Forbidden Anti-Pattern | HIG Violation Citation | Why It Is Prohibited | Mandatory Apple Replacement |
|---|---|---|---|---|
| **1** | **Custom Thick "Dispersion" Slider Tracks** (e.g. 8-14px glowing gradient bars) | `sliders#macOS`, `sliders#Best-practices` | Destroys macOS visual rhythm; distracts from value adjustment; creates un-Apple sci-fi aesthetic. | Standard `4px` subtle track with clean `20px` circular thumb and leading/trailing SF Symbol icons. |
| **2** | **Oversized / Glowing Neon Toggles** (e.g. 52x30px switches with cyan/green blur outer halos) | `toggles#Switches`, `color#Liquid-Glass-color` | Excessively prominent; breaks list row baseline heights; introduces artificial neon glow. | Native `38px × 22px` capsule switch with `18px` white thumb, `#30D158` fill, and directional shadow. |
| **3** | **Sharp 90° Rectangular Tabs or Material Underline Tabs** | `segmented-controls#Best-practices`, `tab-bars` | Belongs to Google Material or Windows Metro; conflicts with Apple squircle and continuous curvature geometry. | Native segmented control with `8px` corner radius and elevated sliding pill indicator. |
| **4** | **Arbitrary Saturated Multi-Color Gradient Cards** | `materials#Liquid-Glass`, `color` | Overwhelms content hierarchy; conflicts with Liquid Glass optical physics and translucency. | Monochromatic translucent Liquid Glass regular panel, with dynamic chromatic mesh placed in wallpaper background. |
| **5** | **Multiple Prominent / Tinted Buttons in One View** | `buttons#Style` | Spikes cognitive load; destroys action hierarchy; users cannot determine primary action. | Exactly **1 prominent button** for primary action (Done/Save); standard beveled push buttons for secondary actions. |
| **6** | **Mixed Text and Icon Segments in One Control** | `segmented-controls#Content` | Creates visual imbalance and cognitive friction. | Strictly all text labels OR all icons/symbols across segments. |
| **7** | **Liquid Glass in the Content Layer** | `materials#Liquid-Glass` | Dilutes the distinction between interactive Chrome and content; causes illegibility. | Restrict Liquid Glass to functional navigation layers (tab bars, sidebars, floating HUD decks); use standard materials for content cards. |
