"""End-to-End Specification & Physics Test Suite for Apple HIG Live
File: tests/test_e2e_specs.py

Genuine file-parsing unit test suite asserting content from:
  - skills/apple-hig-live/references/liquid-glass-physics.md
  - skills/apple-hig-live/references/components-and-controls.md
  - skills/apple-hig-live/references/designer-svg-standards.md
  - skills/apple-hig-live/SKILL.md

Verifies:
  1. DocC JSON endpoints, slug resolution, and all 21 reference citation anchors parsed from files.
  2. Liquid Glass optical physics engine constants, formulas, system variants, and SVG displacement filter parsed from files.
  3. macOS app icon squircle geometry, cubic Bézier path data, tangent continuity, and 4-tier shadow stack parsed from files.
  4. Forbidden control patterns governance table and authentic control dimensions parsed from files.
  5. Typographical weight tables, SF Symbols stroke mappings, and UI hierarchy parsed from files.
  6. Designer-grade SVG templates, CASpring animation easing curves, and SKILL.md alignment parsed from files.
"""

import math
import re
import sys
import unittest
from pathlib import Path


def _resolve_repo_root() -> Path:
    """Resolves the apple-hig-live directory whether executed from tests/ or workspace."""
    candidate = Path(__file__).resolve().parent.parent
    if (candidate / "skills" / "apple-hig-live").exists():
        return candidate
    cwd = Path.cwd()
    if (cwd / "apple-hig-live" / "skills" / "apple-hig-live").exists():
        return cwd / "apple-hig-live"
    if (cwd / "skills" / "apple-hig-live").exists():
        return cwd
    for p in Path(__file__).resolve().parents:
        if (p / "apple-hig-live" / "skills" / "apple-hig-live").exists():
            return p / "apple-hig-live"
        if (p / "skills" / "apple-hig-live").exists():
            return p
    return candidate


REPO_ROOT = _resolve_repo_root()
SKILL_DIR = REPO_ROOT / "skills" / "apple-hig-live"
REFS_DIR = SKILL_DIR / "references"
SCRIPTS_DIR = SKILL_DIR / "scripts"
SKILL_FILE = SKILL_DIR / "SKILL.md"

sys.path.insert(0, str(SCRIPTS_DIR))
import hig  # noqa: E402


