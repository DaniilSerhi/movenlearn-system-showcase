# Product flow

**Synthetic demo data — no real customer information.**

```text
User input
→ schema validation
→ deterministic preliminary orientation
→ optional human review request
→ CRM-like record
→ stage + next action + due date
→ human processing
```

[The example](../demo/admission/sample_profile.json) uses a fictional identifier and a small closed schema. It accepts a document checklist and a declared target, not passports, names, free-text personal histories or contact details.

Orientation reports missing preparation items. Even a complete checklist returns `eligibility_decision: null`. The result states that institutional decisions require human assessment and relevant institutional sources.

An opt-in request creates a record at `REVIEW_REQUESTED`, with a next action, a supplied synthetic date and an initial history event. No opt-in means no record. There are no side effects to appointment, messaging or email systems.

## Replay contract

A caller supplies a submission ID. The demo validates the complete request, computes a stable fingerprint and stores it alongside the record. The same ID and payload return a deep copy of the existing record. A different payload with the same ID raises a conflict. The identity covers the profile, the opt-in flag and the requested review date.

This is a single-process example. It does not provide database persistence, transactions or concurrency guarantees. A real service would require an atomic uniqueness constraint and an explicit policy for changed submissions. The demo does not pretend otherwise.

