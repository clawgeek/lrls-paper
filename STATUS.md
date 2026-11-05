# 发布进度实测报告

更新时间：2026-11-06 00:0x GMT+8
执行：Agent mode，工作区 `C:/Users/10099/WorkBuddy/2026-11-04-19-28-06`

---

## ✅ Zenodo 已正式发布（第一个真实 DOI）

| 项 | 值 |
|---|---|
| **版本 DOI** | `10.5281/zenodo.23984055` |
| **概念 DOI** | `10.5281/zenodo.23984054`（指向最新版，跨版本不变） |
| 记录页 | https://zenodo.org/record/23984055 |
| 规范引用 | https://doi.org/10.5281/zenodo.23984055 |
| deposition id | 23984055 |
| 状态 | `submitted / done`（deposit API 返回 http 202，DataCite 元数据已可解析） |
| 许可 | CC BY 4.0（正文），参考实现 MIT |
| 文件 | 8 个，1.96 MB，英文 PDF 排首位 |
| 发布时刻 | 2026-11-05 |

DataCite 侧已核对：`https://api.datacite.org/dois/10.5281/zenodo.23984055` 返回完整元数据，作者 `Sang, Jason`、publicationYear 2026、publisher Zenodo、标题一致。

### 上传的 8 个文件（已整理为扁平命名）

```
lrls-v1.1-en.pdf          397,655 B   英文主稿 9 页
lrls-v1.1-zh.pdf          474,215 B   中文主稿 8 页
lrls-v1.1-en.md            23,360 B
lrls-v1.1-zh.md            17,983 B
lrls-v1.1-source.tex       20,743 B   arXiv 可编译源码
lrls-sim.html              49,475 B   单文件离线仿真
fig-simulation.png        516,905 B
fig-parts.png             552,474 B
```

元数据：title / description(1064 字符) / publication_date 2026-11-05 / creators 1 / keywords 10 / upload_type=publication(preprint) / access_right=open / license cc-by-4.0 / related_identifiers 指向 `clawgeek/openclaw-zen` 与 OpenClaw issue #192772。

发布路径：用户完成 Zenodo 的 GitHub OAuth 授权并提供 Personal Access Token（scope: `deposition actions` + `deposit:write`）→ `tools/publish_zenodo.py --live` 建草稿并上传 → 手工整理文件名与顺序 → `POST /actions/publish`。**Token 仅用于本次发布，未写入任何文件、日志、脚本或记忆；发布后应立即在 Zenodo → Applications 撤销。**

---

## 四渠道最终状态

| 渠道 | 状态 | 说明 |
|---|---|---|
| **Zenodo** | ✅ **已发布，DOI 10.5281/zenodo.23984055** | 8 文件全量存档，DataCite 可解析，已作为其余渠道的引用锚点 |
| **ChinaXiv** | ⚠️ 待本人操作 | 中文全文 + `metadata/chinaxiv.md` 表单已回填 Zenodo DOI；需注册 + 实名认证，第三方不得代提交 |
| **TechRxiv** | ⚠️ 待本人操作 / 通道存疑 | 英文全文 + `metadata/techrxiv.md` 已回填；命令行与真实 Edge 均被 Cloudflare 拦截（403），且 2026-05～07 迁移期社区反馈曾暂停收稿。若通道不可用，以 Zenodo DOI 作为英文引用入口 |
| **arXiv** | ⚠️ 待本人操作 | LaTeX 源码与非 TeX PDF 两条路径均就绪，`metadata/arxiv.md` 已回填；硬阻塞是 **endorsement**（2026-01-21 起机构邮箱不再单独够用），需同领域作者背书 |

### 为什么另外三个不能由我代提交

三者都要求作者本人的学术身份动作：ChinaXiv 实名认证、arXiv 同行背书、TechRxiv 的 IEEE 账号与反爬挑战。这些在学术伦理与平台条款上都不适合由第三方代做，本环境也确实无法绕过。我能做的可预置工作（稿件、元数据、表单、源码校验、互链回填）已全部完成，**只需登录 + 粘贴 + 上传**。

---

## 已完成（真实落地，非计划）

| # | 动作 | 结果 |
|---|---|---|
| 1 | 把十轮对话草稿重写为正式预印本 | 英文 9 页 / 中文 8 页，修正 COA 引用、CoRL/CCF 错误、zero-shot 语义，补 8 条 Limitations |
| 2 | 生成中英 PDF | Edge print-to-pdf，字体嵌入、无 JS、公式与作者行已核对 |
| 3 | arXiv LaTeX 源码 | `paper/source/main.tex`，CJK 0、花括号平衡、12 条内嵌参考文献 |
| 4 | 四渠道表单 + Zenodo 元数据 | `metadata/` 全部就绪，现已回填 Zenodo DOI |
| 5 | Zenodo 一键脚本 | `tools/publish_zenodo.py`，`--dry-run` / 草稿 / `--publish` 三级安全档 |
| 6 | GitHub 公开存档 | `clawgeek/lrls-paper`，tag `v1.0` + Release |
| 7 | **Zenodo 正式发布** | **DOI 10.5281/zenodo.23984055**，DataCite 已注册 |
| 8 | 四渠道互链回填 | chinaxiv / techrxiv / arxiv 三个表单全部标注该 DOI |

公开地址：
- Zenodo：https://doi.org/10.5281/zenodo.23984055
- 仓库：https://github.com/clawgeek/lrls-paper
- Release：https://github.com/clawgeek/lrls-paper/releases/tag/v1.0

---

## 用户下一步（最小动作）

1. **立即撤销 Zenodo token**：https://zenodo.org/account/settings/applications/ → 删除本次创建的 `lrls-preprint-upload` / `lrls-deposit-temp`。凭据曾出现在对话中，务必撤销。
2. **ChinaXiv**：注册 + 实名 → 按 `metadata/chinaxiv.md` 粘贴 → 传 `paper/lrls-v1.1-zh.pdf`。
3. **TechRxiv**：换网络/设备试 https://www.techrxiv.org/ ；若仍被拦，用 Zenodo DOI 占位即可。
4. **arXiv**：注册 + 找 `cs.LG` 背书人 → 上传 `paper/source/main.tex`（或单独传英文 PDF，二选一勿混）。
5. 拿到任一新编号后告诉我，我发 Zenodo **新版本**（概念 DOI 不变）把四个编号互相指向，形成完整引用闭环。

## 未做且不冒充已做

- 未在 ChinaXiv / TechRxiv / arXiv 创建任何 deposition，未取得这三个平台的任何编号。
- 未做同行评审、未投会议（AAMAS Blue Sky / RSS / ICRA Arts in Robotics 的时间窗口另见 `LRLS-论文投稿渠道清单.md`）。
- 未代用户点击实名认证或填写背书人信息。
