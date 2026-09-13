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
    if first != replay or len(store) != 1:
        raise RuntimeError("Replay must return the same record without duplication")
    return {"preliminary_result.json": orient(profile), "crm_record.json": first}


def render_report(outputs, written=False):
    result = outputs["preliminary_result.json"]
    record = outputs["crm_record.json"]
    labels = {
        "PREPARATION_INCOMPLETE": "Preparation incomplete",
        "PREPARATION_LIST_COMPLETE": "Preparation list complete",
        "REVIEW_REQUESTED": "Human review requested",
    }
    missing = ", ".join(item.replace("_", " ") for item in result["missing_items"]) or "None"
    action = record["next_action"]
    return "\n".join([
        "MoveNLearn | Admission demo",
        "=" * 52,
        "Synthetic demo data - no real customer information.",
        "",
        "PRELIMINARY ORIENTATION",
        f"  Profile       {result['profile_id']}",
        f"  Result        {labels[result['status']]}",
        f"  Missing       {missing}",
        "  Eligibility   Not decided",
        "",
        "HUMAN REVIEW HANDOFF",
        f"  Record        {record['record_id']}",
        f"  Stage         {labels[record['stage']]}",
        f"  Review date   {record['next_action_date']} (synthetic)",
        "  Next action",
        f"    {action}",
        "",
        "CHECKS",
        "  PASS  Exact replay leaves one record",
        "  PASS  " + ("Demo JSON files regenerated" if written else "Committed JSON matches this run"),
        "",
        result["boundary"],
    ])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Regenerate committed demo JSON files")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary")
    args = parser.parse_args()
    outputs = generate()
    for name, result in outputs.items():
        path = ROOT / "demo/admission" / name
        if args.write:
            path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
        elif json.loads(path.read_text()) != result:
            raise SystemExit("Committed demo output differs: " + name)
    if args.json:
        print(json.dumps({
            "synthetic": True,
            "orientation": outputs["preliminary_result.json"]["status"],
            "stage": outputs["crm_record.json"]["stage"],
            "records_after_replay": 1,
            "eligibility_decision": None,
        }, indent=2))
    else:
        print(render_report(outputs, written=args.write))


if __name__ == "__main__":
    main()
