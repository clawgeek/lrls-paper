# -*- coding: utf-8 -*-
"""Pull author contact emails out of arXiv PDFs.

The X DM route produced no replies; email is the channel that actually works,
but guessing addresses is worse than reading them off the paper. For each
candidate we take their most recent cs papers, download page 1, and scrape
e-mail addresses in order of preference (institutional over webmail).
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

import pymupdf

NS = {"a": "http://www.w3.org/2005/Atom"}
CS = {"cs.LG", "cs.AI", "cs.RO", "cs.MA", "cs.NE", "cs.SY", "cs.CL", "cs.CV", "cs.IR"}
UA = {"User-Agent": "Mozilla/5.0 (lrls-endorser-scan)"}
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")


def query(name, n=40):
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"search_query": 'au:"%s"' % name, "start": 0, "max_results": n,
         "sortBy": "submittedDate", "sortOrder": "descending"})
    root = ET.fromstring(urllib.request.urlopen(
        urllib.request.Request(url, headers=UA), timeout=60).read().decode())
    out = []
    for e in root.findall("a:entry", NS):
        cats = [c.get("term") for c in e.findall("a:category", NS)]
        out.append({
            "id": e.find("a:id", NS).text.split("/abs/")[-1],
            "published": e.find("a:published", NS).text[:10],
            "title": " ".join(e.find("a:title", NS).text.split()),
            "cats": cats,
        })
    return out


def page1_text(arxiv_id):
    """curl for the PDF.

    Two quirks on this network: arXiv keeps the connection open so curl exits 28
    (timeout) even though the file arrived intact, and on Windows the temp file
    cannot be unlinked while pymupdf still holds it. Both are handled here.
    """
    import os
    import subprocess
    import tempfile

    base = arxiv_id.split("v")[0] if re.search(r"v\d+$", arxiv_id) else arxiv_id
    fd, tmp = tempfile.mkstemp(suffix=".pdf")
    os.close(fd)
    try:
        subprocess.run(["curl", "-sL", "--max-time", "60", "-A", "Mozilla/5.0",
                        "-o", tmp, "https://arxiv.org/pdf/%s" % base],
                       timeout=90, check=False)
        if os.path.getsize(tmp) < 20000:
            raise RuntimeError("empty pdf")
        doc = pymupdf.open(tmp)
        try:
            return doc[0].get_text()
        finally:
            doc.close()
    finally:
        for _ in range(3):
            try:
                if os.path.exists(tmp):
                    os.unlink(tmp)
                break
            except PermissionError:
                time.sleep(0.4)


def score(addr):
    """Lower is better: institutional addresses beat webmail."""
    webmail = ("gmail.com", "outlook.com", "hotmail.com", "yahoo.com", "qq.com",
               "163.com", "126.com")
    s = 1
    for w in webmail:
        if addr.endswith(w):
            s = 5
    if "noreply" in addr or "arxiv" in addr or "example" in addr:
        s = 99
    return s


def scan(name, tries=2):
    papers = [p for p in query(name) if set(p["cats"]) & CS]
    found = []
    for p in papers[:tries]:
        try:
            txt = page1_text(p["id"])
        except Exception as exc:                      # noqa: BLE001
            print("  ! pdf fail", p["id"], exc, file=sys.stderr)
            continue
        addr = sorted({a.lower().strip(".,;:()") for a in EMAIL_RE.findall(txt)},
                      key=score)
        addr = [a for a in addr if score(a) < 90]
        found.append({"paper": p["title"], "id": p["id"],
                      "date": p["published"], "emails": addr})
        if any(score(a) == 1 for a in addr):
            break
        time.sleep(6.0)
    return papers[:3], found


def main():
    names = ["Jakob Foerster", "Haoran Xu", "Amy Zhang", "Ke Li", "Somayeh Sojoudi"]
    out = {}
    for n in names:
        print("== %s" % n, file=sys.stderr)
        papers, found = scan(n)
        best = [a for f in found for a in f["emails"] if score(a) == 1]
        out[n] = {
            "papers": [{"id": p["id"], "title": p["title"], "date": p["published"]}
                       for p in papers],
            "scan": found,
            "suggested": best[0] if best else (found[0]["emails"][0]
                                               if found and found[0]["emails"] else None),
        }
        print("   ->", out[n]["suggested"], file=sys.stderr, flush=True)
        # write incrementally so a timeout still leaves usable data
        json.dump(out, open("tools/endorser_emails.json", "w", encoding="utf-8"),
                  indent=1, ensure_ascii=False)
        time.sleep(3.2)
    json.dump(out, open("tools/endorser_emails.json", "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    for n, v in out.items():
        print("%-18s %-34s %s" % (n, v["suggested"] or "-",
                                  v["papers"][0]["title"][:52] if v["papers"] else ""))


if __name__ == "__main__":
    main()