class TestDocCEndpointsAndAnchors(unittest.TestCase):
    """Verifies DocC JSON endpoint querying, slug extraction, and live reference citations parsed from disk."""

    @classmethod
    def setUpClass(cls):
        cls.lg_text = (REFS_DIR / "liquid-glass-physics.md").read_text(encoding="utf-8")
        cls.ctrl_text = (REFS_DIR / "components-and-controls.md").read_text(encoding="utf-8")
        cls.svg_text = (REFS_DIR / "designer-svg-standards.md").read_text(encoding="utf-8")
        cls.skill_text = SKILL_FILE.read_text(encoding="utf-8")

    def test_slug_extraction_docc_uri(self):
        slug = hig.slug_of("doc://com.apple.HIG/documentation/Human-Interface-Guidelines/materials")
        self.assertEqual(slug, "materials")

    def test_slug_extraction_web_url_with_anchor(self):
        slug = hig.slug_of("https://developer.apple.com/design/human-interface-guidelines/materials#Liquid-Glass")
        self.assertEqual(slug, "materials")

    def test_resolve_slug_normalizes_extensions_and_slashes(self):
        self.assertEqual(hig.resolve_slug("materials.json"), "materials")
        self.assertEqual(hig.resolve_slug("/materials/"), "materials")
        self.assertEqual(hig.resolve_slug("segmented-controls"), "segmented-controls")

    def test_all_reference_file_citations_format_valid(self):
        """Extracts all citations directly from project markdown files and validates format."""
        citation_re = re.compile(r"(?:`|\b)([a-z0-9-]+#[A-Za-z0-9_-]+)(?:`|\b)")
        all_citations = set()
        for text in [self.lg_text, self.ctrl_text, self.svg_text, self.skill_text]:
            all_citations.update(citation_re.findall(text))
        all_citations.discard("slug#Anchor")  # documentation placeholder

        self.assertGreaterEqual(len(all_citations), 20, "Should find at least 20 verified citations across files")
        format_re = re.compile(r"^[a-z0-9-]+#[A-Za-z0-9_-]+$")
        for citation in sorted(all_citations):
            self.assertTrue(format_re.match(citation), f"Citation failed format check: {citation}")

    def test_all_extracted_citation_slugs_resolve(self):
        """Ensures every slug in every extracted citation resolves via hig.resolve_slug."""
        citation_re = re.compile(r"(?:`|\b)([a-z0-9-]+#[A-Za-z0-9_-]+)(?:`|\b)")
        all_citations = set()
        for text in [self.lg_text, self.ctrl_text, self.svg_text, self.skill_text]:
            all_citations.update(citation_re.findall(text))
        all_citations.discard("slug#Anchor")

        for citation in all_citations:
            slug, _ = citation.split("#", 1)
            self.assertEqual(hig.resolve_slug(slug), slug, f"Slug {slug} failed normalization")

    def test_invalid_citation_rejected(self):
        invalid_citations = [
            "materials#",
            "#Liquid-Glass",
            "materials##anchor",
            "not a citation",
        ]
        citation_pattern = re.compile(r"^[a-z0-9-]+#[A-Za-z0-9_-]+$")
        for citation in invalid_citations:
            self.assertFalse(citation_pattern.match(citation), f"Should not match invalid citation: {citation}")

    def test_core_citations_exist_in_project_files(self):
        """Asserts mandatory Apple HIG citations are present in the reference documents."""
        combined_text = "\n".join([self.lg_text, self.ctrl_text, self.svg_text, self.skill_text])
        mandatory_citations = [
            "materials#Liquid-Glass",
            "color#Liquid-Glass-color",
            "segmented-controls#Best-practices",
            "buttons#Push-buttons",
            "toggles#Switches",
            "sliders#macOS",
            "app-icons#Specifications",
            "motion#Best-practices",
        ]
        for citation in mandatory_citations:
            self.assertIn(citation, combined_text, f"Mandatory citation {citation} missing from references")


