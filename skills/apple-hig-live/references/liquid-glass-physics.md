# Liquid Glass Optical Physics & Material System Specification

> **Official HIG Lineage:** `materials#Liquid-Glass` (Updated 2025-09-09) | `color#Liquid-Glass-color` (Updated 2025-12-16)  
> **Target Frameworks:** SwiftUI (`glassEffect`), AppKit (`NSVisualEffectView`), UIKit (`UIVisualEffectView`), Web / Electron (SVG Displacement + CSS Multi-Stop Specular Rims)

---

## 1. System Overview & The Functional Layer Rule

Apple Human Interface Guidelines establish a fundamental architectural distinction between materials:
1. **The Functional Layer (Liquid Glass):** Liquid Glass forms a distinct, translucent interactive layer for controls and navigation elements (tab bars, sidebars, toolbars, transient controls). It floats above content, allowing underlying elements to scroll and peek through while preserving absolute legibility.
2. **The Content Layer (Standard Materials):** App backgrounds, card grouping containers, and content-level views must use standard materials (`ultraThin`, `thin`, `regular`, `thick`).

### 🔒 Architectural Commandments:
- **NEVER use Liquid Glass in the content layer.** Liquid Glass is strictly reserved for the functional navigation and control layer. Using it as an app background destroys visual hierarchy.
- **Exception for Transient Content Controls:** Sliders and toggles located in the content layer adopt Liquid Glass appearance *only during user interaction* (drag/press) to emphasize transient state.
- **Never accept flat CSS blur as Liquid Glass.** Authentic Liquid Glass requires optical refraction, chromatic dispersion, grazing Fresnel reflectivity, and multi-tier specular borders.

---

## 2. Mathematical Optical Physics Model

### 2.1. Snell's Law of Refraction & Ray Deflection
Light traversing the interface between air ($n_1 \approx 1.000$) and optical crown glass ($n_2 = 1.520$) bends toward the surface normal according to Snell's Law:

$$n_1 \sin\theta_1 = n_2 \sin\theta_2 \implies \sin\theta_2 = \frac{n_1}{n_2} \sin\theta_1$$

Where:
- $n_1 = 1.000293$ (ambient air refractive index)
- $n_2 = 1.520$ (optical silicate crown glass index at $\lambda = 589.3\text{ nm}$)
- $\theta_1$ is the angle of incidence relative to the surface normal $\mathbf{N}$
- $\theta_2$ is the angle of refraction inside the glass medium

#### Vector Formulation for Ray Tracing:
Given unit incident ray vector $\mathbf{I}$ and unit surface normal $\mathbf{N}$:

$$\mathbf{R}_{\text{refract}} = \eta \mathbf{I} + \left(\eta (\mathbf{N} \cdot \mathbf{I}) - \sqrt{1 - \eta^2 (1 - (\mathbf{N} \cdot \mathbf{I})^2)}\right) \mathbf{N}$$

Where relative index ratio $\eta = \frac{n_1}{n_2} = \frac{1.0}{1.520} \approx 0.65789$.

#### Total Internal Reflection (TIR):
When rays attempt to exit the glass medium ($n_1 = 1.520 \to n_2 = 1.000$), total internal reflection occurs at angles exceeding the critical angle:

$$\theta_c = \arcsin\left(\frac{1}{n}\right) = \arcsin\left(\frac{1}{1.520}\right) \approx 41.14^\circ$$

#### UI Engineering Implication:
At the curved outer perimeter chamfer of a UI container ($0\text{px} - 8\text{px}$ bevel boundary), the surface normal $\mathbf{N}$ tilts rapidly from $0^\circ$ to $90^\circ$. This creates acute pixel displacement warping background content inward toward the container center. Flat central regions ($\theta_1 \approx 0^\circ$) exhibit near-zero directional deviation.

---

### 2.2. Abbe Number & Chromatic Dispersion
In physical optics, the refractive index varies by wavelength ($n = n(\lambda)$). Standard optical glass is parameterized by the **Abbe Number** ($V_d$):

$$V_d = \frac{n_d - 1}{n_F - n_C} \approx 58.6$$

