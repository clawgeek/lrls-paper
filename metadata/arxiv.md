# arXiv 投稿表单内容（复制粘贴即用）

平台：https://arxiv.org/submit  （需注册账号，首次投稿需 endorsement）
官方指南：https://info.arxiv.org/help/submit/index.html
PDF-only 规则：https://info.arxiv.org/help/submit_pdf.html

---

## 提交方式（二选一，**不要混用**）

### 方式 A（推荐）：提交 LaTeX 源码，由 arXiv 编译

上传目录 `paper/source/`，只含：

```
main.tex
```

`main.tex` 刻意只用标准 `article` + `amsmath` + `geometry` + `hyperref`，无图、无 bibtex、无 CJK 字符，参考文献用内嵌 `thebibliography`（12 条）。已做静态校验：CJK 0 字符、花括号平衡、`\begin{document}` / `\end{document}` 各 1 次。arXiv 会自动检测 pdflatex 并生成 PDF + HTML 版。

> 注意：**不要**把本包里由 HTML 打印的 `lrls-v1.1-en.pdf` 与 `main.tex` 一起上传。arXiv 明确规定「由 TeX/LaTeX 生成的 PDF」会被拒（因为会与源码编译结果冲突）。

### 方式 B：只提交 PDF（非 TeX 生成）

上传单个 `paper/lrls-v1.1-en.pdf`。该 PDF 由 HTML → Edge print-to-pdf 生成，**不是** TeX 产物，因此符合官方 "PDF-only" 条款（适用于非 TeX 写作工具导出的 PDF）。要求：所有字体嵌入、无 JavaScript、无多个 PDF 拼合。已实测为 PDF-1.4、9 页、397 KB。

---

## 表单字段

### Title

LRLS-v1.1: A Specification and Reference Simulation for Dual-Agent Exploration–Exploitation under Hard Constraints

### Authors

Jason Sang

### Abstract（粘贴到独立摘要框）

We present LRLS (Lobster RL Specification), a formal specification for constrained optimisation in which the classical exploration–exploitation trade-off is role-separated into two heterogeneous agent populations plus a scheduler. A high-entropy crayfish population generates coarse candidate habitats ("mud caves"); a low-entropy, constraint-aware Boston lobster population promotes candidates into verified feasible solutions ("reef gaps") via local refinement and constraint projection; a scheduler allocates population budgets, dispatches tasks and triggers global resampling. The specification fixes the state decomposition, six action primitives, a single reward structure, a shared memory-pool schema, a four-stage training pipeline, seven mandatory reported metrics and a safety layer. We additionally describe v1.1 RoboZero, which maps the agents onto a heterogeneous robot fleet with a geometric embedding space, gossip-synchronised memory, multi-robot consensus voting and zero-shot transfer routes. To make the specification executable, we release a dependency-free deterministic reference simulation (single HTML file, 1100 ticks, 22x22 reward terrain, 22 agents) and report illustrative single-run behaviour across four difficulty settings. This is a specification and a reference implementation, not a claim of algorithmic superiority. No learned policy, no multi-seed statistics, no baseline comparison and no physical-robot experiment are reported here; Section 6 states these limitations explicitly. The aim is to give the central hypothesis — that a learned switching scheduler outperforms fixed temperature or entropy annealing — a precise, reproducible target that can subsequently be falsified.

### Primary category

`cs.LG`（Machine Learning）

### Cross-lists

`cs.RO`（Robotics）、`cs.MA`（Multiagent Systems）

### Comments

9 pages, 4 tables, 1 figure-free reference simulation distributed as ancillary file. Preprint of a specification; not a conference submission. Limitations in Section 6. Companion repository: https://github.com/clawgeek/openclaw-zen

### License

推荐 `arXiv.org perpetual, non-exclusive license`（默认）或 `CC BY 4.0`（与 Zenodo 保持一致）。

### DOI / journal-ref

留空。arXiv 不分配 DOI，只给 `arXiv:2611.xxxxx` 编号（可另由 Zenodo 提供 DataCite DOI）。

---

## 2026 新规核对（提交前必看）

| 规则 | 对本稿的影响 |
|---|---|
| 2026-02-11 起：投稿须英文撰写或附完整英文翻译 | ✅ 本稿为完整英文；中文版作为 Zenodo/ChinaXiv 补充，不影响 |
| 首次投稿 / 新分类需 **endorsement**（机构邮箱自 2026-01-21 起不再单独够） | ⚠️ **硬阻塞**：需一位已在 `cs.LG` 活跃投稿的 arXiv 作者背书 |
| CS 的 review / survey / position paper 必须先经同行评审 | ⚠️ 本稿定位为 **specification + reference simulation**，标题/摘要刻意不出现 review/survey/perspective/position 字样；但审核员仍可能判定为 position paper，需在 cover note 强调含可执行实现与说明性结果 |
| 2026-10-01 起：每人每月最多 2 篇、在审最多 3 篇 | ✅ 本稿为第 1 篇，无冲突 |
| 所有投稿需 moderation（非同行评审） | 通常 1–2 个工作日公告；约 6% 被 hold、2% 被拒 |

## 获取 endorsement 的三种途径

1. 找一位近年在 `cs.LG` / `cs.RO` 发过 arXiv 论文的合作者，在提交时填其邮箱，系统自动发确认信。
2. 若作者已有 arXiv 账号且在其他分类有投稿记录，可申请分类扩展而非新用户背书。
3. 先投 **Zenodo / ChinaXiv / TechRxiv** 建立公开记录，再以引用关系联系潜在背书人。

## 提交后回填

拿到 `arXiv:2611.xxxxx` 后，把它写入 `metadata/zenodo.json` 的 `related_identifiers`（relation: `isIdenticalTo`），并同步更新 Zenodo 的新版本，让四个渠道互相指向，形成完整的可引用链。