class TestLiquidGlassPhysicsEngine(unittest.TestCase):
    """Verifies optical physics equations adhering to HIG materials#Liquid-Glass parsed from disk."""

    @classmethod
    def setUpClass(cls):
        cls.filepath = REFS_DIR / "liquid-glass-physics.md"
        cls.lg_text = cls.filepath.read_text(encoding="utf-8")
        cls.skill_text = SKILL_FILE.read_text(encoding="utf-8")

    def test_optical_constants_parsed_from_markdown(self):
        """Parses n2, Vd, Fraunhofer lines, theta_c, and R0 from liquid-glass-physics.md."""
        m_n2 = re.search(r"n_2\s*=\s*(1\.\d+)", self.lg_text)
        self.assertIsNotNone(m_n2, "Refractive index n_2 not found in liquid-glass-physics.md")
        n2 = float(m_n2.group(1))
        self.assertEqual(n2, 1.520)

        m_vd = re.search(r"V_d.*?(\d+\.\d+)", self.lg_text)
        self.assertIsNotNone(m_vd, "Abbe number V_d not found in liquid-glass-physics.md")
        vd = float(m_vd.group(1))
        self.assertEqual(vd, 58.6)

        m_nd = re.search(r"n_d\s*=\s*(1\.\d+)", self.lg_text)
        m_nf = re.search(r"n_F\s*=\s*(1\.\d+)", self.lg_text)
        m_nc = re.search(r"n_C\s*=\s*(1\.\d+)", self.lg_text)
        self.assertTrue(m_nd and m_nf and m_nc, "Fraunhofer spectral lines missing from liquid-glass-physics.md")
        self.assertEqual(float(m_nd.group(1)), 1.5200)
        self.assertEqual(float(m_nf.group(1)), 1.5250)
        self.assertEqual(float(m_nc.group(1)), 1.5162)

        m_tc = re.search(r"\\theta_c\s*=.*?\\approx\s*(\d+\.\d+)", self.lg_text)
        self.assertIsNotNone(m_tc, "Critical angle theta_c not found in liquid-glass-physics.md")
        self.assertAlmostEqual(float(m_tc.group(1)), 41.14, delta=0.01)

        m_r0 = re.search(r"R_0.*?(\d+\.\d+)\s*\\quad", self.lg_text)
        self.assertIsNotNone(m_r0, "Fresnel normal reflectance R_0 not found in liquid-glass-physics.md")
        self.assertAlmostEqual(float(m_r0.group(1)), 0.04258, delta=0.0001)

    def test_abbe_dispersion_calculation_from_parsed_indices(self):
        """Verifies Abbe number Vd = (nd - 1) / (nF - nC) calculated from parsed values."""
        m_nd = re.search(r"n_d\s*=\s*(1\.\d+)", self.lg_text)
        m_nf = re.search(r"n_F\s*=\s*(1\.\d+)", self.lg_text)
        m_nc = re.search(r"n_C\s*=\s*(1\.\d+)", self.lg_text)
        nd = float(m_nd.group(1))
        nf = float(m_nf.group(1))
        nc = float(m_nc.group(1))

        calculated_vd = (nd - 1.0) / (nf - nc)
        self.assertAlmostEqual(calculated_vd, 59.09, delta=0.1)

        m_vd = re.search(r"V_d.*?(\d+\.\d+)", self.lg_text)
        documented_vd = float(m_vd.group(1))
        self.assertAlmostEqual(documented_vd, 58.6, delta=0.1)
        self.assertLess(abs(calculated_vd - documented_vd), 1.0)

    def test_critical_angle_calculation_from_parsed_index(self):
        """Calculates critical angle theta_c = arcsin(1/n) from parsed n2 and verifies match."""
        m_n2 = re.search(r"n_2\s*=\s*(1\.\d+)", self.lg_text)
        n2 = float(m_n2.group(1))
        calculated_theta_c = math.degrees(math.asin(1.0 / n2))
        self.assertAlmostEqual(calculated_theta_c, 41.14, delta=0.01)

        m_tc = re.search(r"\\theta_c\s*=.*?\\approx\s*(\d+\.\d+)", self.lg_text)
        documented_theta_c = float(m_tc.group(1))
        self.assertAlmostEqual(calculated_theta_c, documented_theta_c, delta=0.01)

    def test_snell_refraction_angle_from_parsed_index(self):
        """Verifies Snell's law refraction angles using the parsed refractive index."""
        m_n2 = re.search(r"n_2\s*=\s*(1\.\d+)", self.lg_text)
        n2 = float(m_n2.group(1))

        # Incidence at 30 deg in air (n1 = 1.0)
        theta1_deg = 30.0
        sin_theta2 = math.sin(math.radians(theta1_deg)) / n2
        theta2_deg = math.degrees(math.asin(sin_theta2))
        self.assertAlmostEqual(theta2_deg, 19.20, delta=0.05)

        # Normal incidence (0 deg)
        self.assertAlmostEqual(math.degrees(math.asin(math.sin(0.0) / n2)), 0.0)

        # Total internal reflection when exiting glass at 50 deg > theta_c
        sin_exit = math.sin(math.radians(50.0)) * n2
        self.assertGreater(sin_exit, 1.0, "Ray at 50 deg should exceed critical angle and undergo TIR")

    def test_fresnel_reflectance_from_parsed_indices(self):
        """Verifies Schlick Fresnel reflectivity calculated from parsed n2."""
        m_n2 = re.search(r"n_2\s*=\s*(1\.\d+)", self.lg_text)
        n2 = float(m_n2.group(1))
        n1 = 1.0
        r0 = ((n1 - n2) / (n1 + n2)) ** 2
        self.assertAlmostEqual(r0, 0.04258, delta=0.0001)

        # Grazing angle 90 deg: (1 - cos(90))^5 = 1.0 -> R(90) = 1.0
        r90 = r0 + (1.0 - r0) * ((1.0 - math.cos(math.radians(90.0))) ** 5)
        self.assertAlmostEqual(r90, 1.0, delta=1e-5)

    def test_clear_glass_dimming_scrim_opacity_parsed_from_files(self):
        """Parses the mandatory 35% dimming layer scrim opacity from liquid-glass-physics.md and SKILL.md."""
        m_scrim_css = re.search(r"--liquid-glass-dimming-scrim:\s*rgba\(0,\s*0,\s*0,\s*([0-9.]+)\)", self.lg_text)
        self.assertIsNotNone(m_scrim_css, "--liquid-glass-dimming-scrim token missing from liquid-glass-physics.md")
        self.assertEqual(float(m_scrim_css.group(1)), 0.35)

        m_scrim_skill = re.search(r"rgba\(0,\s*0,\s*0,\s*([0-9.]+)\)", self.skill_text)
        self.assertIsNotNone(m_scrim_skill, "Scrim rgba missing from SKILL.md")
        self.assertEqual(float(m_scrim_skill.group(1)), 0.35)

        self.assertIn("35%", self.lg_text)
        self.assertIn("35%", self.skill_text)

    def test_liquid_glass_system_variants_and_classes_parsed(self):
        """Verifies both regular and clear variants and their production CSS classes in the document."""
        self.assertIn("Variant 1: `regular`", self.lg_text)
        self.assertIn("Variant 2: `clear`", self.lg_text)

        required_classes = [
            ".apple-liquid-glass-regular",
            ".apple-liquid-glass-clear-container",
            ".apple-liquid-glass-clear-scrim",
            ".apple-liquid-glass-clear",
        ]
        for cls in required_classes:
            self.assertIn(cls, self.lg_text, f"CSS class {cls} missing from liquid-glass-physics.md")

    def test_svg_displacement_filter_specification_parsed(self):
        """Verifies SVG displacement filter definition in liquid-glass-physics.md."""
        self.assertIn('id="hig-liquid-glass-dispersion"', self.lg_text)
        self.assertIn('<feTurbulence', self.lg_text)
        self.assertIn('<feColorMatrix', self.lg_text)
        self.assertIn('<feDisplacementMap', self.lg_text)
        self.assertIn('scale="16"', self.lg_text)
        self.assertIn('<feOffset', self.lg_text)
        self.assertIn('<feBlend', self.lg_text)


