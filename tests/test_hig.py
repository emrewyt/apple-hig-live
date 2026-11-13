"""Unit tests for apple-hig-live (hig.py).
Tests parsing, rendering, platform filters, verification, symbol search, and CLI entry points.
"""
import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

# Add skills/apple-hig-live/scripts to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent.parent / "skills" / "apple-hig-live" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import hig  # noqa: E402


class TestHigHelpers(unittest.TestCase):
    def test_slug_of(self):
        self.assertEqual(
            hig.slug_of("doc://com.apple.HIG/documentation/Human-Interface-Guidelines/layout"),
            "layout",
        )
        self.assertEqual(
            hig.slug_of("/design/human-interface-guidelines/tab-bars#Best-practices"),
            "tab-bars",
        )
        self.assertEqual(
            hig.slug_of("https://developer.apple.com/tutorials/data/design/human-interface-guidelines/color.json"),
            "color",
        )
        self.assertIsNone(hig.slug_of(None))
        self.assertIsNone(hig.slug_of("https://example.com/other/path"))

    def test_resolve_slug(self):
        self.assertEqual(hig.resolve_slug("layout"), "layout")
        self.assertEqual(hig.resolve_slug("layout.json"), "layout")
        self.assertEqual(hig.resolve_slug("/layout/"), "layout")
        self.assertEqual(
            hig.resolve_slug("https://developer.apple.com/design/human-interface-guidelines/layout"),
            "layout",
        )
        self.assertEqual(
            hig.resolve_slug("https://developer.apple.com/design/human-interface-guidelines/tab-bars#Best-practices"),
            "tab-bars",
        )
        self.assertEqual(
            hig.resolve_slug("https://developer.apple.com/tutorials/data/design/human-interface-guidelines/materials.json"),
            "materials",
        )
        self.assertEqual(hig.resolve_slug(""), "")
        self.assertEqual(hig.resolve_slug(None), "")

    def test_plain(self):
        nodes = [
            {"type": "text", "text": "Hello "},
            {"type": "codeVoice", "code": "world"},
            {"type": "inlineHead", "inlineContent": [{"type": "text", "text": "!"}]},
        ]
        self.assertEqual(hig.plain(nodes), "Hello world!")
        self.assertEqual(hig.plain(None), "")

    def test_trim(self):
        self.assertEqual(hig.trim("Short text", 20), "Short text")
        self.assertEqual(hig.trim("This is a much longer text that needs trimming", 15), "This is a much…")


class TestHigRenderer(unittest.TestCase):
    def setUp(self):
        self.sample_doc = {
            "metadata": {"title": "Sample Component"},
            "references": {
                "doc://com.apple.HIG/documentation/Human-Interface-Guidelines/color": {
                    "title": "Color",
                    "role": "article",
                }
            },
            "primaryContentSections": [
                {
                    "kind": "content",
                    "content": [
                        {"type": "heading", "level": 2, "text": "Overview", "anchor": "Overview"},
                        {
                            "type": "paragraph",
                            "inlineContent": [
                                {"type": "text", "text": "Use standard colors from "},
                                {
                                    "type": "reference",
                                    "identifier": "doc://com.apple.HIG/documentation/Human-Interface-Guidelines/color",
                                },
                                {"type": "text", "text": "."},
                            ],
                        },
                        {
                            "type": "unorderedList",
                            "items": [
                                {
                                    "content": [
                                        {
                                            "type": "paragraph",
                                            "inlineContent": [{"type": "text", "text": "Item A"}],
                                        }
                                    ]
                                },
                                {
                                    "content": [
                                        {
                                            "type": "paragraph",
                                            "inlineContent": [{"type": "text", "text": "Item B"}],
                                        }
                                    ]
                                },
                            ],
                        },
                        {
                            "type": "table",
                            "rows": [
                                [
                                    [{"type": "paragraph", "inlineContent": [{"type": "text", "text": "Col 1"}]}],
                                    [{"type": "paragraph", "inlineContent": [{"type": "text", "text": "Col 2"}]}],
                                ],
                                [
                                    [{"type": "paragraph", "inlineContent": [{"type": "text", "text": "Val 1"}]}],
                                    [{"type": "paragraph", "inlineContent": [{"type": "text", "text": "Val 2"}]}],
                                ],
                            ],
                        },
                        {
                            "type": "aside",
                            "style": "note",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "inlineContent": [{"type": "text", "text": "Important aside notice."}],
                                }
                            ],
                        },
                        {
                            "type": "codeListing",
                            "syntax": "swift",
                            "code": ["let x = 10", "print(x)"],
                        },
                    ],
                }
            ],
        }

    def test_rendering(self):
        r = hig.Renderer(self.sample_doc)
        blocks = self.sample_doc["primaryContentSections"][0]["content"]
        rendered = r.blocks(blocks)

        self.assertIn("## Overview  {#Overview}", rendered)
        self.assertIn("Color (-> color)", rendered)
        self.assertIn("- Item A\n- Item B", rendered)
        self.assertIn("| Col 1 | Col 2 |", rendered)
        self.assertIn("> **Note:** Important aside notice.", rendered)
        self.assertIn("```swift\nlet x = 10\nprint(x)\n```", rendered)

    def test_rendering_special_blocks(self):
        doc = {
            "metadata": {"title": "Special Blocks"},
            "references": {
                "doc://com.apple.HIG/design/Human-Interface-Guidelines/icons": {
                    "title": "Icons",
                    "url": "/design/human-interface-guidelines/icons",
                }
            },
        }
        r = hig.Renderer(doc)
        blocks = [
            {"type": "thematicBreak"},
            {
                "type": "tabNavigator",
                "tabs": [
                    {
                        "title": "Tab 1",
                        "content": [{"type": "paragraph", "inlineContent": [{"type": "text", "text": "Tab 1 Content"}]}],
                    }
                ],
            },
            {
                "type": "links",
                "items": ["doc://com.apple.HIG/design/Human-Interface-Guidelines/icons"],
            },
        ]
        rendered = r.blocks(blocks)
        self.assertIn("---", rendered)
        self.assertIn("**Tab 1**", rendered)
        self.assertIn("Tab 1 Content", rendered)
        self.assertIn("Icons (-> icons)", rendered)


