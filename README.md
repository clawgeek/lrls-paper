# LRLS-v1.1 — 论文发布包 / Preprint Submission Kit

**LRLS-v1.1: A Specification and Reference Simulation for Dual-Agent Exploration–Exploitation under Hard Constraints**

作者：桑杰逊 Jason Sang · 独立研究者 · 预印本 v1.0 · 2026-11-05

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23984055.svg)](https://doi.org/10.5281/zenodo.23984055)

**已正式发布到 Zenodo**：DOI [`10.5281/zenodo.23984055`](https://doi.org/10.5281/zenodo.23984055) · 概念 DOI `10.5281/zenodo.23984054` · [记录页](https://zenodo.org/record/23984055) · 8 个文件 / 1.96 MB / CC BY 4.0。

引用格式：

```
Sang, J. (2026). LRLS-v1.1: A Specification and Reference Simulation for
Dual-Agent Exploration–Exploitation under Hard Constraints. Zenodo.
https://doi.org/10.5281/zenodo.23984055
```

本仓库是《龙虾双体智能体强化学习规范》从对话草稿整理成的**正式预印本**及其在四个发布渠道（Zenodo / ChinaXiv / TechRxiv / arXiv）的提交包。

> 定位说明：本文是**规范 + 参考实现**，不是性能更优的算法论文。文中没有学习式调度策略、多种子统计、基线对比或真实机器人实验，第 6 节逐条列明局限。核心待验证假设是「学习式切换调度器优于固定温度／熵退火」。

---

## 四渠道状态一览

| 渠道 | 产出 | 状态（2026-11-06） |
|---|---|---|
| **Zenodo** | ✅ **`10.5281/zenodo.23984055`**（概念 DOI `…23984054`） | **已发布**：8 文件 / 1.96 MB / CC BY 4.0，DataCite 元数据已可解析 |
| **ChinaXiv** | `10.12074/…` DOI + CSTR + 科创链 TXID | ⚠️ 中文全文与表单就绪并已回填 Zenodo DOI；需本人注册 + 实名 |
| **TechRxiv** | IEEE 预印本 DOI | ⚠️ 表单就绪并已回填；真实浏览器亦被 Cloudflare 拦（403），投稿通道存疑 |
| **arXiv** | `arXiv:2611.xxxxx`，cs.LG + cs.RO/cs.MA | ⚠️ LaTeX / PDF 两条路径就绪并已回填；硬阻塞是 endorsement（需同领域作者背书） |

**为什么另外三个需要你本人操作**：都要求作者本人的学术身份动作（实名、IEEE 账号、同行背书），学术伦理与平台条款上不宜由第三方代做。本包已完成全部可预置工作，你只需登录 + 粘贴 + 上传。实测细节见 `STATUS.md`。

> **诚实声明**：**已取得 1 个真实 DOI（Zenodo）**；ChinaXiv / TechRxiv / arXiv 尚未取得任何编号，未做任何虚构。

---

## 逐步执行

### Step 0 — 优先权时间戳（已完成）

本仓库的 commit 与 `v1.0` tag/release 即为公开、可验证的时间戳。Zenodo 开启 GitHub 集成后，打 tag 会自动存档。

### Step 1 — Zenodo（✅ 已完成）

**实际结果**：版本 DOI `10.5281/zenodo.23984055`，概念 DOI `10.5281/zenodo.23984054`，记录页 https://zenodo.org/record/23984055 。发布脚本与结果保存在 `tools/publish_zenodo.py`、`metadata/zenodo-result.json`。

以下为可复现命令（**不需要再执行**）：

```bash
# 1. 创建 token（scopes: deposit:write, deposit:actions）
#    https://zenodo.org/account/settings/applications/tokens/new/
#    测试用沙盒：https://sandbox.zenodo.org/account/settings/applications/tokens/new/

# 2. 先试运行（无网络、无 token）
python tools/publish_zenodo.py --dry-run

# 3. 沙盒建草稿（可逆，不会产生永久 DOI）
set ZENODO_TOKEN=你的token
python tools/publish_zenodo.py --sandbox

# 4. 确认无误后正式发布（不可逆）
python tools/publish_zenodo.py --live --publish
```

脚本默认**只建草稿、不发布**；只有显式 `--publish` 才会生成永久 DOI。结果写入 `metadata/zenodo-result.json`。

> 也可走网页：登录 Zenodo → `+ New upload` → 上传 `paper/lrls-v1.1-en.pdf` 等文件 → 按 `metadata/zenodo.json` 填表 → Publish。

### Step 2 — ChinaXiv

打开 https://chinaxiv.org/ 注册并实名 → 「提交论文」→ 逐项复制 `metadata/chinaxiv.md` 里的标题/摘要/关键词 → 上传 `paper/lrls-v1.1-zh.pdf` → 提交。
预计获得 `ChinaXiv:202611.XXXXX`、`10.12074/202611.XXXXX`、CSTR 与科创链 TXID。在说明栏注明 Zenodo DOI 即可，已有「先 Zenodo 再同内容存缴」的公开先例，不算重复发表。

### Step 3 — TechRxiv

打开 https://www.techrxiv.org/ 用 IEEE 账号登录 → Submit → 按 `metadata/techrxiv.md` 填表 → 上传 `paper/lrls-v1.1-en.pdf` → 选许可 → 提交，通常 48h 内通过范围审核并给 DOI。
**注意**：本环境实测 `www.techrxiv.org` 与 `techrxiv.figshare.com` 均返回 403（Cloudflare 挑战），且社区反馈 2026 年 5–7 月平台迁移期间曾暂停收稿。请在真实浏览器里确认 Submit 入口是否可用；若关闭，先用 Zenodo 的 DOI 占位，材料无需改动。

### Step 4 — arXiv（最难，最后做）

1. 注册 https://arxiv.org/user/ 并**取得 endorsement**（找一位近年在 `cs.LG`/`cs.RO` 发过 arXiv 的作者；2026-01-21 起机构邮箱不再单独够用）。
2. 二选一提交，**不要混用**：
   - **方式 A（推荐）**：上传 `paper/source/main.tex` 单文件，由 arXiv 编译。已做静态校验（CJK 0 字符、花括号平衡、12 条参考文献内嵌、只依赖标准宏包）。
   - **方式 B**：只上传 `paper/lrls-v1.1-en.pdf`。该 PDF 由 HTML→Edge 打印生成，**不是 TeX 产物**，符合 arXiv 的 PDF-only 条款；若改由 TeX 生成再提交 PDF 会被拒。
3. 表单字段全部在 `metadata/arxiv.md`，摘要可直接粘贴。主分类 `cs.LG`，交叉 `cs.RO` / `cs.MA`。
4. 拿到 `arXiv:2611.xxxxx` 后回填到 `metadata/zenodo.json` 的 `related_identifiers`（`isIdenticalTo`），并发一个 Zenodo 新版本，让四个渠道互链。

### Step 5 — 回填闭环

把四个渠道拿到的 DOI / 编号统一写入 `metadata/zenodo-result.json` 与 `metadata/arxiv.md`，并在 GitHub release notes 里列出，形成单一可引用入口。

**当前进度**：Zenodo DOI 已回填到 `chinaxiv.md` / `techrxiv.md` / `arxiv.md` 三个表单及本 README。拿到其余三个编号后，发一个 Zenodo 新版本（`newversion`）即可闭合互链——概念 DOI `10.5281/zenodo.23984054` 保持不变。

> **安全提醒**：本次发布使用的 Zenodo Personal Access Token 曾出现在对话中，请立即到 https://zenodo.org/account/settings/applications/ 删除 `lrls-preprint-upload` / `lrls-deposit-temp` 两个临时 token。

---

## 文件树

```
LRLS-paper/
├── README.md                         本文件
├── paper/
│   ├── lrls-v1.1-en.md / .html / .pdf    英文主稿（9 页）
│   ├── lrls-v1.1-zh.md / .html / .pdf    中文主稿（8 页，ChinaXiv 用）
│   ├── source/main.tex                   arXiv LaTeX 源码（无 CJK、无外部依赖）
│   └── assets/
│       ├── lrls-sim.html                 单文件离线参考仿真（49 KB）
│       ├── fig-simulation.png            仿真全景 t=680
│       └── fig-parts.png                 部件剖开视图
├── metadata/
│   ├── zenodo.json                      Zenodo deposition 元数据 + 文件清单
│   ├── zenodo-result.json               已发布结果（DOI / 概念 DOI / 记录页）
│   ├── chinaxiv.md                      ChinaXiv 表单内容（已回填 Zenodo DOI）
│   ├── techrxiv.md                      TechRxiv 表单内容（已回填 Zenodo DOI）
│   └── arxiv.md                         arXiv 表单内容与 2026 新规核对（已回填）
└── tools/
    ├── build_pdf.py                     Markdown → HTML（PDF 由 Edge 打印）
    ├── publish_zenodo.py                一键 Zenodo 存档/发布
    └── push_github.js                   Git Data API 推送（绕过代理）
```

## 稿件要点

- **修正了早期草稿的硬伤**：正确引用 COA（Jia et al., 2023, *Artificial Intelligence Review*），删除占位符参考文献与「CoRL 是 CCF-B」的错误说法；明确「零样本」指 zero-shot transfer 而非 zero-shot learning；声明荀子重读是叙事性语义翻转，不是生物学先验。
- **可执行的参考实现**：确定性 solver 预计算 1100 tick，`render(t)` 为纯函数，所有面板/地形/任务板读同一帧；四档难度实测在违例数、弃窟数、首解 tick 上有真实差异。
- **诚定的结果边界**：表 5-1 明确标为「单次确定性运行的说明性结果」，不声称优于任何基线。

## 相关链接

- 心法文本《龙虾之禅 · The Zen of OpenClaw》：https://github.com/clawgeek/openclaw-zen
- OpenClaw 官方提案与评审回复：https://github.com/openclaw/openclaw/issues/192772
- 投稿渠道调研清单：`LRLS-论文投稿渠道清单.md`（工作区根目录）

## 许可

正文 **CC BY 4.0** · 参考实现与脚本 **MIT** · AI 生成的吉祥物横图不在上述许可范围内。
