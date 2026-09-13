# Document production

The [sample](../demo/pdf/README.md) demonstrates a repeatable content-to-document transformation:

```text
sample-content.json + design.md
→ build_pdf.py
→ editable sample.html
→ Chrome/Chromium
→ sample.pdf
→ Poppler verification
→ preview.png
→ visual review
```

The HTML source remains editable. For repeatable builds, edit the JSON or builder; rebuilding overwrites the generated HTML. If you edit HTML directly, render it without rebuilding.

MoveNLearn defines the document's job, page budget, typography, components and acceptance criteria. The public example uses the same restrained print principles with entirely fictional content. Chrome/Chromium handles rendering; Poppler handles inspection. Neither tool is developed by MoveNLearn.

## Automated checks

The verifier requires one A4 page, a matching HTML page block, required content sections, the synthetic marker, a physical page footer and embedded Unbounded/Source Serif fonts. It rejects unexpected interactive PDF features through the publication verifier.

PNG generation makes inspection possible; it does not make composition judgment automatic. After a change, inspect the preview for clipping, crowded tables, missing glyphs, readability and footers. A structurally valid document can still be poorly designed.

The demo uses a neutral preparation checklist, not a lead magnet containing current university rules or commercial promises.

