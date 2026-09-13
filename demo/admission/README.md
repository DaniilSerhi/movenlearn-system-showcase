# Synthetic intake

**Synthetic demo data — no real customer information.**

Run `python3 scripts/run_admission.py` from the repository root.

The input is [sample_profile.json](sample_profile.json). The committed outputs are [preliminary_result.json](preliminary_result.json) and [crm_record.json](crm_record.json). The runner compares them with fresh results and prints a readable report of preparation gaps, the review handoff and replay checks. Add `--json` for a machine-readable summary. Use `--write` to regenerate those two files.

The fictional profile is missing a language summary. That produces `PREPARATION_INCOMPLETE`. A human review request still creates a record: the point is to surface the missing item for a person, not silently reject someone from a real institution.

The record uses the fixed synthetic date 2030-01-15. Replaying the same request leaves one record and one initial history entry. The store lasts for the current process only.

No contacts, messaging hooks, appointment adapters or marketing enrollment exist in this demo. See [product flow](../../docs/product-flow.md) for the exact replay boundary.

