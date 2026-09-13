# Fictional review service specification

**Synthetic demo data — no real customer information.**

Version: demo-1. This authored fixture describes only the bundled demo service.

## Preparation notes

The checklist has three flags: education summary, language summary and target note. Participants provide flags, not document uploads. The permitted target is fictional-study-preparation.

## Preliminary result

Missing flags are listed as preparation gaps. When all flags are present, the list is complete. Neither result decides eligibility or admission to an institution.

## Human review

A participant may explicitly request human review even when preparation notes are incomplete. A request creates a CRM-like record with a review stage and next action. Without the request, the demo creates no CRM record.

## Repeated requests

Within a single run, the same submission identifier and payload return the existing record. Changed content under the same identifier is rejected as a conflict.

## Data boundary

The demo accepts a closed synthetic schema and has no fields for names, email addresses, phones or identity documents. It has no appointment, messaging or marketing adapters.

