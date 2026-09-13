"""Build editable HTML from the fictional document content."""
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build():
    content = json.loads((ROOT / "demo/pdf/sample-content.json").read_text())
    if content.get("synthetic") is not True:
        raise ValueError("Only synthetic document content is accepted")
    first, second, third = content["sections"]
    checks = "".join("<li><b>" + escape(title) + "</b><span>" + escape(note) + "</span></li>"
                     for title, note in first["items"])
    rows = "".join("<tr><td>" + escape(a) + "</td><td>" + escape(b) + "</td></tr>"
                   for a, b in second["rows"])
    css = """
@font-face{font-family:Unbounded;src:url('../../assets/fonts/Unbounded.ttf');font-weight:200 900}
@font-face{font-family:'Source Serif 4';src:url('../../assets/fonts/SourceSerif4.ttf');font-weight:200 900}
:root{
 --paper:#F5F3EF;--card:#FFFFFF;--ink:#23262C;--soft:#5D636E;
 --accent:#EA580C;--rule:#DAD5CC;--rule-soft:#EDEAE4;
 --display:Unbounded,sans-serif;--body:'Source Serif 4',serif;
 --xs:2mm;--sm:3mm;--md:5mm;--lg:8mm;--xl:12mm;
}
@page{size:A4;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--paper);color:var(--ink);font:400 10.4pt/1.5 var(--body)}
.page{width:210mm;min-height:297mm;padding:17mm 17mm 18mm;position:relative}
.eyebrow{font:600 8pt/1.3 var(--display);color:var(--accent);letter-spacing:.12em;margin-bottom:var(--md)}
h1{font:800 25pt/1.18 var(--display);font-style:normal;margin-bottom:var(--sm)}
.sub{font-size:11.5pt;line-height:1.5;color:var(--soft);max-width:160mm;margin-bottom:var(--lg)}
h2{font:600 11pt/1.3 var(--display);border-bottom:1.3pt solid var(--ink);padding-bottom:var(--xs);margin-bottom:var(--sm)}
section{margin-bottom:var(--md);break-inside:avoid}
.check{list-style:none}
.check li{position:relative;padding-left:8mm;margin-bottom:var(--sm)}
.check li:before{content:'';position:absolute;left:0;top:1mm;width:4mm;height:4mm;border:1pt solid var(--soft)}
.check span{display:block;color:var(--soft);font-size:9.5pt}
table{width:100%;border-collapse:collapse;font-size:9.5pt}
th{text-align:left;color:var(--soft);font-size:8.5pt;padding:0 2mm 2mm 0;border-bottom:1pt solid var(--rule)}
td{padding:2mm 2mm 2mm 0;border-bottom:.5pt solid var(--rule-soft);vertical-align:top}
td:first-child{width:46%;font-weight:600}
.callout{border:1pt solid var(--rule);background:var(--card);padding:var(--sm);font-size:9.5pt;margin-top:var(--sm)}
.cta{border:1pt solid var(--ink);border-left:4pt solid var(--accent);padding:var(--md);margin-top:var(--md)}
.cta b{font:600 10pt/1.4 var(--display)}
.cta p{margin-top:var(--xs);font-size:9.5pt;color:var(--soft)}
.honest{font-size:8.5pt;color:var(--soft);margin-top:var(--md)}
.foot{position:absolute;left:17mm;right:17mm;bottom:9mm;display:flex;justify-content:space-between;font:600 7pt/1.2 var(--display);color:var(--soft)}
"""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Synthetic preparation checklist</title>
<!-- Hallmark PDF · critique: P4 H4 E4 S4 R5 V4; single-page document. -->
<style>{css}</style></head><body>
<div class="page">
<div class="eyebrow">MOVENLEARN / DOCUMENT WORKFLOW DEMO</div>
<h1>{escape(content['title']).replace(chr(10), '<br>')}</h1>
<p class="sub">{escape(content['subtitle'])}</p>
<section><h2>01 / {escape(first['title'])}</h2><ul class="check">{checks}</ul></section>
<section><h2>02 / {escape(second['title'])}</h2>
<table><thead><tr><th>Preparation state</th><th>What the demo says</th></tr></thead><tbody>{rows}</tbody></table>
<div class="callout">{escape(content['callout'])}</div></section>
<section><h2>03 / {escape(third['title'])}</h2><p>{escape(third['body'])}</p></section>
<div class="cta"><b>{escape(content['cta'])}</b><p>{escape(content['cta_detail'])}</p></div>
<p class="honest">{escape(content['notice'])}<br>This fictional example makes no promise about admission or institutional decisions.</p>
<div class="foot"><span>MoveNLearn / System Showcase</span><span>1 / 1</span></div>
</div>
</body></html>
"""


if __name__ == "__main__":
    (ROOT / "demo/pdf/sample.html").write_text(build())
    print("Built demo/pdf/sample.html from synthetic content")

