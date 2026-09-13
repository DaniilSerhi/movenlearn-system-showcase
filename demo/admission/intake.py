"""Synthetic, single-process intake example. No production dependencies."""
from copy import deepcopy
from datetime import date
import hashlib
import json
import re

MARKER = "Synthetic demo data — no real customer information."
DOCUMENTS = ("education_summary", "language_summary", "target_note")


def validate(profile):
    fields = {"synthetic", "profile_id", "locale", "target", "documents"}
    if not isinstance(profile, dict) or set(profile) != fields:
        raise ValueError("Expected the closed synthetic profile schema")
    if profile["synthetic"] is not True:
        raise ValueError("Only explicitly synthetic profiles are accepted")
    if not isinstance(profile["profile_id"], str) or not re.fullmatch(r"SYN-[0-9]{3}", profile["profile_id"]):
        raise ValueError("Expected a synthetic profile identifier")
    if profile["locale"] not in ("en", "ru", "ua"):
        raise ValueError("Unsupported demo locale")
    if profile["target"] != "fictional-study-preparation":
        raise ValueError("Only the fictional target is accepted")
    documents = profile["documents"]
    if not isinstance(documents, dict) or set(documents) != set(DOCUMENTS):
        raise ValueError("Expected the three demo document flags")
    if any(type(value) is not bool for value in documents.values()):
        raise ValueError("Document flags must be booleans")
    return deepcopy(profile)


def orient(profile):
    profile = validate(profile)
    missing = [key for key in DOCUMENTS if not profile["documents"][key]]
    return {
        "notice": MARKER,
        "rules_version": "demo-1",
        "profile_id": profile["profile_id"],
        "status": "PREPARATION_INCOMPLETE" if missing else "PREPARATION_LIST_COMPLETE",
        "missing_items": missing,
        "eligibility_decision": None,
        "boundary": "Preliminary orientation is not an eligibility decision.",
        "next_step": "Human review may be requested; institutional decisions are outside this demo.",
    }


def submit(profile, submission_id, request_review, review_date, store):
    profile = validate(profile)
    if not isinstance(submission_id, str) or not re.fullmatch(r"DEMO-[0-9]{3}", submission_id):
        raise ValueError("Expected a synthetic submission identifier")
    if type(request_review) is not bool:
        raise ValueError("Review request must be a boolean")
    if not isinstance(review_date, str):
        raise ValueError("Expected an ISO date")
    try:
        if date.fromisoformat(review_date).isoformat() != review_date:
            raise ValueError("Expected YYYY-MM-DD")
    except ValueError as error:
        raise ValueError("Expected a valid ISO date") from error
    envelope = {"profile": profile, "request_review": request_review, "review_date": review_date}
    fingerprint = hashlib.sha256(json.dumps(envelope, sort_keys=True).encode()).hexdigest()
    existing = store.get(submission_id)
    if existing:
        if existing["fingerprint"] != fingerprint:
            raise ValueError("Submission identifier conflicts with an existing request")
        return deepcopy(existing["record"])
    if not request_review:
        return None
    record = {
        "notice": MARKER,
        "record_id": "CRM-" + submission_id,
        "profile": profile,
        "orientation": orient(profile),
        "stage": "REVIEW_REQUESTED",
        "next_action": "Review preparation notes and identify questions for human follow-up",
        "next_action_date": review_date,
        "date_scope": "Synthetic scheduling value; not a service promise",
        "attribution": {"source": "synthetic-showcase", "channel": "local-demo"},
        "history": [{"event": "HUMAN_REVIEW_REQUESTED", "actor": "synthetic-participant"}],
    }
    store[submission_id] = {"fingerprint": fingerprint, "record": deepcopy(record)}
    return record

