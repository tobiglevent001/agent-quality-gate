#!/usr/bin/env python3
"""
Basic validation tests for CADVP protocol implementation.

These tests verify the cadvp-verify.py script structure and CADVP protocol
completeness without requiring a running Hermes Agent deployment.
"""
import unittest
import sys
import os
import tempfile

# Add parent dir for import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# We test the protocol spec, not the script against real targets
# (that requires a Hermes profile directory)


class TestProtocolCompleteness(unittest.TestCase):
    """Verify the CADVP protocol specification is complete and self-consistent."""

    def setUp(self):
        self.protocol_path = os.path.join(
            os.path.dirname(__file__), '..', 'protocol', 'index.md'
        )
        with open(self.protocol_path) as f:
            self.protocol = f.read()

    def test_all_13_dimensions_documented(self):
        """All 13 CADVP dimensions must be present in the protocol doc."""
        expected = ['CC-0', 'PC-1', 'PC-2', 'PC-3',
                    'WV-1', 'WV-2', 'WV-3',
                    'RV-1', 'RV-2', 'RV-3', 'RV-4',
                    'GR-1', 'GR-2']
        for d in expected:
            with self.subTest(dimension=d):
                self.assertIn(d, self.protocol,
                              f"Dimension {d} missing from protocol/index.md")

    def test_cc0_is_first(self):
        """CC-0 must be listed before all other dimensions (veto-level priority)."""
        cc0_pos = self.protocol.find('CC-0')
        pc1_pos = self.protocol.find('PC-1')
        self.assertLess(cc0_pos, pc1_pos,
                        "CC-0 should appear before PC-1 in protocol docs")

    def test_three_channels_documented(self):
        """All three injection channels must be documented."""
        for ch in ['Channel A', 'Channel B', 'Channel C']:
            with self.subTest(channel=ch):
                self.assertIn(ch, self.protocol,
                              f"{ch} missing from protocol documentation")


class TestScriptStructure(unittest.TestCase):
    """Verify cadvp-verify.py has the correct structure."""

    def setUp(self):
        self.script_path = os.path.join(
            os.path.dirname(__file__), '..', 'scripts', 'cadvp-verify.py'
        )
        with open(self.script_path) as f:
            self.script = f.read()

    def test_all_13_checks_implemented(self):
        """Script must implement all 13 dimension checks."""
        expected_checks = [
            ('CC-0', 'Channel'),
            ('PC-1', 'Target Identity'),
            ('PC-2', 'Data Channel'),
            ('PC-3', 'Impact Assessment'),
            ('WV-1', 'Data Confirmation'),
            ('WV-2', 'Content Integrity'),
            ('WV-3', 'Write Permissions'),
            ('RV-1', 'Config Activation'),
            ('RV-2', 'Runtime Loading'),
            ('RV-3', 'Tool Accessibility'),
            ('RV-4', 'User Perception'),
            ('GR-1', 'Impact Check'),
            ('GR-2', 'Documentation'),
        ]
        for code, name in expected_checks:
            with self.subTest(check=code):
                self.assertIn(code, self.script,
                              f"Check {code} ({name}) missing from script")

    def test_cc0_function_exists(self):
        """CC-0 channel confirmation function must exist."""
        self.assertIn('def cc0', self.script,
                      "cc0() function must be defined")

    def test_veto_logic(self):
        """Script must contain VETO logic for CC-0 failures."""
        self.assertIn('VETO', self.script,
                      "VETO logic must be present")
        self.assertIn('Channel is unavailable', self.script,
                      "Channel unavailability message required")

    def test_version_string(self):
        """Script must identify its version."""
        self.assertIn('v1.1', self.script,
                      "Script must advertise v1.1 version")


class TestTemplates(unittest.TestCase):
    """Verify templates include CC-0 dimension."""

    def test_template_cc0_inclusion(self):
        template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
        for fname in os.listdir(template_dir):
            if fname.endswith('.md'):
                path = os.path.join(template_dir, fname)
                with open(path) as f:
                    content = f.read()
                with self.subTest(template=fname):
                    self.assertIn('CC-0', content,
                                  f"{fname} should reference CC-0")


class ReadmeTest(unittest.TestCase):
    """Verify README has required sections."""

    def test_readme_sections(self):
        readme = os.path.join(os.path.dirname(__file__), '..', 'README.md')
        with open(readme) as f:
            content = f.read()
        for section in ['Quick Start', 'v1.1', 'License', 'CADVP']:
            with self.subTest(section=section):
                self.assertIn(section, content,
                              f"README missing '{section}' section")


if __name__ == '__main__':
    unittest.main()
