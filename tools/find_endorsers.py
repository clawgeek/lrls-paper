# -*- coding: utf-8 -*-
"""Find candidate arXiv endorsers for cs.LG.

Criteria (arXiv rules): an endorser must have submitted >=3 papers to a cs.*
category within the last 5 years, with at least one submission no older than
~3 months. We also require topical proximity (exploration-exploitation,
constrained RL, multi-agent RL, metaheuristics) since arXiv recommends
choosing an endorser whose work relates to the submitted paper.

Outputs tools/endorser_candidates.json
"""
import json, os, re, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

NS = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://export.arxiv.org/api/query?"

TOPIC_QUERIES = [
    'cat:cs.LG AND (abs:"exploration-exploitation" OR abs:"exploration exploitation")',
    'cat:cs.LG AND abs:"constrained reinforcement learning"',
    'cat:cs.LG AND abs:"multi-agent reinforcement learning"',
    'cat:cs.LG AND abs:"metaheuristic"',
]
CS_CATS = {"cs.LG", "cs.AI", "cs.RO", "cs.MA", "cs.NE", "cs.SY", "cs.CV", "cs.CL", "cs.IR"}


def fetch(query, max_results=40, sort="submittedDate"):
    url = API + urllib.parse.urlencode({
        "search_query": query, "start": 0, "max_results": max_results,
        "sortBy": sort, "sortOrder": "descending"})
    req = urllib.request.Request(url, headers={"User-Agent": "lrls-endorser-scan/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def parse(xml):
    out = []
    root = ET.fromstring(xml)
    for e in root.findall("a:entry", NS):
        aid = e.find("a:id", NS).text.strip()
        title = " ".join(e.find("a:title", NS).text.split())
        pub = e.find("a:published", NS).text[:10]
        cats = [c.get("term") for c in e.findall("a:category", NS)]
        authors = [a.find("a:name", NS).text.strip() for a in e.findall("a:author", NS)]
        out.append({"id": aid.split("/abs/")[-1], "title": title, "published": pub,
                    "cats": cats, "authors": authors})
    return out


def main():
    # 1. topic-relevant recent papers
    recent = {}
    for q in TOPIC_QUERIES:
        try:
            items = parse(fetch(q, 40))
        except Exception as ex:
            print("query failed:", q, ex)
            continue
        for it in items:
            if it["published"] >= "2026-08-01":
                recent[it["id"]] = it
        time.sleep(3.2)
    print("recent topic papers:", len(recent))

    # 2. tally authors
    tally = {}
    for it in recent.values():
        for a in it["authors"]:
            t = tally.setdefault(a, {"papers": [], "topics": 0})
            t["papers"].append(it["id"])
            t["topics"] += 1
    ranked = sorted(tally.items(), key=lambda kv: -kv[1]["topics"])[:10]
    print("top authors considered:", [a for a, _ in ranked])

    # 3. verify each author's 5-year cs submission record
    results = []
    for name, info in ranked:
        q = 'au:"%s"' % name
        try:
            xml = fetch(q, 100, sort="submittedDate")
            items = parse(xml)
        except Exception as ex:
            print("author query failed:", name, ex)
            time.sleep(3.2)
            continue
        cs_items = [i for i in items
                    if set(i["cats"]) & CS_CATS and i["published"] >= "2021-11-01"]
        oldest_recent = max((i["published"] for i in cs_items), default=None)
        results.append({
            "name": name,
            "recent_topic_papers": info["papers"][:3],
            "cs_papers_5y": len(cs_items),
            "latest_cs_paper": oldest_recent,
            "sample_titles": [i["title"][:90] for i in cs_items[:3]],
        })
        print("%-28s cs5y=%-3d latest=%s" % (name, len(cs_items), oldest_recent))
        time.sleep(3.2)

    out = [r for r in results if r["cs_papers_5y"] >= 3 and r["latest_cs_paper"]
           and r["latest_cs_paper"] >= "2026-08-01"]
    out.sort(key=lambda r: -r["cs_papers_5y"])
    with open(os.path.join(ROOT, "tools", "endorser_candidates.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nQUALIFIED:", len(out))
    for r in out:
        print(" ", r["name"], r["cs_papers_5y"], r["latest_cs_paper"])


if __name__ == "__main__":
    main()