class TestHigFilters(unittest.TestCase):
    def test_platform_filter(self):
        blocks = [
            {"type": "heading", "level": 2, "text": "Platform considerations", "anchor": "Platform-considerations"},
            {"type": "heading", "level": 3, "text": "iOS", "anchor": "iOS"},
            {"type": "paragraph", "inlineContent": [{"type": "text", "text": "iOS text"}]},
            {"type": "heading", "level": 3, "text": "macOS", "anchor": "macOS"},
            {"type": "paragraph", "inlineContent": [{"type": "text", "text": "macOS text"}]},
            {"type": "heading", "level": 2, "text": "Specifications", "anchor": "Specifications"},
            {"type": "paragraph", "inlineContent": [{"type": "text", "text": "General spec text"}]},
        ]
        filtered = hig.select_blocks(blocks, platforms=["ios"], full=False)
        rendered = hig.Renderer({}).blocks(filtered)
        self.assertIn("iOS text", rendered)
        self.assertNotIn("macOS text", rendered)
        self.assertIn("General spec text", rendered)

    def test_pick_section(self):
        blocks = [
            {"type": "heading", "level": 2, "text": "First Section", "anchor": "First-Section"},
            {"type": "paragraph", "inlineContent": [{"type": "text", "text": "First body"}]},
            {"type": "heading", "level": 2, "text": "Second Section", "anchor": "Second-Section"},
            {"type": "paragraph", "inlineContent": [{"type": "text", "text": "Second body"}]},
        ]
        # Match by text
        picked = hig.pick_section(blocks, "Second Section")
        rendered = hig.Renderer({}).blocks(picked)
        self.assertNotIn("First body", rendered)
        self.assertIn("Second body", rendered)

        # Match by anchor with leading hash
        picked_hash = hig.pick_section(blocks, "#Second-Section")
        rendered_hash = hig.Renderer({}).blocks(picked_hash)
        self.assertIn("Second body", rendered_hash)

        # Match by hyphenated lowercase
        picked_norm = hig.pick_section(blocks, "second-section")
        rendered_norm = hig.Renderer({}).blocks(picked_norm)
        self.assertIn("Second body", rendered_norm)


