"""Exercise the actual CLI in human and machine-readable modes."""
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


class AdmissionCLITests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts/run_admission.py"), *args],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout

    def test_default_report_exposes_result_and_decision_boundary(self):
        output = self.run_cli()
        self.assertIn("PRELIMINARY ORIENTATION", output)
        self.assertIn("Preparation incomplete", output)
        self.assertIn("language summary", output)
        self.assertIn("HUMAN REVIEW HANDOFF", output)
        self.assertIn("CRM-DEMO-001", output)
        self.assertIn("Exact replay leaves one record", output)
        self.assertIn("Preliminary orientation is not an eligibility decision.", output)
        self.assertFalse(output.lstrip().startswith("{"))
        self.assertNotIn(chr(27), output)

    def test_json_mode_remains_parseable_without_report_text(self):
        result = json.loads(self.run_cli("--json"))
        self.assertTrue(result["synthetic"])
        self.assertEqual(result["orientation"], "PREPARATION_INCOMPLETE")
        self.assertEqual(result["stage"], "REVIEW_REQUESTED")
        self.assertEqual(result["records_after_replay"], 1)
        self.assertIsNone(result["eligibility_decision"])


if __name__ == "__main__":
    unittest.main()
