# 🍎 Apple HIG Live: Apple Human Interface Guidelines Skill for AI Coding Agents

**Teach your AI coding agent the entire Apple Human Interface Guidelines (HIG), live.** Design authentic, native iOS, iPadOS, macOS, watchOS, tvOS and visionOS interfaces with SF Symbols, system colors, SF Pro typography and Liquid Glass — straight from Apple's current docs, with every decision cited to its exact HIG page and anchor.

[![Stars](https://img.shields.io/github/stars/emrewyt/apple-hig-live?style=social)](https://github.com/emrewyt/apple-hig-live/stargazers)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/emrewyt/apple-hig-live/actions/workflows/ci.yml/badge.svg)](https://github.com/emrewyt/apple-hig-live/actions)
![Agent Skill](https://img.shields.io/badge/Agent%20Skill-SKILL.md-black)
![Antigravity 2.0](https://img.shields.io/badge/Antigravity%202.0-supported-4285f4)
![Claude Code](https://img.shields.io/badge/Claude%20Code-supported-d97757)
![Codex](https://img.shields.io/badge/Codex-supported-10a37f)
![Gemini CLI](https://img.shields.io/badge/Gemini%20CLI-supported-8e75ff)
![Cursor & Windsurf](https://img.shields.io/badge/Cursor%20%26%20Windsurf-supported-000000)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen)

> ⭐ **Star this repository** if you care about native, high-grade Apple design and want your AI agents to stop hallucinating UI rules!

---

## ⚡ The Problem: Why AI Agents Fail on Apple HIG

When you prompt an AI agent (Claude Code, ChatGPT, Codex, Antigravity) to *"design this screen following Apple's HIG"*, it usually produces generic, outdated, or hallucinated designs. Why?

**Apple's official design website (`developer.apple.com/design`) is rendered purely with client-side JavaScript.** 
When an AI agent opens the URL, it receives an empty HTML shell. (We tested 7 pages across Apple's design docs — all 7 returned completely blank!) As a result, agents hallucinate non-existent modifiers, invent fake SF Symbol names, or apply web patterns to native iOS/macOS apps.

### 💡 The Solution: Real-Time DocC JSON Endpoints

Apple serves the exact same rich content through its official DocC JSON tutorial API:
- **Index:** `https://developer.apple.com/tutorials/data/design/human-interface-guidelines.json`
- **Page (e.g. layout):** `https://developer.apple.com/tutorials/data/design/human-interface-guidelines/layout.json`

**Apple HIG Live** bridges this gap. It provides:
1. **A standard `SKILL.md` specification** for Claude Code, Antigravity 2.0, Codex, and Gemini CLI.
2. **A zero-dependency CLI parser (`hig.py`)** that fetches Apple's live JSON, strips image bloat (reducing payload by 90%), and formats crisp Markdown with section anchors.
3. **Automated Citation & Verification (`hig.py verify`)** ensuring zero hallucinations.
4. **Offline Resilience:** 24h page caching and 7d index caching with automatic fallback.

| Feature | Static HIG Copies / Cheat Sheets | **Apple HIG Live** |
|---|---|---|
| **Always Up-to-Date** (Liquid Glass, iOS 18+, visionOS) | ❌ Frozen at copy time | ✅ **Live runtime fetch, cached 24h** |
| **Apple Copyright Infringement** | ❌ Redistributes Apple's text | ✅ **None (fetched dynamically on-demand)** |
| **Repo Size & Maintenance** | ❌ Hundreds of markdown files to sync | ✅ **Single script, 0 external deps** |
| **Full HIG Coverage** | ❌ Curated subsets only | ✅ **Entire HIG via dynamic index crawler** |
| **Verifiable Citations** | ❌ Rare / fabricated | ✅ **Every single decision cites `slug#Anchor`** |
| **Platform Filtering** (iOS, macOS, visionOS) | ❌ No | ✅ **`--platform ios,macos` token trimmer** |

---

## 🚀 Quick Install

### Method 1: `npx skills`
```bash
npx skills add emrewyt/apple-hig-live
```

### Method 2: One-Line Automated Installer

Clone the repo and run the installer for your target agents:

```bash
git clone https://github.com/emrewyt/apple-hig-live.git
cd apple-hig-live

# macOS / Linux (All agents: Claude Code, Antigravity, Codex, Gemini)
./install.sh all

# Or install for a specific agent in project scope:
./install.sh antigravity project
./install.sh claude project
```

```powershell
# Windows (PowerShell)
powershell -ExecutionPolicy Bypass -File .\install.ps1

# Or target Antigravity 2.0 or Claude specifically:
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Target antigravity -Scope user
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Target claude -Scope project
```

#### Skill Destination Paths

| Agent | Global / User Scope | Project / Workspace Scope |
|---|---|---|
| **Google Antigravity 2.0** | `~/.gemini/config/skills/` | `.agents/skills/` |
| **Claude Code** | `~/.claude/skills/` | `.claude/skills/` |
| **OpenAI Codex** | `~/.codex/skills/` | `.codex/skills/` |
| **Gemini CLI** | `~/.gemini/skills/` | `.gemini/skills/` |
| **Cursor / Windsurf** | `~/.cursor/skills/` | `.cursor/skills/` |

---

## 📋 Ready-to-Use Prompts (Zero Install Option)

Don't want to install anything? You can copy-paste the official prompt directly into **ChatGPT (GPT-4o)**, **Claude Code**, **Cursor**, or **Windsurf**:

### 🇹🇷 Türkçe Prompt
```text
Uygulamamın ekranlarını Apple'ın Human Interface Guidelines (HIG) kurallarına göre tasarla.

Sayfaları web sitesinden değil, doğrudan Apple'ın JSON adreslerinden oku:
1. Önce https://developer.apple.com/tutorials/data/design/human-interface-guidelines.json ile içindekileri al.
2. İşine yarayan her sayfayı https://developer.apple.com/tutorials/data/design/human-interface-guidelines/SAYFA.json biçiminde aç (en az layout, typography, color, tab-bars, lists-and-tables, sf-symbols ve materials).
3. İkonlarda SF Symbols, renklerde sistem renkleri (system colors), tipografide sistem fontu (Dynamic Type) kullan.
4. Her tasarım kararının yanına hangi HIG sayfasından ve anchor'dan aldığını yaz (Örnek: `// HIG: layout#Size-classes` veya karar tablosu).
5. Hafızandan veya tahminle kural uydurma; aldığın tüm değer ve prensipleri JSON'dan doğrulayarak aktar.
```

### 🇺🇸 English Prompt
```text
Design my app's screens according to Apple's Human Interface Guidelines (HIG).

Read the guidelines directly from Apple's official JSON endpoints, not the web interface:
1. First, fetch https://developer.apple.com/tutorials/data/design/human-interface-guidelines.json for the full index.
2. Fetch each relevant page via https://developer.apple.com/tutorials/data/design/human-interface-guidelines/PAGE.json (at minimum: layout, typography, color, tab-bars, lists-and-tables, sf-symbols, and materials).
3. Use SF Symbols for iconography, system semantic colors for palettes, and system typography with Dynamic Type support.
4. Explicitly cite the source HIG slug and anchor for every single design decision (e.g. `// HIG: layout#Size-classes` or a decision table).
5. Never invent rules or symbol names from memory; strictly verify all measurements, principles, and tokens from the fetched JSON.
```

*(See [PROMPTS.md](PROMPTS.md) for more specialized prompts: SwiftUI audits, Desktop/WPF adaptations, and visionOS).*

---

## 🛠️ CLI Reference (`skills/apple-hig-live/scripts/hig.py`)

The bundled standalone CLI works with **Python 3.8+** using **only the standard library**.

```bash
# 1. Fetch & render pages as clean Markdown (with platform filtering)
python hig.py page layout typography color --platform ios

# 2. View section outline (headings and anchors only to save tokens)
python hig.py page layout --outline

# 3. Read an exact section
python hig.py page materials --section "Liquid Glass"

# 4. Search the live HIG index by keyword
python hig.py search "tab bar navigation"

# 5. Look up verified SF Symbols (never hallucinate icon names)
python hig.py symbols gear

# 6. Verify a design citation before submitting code
python hig.py verify layout#Size-classes

# 7. Print ready-to-copy agent prompts
python hig.py prompt --lang tr
python hig.py prompt --lang en
```

---

## 🔍 Verifiable Decision Audit Trail

Every design produced by an agent using this skill ends with a structured decision log:

| Decision | Rule Applied | HIG Citation |
|---|---|---|
| Sidebar on iPad, Tab Bar on iPhone | Switch navigation structure based on size class; preserve functionality | `layout#Size-classes` |
| Dynamic Type across all labels | Use `.body`, `.headline`, `.subheadline` text styles | `typography#Supporting-Dynamic-Type` |
| Floating navigation layer | Use standard Liquid Glass material for tab bars | `materials#Liquid-Glass` |
| Iconography | `Label("Settings", systemImage: "gearshape")` | `sf-symbols` |

---

## 🖥️ Building for Windows (WPF .NET 8), Electron or Web?

Apple HIG Live is not just for iOS developers! It is widely used by developers who want to bring **Apple-grade design polish and discipline** to **WPF (.NET 8)**, **Electron**, and **React/Tailwind** apps.

- **Port Principles:** Spacing scale (8pt grid), progressive disclosure, clear visual hierarchy, light/dark semantic color tokens, and accessible tap/click targets (44×44 pt).
- **Asset Respect:** Automatically guides agents **not** to bundle proprietary Apple assets (SF Pro fonts, SF Symbols glyphs) in non-Apple software, suggesting compliant platform alternatives like *Segoe UI Variable* and *Lucide Icons*.
- Read [references/non-apple-targets.md](skills/apple-hig-live/references/non-apple-targets.md) for full guidelines.

---

## 📂 Project Structure

```text
apple-hig-live/
├── .github/
│   ├── workflows/ci.yml           # Automated cross-platform tests (Py 3.8-3.12)
│   └── ISSUE_TEMPLATE/            # Bug reports and feature requests
├── skills/
│   └── apple-hig-live/
│       ├── SKILL.md               # Standard skill contract for AI agents
│       ├── scripts/
│       │   └── hig.py             # Zero-dependency DocC JSON parser & CLI
│       └── references/
│           ├── page-map.md        # Task-to-HIG slug mapping catalog
│           ├── sf-symbols.md      # Verified SF Symbols catalog & guidelines
│           ├── non-apple-targets.md # Adapting HIG to WPF, Electron, and Web
│           └── json-schema.md     # DocC JSON schema specification
├── tests/
│   └── test_hig.py                # Comprehensive automated unit test suite
├── install.sh                     # Linux / macOS installer
├── install.ps1                    # Windows PowerShell installer
├── PROMPTS.md                     # Copy-paste prompts (TR & EN)
├── CONTRIBUTING.md                # Contribution guidelines
├── CODE_OF_CONDUCT.md             # Contributor Covenant CoC
├── SECURITY.md                    # Security policy
├── LICENSE                        # MIT License
└── README.md                      # Documentation & SEO hub
```

---

## 🧪 Testing & Verification

Run the test suite locally:
```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## ⚖️ Disclaimer

**Apple HIG Live** is an independent open-source developer tool and is **not** affiliated with, endorsed by, or sponsored by Apple Inc. 
Apple, iOS, iPadOS, macOS, watchOS, tvOS, visionOS, SF Symbols, SF Pro, and Liquid Glass are registered trademarks of Apple Inc. 
Content is fetched dynamically at runtime from Apple's public servers and is never redistributed within this repository.

---

## 📄 License

Licensed under the [MIT License](LICENSE).

---

### 👨‍💻 Created by
**Emre** ([@emrewyt](https://github.com/emrewyt)) · Founder of **FLUVEA**

<sub>**SEO Keywords & Search Indexing:** Apple Human Interface Guidelines, Apple HIG, iOS design system, SwiftUI agent, Claude Code skill, Antigravity 2.0 skill, Codex skill, Gemini CLI skill, SF Symbols, Liquid Glass design, Apple design guidelines, visionOS development, macOS app design, native UI/UX design, AI coding assistant, SKILL.md specification.</sub>