class TestHigNewCommands(unittest.TestCase):
    def test_symbols_lookup(self):
        syms = hig.get_verified_symbols()
        self.assertIn("Navigation", syms)
        self.assertIn("gearshape", syms["Navigation"])

        buf = io.StringIO()
        with patch("sys.stdout", buf):
            code = hig.cmd_symbols(type("Args", (), {"query": "gear"})())
        self.assertEqual(code, 0)
        out = buf.getvalue()
        self.assertIn("gearshape", out)

    def test_prompt_command(self):
        buf_tr = io.StringIO()
        with patch("sys.stdout", buf_tr):
            code_tr = hig.cmd_prompt(type("Args", (), {"lang": "tr"})())
        self.assertEqual(code_tr, 0)
        self.assertIn("Apple'ın Human Interface Guidelines", buf_tr.getvalue())

        buf_en = io.StringIO()
        with patch("sys.stdout", buf_en):
            code_en = hig.cmd_prompt(type("Args", (), {"lang": "en"})())
        self.assertEqual(code_en, 0)
        self.assertIn("Human Interface Guidelines", buf_en.getvalue())

    def test_verify_command_valid_and_invalid(self):
        # Test mock page
        sample_doc = {
            "metadata": {"title": "Layout"},
            "primaryContentSections": [
                {
                    "kind": "content",
                    "content": [
                        {"type": "heading", "level": 2, "text": "Visual hierarchy", "anchor": "Visual-hierarchy"},
                        {"type": "heading", "level": 2, "text": "Size classes", "anchor": "Size-classes"},
                    ],
                }
            ],
        }

        with patch("hig.fetch", return_value=sample_doc):
            # Test simple slug#Anchor
            buf = io.StringIO()
            with patch("sys.stdout", buf):
                code = hig.cmd_verify(type("Args", (), {"citation": "layout#Size-classes", "no_cache": False})())
            self.assertEqual(code, 0)
            self.assertIn("VALID: Layout > Size classes", buf.getvalue())

            # Test full URL with anchor
            buf_url = io.StringIO()
            with patch("sys.stdout", buf_url):
                code_url = hig.cmd_verify(
                    type("Args", (), {"citation": "https://developer.apple.com/design/human-interface-guidelines/layout#Size-classes", "no_cache": False})()
                )
            self.assertEqual(code_url, 0)
            self.assertIn("VALID: Layout > Size classes", buf_url.getvalue())

            # Test .json endpoint with anchor
            buf_json = io.StringIO()
            with patch("sys.stdout", buf_json):
                code_json = hig.cmd_verify(
                    type("Args", (), {"citation": "layout.json#Size-classes", "no_cache": False})()
                )
            self.assertEqual(code_json, 0)
            self.assertIn("VALID: Layout > Size classes", buf_json.getvalue())

            # Test page only
            buf_page = io.StringIO()
            with patch("sys.stdout", buf_page):
                code_page = hig.cmd_verify(type("Args", (), {"citation": "layout", "no_cache": False})())
            self.assertEqual(code_page, 0)
            self.assertIn("VALID: Layout", buf_page.getvalue())

            # Test invalid anchor
            buf_err = io.StringIO()
            with patch("sys.stderr", buf_err):
                code_invalid = hig.cmd_verify(
                    type("Args", (), {"citation": "layout#NonExistentAnchor", "no_cache": False})()
                )
            self.assertEqual(code_invalid, 1)
            self.assertIn("INVALID: anchor 'NonExistentAnchor' not found", buf_err.getvalue())

            # Test empty / missing slug
            buf_empty = io.StringIO()
            with patch("sys.stderr", buf_empty):
                code_empty = hig.cmd_verify(
                    type("Args", (), {"citation": "#Size-classes", "no_cache": False})()
                )
            self.assertEqual(code_empty, 1)
            self.assertIn("INVALID: citation must include a valid page slug", buf_empty.getvalue())

    def test_search_command(self):
        mock_index = {
            "entries": {
                "tab-bars": {
                    "title": "Tab bars",
                    "abstract": "A tab bar lets people navigate between top-level sections.",
                    "group": "components",
                    "parent": "navigation-and-search",
                },
                "sidebars": {
                    "title": "Sidebars",
                    "abstract": "A sidebar appears on the leading side.",
                    "group": "components",
                    "parent": "navigation-and-search",
                },
            }
        }
        with patch("hig.build_index", return_value=mock_index):
            buf = io.StringIO()
            with patch("sys.stdout", buf):
                code = hig.cmd_search(type("Args", (), {"terms": ["tab", "bar"], "limit": 5})())
            self.assertEqual(code, 0)
            self.assertIn("tab-bars", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