Where Fraunhofer spectral reference lines are:
- $n_d = 1.5200$ (Helium yellow $d$-line, $\lambda_d = 587.56\text{ nm}$)
- $n_F = 1.5250$ (Hydrogen blue $F$-line, $\lambda_F = 486.13\text{ nm}$)
- $n_C = 1.5162$ (Hydrogen red $C$-line, $\lambda_C = 656.28\text{ nm}$)

#### Cauchy Dispersion Relation:
$$n(\lambda) = A + \frac{B}{\lambda^2} + \frac{C}{\lambda^4}$$

With empirical constants for optical silicate glass:
- $A = 1.5046$
- $B = 4.20 \times 10^3\text{ nm}^2$
- $C = 5.80 \times 10^7\text{ nm}^4$

#### UI Engineering Implication:
Because blue light bends more sharply than red light ($n_F > n_C$), high-contrast background edges seen through the perimeter bevel split into subtle chromatic fringes. In digital display compositing, the differential angular refraction across standard $4.0\text{mm} - 6.0\text{mm}$ glass plate thickness translates to an optimal subpixel dispersion offset of $\pm 1.2\text{px}$ (calibrated for standard @2x Retina display density):
- Outward perimeter fringe: Red / amber shift ($+1.2\text{px}$ horizontal displacement `dx="1.2"`)
- Inward perimeter fringe: Cyan / blue shift ($-1.2\text{px}$ horizontal displacement `dx="-1.2"`)
- Neutral center: Unshifted green / master channel ($0\text{px}$ displacement `dx="0"`)

---

### 2.3. Fresnel Reflectivity (Schlick's Approximation)
The proportion of light reflected from the glass surface increases dramatically at shallow viewing angles, governed by the Fresnel equations. Schlick's approximation models this behavior:

$$R(\theta) = R_0 + (1 - R_0)(1 - \cos\theta)^5$$

Where normal incidence reflectance $R_0$ is:

$$R_0 = \left(\frac{n_1 - n_2}{n_1 + n_2}\right)^2 = \left(\frac{1.0 - 1.520}{1.0 + 1.520}\right)^2 = \left(\frac{-0.52}{2.52}\right)^2 \approx 0.04258 \quad (\approx 4.26\%)$$

#### Reflectance Curve Progression:
| Viewing Angle ($\theta$) | $\cos\theta$ | $(1 - \cos\theta)^5$ | Total Reflectivity $R(\theta)$ | Visual UI Manifestation |
|---|---|---|---|---|
| $0^\circ$ (Perpendicular center) | $1.0000$ | $0.000000$ | $4.26\%$ | High transmission ($95.74\%$), deep background clarity |
| $15^\circ$ | $0.9659$ | $0.000000$ ($4.6 \times 10^{-8}$) | $4.26\%$ | Negligible change, persistent core clarity |
| $30^\circ$ | $0.8660$ | $0.000043$ | $4.26\%$ | Minimal surface sheen accumulation |
| $45^\circ$ | $0.7071$ | $0.002155$ ($\approx 0.0022$) | $4.47\%$ | Subtle transition point; specular onset |
| $60^\circ$ | $0.5000$ | $0.031250$ ($\approx 0.0313$) | $7.25\%$ | Moderate highlight accumulation |
| $75^\circ$ | $0.2588$ | $0.223677$ ($\approx 0.2237$) | $25.67\%$ | Pronounced specular reflection on bevel curvature |
| $85^\circ$ | $0.0872$ | $0.633846$ ($\approx 0.6338$) | $64.94\%$ | Intense specular glint approaching grazing angle |
| $90^\circ$ (Grazing bevel edge) | $0.0000$ | $1.000000$ | $100.00\%$ ($\approx 98.5\%$ physical)* | Razor-sharp luminous specular rim highlight |

*\*Note: Schlick's theoretical mathematical limit evaluates to strictly $100.00\%$ at $\theta = 90^\circ$. In real-world physical optics and Apple UI rendering, microfacet surface roughness and anti-reflective characteristics yield an effective perceptual highlight peak of $\approx 98.50\%$.*

