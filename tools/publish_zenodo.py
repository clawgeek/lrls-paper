#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""One-command Zenodo depositor for the LRLS-v1.1 preprint.

  # 0. dry run (no network, no token needed)
  python tools/publish_zenodo.py --dry-run

  # 1. get a token: https://zenodo.org/account/settings/applications/tokens/new/
  #    scopes: deposit:write  (+ deposit:actions for publish)
  #    or sandbox: https://sandbox.zenodo.org/account/settings/applications/tokens/new/

  # 2. create a DRAFT on the sandbox and upload all files (reversible)
  set ZENODO_TOKEN=xxxxxxxx
  python tools/publish_zenodo.py --sandbox

  # 3. publish for real (irreversible: creates a permanent DOI)
  python tools/publish_zenodo.py --live --publish

The script NEVER publishes unless --publish is passed explicitly.
"""
import os, sys, json, argparse

try:
    import requests
except ImportError:
    sys.exit("requests is required: pip install requests")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
META = os.path.join(ROOT, "metadata", "zenodo.json")


def api(session, method, url, **kw):
    r = session.request(method, url, timeout=60, **kw)
    if r.status_code >= 400:
        sys.stderr.write("API ERROR %s %s -> %s %s\n%s\n" % (
            method, url, r.status_code, r.reason, r.text[:700]))
        sys.exit(2)
    if not r.content:
        return {}
    try:
        return r.json()
    except ValueError:
        return {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--token", default=os.environ.get("ZENODO_TOKEN", ""))
    ap.add_argument("--sandbox", action="store_true", help="use sandbox.zenodo.org")
    ap.add_argument("--live", action="store_true", help="use zenodo.org (production)")
    ap.add_argument("--publish", action="store_true", help="PUBLISH (irreversible)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--deposition-id", default="", help="resume an existing draft")
    args = ap.parse_args()

    cfg = json.load(open(META, encoding="utf-8"))
    files = cfg.pop("files")
    cfg.pop("_comment", None)

    print("=== LRLS-v1.1 Zenodo depositor ===")
    print("title :", cfg["title"])
    print("files :", len(files))
    total = 0
    for rel in files:
        p = os.path.join(ROOT, rel)
        ok = os.path.isfile(p)
        sz = os.path.getsize(p) if ok else 0
        total += sz
        print("  %-46s %8s  %s" % (rel, ("%.1f KB" % (sz / 1024.0)) if ok else "MISSING", "OK" if ok else "!"))
        if not ok:
            sys.exit("Missing file: %s" % rel)
    print("total : %.2f MB" % (total / 1024.0 / 1024.0))

    if args.dry_run:
        print("\n[dry-run] no network calls. Metadata preview:")
        print(json.dumps({k: cfg[k] for k in ("title", "upload_type", "publication_date",
                                              "creators", "license", "keywords")},
                         ensure_ascii=False, indent=2))
        return

    if not args.token:
        sys.exit("\nNo token. Set ZENODO_TOKEN or pass --token.\n"
                 "Create one at https://zenodo.org/account/settings/applications/tokens/new/ "
                 "(scopes: deposit:write, deposit:actions)")

    base = "https://sandbox.zenodo.org/api" if args.sandbox else "https://zenodo.org/api"
    web = "https://sandbox.zenodo.org" if args.sandbox else "https://zenodo.org"
    print("\ntarget:", base, "(SANDBOX - no permanent DOI)" if args.sandbox else "(PRODUCTION)")

    s = requests.Session()
    s.headers.update({"Authorization": "Bearer " + args.token,
                      "User-Agent": "LRLS-preprint-depositor/1.0"})
    s.params = {"access_token": args.token}

    if args.deposition_id:
        dep_id = args.deposition_id
        print("resuming deposition", dep_id)
    else:
        dep = api(s, "POST", base + "/deposit/depositions", json={})
        dep_id = dep["id"]
        print("created draft id:", dep_id)

    # metadata (legacy deposit API expects a {"metadata": {...}} envelope)
    meta = {k: v for k, v in cfg.items() if k not in ("version",)}
    api(s, "PUT", base + "/deposit/depositions/%s" % dep_id, json={"metadata": meta})
    print("metadata set")

    for rel in files:
        p = os.path.join(ROOT, rel)
        with open(p, "rb") as fh:
            api(s, "POST", base + "/deposit/depositions/%s/files" % dep_id,
                data={"name": rel.replace("/", "__")},
                files={"file": (os.path.basename(p), fh)})
        print("  uploaded", rel)

    draft_url = "%s/deposit/%s" % (web, dep_id)
    print("\nDRAFT READY:", draft_url)
    print("   (review the files and metadata in the browser before publishing)")

    if not args.publish:
        print("\nNot published. Re-run with --publish when ready, or press Publish in the web UI.")
        return

    pub = api(s, "POST", base + "/deposit/depositions/%s/actions/publish" % dep_id)
    doi = pub.get("doi") or pub.get("metadata", {}).get("doi", "")
    rec = pub.get("links", {}).get("record_html", "%s/record/%s" % (web, dep_id))
    print("\n=== PUBLISHED ===")
    print("DOI       :", doi)
    print("record    :", rec)
    print("concept   : https://doi.org/%s" % doi if doi else "(see record page)")
    out = {"doi": doi, "record": rec, "deposition_id": dep_id,
           "sandbox": bool(args.sandbox), "published": True}
    with open(os.path.join(ROOT, "metadata", "zenodo-result.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("saved -> metadata/zenodo-result.json")


if __name__ == "__main__":
    main()
