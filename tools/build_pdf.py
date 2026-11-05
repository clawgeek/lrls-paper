# -*- coding: utf-8 -*-
"""Minimal, dependency-free Markdown -> academic HTML -> PDF builder.

Usage: python tools/build_pdf.py
It reads paper/*.md, writes paper/*.html, then prints instructions for the
Edge headless --print-to-pdf step (invoked from build_pdf.sh).
"""
import os, re, html, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPER = os.path.join(ROOT, "paper")

CSS = """
@page { size: A4; margin: 20mm 19mm 18mm 19mm; }
* { box-sizing: border-box; }
body {
  font-family: "Times New Roman", "Songti SC", "SimSun", Georgia, serif;
  font-size: 10.6pt; line-height: 1.62; color: #17181a; margin: 0;
}
h1 { font-size: 19pt; line-height: 1.32; font-weight: 700; text-align: center;
     margin: 0 0 14pt; letter-spacing: .1pt; }
h2 { font-size: 13pt; font-weight: 700; margin: 20pt 0 8pt; padding-bottom: 4pt;
     border-bottom: .6pt solid #c9ccd1; }
h3 { font-size: 11.2pt; font-weight: 700; margin: 14pt 0 6pt; color: #1f2937; }
p { margin: 0 0 8pt; text-align: justify; hyphens: auto; }
.meta { text-align: center; font-size: 10pt; color: #4b5563; margin: 0 0 3pt; }
.meta.strong { font-weight: 700; color: #111827; font-size: 11pt; }
hr { border: 0; border-top: .6pt solid #d4d7dc; margin: 16pt 0; }
strong { font-weight: 700; }
em { font-style: italic; }
code, .m { font-family: "Cambria Math", "Times New Roman", serif; font-style: italic;
           background: #f5f5f2; padding: 0 1.5pt; border-radius: 2pt; font-size: 10.2pt; }
code { font-style: normal; font-family: Consolas, Menlo, monospace; font-size: 9pt; }
pre { background: #f7f7f4; border: .6pt solid #dcded9; border-radius: 4pt;
      padding: 8pt 10pt; font-size: 8.8pt; line-height: 1.45; margin: 6pt 0 10pt;
      white-space: pre-wrap; overflow-wrap: anywhere; }
pre code { background: none; padding: 0; font-size: 8.8pt; }
.blockmath { text-align: center; margin: 10pt 0; font-style: italic; font-size: 11.5pt; }
table { border-collapse: collapse; width: 100%; margin: 8pt 0 12pt; font-size: 9.2pt; }
th, td { border: .5pt solid #c9ccd1; padding: 4pt 6pt; text-align: left; vertical-align: top; }
th { background: #f0f1ee; font-weight: 700; }
tr:nth-child(even) td { background: #fbfbf9; }
ul, ol { margin: 4pt 0 10pt; padding-left: 20pt; }
li { margin: 0 0 4pt; }
.ref { padding-left: 20pt; text-indent: -20pt; font-size: 9.5pt; margin: 0 0 5pt; }
.abstract { background: #f7f7f4; border-left: 2.4pt solid #9c2f2a;
            padding: 9pt 12pt; margin: 12pt 0 16pt; }
.abstract p { margin-bottom: 6pt; }
.abstract p:last-child { margin-bottom: 0; }
.foot { margin-top: 18pt; padding-top: 8pt; border-top: .6pt solid #d4d7dc;
        font-size: 8.6pt; color: #6b7280; text-align: center; }
h2, h3 { break-after: avoid; }
table, pre, .abstract { break-inside: avoid; }
"""

def tex2txt(s):
    """Render a small subset of LaTeX math as readable HTML (no MathJax)."""
    repl = {
        r"\lambda_v": "λ_v", r"\lambda_{v}": "λ_v",
        r"\lambda_e": "λ_e", r"\lambda_{e}": "λ_e",
        r"\lambda_m": "λ_m", r"\lambda_{m}": "λ_m",
        r"\mathcal{H}": "ℋ", r"\mathcal{M}": "M",
        r"\times": "×", r"\cdot": "·", r"\approx": "≈",
        r"\geq": "≥", r"\leq": "≤", r"\neq": "≠",
        r"\in": "∈", r"\sum": "Σ", r"\varepsilon": "ε",
        r"\,": " ", r"\;": " ", r"\!": "",
    }
    for a, b in repl.items():
        s = s.replace(a, b)
    s = re.sub(r"\\texttt\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\text\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\mathrm\{([^}]*)\}", r"\1", s)
    s = re.sub(r"_\{([^}]*)\}", r"<sub>\1</sub>", s)
    s = re.sub(r"\^\{([^}]*)\}", r"<sup>\1</sup>", s)
    s = re.sub(r"_([A-Za-z0-9])", r"<sub>\1</sub>", s)
    s = re.sub(r"\\[A-Za-z]+", "", s)
    return s.replace("{", "").replace("}", "").strip()

def inline(s):
    s = html.escape(s, quote=False)
    # protect math first
    maths = []
    def keep(m):
        maths.append(tex2txt(m.group(1)))
        return "\x00M%d\x00" % (len(maths) - 1)
    s = re.sub(r"\$([^$]+)\$", keep, s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\\texttt\{([^}]+)\}", r"<code>\1</code>", s)
    # links: bare URLs
    s = re.sub(r"(https?://[^\s)<,]+)", r'<span style="word-break:break-all">\1</span>', s)
    for i, v in enumerate(maths):
        s = s.replace("\x00M%d\x00" % i, '<span class="m">%s</span>' % v)
    return s