class TestSquircleMathAndIconography(unittest.TestCase):
    """Verifies macOS app icon geometry, Lamé superellipse math, and continuous curvature parsed from disk."""

    @classmethod
    def setUpClass(cls):
        cls.filepath = REFS_DIR / "designer-svg-standards.md"
        cls.svg_text = cls.filepath.read_text(encoding="utf-8")

    def test_macos_app_icon_dimensions_parsed_from_markdown(self):
        """Parses canvas size, body size, padding margins, and corner radius from markdown table."""
        m_canvas = re.search(r"\*\*Canvas Size\*\*\s*\|\s*(\d+)\s*[×x]\s*(\d+)\s*px", self.svg_text)
        m_body = re.search(r"\*\*Squircle Body Size\*\*\s*\|\s*(\d+)\s*[×x]\s*(\d+)\s*px", self.svg_text)
        m_margin = re.search(r"\*\*Canvas Margins \(Padding\)\*\*\s*\|\s*(\d+)\s*px", self.svg_text)
        m_radius = re.search(r"\*\*Corner Radius \(\$r\$\)\*\*\s*\|\s*(\d+\.\d+)\s*px", self.svg_text)
        m_radius_ratio = re.search(r"(\d+(?:\.\d+)?)%\s*of body width", self.svg_text)

        self.assertTrue(all([m_canvas, m_body, m_margin, m_radius, m_radius_ratio]), "Squircle specs table missing fields")

        canvas_size = int(m_canvas.group(1))
        body_size = int(m_body.group(1))
        margin = int(m_margin.group(1))
        radius = float(m_radius.group(1))
        ratio = float(m_radius_ratio.group(1))

        self.assertEqual(canvas_size, 1024)
        self.assertEqual(body_size, 824)
        self.assertEqual(margin, 100)
        self.assertEqual(body_size + 2 * margin, canvas_size)
        self.assertAlmostEqual(radius, 185.4, delta=0.01)
        self.assertAlmostEqual(body_size * (ratio / 100.0), radius, delta=0.01)

    def test_lame_superellipse_parameters_parsed(self):
        """Parses exponent and center/semi-axis parameters for Lamé superellipse."""
        m_exp = re.search(r"n\s*\\approx\s*(\d+\.\d+)\s*-\s*(\d+\.\d+)", self.svg_text)
        self.assertIsNotNone(m_exp, "Lamé superellipse exponent range missing from designer-svg-standards.md")
        n_min, n_max = float(m_exp.group(1)), float(m_exp.group(2))
        self.assertGreaterEqual(n_min, 4.0)
        self.assertLessEqual(n_max, 5.0)

        # Lamé equation |x/a|^n + |y/a|^n <= 1 for center (0,0) and edge points
        a = 412.0
        n = 4.2
        # Center inside
        self.assertLess((abs(0 / a) ** n) + (abs(0 / a) ** n), 1.0)
        # Point near edge inside
        self.assertLess((abs(390 / a) ** n) + (abs(0 / a) ** n), 1.0)
        # Corner of bounding box outside
        self.assertGreater((abs(412 / a) ** n) + (abs(412 / a) ** n), 1.0)

    def test_cubic_bezier_path_data_parsed_from_svg_standards(self):
        """Parses the cubic Bézier path data from designer-svg-standards.md and verifies geometry."""
        m_path = re.search(r'<path d="([^"]+)"', self.svg_text)
        self.assertIsNotNone(m_path, "Squircle cubic Bézier path data missing from designer-svg-standards.md")
        path_str = m_path.group(1)

        coords = [(float(x), float(y)) for x, y in re.findall(r"([\d.]+),([\d.]+)", path_str)]
        self.assertEqual(len(coords), 37, "Path must contain 37 coordinate points (1 M + 12 C segments * 3)")

        xs = [c[0] for c in coords]
        ys = [c[1] for c in coords]

        self.assertEqual(min(xs), 100.0)
        self.assertEqual(max(xs), 924.0)
        self.assertEqual(max(xs) - min(xs), 824.0, "Squircle width must be exactly 824px")

        self.assertEqual(min(ys), 100.0)
        self.assertEqual(max(ys), 924.0)
        self.assertEqual(max(ys) - min(ys), 824.0, "Squircle height must be exactly 824px")

        center_x = (min(xs) + max(xs)) / 2.0
        center_y = (min(ys) + max(ys)) / 2.0
        self.assertEqual((center_x, center_y), (512.0, 512.0), "Squircle must be centered at (512, 512)")

    def test_cubic_bezier_tangent_continuity_verified(self):
        """Verifies C1 tangent continuity across the segment junction knot parsed from the path."""
        m_path = re.search(r'<path d="([^"]+)"', self.svg_text)
        coords = [(float(x), float(y)) for x, y in re.findall(r"([\d.]+),([\d.]+)", m_path.group(1))]

        # Segment 1 end: P2 = coords[2], P3 = coords[3] (knot)
        # Segment 2 start: Q0 = coords[3], Q1 = coords[4]
        p2 = coords[2]
        p3 = coords[3]
        q1 = coords[4]

        v_in = (round(p3[0] - p2[0], 4), round(p3[1] - p2[1], 4))
        v_out = (round(q1[0] - p3[0], 4), round(q1[1] - p3[1], 4))

        self.assertEqual(v_in, v_out, f"Tangent discontinuity at knot: incoming {v_in} != outgoing {v_out}")
        self.assertEqual(v_in, (59.2, 24.6))

    def test_four_tier_drop_shadow_stack_parsed_from_markdown(self):
        """Parses the 4-tier optical drop shadow specification and SVG filter tiers."""
        self.assertIn("Direct Drop Shadow", self.svg_text)
        self.assertIn("Ambient Ground Shadow", self.svg_text)
        self.assertIn("Contact Edge Shadow", self.svg_text)
        self.assertIn("Specular Rim Light & Inner Bevel", self.svg_text)

        # Verify SVG filter feDropShadow tiers
        drops = re.findall(r'<feDropShadow\s+([^>]+)/>', self.svg_text)
        self.assertGreaterEqual(len(drops), 3, "SVG filter must contain at least 3 feDropShadow layers")

        results = [re.search(r'result="([^"]+)"', d).group(1) for d in drops[:3]]
        self.assertEqual(results, ["ambient", "direct", "contact"])

        dys = [re.search(r'dy="([^"]+)"', d).group(1) for d in drops[:3]]
        self.assertEqual(dys, ["40", "20", "4"])


