# Validation notes

Validation performed during local preparation on 2026-09-13. These results concern this showcase only.

| Check | Result | Boundary |
| --- | --- | --- |
| Intake runner | Passed; exact replay leaves one record | Single-process, in-memory example |
| Unit tests | 12 passed | Seven intake tests and five publication-safety tests |
| PDF regeneration | Passed with installed Chromium headless shell | Renderer version may affect binary output |
| Physical PDF | One A4 page; required sections, footer and embedded fonts present | Structural checks do not judge composition |
| PDF inspection | No attachments or annotations; neutral title/creator metadata | Checked sample only |
| Visual inspection | PDF page and both diagrams inspected during AI-assisted preparation | Final human acceptance remains pending |
| README rendering | Local Markdown render inspected at desktop and mobile widths | GitHub's renderer was not used; no remote publication |
| Images | No broken images; no page overflow at the checked mobile width | Small diagrams can be opened at full size |
| Local links | All local targets and referenced heading fragments resolve | Existence does not prove source support |
| External links | Linked public destinations checked during preparation | Future availability is outside the repository |
| Publication patterns | Working files and reachable Git history pass | Defined heuristics, not a privacy certification |

The public product link was checked in a browser and resolved to the English site. A plain HTTP client did not reproduce that browser navigation; no production changes were made.

Python 3.14.6 and Poppler 26.07.0 were used for the primary command checks. A separate temporary QA environment used Python 3.12 with Python-Markdown, Playwright, Pillow and pypdf for rendering and inspection. Those QA dependencies are not needed for the intake demo or unit tests.

The PDF uses local licensed fonts. Publication checks validate their hashes against the committed manifest. Upstream font/license files are a narrowly identified attribution exception to the generic email scan; they are not customer data.

## Commands

```bash
python3 scripts/run_admission.py
python3 -m unittest discover -s tests -v
python3 scripts/build_pdf.py
python3 scripts/render_pdf.py
python3 scripts/verify_pdf.py
python3 scripts/check_links.py
python3 scripts/verify_public_repo.py
```

Open the generated preview after rendering. Review prose and source support before accepting an editorial change. Re-run publication checks after the final commit because deleted historical content can still be pushed.

Initial preparation was completed locally. The owner separately authorized creation of the public GitHub repository and publication of the prepared history.

