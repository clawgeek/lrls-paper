# cs.LG 背书人候选清单（2026-11-06 核验）

筛选口径 = arXiv 官方规则（近 5 年内 ≥3 篇 cs 分类投稿、最近一次不早于约 3 个月）
\+ 主题相关（MARL / 探索–开发 / 约束 RL）+ X 上可触达。

核验方法：`tools/find_endorsers.py` 抓取近 3 个月 cs.LG 相关论文 → 作者去重 →
逐个用 arXiv API `au:"Name"` 统计 5 年内 cs 论文数与最新投稿日。

## 第一梯队（主题最贴近，X 账号已确认）

| # | 姓名 | X 账号 | 单位 / 方向 | 近 5 年 cs 论文 | 最新投稿 |
|---|---|---|---|---|---|
| 1 | Jakob Foerster | **@j_foerst** | Oxford 副教授 / Meta AI；多智能体协调、零样本协调 | 117 | 2026-11-04 |
| 2 | Amy Zhang | **@amyzhanginRL** | UT Austin ECE 助理教授；RL 泛化、状态抽象 | 79 | 2026-10-19 |
| 3 | Shimon Whiteson | **@shimon8282** | Oxford / Google DeepMind；MARL | 46 | 2026-10-20 |

Foerster 的最新一篇正是 *Zero-Shot Coordination among LLM Agents*（2026-11-04），
与本稿「双体角色分离 + 调度器」的主题重合度最高，优先联系他。

## 第二梯队（学术匹配但 X 触达性未知）

| 姓名 | 单位 / 方向 | 近 5 年 cs 论文 | 最新投稿 | 备注 |
|---|---|---|---|---|
| Ke Li | 进化计算 / LLM agent | 94 | 2026-11-03 | X 账号未确认 |
| Yuping Wang | 多机器人 / 启发式设计 | 45 | 2026-10-19 | X 账号未确认 |
| Biao Luo | 中南大学；合作式 MARL | 14 | 2026-10-16 | 中文语境，可邮件联系 |
| Dongsu Lee | 合作式 MARL、test-time 协调 | 9 | 2026-10-12 | 主题极贴近，X 账号未确认 |
| Tianmeng Hu | MARL + RNA 设计 | 7 | 2026-10-19 | — |

## 私信草稿（英文，控制在 4 句内）

> Hi — I'm an independent researcher working on role-separated exploration–exploitation
> (two heterogeneous agent pools + a scheduler) with a deterministic reference sim.
> I'm trying to submit my first cs.LG preprint (DOI 10.5281/zenodo.23984055, code public at
> github.com/clawgeek/lrls-paper) and need an arXiv endorser.
> If you've submitted 3+ cs papers in the last five years and are willing to help, I can send
> my endorsement code — it takes about 30 seconds at arxiv.org/auth/endorse.
> No worries at all if not. Thanks for your time.

礼貌要点：① 说明已公开可核验（DOI + 代码）；② 明确「30 秒」降低心理成本；
③ 主动给出拒绝的台阶；④ 不在公开推文里贴背书码。

## 触达现状

- 公开推文已从 @clawgeek 发出（2026-11-06 01:5x），内容含题目摘要与 Zenodo DOI，
  请对方私信联系；未公开背书码 `KDOBWQ`。
- X 私信被 4 位 Chat passcode 加密锁住（x.com/i/chat 要求输入 passcode），
  未解锁前无法自动发私信。解锁后可照上表逐条发送。
