"""Run the bundled synthetic case and compare its public JSON artifacts."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from demo.admission.intake import orient, submit


def generate():
    profile = json.loads((ROOT / "demo/admission/sample_profile.json").read_text())
    store = {}
    first = submit(profile, "DEMO-001", True, "2030-01-15", store)
    replay = submit(profile, "DEMO-001", True, "2030-01-15", store)
    assert first == replay and len(store) == 1
    return {"preliminary_result.json": orient(profile), "crm_record.json": first}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    outputs = generate()
    for name, result in outputs.items():
        path = ROOT / "demo/admission" / name
        if args.write:
            path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
        elif json.loads(path.read_text()) != result:
            raise SystemExit("Committed demo output differs: " + name)
    print(json.dumps({"synthetic": True, "orientation": outputs["preliminary_result.json"]["status"],
                      "stage": outputs["crm_record.json"]["stage"], "records_after_replay": 1,
                      "eligibility_decision": None}, indent=2))


if __name__ == "__main__":
    main()

