# Ready-to-Use Prompts for AI Agents & LLMs

Copy and paste these battle-tested prompts directly into **Claude Code**, **ChatGPT**, **Google Antigravity 2.0**, **Codex**, **Cursor**, or **Windsurf** to get authentic, native Apple-grade designs with zero hallucinations and full HIG citations.

---

## 🇹🇷 Türkçe Prompts

### 1. Ana Sistem Promptu (Claude Code, ChatGPT, Codex, Antigravity)
Kopyala ve ajana yapıştır:

```text
Uygulamamın ekranlarını Apple'ın Human Interface Guidelines (HIG) kurallarına göre tasarla.

Sayfaları web sitesinden değil, doğrudan Apple'ın JSON adreslerinden oku:
1. Önce https://developer.apple.com/tutorials/data/design/human-interface-guidelines.json ile içindekileri al.
2. İşine yarayan her sayfayı https://developer.apple.com/tutorials/data/design/human-interface-guidelines/SAYFA.json biçiminde aç (en az layout, typography, color, tab-bars, lists-and-tables, sf-symbols ve materials).
3. İkonlarda SF Symbols, renklerde sistem renkleri (system colors), tipografide sistem fontu (Dynamic Type) kullan.
4. Her tasarım kararının yanına hangi HIG sayfasından ve anchor'dan aldığını yaz (Örnek: `// HIG: layout#Size-classes` veya karar tablosu).
5. Hafızandan veya tahminle kural uydurma; aldığın tüm değer ve prensipleri JSON'dan doğrulayarak aktar.
```

### 2. SwiftUI Ekran Tasarımı & Mimari İnceleme
```text
SwiftUI ile geliştirdiğim [Ekran Adı / Akış] ekranını Apple HIG standartlarına göre sıfırdan tasarla veya refactor et.
- Hedef platformlar: iOS 27+ (iPadOS uyumlu)
- Bileşen hiyerarşisi: Liquid Glass malzemeleri, navigation bar / toolbar, safe area boşlukları.
- Dinamik Tipler: Body için .body, başlıklar için semantik text style.
- SF Symbols: Yalnızca doğrulanmış SF Symbol isimleri kullan, rendering modlarını belirt (.hierarchical / .tint).
- Her bileşenin yanına ilgili HIG kararını dipnot olarak ekle.
```

### 3. Masaüstü & Web Uyarlaması (WPF / Electron / React)
```text
Apple'ın Human Interface Guidelines prensiplerini [WPF .NET 8 / React Tailwind / Electron] uygulamama uyarla:
- Görsel hiyerarşi, boşluk ritmi (8pt grid mantığı) ve semantik renk rollerini Apple HIG'den esinlenerek kur.
- Apple lisanslı varlıkları (SF Pro, SF Symbols glyph dosyaları) doğrudan kopyalama; yerine platform alternatiflerini (Segoe UI Variable / Segoe Fluent Icons veya Lucide) öner.
- Tasarım karar tablosunda her kararı "adapted from <slug>#<anchor>" formatında açıkla.
```

---

## 🇺🇸 English Prompts

### 1. Core System Prompt (Universal)
Copy & paste into your agent:

```text
Design my app's screens according to Apple's Human Interface Guidelines (HIG).

Read the guidelines directly from Apple's official JSON endpoints, not the web interface:
1. First, fetch https://developer.apple.com/tutorials/data/design/human-interface-guidelines.json for the full index.
2. Fetch each relevant page via https://developer.apple.com/tutorials/data/design/human-interface-guidelines/PAGE.json (at minimum: layout, typography, color, tab-bars, lists-and-tables, sf-symbols, and materials).
3. Use SF Symbols for iconography, system semantic colors for palettes, and system typography with Dynamic Type support.
4. Explicitly cite the source HIG slug and anchor for every single design decision (e.g. `// HIG: layout#Size-classes` or a decision table).
5. Never invent rules or symbol names from memory; strictly verify all measurements, principles, and tokens from the fetched JSON.
```

### 2. SwiftUI Screen Design & Audit
```text
Design and implement the [Screen Name] view in SwiftUI following the current Apple HIG.
- Targets: iOS 27+, iPadOS adaptive layout.
- Controls: Tab bar navigation, toolbar items, modal sheets, and safe area insets.
- Visuals: Standard materials and Liquid Glass layering where appropriate.
- Icons: Valid SF Symbols only with .hierarchical or .palette rendering modes.
- Output: Complete SwiftUI view code with inline `// HIG: page#section` citations and an audit summary table.
```

### 3. Non-Apple Adaptation (WPF, Electron, Web)
```text
Port Apple HIG design discipline to my [WPF .NET 8 / Web / Electron] project:
- Adapt structural principles: progressive disclosure, typography scales, light/dark semantic tokens, 44pt touch/pointer target minimums.
- Do NOT bundle proprietary Apple assets (SF Pro font files or SF Symbols artwork); recommend legal cross-platform alternatives (e.g. Segoe UI Variable, Lucide Icons, system-ui).
- Include a decision table citing `adapted from <slug>#<section>`.
```