def convert(md):
    lines = md.split("\n")
    out, i, in_abs = [], 0, False
    n = len(lines)
    while i < n:
        ln = lines[i].rstrip()
        st = ln.strip()

        if not st:
            i += 1; continue

        if st.startswith("```"):
            lang = st[3:].strip(); i += 1; buf = []
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i]); i += 1
            i += 1
            out.append("<pre><code>%s</code></pre>" % html.escape("\n".join(buf)))
            continue

        if st.startswith("$$"):
            expr = st[2:].strip()
            if expr.endswith("$$"):
                out.append('<div class="blockmath">%s</div>' % inline("$" + expr[:-2] + "$"))
                i += 1; continue
            i += 1; buf = []
            while i < n and not lines[i].strip().startswith("$$"):
                buf.append(lines[i].strip()); i += 1
            i += 1
            out.append('<div class="blockmath">%s</div>' % inline("$" + " ".join(buf) + "$"))
            continue

        if st.startswith("|") and i + 1 < n and re.match(r"^\|[\s:|-]+\|$", lines[i+1].strip()):
            hdr = [c.strip() for c in st.strip("|").split("|")]
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            t = ["<table><thead><tr>" + "".join("<th>%s</th>" % inline(c) for c in hdr) + "</tr></thead><tbody>"]
            for r in rows:
                t.append("<tr>" + "".join("<td>%s</td>" % inline(c) for c in r) + "</tr>")
            t.append("</tbody></table>")
            out.append("".join(t))
            continue

        if st == "---":
            if in_abs:
                out.append("</div>"); in_abs = False
            out.append("<hr>"); i += 1; continue

        if st.startswith("### "):
            out.append("<h3>%s</h3>" % inline(st[4:])); i += 1; continue
        if st.startswith("## "):
            title = st[3:]
            if in_abs:
                out.append("</div>"); in_abs = False
            if title.strip().lower().startswith("abstract") or title.strip().startswith("摘要"):
                out.append('<div class="abstract">'); in_abs = True
            out.append("<h2>%s</h2>" % inline(title)); i += 1; continue
        if st.startswith("# "):
            out.append("<h1>%s</h1>" % inline(st[2:])); i += 1; continue

        if re.match(r"^\[\d+\]", st):
            out.append('<p class="ref">%s</p>' % inline(st)); i += 1; continue

        if re.match(r"^\d+\.\s", st) or st.startswith("- "):
            items = []
            ordered = bool(re.match(r"^\d+\.\s", st))
            while i < n:
                q = lines[i].strip()
                if ordered and re.match(r"^\d+\.\s", q):
                    items.append(re.sub(r"^\d+\.\s+", "", q)); i += 1
                elif not ordered and q.startswith("- "):
                    items.append(q[2:]); i += 1
                else:
                    break
            tag = "ol" if ordered else "ul"
            out.append("<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % inline(x) for x in items), tag))
            continue

        # paragraph: merge consecutive plain lines
        buf = [st]; i += 1
        while i < n:
            q = lines[i].strip()
            if (not q or q.startswith(("#", "|", "```", "$$", "---", "- ", "["))
                    or re.match(r"^\d+\.\s", q)):
                break
            buf.append(q); i += 1
        text = " ".join(buf)
        cls = ' class="meta strong"' if text.startswith("**Jason Sang") or text.startswith("**桑杰逊") else (
              ' class="meta"' if ("Independent Researcher" in text or "Preprint version" in text
                                 or "独立研究者" in text or "预印本 v1.0" in text) else "")
        out.append("<p%s>%s</p>" % (cls, inline(text)))
    if in_abs:
        out.append("</div>")
    return "\n".join(out)

def build(src, dst, lang, subtitle):
    md = open(src, encoding="utf-8").read()
    body = convert(md)
    foot = ("Preprint v1.0 · 2026-11-05 · LRLS-v1.1 · Text CC BY 4.0 / Code MIT"
            if lang == "en" else
            "预印本 v1.0 · 2026-11-05 · LRLS-v1.1 · 正文 CC BY 4.0 / 代码 MIT")
    doc = ("<!DOCTYPE html><html lang=\"%s\"><head><meta charset=\"utf-8\">"
           "<title>%s</title><style>%s</style></head><body>%s"
           "<div class=\"foot\">%s</div></body></html>") % (
               lang, html.escape(subtitle), CSS, body, html.escape(foot))
    open(dst, "w", encoding="utf-8").write(doc)
    print("HTML  %-28s %7d bytes" % (os.path.basename(dst), os.path.getsize(dst)))

if __name__ == "__main__":
    build(os.path.join(PAPER, "lrls-v1.1-en.md"),
          os.path.join(PAPER, "lrls-v1.1-en.html"), "en",
          "LRLS-v1.1: A Specification and Reference Simulation")
    build(os.path.join(PAPER, "lrls-v1.1-zh.md"),
          os.path.join(PAPER, "lrls-v1.1-zh.html"), "zh-CN",
          "LRLS-v1.1：硬约束下双体探索–开发强化学习规范与参考仿真")
