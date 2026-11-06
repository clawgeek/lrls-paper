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
/* IEEE conference template: US Letter, top .75in, bottom 1in, sides .625in */
@page { size: Letter; margin: 0.75in 0.625in 1in 0.625in; }
* { box-sizing: border-box; }
body { font-family: "Times New Roman", "Nimbus Roman", Georgia, serif;
       font-size: 9.5pt; line-height: 1.23; color: #000; margin: 0;
       text-align: justify; hyphens: auto; }
.cols { column-count: 2; column-gap: 0.25in; column-fill: balance;
        orphans: 2; widows: 2; }
.cols ol, .cols ul { break-inside: auto; }
.cols li { break-inside: avoid; margin-bottom: 1pt; }
.cols p { orphans: 2; widows: 2; }
.titleblock { column-span: all; text-align: center; margin-bottom: 8pt; }
h1 { font-size: 16.5pt; line-height: 1.18; font-weight: 700; margin: 0 0 8pt;
     text-align: center; letter-spacing: .1pt; }
.titleblock p { text-align: center; font-size: 10.5pt; margin: 0 0 2pt; }
h2 { font-size: 10.2pt; font-weight: 700; margin: 7pt 0 2.5pt; text-align: left;
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
        break-inside: avoid;
        margin: 4pt 0 6pt; line-height: 1.2; }
th, td { border: .4pt solid #555; padding: 1.6pt 2.2pt; text-align: left;
         vertical-align: top; word-break: break-word; }
