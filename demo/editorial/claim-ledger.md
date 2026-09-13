# Claim ledger

**Synthetic demo data — no real customer information.**

| ID | Permitted claim | Source | Status / boundary |
| --- | --- | --- | --- |
| C1 | The checklist has education, language and target flags | [Preparation notes](../research/sources/review-spec.md#preparation-notes) | Accepted for this fictional service |
| C2 | A complete list does not determine eligibility | [Preliminary result](../research/sources/review-spec.md#preliminary-result) | Accepted |
| C3 | Only explicit review requests create a CRM-like record | [Human review](../research/sources/review-spec.md#human-review) | Accepted |
| C4 | Exact replay returns the existing record within a run | [Repeated requests](../research/sources/review-spec.md#repeated-requests) | Accepted; no concurrency claim |
| C5 | No personal contact fields or downstream adapters exist in the demo | [Data boundary](../research/sources/review-spec.md#data-boundary) | Accepted for this repository only |
| R1 | A completed checklist guarantees an institutional outcome | [Rejected candidate](../research/sources/unsupported-outcome.md) | Rejected; unsupported |

The source describes the intended demo contract. Behavioral tests provide separate evidence of implementation. Neither source nor tests establish real university rules.

