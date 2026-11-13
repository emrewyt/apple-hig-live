# Contributing to Apple HIG Live

Thank you for your interest in contributing to **Apple HIG Live**! We welcome bug fixes, documentation improvements, new platform guides, and expanded SF Symbols mappings.

---

## How to Contribute

1. **Fork the repository** on GitHub.
2. **Clone your fork**:
   ```bash
   git clone https://github.com/emrewyt/apple-hig-live.git
   cd apple-hig-live
   ```
3. **Create a branch**:
   ```bash
   git checkout -b feature/my-new-feature
   ```
4. **Make your changes** following our guidelines:
   - Zero third-party dependencies for `hig.py` (standard library only).
   - Python 3.8+ compatibility.
   - Run tests: `python -m unittest discover -s tests -p "test_*.py"`.
5. **Commit and push**:
   ```bash
   git commit -m "feat: add support for new HIG components"
   git push origin feature/my-new-feature
   ```
6. **Open a Pull Request** describing your changes.

---

## Reporting Rendering Bugs

If Apple modifies a DocC page layout and `hig.py` renders it improperly:
1. Run `python hig.py page <slug> --raw > page.json` to capture the raw Apple JSON.
2. Note the slug and section.
3. Open an issue with the snippet and expected Markdown output.

---

## Adding Verified SF Symbols

To add common symbols to `references/sf-symbols.md`:
- Verify the symbol name in Apple's official **SF Symbols 6+** macOS app.
- Ensure the symbol is available on standard iOS / macOS targets.
- Categorize appropriately.

Thank you for helping developers build beautiful, native Apple-quality experiences!
