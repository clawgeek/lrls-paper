# -*- coding: utf-8 -*-
"""Figure: budget-matched baseline comparison (5 seeds x 4 profiles x 5 methods).

Panel (a): evaluations needed to reach 99% of the best feasible value (mean, sd).
Panel (b): constraint violations accumulated BEFORE that threshold is reached.

Data: tools/baseline_data.json produced by tools/run_baselines.js
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(os.path.join(ROOT, "tools", "baseline_data.json"), encoding="utf-8"))

METHODS = ["RS", "SP-EA", "SA", "COA-T", "LRLS"]
LABEL = {"RS": "Random search", "SP-EA": "Single pool +\nentropy annealing",
         "SA": "Simulated\nannealing", "COA-T": "COA-style\ntemperature gate",
         "LRLS": "LRLS\n(this work)"}
# Okabe-Ito, LRLS highlighted
COLOR = {"RS": "#999999", "SP-EA": "#56B4E9", "SA": "#E69F00",
         "COA-T": "#009E73", "LRLS": "#D55E00"}

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix", "font.size": 8.5, "axes.linewidth": .8,
    "axes.labelsize": 9, "xtick.labelsize": 7.6, "ytick.labelsize": 7.6,
    "legend.fontsize": 7.4, "figure.dpi": 300,
})

fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.3))
profiles = [s["name"] for s in DATA["summary"]]
x = np.arange(len(profiles))
w = 0.16

for ax, key, title, logy in [
    (axes[0], "n99", "(a) Evaluations to reach 99% of the optimum", True),
    (axes[1], "vioAt99", "(b) Constraint violations before that point", False),
]:
    for i, m in enumerate(METHODS):
        vals, errs = [], []
        for s in DATA["summary"]:
            v = s["methods"][m][key]
            vals.append(np.nan if v["mean"] is None else v["mean"])
            errs.append(0 if v["sd"] is None else v["sd"])
        vals = np.array(vals, dtype=float)
        errs = np.array(errs, dtype=float)
        pos = x + (i - 2) * w
        yerr = np.vstack([np.minimum(errs, np.nan_to_num(vals)), errs])
        ax.bar(pos, np.nan_to_num(vals), w, yerr=yerr, capsize=1.6,
               color=COLOR[m], edgecolor="black", linewidth=.4,
               error_kw=dict(lw=.6, capthick=.6), label=LABEL[m])
        for px_, v in zip(pos, vals):
            if np.isnan(v):
                ax.text(px_, 0.4 if logy else 0.6, "×", ha="center", va="bottom",
                        fontsize=8, color="black")
    ax.set_xticks(x)
    ax.set_xticklabels([p.replace("-", "\n") for p in profiles], fontsize=7.2)
    ax.set_title(title, fontsize=8.6, loc="left", pad=4)
    ax.grid(axis="y", ls=":", lw=.5, alpha=.6)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    if logy:
        ax.set_yscale("log")
        ax.set_ylabel("evaluations (log scale)")
    else:
        ax.set_ylabel("violations")
    ax.margins(x=.02)

handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, ncol=5, frameon=False, loc="lower center",
           handlelength=1.0, columnspacing=1.2, handletextpad=.5,
           bbox_to_anchor=(.5, -.02))

fig.tight_layout(pad=.6, rect=(0, .10, 1, 1))
out = os.path.join(ROOT, "paper", "assets", "fig-baselines.png")
fig.savefig(out, bbox_inches="tight")
print("wrote", out, os.path.getsize(out), "bytes")
