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

## 触达现状（2026-11-06 02:0x 实测）

| 对象 | 渠道 | 结果 |
|---|---|---|
| Jakob Foerster @j_foerst | X 私信（两条） | ✅ **已送达**（会话已置顶，含 DOI 与背书码），暂无回复 |
| **Haoran Xu @ryanxhr** | X 私信（一条） | ✅ **已送达**（UT Austin 博士生，70 篇 cs 论文，最新 2026-11-02；置顶推文正是 arXiv 2604.14265） |
| Amy Zhang @amyzhanginRL | X 私信 | ❌ 收件箱关闭（closed inbox） |
| Shimon Whiteson @shimon8282 | X 私信 | ❌ 收件箱关闭 |

### 你的 X 关注列表扫描结果（@clawgeek，939 关注）

抽样查看前 40 余个关注账号，全部为加密/Web3、AI 工具、自媒体与公司号
（NVIDIAAP、0xMorlex、N1njaCodex、NousResearch、chr1sa、EuniceQXZ、chenmo、
forgivenever、Kimi_Moonshot、bensen、xincctnnq、ziqi_biuty、cryptonerdcn、
sukicao2、thevikitalks、SandAI_HQ、HoodieFade_、anxuanng、hongseyanqiu…）。
**其中没有任何 arXiv 活跃作者**，因此「从关注列表找人」这条路走不通——
需要先关注目标学者（建立真实互动）再谈背书，或直接走论文作者路径。

### 从 2604.14265（VGF, ICLR 2026）作者反查出的新线索

| 作者 | 单位 | 近 5 年 cs 论文 | 最新投稿 | X |
|---|---|---|---|---|
| Haoran Xu | UT Austin 博士生 / Amazon Science Fellow | 70 | 2026-11-02 | @ryanxhr ✅ 已私信 |
| Somayeh Sojoudi | UC Berkeley 教授 | 42 | 2026-10-13 | 账号未确认 |
| Kaiwen Hu | — | 5 | 2026-04-15 | 未知 |
| Amy Zhang | UT Austin 教授 | 79 | 2026-10-19 | @amyzhanginRL（收件箱关闭） |

> 推论：**「读过的论文作者」是最好的背书人来源**——既能证明你熟悉其工作（对方更愿意回应），
> 又能直接用 arXiv API 核实其投稿数是否达标。这条路径比按姓名盲搜可靠得多。


另：`@clawgeek` 已发一条公开求助推文（含题目摘要 + Zenodo DOI，未贴背书码）。

### ⚠️ 重要观察：X 上这类请求正在被嘲讽

搜索 `"arxiv endorsement"` 的最新时间线里，热度最高的一条（7 小时前）是：

> "do you also get weird emails from AI-psychotic independent researchers who want an arXiv endorsement?"

同一时间线还有多人公开求背书（@FabyrkaAI、@copycode69 等）。也就是说，
**冷启动私信求助已经变成一种被社区侧目的行为**。继续群发会伤及作者声誉，
也可能触发 X 的反垃圾限制。建议就此停止广撒网，改走以下优先级：

1. **熟人背书（最高成功率）**：找一位你实际认识、且在 cs 系分类有 3 篇以上投稿的老师/合作者。
   国内做 MARL/RL 的高校作者大多满足条件，一条微信/邮件即可，不必公开求助。
2. **改用不需要背书的渠道**：TechRxiv（本轮已确认 Cloudflare 放行、登录页可达）与 ChinaXiv
   都不设背书门槛，可先拿到公开预印本编号，再回过头补 arXiv。
3. 已有 Zenodo DOI 作为公开可核验锚点，本身已能证明工作存在，背书只是 arXiv 的账号风控要求。

### 操作要点（可复用）

- 打开别人私信：主页 `⋯` 菜单 → 发送消息；若显示 "This user has a closed inbox"，无法私信。
- X Chat 需 4 位 passcode 解锁；发送用 **Ctrl+Enter**（点纸飞机按钮在本机会静默失败）。
- 首条私信若含长链接会被吞，先发一句短文本建立会话，再补细节。

