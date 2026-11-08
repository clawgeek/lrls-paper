# -*- coding: utf-8 -*-
"""Generate ready-to-send .eml files for the arXiv endorsement requests.

Every address below was read off an official page, not guessed:
  jakob.foerster@eng.ox.ac.uk   St Anne's College / Dept of Engineering Science
  haoran.xu@utexas.edu          UT Austin course page (TA listing)
  amy.zhang@austin.utexas.edu   UT CS faculty page + WNCG profile
  k.li@exeter.ac.uk             COLA Lab @ Exeter contact block

Double-clicking an .eml opens the default mail client with To / Subject / body
filled in; the user only has to press Send. Bodies are plain ASCII so no mail
client can mangle the encoding.
"""
import os
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "metadata" / "emails"

FROM = "Jason Sang <sangjiexun@gmail.com>"

COMMON_TAIL = """
Preprint: doi.org/10.5281/zenodo.23984055
Code and data: github.com/clawgeek/lrls-paper

If you are willing, my endorsement code is KDOBWQ at
https://arxiv.org/auth/endorse - it takes about thirty seconds. If not, that is
entirely fine; I will not follow up.

Best regards,
Jason Sang (Sang Jiexun)
Independent Researcher, China
sangjiexun@gmail.com
"""

TARGETS = [
    {
        "file": "1-foerster",
        "to": "jakob.foerster@eng.ox.ac.uk",
        "subject": "arXiv endorsement request (cs.LG) - one 30-second step",
        "body": """Dear Professor Foerster,

I am an independent researcher working on constrained exploration-exploitation in
multi-agent optimisation. I am writing to ask whether you would endorse my first
cs.LG submission to arXiv. This is an account requirement for new submitters, not
a request for you to review or vouch for the work.

Your zero-shot coordination work is why I framed the coordination side of this
problem as role separation rather than as a schedule. The paper moves the
exploration-exploitation switch out of a scalar temperature into two
heterogeneous populations plus a scheduler, ships a dependency-free reference
implementation, and reports a five-seed, budget-matched comparison against four
baselines. The headline result is unflattering to my own method: random search
and a single-pool ablation reach 99% of the optimum 1.3-2.9x faster than mine.
What role separation buys is constraint safety on the path - zero hazard-zone
evaluations before the quality threshold in every seed, versus 16-456 for every
baseline.
""" + COMMON_TAIL,
    },
    {
        "file": "2-xu",
        "to": "haoran.xu@utexas.edu",
        "subject": "arXiv endorsement request (cs.LG) - one 30-second step",
        "body": """Dear Haoran,

I am an independent researcher working on constrained exploration-exploitation in
multi-agent optimisation. I am writing to ask whether you would endorse my first
cs.LG submission to arXiv. This is an account requirement for new submitters, not
a request for you to review the work.

Reading your value-gradient-flow paper is what convinced me to treat the
exploration term as a transport cost rather than as a bonus. The paper moves the
exploration-exploitation switch out of a scalar schedule into two heterogeneous
populations plus a scheduler, ships a dependency-free reference implementation,
and reports a five-seed, budget-matched comparison against four baselines. The
headline result is unflattering to my own method: random search and a single-pool
ablation reach 99% of the optimum 1.3-2.9x faster than mine. What role separation
buys is constraint safety on the path - zero hazard-zone evaluations before the
quality threshold in every seed, versus 16-456 for every baseline.
""" + COMMON_TAIL,
    },
    {
        "file": "3-zhang",
        "to": "amy.zhang@austin.utexas.edu",
        "subject": "arXiv endorsement request (cs.LG) - one 30-second step",
        "body": """Dear Professor Zhang,

I am an independent researcher working on constrained exploration-exploitation.
I am writing to ask whether you would endorse my first cs.LG submission to arXiv.
This is an account requirement for new submitters, not a request for you to
review or vouch for the work.

Your work on sample efficiency and generalisation is the yardstick I used to
report my own result honestly. The paper moves the exploration-exploitation
switch out of a scalar schedule into two heterogeneous populations plus a
scheduler, and reports a five-seed, budget-matched comparison against four
baselines. The headline finding is a negative one for speed: random search and a
single-pool ablation reach 99% of the optimum 1.3-2.9x faster than mine. What
role separation buys is constraint safety on the path - zero hazard-zone
evaluations before the quality threshold in every seed, versus 16-456 for every
baseline. The paper argues for a property, not a speed-up.
""" + COMMON_TAIL,
    },
    {
        "file": "4-li",
        "to": "k.li@exeter.ac.uk",
        "subject": "arXiv endorsement request (cs.LG) - one 30-second step",
        "body": """Dear Professor Li,

I am an independent researcher working on constrained exploration-exploitation in
metaheuristics. I am writing to ask whether you would endorse my first cs.LG
submission to arXiv. This is an account requirement for new submitters, not a
request for you to review the work.

Your MOEA/D survey and the constraint-handling material in it shaped how I set up
the feasibility gate in this work. The paper compares a role-separated scheme
against random search, simulated annealing, a single-pool ablation and a
COA-style temperature gate, all under the same evaluation budget and the same
feasibility threshold, five seeds per setting. The headline result is
unflattering to my own method: random search and the single-pool ablation reach
99% of the optimum 1.3-2.9x faster. What the role separation buys is constraint
safety on the path - zero hazard-zone evaluations before the threshold in every
seed, versus 16-456 for every baseline, and the COA-style gate is worse on both
axes.
""" + COMMON_TAIL,
    },
]


def build(target):
    return (
        "To: {to}\n"
        "From: {frm}\n"
        "Subject: {subject}\n"
        "MIME-Version: 1.0\n"
        'Content-Type: text/plain; charset="utf-8"\n'
        "Content-Transfer-Encoding: 8bit\n"
        "X-Unsent: 1\n"
        "\n"
        "{body}\n"
    ).format(to=target["to"], frm=FROM, subject=target["subject"],
             body=target["body"])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for t in TARGETS:
        path = OUT / (t["file"] + ".eml")
        path.write_text(build(t), encoding="utf-8")
        words = len(t["body"].split())
        print("%-28s %-30s %d words" % (path.name, t["to"], words))
    print("\ndir:", OUT)


if __name__ == "__main__":
    main()
