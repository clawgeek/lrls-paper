# 期刊/会议选刊方案（2026-11-07）

前提：稿件的自我定位是 **规范 + 参考实现**，第 6 节明确写了「无学习式策略、无多种子统计、无基线对比、无实机实验」。
这决定了两条互斥的路径：

- **路径 A（推荐）**：承认它是软件/规范类论文，投**不看 SOTA 的软件期刊**。今天就能准备，无需补实验。
- **路径 B**：先补基线 + 多种子统计，再投算法类期刊。工作量约 1–2 周（代码已有，能跑）。

---

## 路径 A：软件类期刊（无需补实验）

| 期刊 | 定位 | 指标 | 费用 | 周期 | 匹配度 |
|---|---|---|---|---|---|
| **SoftwareX**（Elsevier） | 专门发"软件论文"：软件本身是贡献，不要求性能优势 | SCIE，IF≈1.9，Q2/Q3 | 约 1,200–1,560 USD（各源不一，以官网为准，有豁免政策） | 中位 79 天见刊，最快 17 天 | ★★★★★ 与本文形态完全吻合 |
| **Journal of Open Research Software**（Ubiquity） | 开源研究软件 | ESCI/Scopus | 较低（有豁免） | 约 2–3 个月 | ★★★★ 但要求软件包规范、有文档与测试 |
| **JOSS** | 开源科研软件，需 repo + 文档 + 测试 + 持续集成 | Scopus | **免费** | 2–4 周（评审在 GitHub 公开进行） | ★★★ 需补测试与 CI，单 HTML 文件可能被判"非科研基础设施" |

**SoftwareX 的硬性要求**（决定成败）：
1. 固定模板（6–8 页）：Motivation → Software description（架构图 + 关键代码片段）→ Illustrative examples（截图/结果）→ Impact → 结论；
2. 必须提供可获取的代码仓库、许可证、依赖说明、运行环境；
3. 必须有"软件元数据表"（当前版本、语言、系统要求、开发者、DOI）；
4. 期刊明确**不要求**与同类方法对比性能——这正是我们的护城河。

**改造工作量**：把现有 11 页规范论文压成 6–8 页 SoftwareX 模板，把 §5 的实验改成 Illustrative examples，把 §3 的规范压缩成一张架构图 + 一段文字。约 3–4 小时，我可以直接产出。

---

## 路径 B：算法类期刊（需先补实验）

| 期刊 | 指标 | 费用 | 周期 | 需要补什么 |
|---|---|---|---|---|
| **Algorithms**（MDPI） | JCR Q2（CS Theory & Methods）、CiteScore Q1 | 1,800 CHF | 初审中位 **17.6 天**，录用后 3.9 天见刊 | 至少 1 个基线 + 5 seeds + 均值±方差 |
| **IEEE Access** | Q2，覆盖广 | 约 1,950 USD | 约 4 周初审，4–6 周见刊 | 同上，且审稿人通常要求更强的新颖性论证 |
| **Complex & Intelligent Systems**（Springer） | Q1/Q2 | 约 2,000+ USD | 2–4 个月 | 同上，且要求与 COA/MARL 基线对比 |

**可补的实验（代码已具备，我能直接跑）**：
- 基线 1：随机搜索（均匀采样 + 取最优可行）
- 基线 2：固定温度退火（模拟 COA 的阈值切换）
- 基线 3：单一种群 + 熵退火（去掉调度器，保留双动作集）
- 指标：best feasible、首解步数、违例次数、收敛步数，每档 5 seeds，报告 mean ± std
- 预期结论：调度器版本在"高约束档"上违例更少、闭环更早——即使优势不显著，也是一个诚实的负结果/边际结果

---

## 不推荐

- **顶会（NeurIPS/ICML/ICLR/AAAI）**：截稿已过，且本文无基线，必拒。
- **arXiv**：仍卡 cs.LG 背书（草稿 8335852 保留至 11-19），与期刊投稿不冲突，可并行。
- **同时投多家期刊**：违反一稿多投，绝对不行。

---

## 建议决策

1. **想尽快有一篇正式发表**：走 SoftwareX。今天我做模板改造，2 天内可投。
2. **想要更好的分区/影响因子**：先在 Algorithms 上冲一把，代价是补 1–2 周实验；即便被拒，审稿意见也能用于改稿。
3. **两条并行**：先投 SoftwareX（软件论文），把规范理论部分扩写成第二篇投 Algorithms——内容不重复（一篇讲软件、一篇讲方法与实验），不构成一稿多投。

---

## 投稿信草稿（SoftwareX）

> Dear Editor,
>
> We submit "LRLS: A Deterministic Reference Implementation of Dual-Agent Exploration–Exploitation under Hard Constraints" for consideration as a software paper in SoftwareX.
>
> The submission accompanies an open-source, dependency-free simulator that implements a formal specification for role-separated exploration–exploitation: a high-entropy explorer pool proposes candidate regions, a constraint-aware refiner pool verifies them, and a scheduler allocates budget between the two. The software runs as a single offline HTML file, is fully deterministic under a seeded PRNG, and exposes every intermediate state through a tick-level timeline, making the specification directly inspectable rather than merely described.
>
> We believe it fits SoftwareX because the contribution is the software artefact and the executable specification it embodies, not a claim of superior performance. The manuscript follows the SoftwareX template and reports four operating profiles as illustrative examples, together with an explicit statement of the current limitations (no learned scheduler, no multi-seed statistics, no physical-robot experiments).
>
> The code is available at https://github.com/clawgeek/lrls-paper under the MIT licence, archived at DOI 10.5281/zenodo.23984055, and the preprint is registered as Preprints.org 242857.
>
> Sincerely,
> Jason Sang