th { background: #eee; font-weight: 700; }
.fig { margin: 5pt 0 7pt; text-align: center; break-inside: avoid; }
.fig img { width: 100%; height: auto; }
.figcap { font-size: 7.9pt; line-height: 1.25; text-align: justify;
          margin-top: 3pt; }
.m { font-family: "Cambria Math", "Times New Roman", serif; font-style: normal;
     white-space: nowrap; }
.m sup, .m sub { font-size: 68%; line-height: 0; }
.eq { text-align: center; margin: 5pt 0 5pt; }
.ref { font-size: 7.7pt; line-height: 1.22; margin: 0 0 1.8pt;
        text-indent: -11pt; padding-left: 11pt; }
.tcap { text-align: center; font-size: 7.6pt; margin: 6pt 0 2.5pt;
        break-after: avoid; }
.tcap b { font-weight: 700; }
.foot { column-span: all; font-size: 7.6pt; color: #333; text-align: center;
        margin-top: 8pt; border-top: .5pt solid #999; padding-top: 4pt; }
"""

ABSTRACT_CSS = """
.abstract { font-size: 9pt; margin: 0 0 6pt; }
.abstract p { margin-bottom: 4pt; }
"""



# --- minimal LaTeX -> unicode/HTML renderer (IEEE-style inline math) ----------
SYM = [
    (r"\mathbb{R}", "\u211d"), (r"\mathbb{E}", "\U0001d53c"), (r"\mathcal{H}", "\u210b"),
    (r"\arg\max", None), (r"\max", None), (r"\min", None), (r"\log", None), (r"\exp", None),
    (r"\ast", "\u2217"), (r"\subset", "\u2282"), (r"\to", "\u2192"), (r"\le", "\u2264"),
    (r"\ge", "\u2265"), (r"\times", "\u00d7"), (r"\dagger", "\u2020"), (r"\approx", "\u2248"),
    (r"\cdot", "\u00b7"), (r"\in", "\u2208"), (r"\infty", "\u221e"), (r"\pm", "\u00b1"),
    (r"\Omega", "\u03a9"), (r"\Delta", "\u0394"), (r"\rho", "\u03c1"), (r"\tau", "\u03c4"),
    (r"\varepsilon", "\u03b5"), (r"\epsilon", "\u03b5"), (r"\lambda", "\u03bb"),
    (r"\mu", "\u03bc"), (r"\sigma", "\u03c3"), (r"\theta", "\u03b8"), (r"\alpha", "\u03b1"),
    (r"\beta", "\u03b2"), (r"\gamma", "\u03b3"), (r"\delta", "\u03b4"), (r"\pi", "\u03c0"),
    (r"\ldots", "\u2026"), (r"\dots", "\u2026"), (r"\quad", "\u2003"), (r"\;", "\u2009"),
    (r"\,", "\u2009"), (r"\:", "\u2009"), (r"\ ", " "),
]
UPRIGHT = {"arg max", "max", "min", "log", "exp"}


def _mrender(tex):
    """Render one LaTeX fragment into small inline HTML."""
    s = tex
    stash = []

    def keep(txt):
        stash.append(txt)
        return "\ue000%d\ue001" % (len(stash) - 1)

    # 1. commands whose argument is upright text
    for cmd in ("textsc", "textrm", "mathrm", "operatorname", "text", "mbox"):
        s = re.sub(r"\\%s\{([^{}]*)\}" % cmd, lambda m: keep(m.group(1)), s)
    # 2. upright function names
    for name, _ in SYM:
        if name in (r"\arg\max", r"\max", r"\min", r"\log", r"\exp"):
            s = s.replace(name, keep(name[1:]))
    # 3. combining accents
    s = re.sub(r"\\hat\{([^{}]*)\}", lambda m: m.group(1) + "\u0302", s)
    s = re.sub(r"\\bar\{([^{}]*)\}", lambda m: m.group(1) + "\u0304", s)
    # 4. literal braces
    s = s.replace(r"\{", keep("{")).replace(r"\}", keep("}"))
    # 5. greek / operators
    for name, rep in SYM:
        if rep is not None:
            s = s.replace(name, rep)
    # 6. superscripts / subscripts (recursive so inner letters italicise)
    s = re.sub(r"\^\{([^{}]*)\}", lambda m: keep("<sup>%s</sup>" % _mrender(m.group(1))), s)
    s = re.sub(r"_\{([^{}]*)\}", lambda m: keep("<sub>%s</sub>" % _mrender(m.group(1))), s)
    s = re.sub(r"\^(\S)", lambda m: keep("<sup>%s</sup>" % _mrender(m.group(1))), s)
    s = re.sub(r"_(\S)", lambda m: keep("<sub>%s</sub>" % _mrender(m.group(1))), s)
    # 7. leftover commands -> upright word
    s = re.sub(r"\\([A-Za-z]+)", lambda m: keep(m.group(1)), s)
    # 8. stray grouping braces
    s = s.replace("{", "").replace("}", "")
    # 9. italicise variable letters
    s = re.sub(r"[A-Za-z]+", lambda m: "<i>%s</i>" % m.group(0), s)
    # 10. restore
    for i, txt in enumerate(stash):
        tok = "\ue000%d\ue001" % i
        if tok in s:
            s = s.replace(tok, txt)
    return s


def extract_math(md):
    """Pull TeX out of the markdown BEFORE conversion so markdown cannot mangle it."""
    store = {"disp": [], "inl": []}

    def disp(m):
        store["disp"].append(m.group(1).replace("\n", " "))
        return "ZHDISPLAY%dEND" % (len(store["disp"]) - 1)

    def inl(m):
        store["inl"].append(m.group(1))
        return "ZHINL%dEND" % (len(store["inl"]) - 1)

    md = re.sub(r"\$\$(.+?)\$\$", disp, md, flags=re.S)
    md = re.sub(r"(?<!\$)\$([^$\n]+?)\$(?!\$)", inl, md)
    return md, store


def restore_math(html_str, store):
    html_str = re.sub(
        r"<p>\s*ZHDISPLAY(\d+)END\s*</p>",
        lambda m: '<div class="eq"><span class="m">%s</span></div>'
                  % _mrender(store["disp"][int(m.group(1))]),
        html_str)
    html_str = re.sub(
        r"ZHDISPLAY(\d+)END",
        lambda m: '<div class="eq"><span class="m">%s</span></div>'
                  % _mrender(store["disp"][int(m.group(1))]),
        html_str)
    html_str = re.sub(
        r"ZHINL(\d+)END",
        lambda m: '<span class="m">%s</span>' % _mrender(store["inl"][int(m.group(1))]),
        html_str)
    return html_str


def split_titleblock(body):
    """Pull <h1> and the following author paragraph into a span-all block."""
    m = re.search(r"<h1>(.*?)</h1>\s*(<p[^>]*>.*?</p>)?", body, re.S)
    if not m:
        return body, ""
    title = "<h1>%s</h1>" % m.group(1)
    author = m.group(2) or ""
    block = '<div class="titleblock">%s%s</div>' % (title, author)
    return body[:m.start()] + body[m.end():], block


def main():
    md = open(SRC, encoding="utf-8").read()
    md, mstore = extract_math(md)
    body = convert(md)
    body = restore_math(body, mstore)
    body = re.sub(r"<p><strong>(TABLE [IVX]+\.)</strong>",
                  r'<p class="tcap"><b>\1</b>', body)
    body = re.sub(r"<p>\[(\d+)\]", r'<p class="ref">[\1]', body)
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