#### UI Engineering Implication:
A flat box border or single uniform stroke looks artificial because real glass has a specular highlight that surges to $\approx 98.5\%$ along grazing perimeter edges. To replicate this, UI borders must use directional multi-stop specular highlights (bright white at the top edge facing light, dark ambient occlusion at the bottom edge).*

---

### 2.4. Volumetric Absorption & Beer-Lambert Law
Light penetrating the thickness $z$ of the glass medium experiences wavelength-dependent volumetric absorption:

$$I(z) = I_0 \cdot \exp(-\alpha(\lambda) \cdot z)$$

Where:
- $I_0$ is initial incident light intensity
- $\alpha \approx 0.08\text{ mm}^{-1}$ (absorption coefficient for clear silicate glass)
- $z$ is effective optical path length ($4.0\text{ mm} - 6.0\text{ mm}$)

$$\text{Transmittance } T = \frac{I}{I_0} = e^{-0.08 \times 5.0} = e^{-0.40} \approx 0.6703 \quad (67\% \text{ direct transmission})$$

In Apple's material pipeline, this absorption is coupled with high-frequency scattering (blur) and vibrancy boost ($200\%$) to keep underlying colors saturated rather than washed out.

---

## 3. The Two Official System Variants

| Parameter | Variant 1: `regular` | Variant 2: `clear` |
|---|---|---|
| **Primary HIG Purpose** | Functional navigation, sidebars, tab bars, toolbars, alerts, popovers | Floating media decks, video controls, camera viewports, spatial HUDs |
| **Translucency / Opacity** | Medium translucent (`rgba(22, 28, 45, 0.52)`) | Highly translucent (`rgba(255, 255, 255, 0.07)`) |
| **Background Requirement** | Variable desktop backgrounds, scrolling lists, documents | Strictly visually rich media (photos, videos, spatial mesh) |
| **Diffusion Blur Radius** | $40\text{px} - 50\text{px}$ | $28\text{px} - 36\text{px}$ |
| **Vibrancy / Saturation** | $190\% - 210\%$ | $220\% - 240\%$ |
| **Luminance Adjustment** | $+3\% \text{ to } +5\%$ (`brightness(1.04)`) | Neutral (`brightness(1.00)`) |
| **Mandatory Dimming Layer** | None required (built-in contrast) | **35% Dark Scrim (`rgba(0,0,0,0.35)`)** required over bright media |
| **WCAG Contrast** | Guarantees AA ($\ge 4.5:1$) for SF Pro typography | Preserved via underlying 35% dimming layer |

### The 35% Dimming Layer Rule:
Official HIG statement: *"If the underlying content is bright, consider adding a dark dimming layer of 35% opacity (`rgba(0, 0, 0, 0.35)`)."*
In Web/Electron DOM structure, this requires a dedicated composite sibling or background element:
```html
<!-- Primary Contract DOM (Compatible with both PROJECT.md and Namespaced Selectors) -->
<div class="hud-deck-container liquid-glass-clear-container apple-liquid-glass-clear-container">
  <div class="hud-dimming-layer apple-liquid-glass-clear-scrim" aria-hidden="true"></div>
  <div class="liquid-glass-clear liquid-glass-clear-hud apple-liquid-glass-clear">
    <!-- Interactive foreground controls -->
  </div>
</div>
```

---

## 4. Web & Electron Realization Architecture

### 4.1. SVG Displacement & Chromatic Aberration Filter
Place this shared SVG definition once at the top of the HTML body or inside a hidden SVG defs sprite:

