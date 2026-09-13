# Quality and governance

Requirements and accepted sources come before implementation. In the broader working model, business decisions, technical behavior and task status have separate owners. This public repository carries only its own demo specifications; it does not publish the private Sources of Truth.

## Automated

- Intake validation rejects malformed, unknown and non-synthetic fields.
- Determinism tests compare stable results for equivalent requests.
- Opt-in and replay tests check record creation boundaries and conflicts.
- Artifact checks compare committed JSON with executable results.
- PDF checks inspect physical pages, required text, footer and embedded fonts.
- The publication verifier scans files, PDF text/metadata and reachable Git history.
- The link checker resolves relative Markdown/HTML targets and fragments.

Tests have explicit boundaries. An in-memory replay test is not a distributed-systems guarantee. Required PDF text is not a complete visual check. Pattern scanning is not a complete data-loss-prevention system.

## Human review

A reviewer assesses source authority, whether an article overstates its evidence, whether a PDF is readable, and whether an operational request needs more information. Institutional eligibility and publication decisions remain human responsibilities.

For this showcase, every person-like identifier is fictional. No customer input is requested. Public research fixtures contain no contacts. The next-action date is a demo value, not a service deadline.

## Before publishing a change

Run the documented checks, review the full diff and inspect the final preview. Examine generated files and history, not just visible Markdown. Check contribution wording and tool attribution. Resolve any unexpected file before publication.

A successful verifier is one input to acceptance. It is not proof that all possible secrets or commercially sensitive statements have been detected.

