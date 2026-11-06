# -*- coding: utf-8 -*-
"""Build the IEEE-style two-column conference PDF for IEEE CEC.

Reuses the markdown converter from build_pdf.py, wraps the body in a two-column
flow, and lets the title block span both columns.
"""
import html
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_pdf import convert  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "paper", "cec", "cec-v1.md")
OUT_HTML = os.path.join(ROOT, "paper", "cec", "cec-v1.html")
OUT_PDF = os.path.join(ROOT, "paper", "cec", "cec-v1.pdf")

CSS = """
@page { size: A4; margin: 16mm 14mm 18mm 14mm; }
* { box-sizing: border-box; }
body { font-family: "Times New Roman", "Nimbus Roman", Georgia, serif;
       font-size: 9.5pt; line-height: 1.30; color: #000; margin: 0;
       text-align: justify; hyphens: auto; }
.cols { column-count: 2; column-gap: 7mm; }
.titleblock { column-span: all; text-align: center; margin-bottom: 8pt; }
h1 { font-size: 16.5pt; line-height: 1.18; font-weight: 700; margin: 0 0 8pt;
     text-align: center; letter-spacing: .1pt; }
.titleblock p { text-align: center; font-size: 10.5pt; margin: 0 0 2pt; }
h2 { font-size: 10.2pt; font-weight: 700; margin: 9pt 0 3pt; text-align: left;
     font-variant: small-caps; letter-spacing: .3pt; }
h3 { font-size: 9.6pt; font-weight: 700; font-style: italic; margin: 7pt 0 2pt; }
p { margin: 0 0 4.5pt; }
ul, ol { margin: 3pt 0 5pt; padding-left: 13pt; }
li { margin: 0 0 2pt; }
strong { font-weight: 700; }
em { font-style: italic; }
code { font-family: Consolas, monospace; font-size: 8.4pt; }
pre { white-space: pre-wrap; word-wrap: break-word; overflow-wrap: anywhere;
      font-family: Consolas, "DejaVu Sans Mono", monospace; font-size: 7.1pt;
      line-height: 1.22; background: #f6f6f6; border: .4pt solid #bbb;
      padding: 3pt 4pt; margin: 4pt 0 6pt; }
table { border-collapse: collapse; width: 100%; table-layout: fixed; font-size: 7.5pt;
        margin: 4pt 0 6pt; line-height: 1.2; }
th, td { border: .4pt solid #555; padding: 1.6pt 2.2pt; text-align: left;
         vertical-align: top; word-break: break-word; }
th { background: #eee; font-weight: 700; }
.fig { margin: 5pt 0 7pt; text-align: center; break-inside: avoid; }
.fig img { width: 100%; height: auto; }
.figcap { font-size: 7.9pt; line-height: 1.25; text-align: justify;
          margin-top: 3pt; }
.foot { column-span: all; font-size: 7.6pt; color: #333; text-align: center;
        margin-top: 8pt; border-top: .5pt solid #999; padding-top: 4pt; }
"""

ABSTRACT_CSS = """
.abstract { font-size: 9pt; margin: 0 0 6pt; }
.abstract p { margin-bottom: 4pt; }
"""


def split_titleblock(body):
    """Pull <h1> and the following author paragraph into a span-all block."""
    m = re.search(r"<h1>(.*?)</h1>\s*(<p>.*?</p>)?", body, re.S)
    if not m:
        return body, ""
    title = "<h1>%s</h1>" % m.group(1)
    author = m.group(2) or ""
    block = '<div class="titleblock">%s%s</div>' % (title, author)
    return body[:m.start()] + body[m.end():], block


def main():
    md = open(SRC, encoding="utf-8").read()
    body = convert(md)
    rest, block = split_titleblock(body)

    doc = ("<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\">"
           "<title>LRLS - IEEE CEC 2027 submission</title><style>%s%s</style>"
           "</head><body>%s<div class=\"cols\">%s</div>"
           "<div class=\"foot\">Preprint v1.1 - IEEE CEC 2027 submission draft - "
           "code and data: github.com/clawgeek/lrls-paper</div>"
           "</body></html>") % (CSS, ABSTRACT_CSS, block, rest)
    open(OUT_HTML, "w", encoding="utf-8").write(doc)
    print("HTML", OUT_HTML, os.path.getsize(OUT_HTML), "bytes")

    edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    url = "file:///" + OUT_HTML.replace("\\", "/")
    subprocess.run([edge, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--print-to-pdf=" + OUT_PDF, url],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    if os.path.exists(OUT_PDF):
        from pypdf import PdfReader
        r = PdfReader(OUT_PDF)
        print("PDF ", OUT_PDF, len(r.pages), "pages", os.path.getsize(OUT_PDF), "bytes")


if __name__ == "__main__":
    main()