```html
<!-- Reusable Optical Liquid Glass SVG Filter Engine -->
<svg style="position: absolute; width: 0; height: 0; overflow: hidden;" aria-hidden="true">
  <defs>
    <filter id="hig-liquid-glass-dispersion" x="-15%" y="-15%" width="130%" height="130%">
      <!-- Step 1: Generate smooth gradient noise representing surface normal perturbation -->
      <feTurbulence type="fractalNoise" baseFrequency="0.015" numOctaves="2" result="surfaceNoise" />
      
      <!-- Step 2: Normalize and amplify gradients into X/Y displacement vectors -->
      <feColorMatrix type="matrix" in="surfaceNoise" result="normalVectors"
        values="1 0 0 0 0
                0 1 0 0 0
                0 0 1 0 0
                0 0 0 7 -2.8" />
                
      <!-- Step 3: Primary Snell Refraction Displacement (Green/Master channel) -->
      <feDisplacementMap in="SourceGraphic" in2="normalVectors" scale="16"
        xChannelSelector="R" yChannelSelector="G" result="refractedCenter" />
        
      <!-- Step 4: Chromatic Abbe Ray Separation (Red outward fringe) -->
      <feOffset in="refractedCenter" dx="1.2" dy="0" result="redFringe" />
      <feColorMatrix type="matrix" in="redFringe" result="redChannel"
        values="1 0 0 0 0
                0 0 0 0 0
                0 0 0 0 0
                0 0 0 1 0" />

      <!-- Step 5: Chromatic Abbe Ray Separation (Blue inward fringe) -->
      <feOffset in="refractedCenter" dx="-1.2" dy="0" result="blueFringe" />
      <feColorMatrix type="matrix" in="blueFringe" result="blueChannel"
        values="0 0 0 0 0
                0 0 0 0 0
                0 0 1 0 0
                0 0 0 1 0" />

      <!-- Step 6: Center Green Channel -->
      <feColorMatrix type="matrix" in="refractedCenter" result="greenChannel"
        values="0 0 0 0 0
                0 1 0 0 0
                0 0 0 0 0
                0 0 0 1 0" />

      <!-- Step 7: Recombine dispersed spectral rays -->
      <feBlend mode="screen" in="redChannel" in2="greenChannel" result="rgBlend" />
      <feBlend mode="screen" in="rgBlend" in2="blueChannel" result="dispersedFinal" />
    </filter>
  </defs>
</svg>
```

---

### 4.2. Production CSS Tokens & Material Classes

```css
/* ==========================================================================
   Apple Liquid Glass Design Tokens (HIG: materials#Liquid-Glass)
   ========================================================================== */
:root {
  /* Color Bases */
  --liquid-glass-regular-bg: rgba(22, 28, 45, 0.52);
  --liquid-glass-clear-bg: rgba(255, 255, 255, 0.07);
  --liquid-glass-dimming-scrim: rgba(0, 0, 0, 0.35);

  /* Specular Highlight Tokens (Fresnel R_90 and R_0) */
  --liquid-glass-specular-top: rgba(255, 255, 255, 0.42);
  --liquid-glass-specular-sub: rgba(255, 255, 255, 0.16);
  --liquid-glass-specular-rim: rgba(255, 255, 255, 0.14);
  --liquid-glass-ambient-bottom: rgba(0, 0, 0, 0.24);

  /* Shadow Elevation */
  --liquid-glass-shadow-regular: 
    0 24px 48px -12px rgba(0, 0, 0, 0.65),
    0 1px 3px 0 rgba(0, 0, 0, 0.20);
  --liquid-glass-shadow-clear: 
    0 28px 60px -15px rgba(0, 0, 0, 0.70),
    0 2px 4px 0 rgba(0, 0, 0, 0.25);
}

/* --------------------------------------------------------------------------
   Variant 1: Regular Liquid Glass (Navigation, Sidebars, Toolbars)
   Contract Aliases: .liquid-glass-regular (PROJECT.md) | .apple-liquid-glass-regular
   -------------------------------------------------------------------------- */
.liquid-glass-regular,
.apple-liquid-glass-regular {
  background: var(--liquid-glass-regular-bg);
  backdrop-filter: blur(48px) saturate(200%) brightness(1.04);
  -webkit-backdrop-filter: blur(48px) saturate(200%) brightness(1.04);
  border: 0.5px solid var(--liquid-glass-specular-rim);
  border-radius: 12px;
  box-shadow: 
    var(--liquid-glass-shadow-regular),
    /* Grazing Fresnel Specular Top Rim (1px razor highlight) */
    inset 0 1px 1px 0 var(--liquid-glass-specular-top),
    /* Secondary internal caustic glow */
    inset 0 2px 4px 0 var(--liquid-glass-specular-sub),
    /* Bottom ambient occlusion bevel */
    inset 0 -1px 1px 0 var(--liquid-glass-ambient-bottom);
}

/* --------------------------------------------------------------------------
   Variant 2: Clear Liquid Glass with Mandatory 35% Dimming Layer (Media HUDs)
   -------------------------------------------------------------------------- */
.hud-deck-container,
.liquid-glass-clear-container,
.apple-liquid-glass-clear-container {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
}

/* Mandatory 35% Dark Ambient Dimming Scrim */
.hud-dimming-layer,
.liquid-glass-scrim,
.apple-liquid-glass-clear-scrim {
  position: absolute;
  inset: 0;
  background: var(--liquid-glass-dimming-scrim);
  pointer-events: none;
  z-index: 1;
}

/* Clear Translucent Refractive Shell */
.liquid-glass-clear,
.liquid-glass-clear-hud,
.apple-liquid-glass-clear {
  position: relative;
  z-index: 2;
  background: var(--liquid-glass-clear-bg);
  backdrop-filter: url(#hig-liquid-glass-dispersion) blur(32px) saturate(220%);
  -webkit-backdrop-filter: blur(32px) saturate(220%);
  border: 0.5px solid rgba(255, 255, 255, 0.22);
  border-radius: 16px;
  box-shadow: 
    var(--liquid-glass-shadow-clear),
    /* Grazing Fresnel Top Rim */
    inset 0 1.5px 1.5px 0 rgba(255, 255, 255, 0.48),
    /* Internal Volume Glow */
    inset 0 3px 6px 0 rgba(255, 255, 255, 0.12),
    /* Bottom Edge Occlusion */
    inset 0 -1px 1px 0 rgba(0, 0, 0, 0.28);
}
```