class TestForbiddenControlPatternsGovernance(unittest.TestCase):
    """Verifies detection and prohibition of non-Apple control patterns parsed from disk."""

    @classmethod
    def setUpClass(cls):
        cls.ctrl_filepath = REFS_DIR / "components-and-controls.md"
        cls.ctrl_text = cls.ctrl_filepath.read_text(encoding="utf-8")
        cls.lg_text = (REFS_DIR / "liquid-glass-physics.md").read_text(encoding="utf-8")
        cls.svg_text = (REFS_DIR / "designer-svg-standards.md").read_text(encoding="utf-8")

    def test_forbidden_control_patterns_table_parsed(self):
        """Parses Section 5 of components-and-controls.md and asserts all 7 anti-patterns are documented."""
        forbidden_rows = re.findall(r"\|\s*\*\*(\d+)\*\*\s*\|\s*\*\*([^*]+)\*\*", self.ctrl_text)
        self.assertEqual(len(forbidden_rows), 7, "Section 5 must document exactly 7 forbidden anti-patterns")

        pattern_names = [name.strip() for _, name in forbidden_rows]
        expected_patterns = [
            'Custom Thick "Dispersion" Slider Tracks',
            "Oversized / Glowing Neon Toggles",
            "Sharp 90° Rectangular Tabs or Material Underline Tabs",
            "Arbitrary Saturated Multi-Color Gradient Cards",
            "Multiple Prominent / Tinted Buttons in One View",
            "Mixed Text and Icon Segments in One Control",
            "Liquid Glass in the Content Layer",
        ]
        for expected in expected_patterns:
            self.assertIn(expected, pattern_names, f"Forbidden pattern '{expected}' missing from table")

    def test_reference_docs_do_not_contain_forbidden_classes(self):
        """Scans CSS blocks across all reference files to ensure no forbidden classes are implemented."""
        forbidden_css = ["liquid-toggle", "liquid-slider", "non-apple-toggle"]
        all_css_texts = "\n".join([self.ctrl_text, self.lg_text, self.svg_text])

        for forbidden in forbidden_css:
            # Matches class selector declarations e.g. .liquid-toggle {
            match = re.search(rf"\.{forbidden}\s*\{{", all_css_texts)
            self.assertIsNone(match, f"Forbidden class '.{forbidden}' must not be declared in CSS specifications")

        # Authentic replacements must be declared
        self.assertIn(".apple-segmented-control", self.ctrl_text)
        self.assertIn(".apple-switch", self.ctrl_text)
        self.assertIn(".apple-slider", self.ctrl_text)
        self.assertIn(".apple-btn-push", self.ctrl_text)
        self.assertIn(".apple-btn-prominent", self.ctrl_text)

    def test_native_apple_control_dimensions_parsed(self):
        """Parses dimensional requirements for authentic Apple components from components-and-controls.md."""
        # Segmented control height 28px regular, 32px large, 2px padding, 6px pill radius
        m_seg_h = re.search(r"`(28px)`\s*\(regular\)\s*/\s*`(32px)`", self.ctrl_text)
        self.assertIsNotNone(m_seg_h, "Segmented control heights missing")
        self.assertEqual(m_seg_h.groups(), ("28px", "32px"))
        self.assertIn("padding: 2px", self.ctrl_text)
        self.assertIn("border-radius: 6px", self.ctrl_text)

        # Switch dimensions: 38px width, 22px height, 18px thumb, 16px travel
        m_switch = re.search(r"Width\s*`(38px)`,\s*height\s*`(22px)`", self.ctrl_text)
        self.assertIsNotNone(m_switch, "Native switch dimensions missing")
        self.assertEqual(m_switch.groups(), ("38px", "22px"))
        self.assertIn("width: 18px", self.ctrl_text)
        self.assertIn("transform: translateX(16px)", self.ctrl_text)

        # Slider track: strictly 4px height, 20px thumb
        m_slider = re.search(r"Track Height:\*\* Strictly\s*`(4px)`", self.ctrl_text)
        self.assertIsNotNone(m_slider, "Native slider track height missing")
        self.assertEqual(m_slider.group(1), "4px")
        self.assertIn("width: 20px", self.ctrl_text)

        # Buttons: 24px/28px, 6px radius, max 1 prominent button rule
        self.assertIn("Height: `24px` (regular) or `28px` (large)", self.ctrl_text)
        self.assertIn("Strictly max 1 (or at most 2) per view", self.ctrl_text)


