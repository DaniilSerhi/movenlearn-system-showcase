# Prepare a human review request in the demo

**Synthetic demo data — no real customer information.**

Start with the three preparation flags: education summary, language summary and target note. The demo asks whether each note is available; it does not accept certificates or other document uploads. The target is fictional. [Preparation specification](../research/sources/review-spec.md#preparation-notes)

## Read the result as a preparation check

A missing flag appears as a preparation gap. If all flags are present, the preparation list is complete. Neither result establishes eligibility for a university or another institution. [Result boundary](../research/sources/review-spec.md#preliminary-result)

## Decide whether to request human review

You can request review with an incomplete list. That explicit request creates a CRM-like record with a stage and next action. Without it, the demo creates no record. The local example has no contact fields or adapters that forward the request into appointment, messaging or marketing systems. [Review rule](../research/sources/review-spec.md#human-review), [data boundary](../research/sources/review-spec.md#data-boundary)

An identical replay returns the existing record within the same run. Changed content under the same identifier is a conflict. This demonstrates repeat handling in memory, not a persistent production service. [Replay rule](../research/sources/review-spec.md#repeated-requests)

[Inspect the synthetic CRM record](../admission/crm_record.json) to see the profile, preliminary result and next action together.