---

## 5. Distinction Matrix: Liquid Glass vs Naive CSS Blur

| Dimension | Naive CSS Blur | Authentic Apple Liquid Glass |
|---|---|---|
| **Underlying Math** | Uniform 2D Gaussian Kernel $G(x,y) = \frac{1}{2\pi\sigma^2} e^{-\frac{x^2+y^2}{2\sigma^2}}$ | Snell's Law $n=1.520$ + Abbe Dispersion $V_d=58.6$ + Schlick Fresnel $R_0=4.3\%$ |
| **Pixel Displacement** | Zero. Pixels stay at exact coordinate positions | Non-zero. Edge normals displace background coordinates by $14\text{px}-18\text{px}$ |
| **Chromatic Splitting** | Monochromatic blur | Spectral separation of Red ($656\text{nm}$) and Blue ($486\text{nm}$) fringes |
| **Perimeter Edges** | Flat `1px solid rgba(255,255,255,0.1)` | Multi-stop Fresnel rim: top specular highlight ($98.5\%$), bottom occlusion |
| **Media Legibility** | Foreground text drowns over bright media | 35% dark dimming layer guarantees WCAG AA ($4.5:1$) contrast |
| **Layer Placement** | Frequently misplaced on whole background | Restricted exclusively to functional navigation layer |
| **Transient Controls** | Static styling on sliders/toggles | Adopts Liquid Glass appearance only during active user interaction |

---

## 6. Performance & Implementation Guardrails

1. **Avoid Multi-Filter Stacking in Scroll Views:**  
   Do not attach `<feDisplacementMap>` filters to repeated list items inside long scroll views. Limit the SVG displacement filter to top-level navigation shells, floating HUD panels, or modal overlays.
2. **Subordinate Cards Strategy:**  
   Subordinate content cards must use pure CSS multi-stop specular borders with standard CSS blur (`backdrop-filter: blur(...)`) to maintain a sustained 120 FPS on integrated GPUs.
3. **GPU Layer Promotion:**  
   Always declare `will-change: transform` or `transform: translateZ(0)` on Liquid Glass containers to ensure dedicated GPU compositing surfaces in Chromium/WebKit.
