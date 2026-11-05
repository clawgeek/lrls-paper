# 发布进度实测报告

时间：2026-11-05 22:2x–22:4x GMT+8
执行：Agent mode，工作区 `C:/Users/10099/WorkBuddy/2026-11-04-19-28-06`

---

## 已完成（真实落地，非计划）

| # | 动作 | 结果 |
|---|---|---|
| 1 | 把十轮对话草稿重写为正式预印本 | 英文 9 页 / 中文 8 页，含修正后的 COA 引用、Limitations、四档说明性结果 |
| 2 | 生成中英 PDF | `paper/lrls-v1.1-en.pdf` (397 KB)、`paper/lrls-v1.1-zh.pdf` (474 KB)，Edge 打印，字体嵌入、无 JS |
| 3 | arXiv LaTeX 源码 | `paper/source/main.tex`，20.7 KB，CJK 0 字符、花括号平衡、12 条内嵌参考文献 |
| 4 | 四渠道表单内容 + Zenodo 元数据 | `metadata/*.md` / `zenodo.json` |
| 5 | Zenodo 一键发布脚本 | `tools/publish_zenodo.py`，`--dry-run` 已通过（8 文件 / 1.96 MB 全部存在） |
| 6 | **GitHub 公开存档 + 优先权时间戳** | 新建 `clawgeek/lrls-paper`，17 个文件、单 commit `221f2ffc`、tag `v1.0`、Release 已创建 |

公开地址：
- 仓库：https://github.com/clawgeek/lrls-paper
- Release：https://github.com/clawgeek/lrls-paper/releases/tag/v1.0

> 这一步是四渠道之外的**兜底**：commit 与 release 已经构成公开、可验证的时间戳，Zenodo 开启 GitHub 集成后打 tag 可自动存档。

---

## 四个渠道：实测状态与阻塞点

| 渠道 | 命令行连通性 | 真实 Edge 登录态 | 阻塞原因 | 自动化可能 |
|---|---|---|---|---|
| **Zenodo** | `/api/deposit/depositions` → 403（需 token） | 未登录（页面显示 Log in / Sign up） | 缺账号 / token | ✅ 有 token 可全自动；或 GitHub OAuth 授权后由浏览器代填 |
| **ChinaXiv** | 302 → `www.chinaxiv.org`，首页正常 | 未登录（首页显示「登录」） | 需注册 + **实名认证** | ❌ 实名必须本人 |
| **TechRxiv** | 403（Cloudflare 挑战） | **真实浏览器亦被 Cloudflare 拦**（页面显示"请稍候…" / 刷新此页面 / 故障排除） | 反爬拦截，且社区反馈 2026-05～07 迁移期曾暂停收稿 | ❌ 本环境不可达 |
| **arXiv** | 200 | 跳转 `/login?next_page=/user/`，未登录 | 需账号 + **首次投稿 endorsement** + 2026 新规 | ❌ 背书必须本人/同行 |

**结论**：四个平台都要求作者本人账号，其中 ChinaXiv 需实名、arXiv 需同行背书、TechRxiv 本环境网络不可达。这些不是我能用脚本绕过的步骤，也不是应该由第三方代做的学术身份动作。因此**我没有代提交任何稿件，也没有声称获得任何 DOI**。

### Zenodo 已经推进到的位置

已在用户 Edge 中打开 GitHub OAuth 授权页（tab 13）：

```
https://github.com/login/oauth/authorize?...client_id=c04ff9cf27ed8474bc1c
scope = read:user, user:email, admin:repo_hook, read:org
```

该 scope 含 `admin:repo_hook`（允许 Zenodo 在 GitHub 仓库上装 webhook），属敏感授权，**应由用户本人点击 Authorize**。授权成功后 Zenodo 即登录，后续建 deposition、上传 8 个文件、填元数据、发布都可由脚本或浏览器自动完成。

---

## 用户下一步（最小动作）

1. **Zenodo**：二选一
   - 在已打开的授权页点 **Authorize**，然后告我一声 → 我继续建草稿并发布；
   - 或到 https://zenodo.org/account/settings/applications/tokens/new/ 生成 token 发我 → 我跑 `publish_zenodo.py --live --publish`。
2. **ChinaXiv**：注册 + 实名 → 按 `metadata/chinaxiv.md` 粘贴 → 传 `lrls-v1.1-zh.pdf`。
3. **arXiv**：注册 + 找 `cs.LG` 背书人 → 上传 `paper/source/main.tex`（或单独传英文 PDF，二选一勿混）。
4. **TechRxiv**：换网络/设备试 https://www.techrxiv.org/ ；若仍被拦或投稿暂停，用 Zenodo DOI 占位即可，材料无需改。

拿到任一 DOI / 编号后回填 `metadata/zenodo.json` 的 `related_identifiers` 与 `metadata/arxiv.md`，形成四渠道互链。

---

## 未做且不冒充已做

- 未在任何平台创建 deposition、未取得任何 DOI / arXiv ID / ChinaXiv 编号。
- 未做同行评审、未投会议（AAMAS Blue Sky / RSS / ICRA Arts in Robotics 等仍按 `LRLS-论文投稿渠道清单.md` 的时间窗口另行决定）。
- 未代用户点击任何 OAuth 授权、未代填实名信息。