class TestTypographyAndHierarchy(unittest.TestCase):
    """Verifies typographical weights, SF Symbols mappings, and font hierarchy parsed from disk."""

    @classmethod
    def setUpClass(cls):
        cls.svg_text = (REFS_DIR / "designer-svg-standards.md").read_text(encoding="utf-8")
        cls.ctrl_text = (REFS_DIR / "components-and-controls.md").read_text(encoding="utf-8")
        cls.skill_text = SKILL_FILE.read_text(encoding="utf-8")

    def test_sf_symbols_typographical_weights_table_parsed(self):
        """Parses the 9 typographical weights and stroke mappings from designer-svg-standards.md."""
        weights = re.findall(
            r"\|\s*\*\*([^*]+)\*\*\s*\|\s*(\d+)(?:\s*\([^)]*\))?\s*\|\s*([\d.]+)\s*px\s*\|\s*([\d.]+)\s*px",
            self.svg_text,
        )
        self.assertEqual(len(weights), 9, "Must parse all 9 typographical weights from SF Symbols table")

        names = [w[0] for w in weights]
        expected_names = ["Ultralight", "Thin", "Light", "Regular", "Medium", "Semibold", "Bold", "Heavy", "Black"]
        self.assertEqual(names, expected_names)

        font_weights = [int(w[1]) for w in weights]
        self.assertEqual(font_weights, [100, 200, 300, 400, 500, 600, 700, 800, 900])

        strokes_24 = [float(w[2]) for w in weights]
        self.assertEqual(strokes_24, [0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 3.5])
        # Verify strictly monotonically increasing stroke widths
        for i in range(len(strokes_24) - 1):
            self.assertLess(strokes_24[i], strokes_24[i + 1])

    def test_component_typography_specifications_parsed(self):
        """Parses typography specifications for segmented controls and buttons."""
        self.assertIn('font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text"', self.ctrl_text)
        self.assertIn("font-size: 13px", self.ctrl_text)
        self.assertIn("font-weight: 500", self.ctrl_text)
        self.assertIn("font-weight: 600", self.ctrl_text)
        self.assertIn("letter-spacing: -0.08px", self.ctrl_text)

    def test_skill_typography_dynamic_type_rules(self):
        """Verifies typography citations and Dynamic Type requirements in SKILL.md."""
        self.assertIn("typography#Supporting-Dynamic-Type", self.skill_text)
        self.assertIn("survives larger Dynamic Type sizes", self.skill_text)


