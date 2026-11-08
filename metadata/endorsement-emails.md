# 背书请求邮件（可直接发送）

**结论先行**：arXiv 对 cs.LG 首投要求背书，这一条无法由程序绕过；X 私信两天零回复，
改走邮件。下面四个邮箱全部来自**官方页面**（院系主页 / 实验室联系页 / 课程页），不是猜的。

## 收件人（按优先级）

| # | 学者 | 邮箱 | 来源 | 5 年 cs | 最新投稿 |
|---|---|---|---|---|---|
| 1 | Jakob Foerster（Oxford，工程科学系教授） | `jakob.foerster@eng.ox.ac.uk` | St Anne's College 人物页 | 117 | 2026-11-04 |
| 2 | Haoran Xu（UT Austin，VGF 一作） | `haoran.xu@utexas.edu` | UT 课程页助教联系方式 | 70 | 2026-11-02 |
| 3 | Amy Zhang（UT Austin，ECE 助理教授） | `amy.zhang@austin.utexas.edu` | UT CS 教师页 + WNCG 档案 | 79 | 2026-10-19 |
| 4 | Ke Li（Exeter，COLA Lab） | `k.li@exeter.ac.uk` | COLA Lab 联系区块 | 94 | 2026-11-03 |

四人都满足 arXiv 的背书资格：5 年内 ≥3 篇 cs 分类，且最近一篇不早于 3 个月前。

## 怎么发（10 分钟）

1. 进 `metadata/emails/`，双击 `1-foerster.eml` → 系统邮件客户端自动打开，收件人/主题/正文都填好 → 点发送。
2. 依次发 2、3、4。**一次发 3 封即可，不要 4 封全发**（这几位互相认识，同一时间收到一模一样的请求是负分）。
3. 发完等 3–5 个工作日。不回就发第 4 封给 Ke Li，**不要重复追问同一个人**。

> 如果双击 `.eml` 打开方式不对（有的机器默认用记事本），右键 →「打开方式」→ 邮件客户端；
> 或者直接把正文复制到 gmail 网页版。

## 邮件正文（英文，四封只在第一段引用对方工作时不同）

```
Dear Professor [NAME],

I am an independent researcher working on constrained exploration-exploitation in
multi-agent optimisation. I am writing to ask whether you would endorse my first
cs.LG submission to arXiv. This is an account requirement for new submitters, not
a request for you to review or vouch for the work.

[一句为什么写给他 - 引用他具体的工作]

The paper moves the exploration-exploitation switch out of a scalar schedule into
two heterogeneous populations plus a scheduler, ships a dependency-free reference
implementation, and reports a five-seed, budget-matched comparison against four
baselines. The headline result is unflattering to my own method: random search and
a single-pool ablation reach 99% of the optimum 1.3-2.9x faster than mine. What
role separation buys is constraint safety on the path - zero hazard-zone
evaluations before the quality threshold in every seed, versus 16-456 for every
baseline.

Preprint: doi.org/10.5281/zenodo.23984055
Code and data: github.com/clawgeek/lrls-paper

If you are willing, my endorsement code is KDOBWQ at
https://arxiv.org/auth/endorse - it takes about thirty seconds. If not, that is
entirely fine; I will not follow up.

Best regards,
Jason Sang (Sang Jiexun)
Independent Researcher, China
sangjiexun@gmail.com
```

三处刻意如此：
- **"not a request for you to review or vouch for the work"** —— 明确这是账号门槛，
  否则对方会以为你在要审稿意见，直接不回。
- **把对自己不利的结果写在正文里** —— 陌生人的请求里，一句诚实的负面结果比十句自我推销更可信。
- **"I will not follow up"** —— 降低对方的心理成本，回复率反而更高。

## 对方背书之后

1. arXiv 会发邮件通知；也可自查
   <https://arxiv.org/auth/need-endorsement.php?category_id=cs.LG>
   —— 不再显示 "Endorsement needed" 即为通过。
2. 回到 <https://arxiv.org/submit/8335852/start> → 勾四类选项 → Add Files 上传
   `paper/arxiv-package.zip`（TeX 源 + 4 张图）→ Process → 填元数据 → Submit。
3. 草稿 8335852 有效期至 **2026-11-19**，过期重建一份即可，内容不变。

## 备用通道

- 认识的国内老师/合作者，只要 5 年内在 cs 系列投过 3 篇以上，一条微信就能解决，成功率最高。
- `tools/find_emails.py` 可按姓名批量抓论文首页邮箱（arXiv 限流严重，一次跑 1–2 人）。
- `tools/gen_emails.py` 重新生成 `.eml`；改 `TARGETS` 里的 `to` / 引用句即可复用。
