# Architecture

The case study abstracts five workflows from MoveNLearn's internal working model. The executable examples are new, deliberately smaller implementations. No private backend or audit document is included.

![System architecture](../assets/architecture-overview.svg)

Requirements and sources constrain two connected content workflows and a separate intake workflow. Research hands evidence to editorial. Editorial produces content; document production turns selected content into a formatted artifact. Intake produces preliminary orientation and, with an explicit request, a record for human processing.

QA is a cross-cutting layer. Source checking belongs before writing; structural checks follow rendering; human review sits at consequential decisions. The diagram does not imply a scheduler that runs all of these steps automatically.

| Layer | Owns | Does not establish |
| --- | --- | --- |
| Requirements and sources | Scope, accepted facts, behavior boundaries | That every implementation conforms |
| Workflow instructions | Steps, inputs and review gates | Autonomous execution |
| Implementations | Validation, records, content transformations | Institutional decisions |
| Automated checks | Defined invariants and regressions | Complete production correctness |
| Human review | Interpretation and acceptance | Guaranteed external outcomes |

## Repository boundary

The public examples run locally. The intake store is an in-memory dictionary; the PDF source is local JSON and HTML; research uses fictional Markdown fixtures. There are no production adapters.

The broader working model includes website, CRM, email, payments and analytics. Those integrations are not connected here. This repository proves its own demonstration behavior and describes the surrounding design at an architectural level.

