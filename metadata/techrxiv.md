# TechRxiv 投稿表单内容（复制粘贴即用）

平台：https://www.techrxiv.org/ （IEEE 官方预印本，底层 Figshare）
账号：需 IEEE / Figshare 账号登录，作者本人操作
**本环境实测状态（2026-11-05 22:2x GMT+8）**：`www.techrxiv.org`、`techrxiv.figshare.com` 均返回 **HTTP 403（Cloudflare 挑战页）**，`/submit` 在网页抓取器下返回 404。这是反爬拦截，不等于平台关闭；但意味着**无法从命令行/API 代提交**，必须用真实浏览器。另有社区反馈（2026 年 5–7 月）称平台迁移期间曾暂停收稿，请在投稿页现场确认是否有 "Submit" 入口。若确实暂停，见文末替代方案。

---

## Title

LRLS-v1.1: A Specification and Reference Simulation for Dual-Agent Exploration–Exploitation under Hard Constraints

## Authors

Jason Sang (桑杰逊) — Independent Researcher

## Abstract

We present LRLS (Lobster RL Specification), a formal specification for constrained optimisation in which the classical exploration–exploitation trade-off is role-separated into two heterogeneous agent populations plus a scheduler. A high-entropy crayfish population generates coarse candidate habitats ("mud caves"); a low-entropy, constraint-aware Boston lobster population promotes candidates into verified feasible solutions ("reef gaps") via local refinement and constraint projection; a scheduler allocates population budgets, dispatches tasks and triggers global resampling. The specification fixes the state decomposition, six action primitives, a single reward structure, a shared memory-pool schema, a four-stage training pipeline, seven mandatory reported metrics and a safety layer. We additionally describe v1.1 RoboZero, which maps the agents onto a heterogeneous robot fleet with a geometric embedding space, gossip-synchronised memory, multi-robot consensus voting and zero-shot transfer routes. To make the specification executable, we release a dependency-free deterministic reference simulation (single HTML file, 1100 ticks, 22x22 reward terrain, 22 agents) and report illustrative single-run behaviour across four difficulty settings. This is a specification and a reference implementation, not a claim of algorithmic superiority. No learned policy, no multi-seed statistics, no baseline comparison and no physical-robot experiment are reported; Section 6 states these limitations explicitly. The aim is to give the central hypothesis — that a learned switching scheduler outperforms fixed temperature or entropy annealing — a precise, reproducible target that can subsequently be falsified.

## Keywords

reinforcement learning; exploration–exploitation; multi-agent systems; constrained optimisation; crayfish optimization algorithm; heterogeneous robot fleet; zero-shot transfer; engineering specification; simulation

## Subject category（按平台下拉项选最接近者）

Computer Science / Artificial Intelligence / Robotics and Control Systems（或 "Machine Learning"）

## Upload files

- 主文件：`paper/lrls-v1.1-en.pdf`（英文全文，9 页）
- 补充文件：`paper/assets/lrls-sim.html`（参考仿真）、`paper/assets/fig-simulation.png`（仿真截图）

## License

建议 **CC BY-NC-ND** 或保留版权（与后续投 IEEE 会议/期刊兼容；若已确定走完全 OA，可选 CC BY 4.0 与 Zenodo 一致）。

## Comments / Notes 栏

Preprint v1.0. This is a specification and reference implementation, not a claim of algorithmic superiority; limitations are listed in Section 6. Companion repository: https://github.com/clawgeek/openclaw-zen . No prior publication; not currently under peer review at any IEEE venue. IEEE explicitly treats preprint posting as not prior publication (see e.g. ICASSP 2026 preprint policy).

## 预期产出

- TechRxiv DOI（`10.36227/techrxiv.…` 形式，由平台分配）
- 版本化：每次修订生成新版本 DOI，概念 DOI 指向最新版

## 兼容性说明

IEEE 明确预印本不构成 prior publication，后续投 ICRA / IROS / RA-L 不受影响（个别期刊可另设政策，投稿前查目标 venue 的 author guidelines）。

## 若投稿通道关闭的替代方案

1. 等 TechRxiv 恢复后重投（材料已备好，无需改稿）。
2. 先用 **Zenodo** 拿到 DataCite DOI 固化时间戳（本包已提供一键脚本），功能等价且更稳。
3. 中文场景可用 **ChinaXiv**（本包含中文全文），英文场景可用 **arXiv**（需背书）。