class TestDesignerSVGAndSpringAnimation(unittest.TestCase):
    """Verifies designer-grade SVG requirements, CASpring curves, and SKILL.md alignment parsed from disk."""

    @classmethod
    def setUpClass(cls):
        cls.svg_text = (REFS_DIR / "designer-svg-standards.md").read_text(encoding="utf-8")
        cls.skill_text = SKILL_FILE.read_text(encoding="utf-8")

    def test_caspring_curves_parsed_from_markdown(self):
        """Parses CASpringAnimation cubic Bézier curves from designer-svg-standards.md."""
        springs = dict(re.findall(r"\*\*([^*]+)\*\*\s*\|\s*`cubic-bezier\(([^)]+)\)`", self.svg_text))

        self.assertIn("Snappy Interactive", springs)
        self.assertIn("Fluid Spatial", springs)
        self.assertIn("Elastic Micro-Bounce", springs)

        snappy_params = [float(x.strip()) for x in springs["Snappy Interactive"].split(",")]
        self.assertEqual(snappy_params, [0.16, 1.0, 0.3, 1.0])

        fluid_params = [float(x.strip()) for x in springs["Fluid Spatial"].split(",")]
        self.assertEqual(fluid_params, [0.2, 0.8, 0.2, 1.0])

        elastic_params = [float(x.strip()) for x in springs["Elastic Micro-Bounce"].split(",")]
        self.assertEqual(elastic_params, [0.34, 1.56, 0.64, 1.0])

    def test_production_svg_templates_parsed_and_validated(self):
        """Parses the 3 production SVG templates in Section 6 of designer-svg-standards.md."""
        # Template 1: App icon template
        self.assertIn('viewBox="0 0 1024 1024"', self.svg_text)
        self.assertIn('width="1024" height="1024"', self.svg_text)
        self.assertIn('<clipPath id="squircle-clip">', self.svg_text)
        self.assertIn('<filter id="macos-4tier-shadow"', self.svg_text)

        # Template 2: 24x24 vector icon
        self.assertIn('viewBox="0 0 24 24" width="24" height="24"', self.svg_text)
        self.assertIn('id="symbol-primary"', self.svg_text)
        self.assertIn('id="symbol-secondary"', self.svg_text)
        self.assertIn('class="symbol-accent symbol-secondary"', self.svg_text)
        self.assertIn('class="symbol-primary"', self.svg_text)
        self.assertIn('symbol-accent', self.svg_text)
        self.assertIn('stroke="currentColor"', self.svg_text)

        # Template 3: Animated telemetry radar
        self.assertIn('viewBox="0 0 80 80"', self.svg_text)
        self.assertIn("@media (prefers-reduced-motion: no-preference)", self.svg_text)
        self.assertIn("@media (prefers-reduced-motion: reduce)", self.svg_text)
        self.assertIn("animation: appleSpringPulse 3.8s cubic-bezier(0.16, 1, 0.3, 1) infinite", self.svg_text)

    def test_skill_rules_and_standards_alignment(self):
        """Verifies that SKILL.md contains all required rules (Rules 7-10)."""
        self.assertIn("7. **Authentic Liquid Glass Optical Physics:**", self.skill_text)
        self.assertIn("8. **Strict Apple Component Architecture:**", self.skill_text)
        self.assertIn("9. **Designer-Grade Vector Iconography:**", self.skill_text)
        self.assertIn("10. **Layer Separation:**", self.skill_text)

        # Check key physics tokens in SKILL.md Rule 7
        self.assertIn("n = 1.520", self.skill_text)
        self.assertIn("V_d = 58.6", self.skill_text)
        self.assertIn("rgba(0,0,0,0.35)", self.skill_text)


if __name__ == "__main__":
    unittest.main()
