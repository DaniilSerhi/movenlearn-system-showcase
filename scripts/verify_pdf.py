"""Verify the physical PDF, not just its HTML source."""
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def verify():
    pdf = ROOT / "demo/pdf/sample.pdf"
    info = subprocess.check_output(["pdfinfo", str(pdf)], text=True)
    text = subprocess.check_output(["pdftotext", "-layout", str(pdf), "-"], text=True)
    fonts = subprocess.check_output(["pdffonts", str(pdf)], text=True)
    source = (ROOT / "demo/pdf/sample.html").read_text()
    content = json.loads((ROOT / "demo/pdf/sample-content.json").read_text())
    assert re.search(r"Pages:\s+1\b", info), "Expected one physical PDF page"
    size = re.search(r"Page size:\s+([0-9.]+) x ([0-9.]+)", info)
    assert size and abs(float(size[1])-595.276) < 1 and abs(float(size[2])-841.89) < 1, "Expected A4"
    assert source.count('<div class="page">') == 1, "Expected one HTML page block"
    normalized = " ".join(text.split()).replace("—", "-")
    for heading in [section["title"] for section in content["sections"]]:
        assert heading in normalized, "Missing required section"
    assert "Synthetic demo data" in normalized and "no real customer information." in normalized
    assert re.search(r"1\s*/\s*1", text), "Missing physical page footer"
    assert "Unbounded" in fonts and "SourceSerif" in fonts, "Required fonts missing"
    rows = [line.split() for line in fonts.splitlines()[2:] if line.strip()]
    assert rows and all(row[-5] == "yes" for row in rows), "Every font must be embedded"
    print("PDF verified: one A4 page, required sections, synthetic marker, footer, embedded fonts")


if __name__ == "__main__":
    verify()

