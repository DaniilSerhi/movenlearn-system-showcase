# Document production demo

**Synthetic demo data — no real customer information.**

[Open the PDF](sample.pdf) · [Editable HTML](sample.html) · [Design requirements](design.md)

![Sample PDF preview](preview.png)

The sample is a fictional preparation checklist. Its text comes from [sample-content.json](sample-content.json). It does not state actual university requirements.

Run from the repository root:

```bash
python3 scripts/build_pdf.py
python3 scripts/render_pdf.py
python3 scripts/verify_pdf.py
```

Python 3.10+, Chrome/Chromium and Poppler are required. The render script accepts `--chrome` if executable discovery is insufficient. It uses an isolated temporary browser profile. Both font families are bundled with their licenses.

The builder writes HTML; Chrome writes PDF; Poppler verifies the result and creates the PNG. Manual visual inspection remains necessary. HTML, PDF and preview are committed for readers who do not install the tools.

Hallmark PDF informed the preparation workflow as an external local tool. Its scripts and prompts are not bundled or claimed as MoveNLearn code.

