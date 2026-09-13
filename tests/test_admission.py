import json
from copy import deepcopy
from pathlib import Path
import unittest

from demo.admission.intake import orient, submit, validate
from scripts.run_admission import generate

ROOT = Path(__file__).resolve().parents[1]


class IntakeTests(unittest.TestCase):
    def setUp(self):
        self.profile = json.loads((ROOT / "demo/admission/sample_profile.json").read_text())

    def test_invalid_or_extra_personal_fields_rejected(self):
        mutations = [
            lambda p: p.update(synthetic=False),
            lambda p: p.update(email="fictional@example.invalid"),
            lambda p: p["documents"].update(language_summary="yes"),
            lambda p: p.update(profile_id=123),
            lambda p: p.update(locale="unsupported"),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                p = deepcopy(self.profile)
                mutate(p)
                with self.assertRaises(ValueError):
                    validate(p)

    def test_orientation_is_deterministic_and_never_eligibility(self):
        first = orient(self.profile)
        self.assertEqual(first, orient(dict(reversed(list(self.profile.items())))))
        self.assertEqual(first["missing_items"], ["language_summary"])
        self.assertIsNone(first["eligibility_decision"])
        complete = deepcopy(self.profile)
        complete["documents"] = dict.fromkeys(complete["documents"], True)
        result = orient(complete)
        self.assertEqual(result["status"], "PREPARATION_LIST_COMPLETE")
        self.assertIsNone(result["eligibility_decision"])

    def test_no_review_request_creates_no_record(self):
        store = {}
        self.assertIsNone(submit(self.profile, "DEMO-001", False, "2030-01-15", store))
        self.assertEqual(store, {})

    def test_replay_does_not_duplicate_or_expose_mutable_store(self):
        store = {}
        first = submit(self.profile, "DEMO-001", True, "2030-01-15", store)
        first["history"].append({"event": "LOCAL_MUTATION"})
        replay = submit(self.profile, "DEMO-001", True, "2030-01-15", store)
        self.assertEqual(len(store), 1)
        self.assertEqual(len(replay["history"]), 1)
        self.assertEqual(replay["stage"], "REVIEW_REQUESTED")

    def test_reused_identifier_rejects_changed_payload(self):
        store = {}
        submit(self.profile, "DEMO-001", True, "2030-01-15", store)
        changed = deepcopy(self.profile)
        changed["documents"]["language_summary"] = True
        with self.assertRaises(ValueError):
            submit(changed, "DEMO-001", True, "2030-01-15", store)
        with self.assertRaises(ValueError):
            submit(self.profile, "DEMO-001", False, "2030-01-15", store)
        with self.assertRaises(ValueError):
            submit(self.profile, "DEMO-001", True, "2030-01-16", store)

    def test_bad_control_values_rejected_before_storage(self):
        for identifier, flag, day in [("real-id", True, "2030-01-15"),
                                      ("DEMO-001", "true", "2030-01-15"),
                                      ("DEMO-001", True, "2030-02-30")]:
            with self.subTest(identifier=identifier, flag=flag, day=day):
                store = {}
                with self.assertRaises(ValueError):
                    submit(self.profile, identifier, flag, day, store)
                self.assertFalse(store)

    def test_committed_outputs_match_executable_case(self):
        for name, value in generate().items():
            self.assertEqual(value, json.loads((ROOT / "demo/admission" / name).read_text()))


if __name__ == "__main__":
    unittest.main()

