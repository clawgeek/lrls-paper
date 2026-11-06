# IEEE CEC 2027 投稿材料（CCF-C）

会议：IEEE Congress on Evolutionary Computation 2027，爱丁堡，2027-07-25~28
CCF 等级：C（ICORE B）
截稿：**Full paper 2027-02-28**；Short paper 2027-03-15（官方明确“不延期”）
通知：2027-04-07；终稿 + 早注册：2027-05-01

**投稿系统：EDAS**（不是 PaperPlaza）
会议投稿页：https://edas.info/N35695
CFP 页（含 Submit Here 链接）：https://ieeecec.org/2027/authors/call-for-papers

> ⚠️ EDAS 会拒绝来自主机/IDC/VPN 出口 IP 的连接，报错形如
> `We do not accept connections from hosting providers, such as VPNs: <IP>`。
> 本机经代理出口 92.113.124.75 访问被拒，**必须关闭 VPN / 用普通宽带**才能登录或提交。

---

## 作者信息（照抄）

| 字段 | 内容 |
|---|---|
| First name | Jason |
| Last name | Sang |
| Full name as printed | Jason Sang (Sang Jiexun) |
| Email | sangjeixun@gmail.com |
| Affiliation | Independent Researcher |
| Country | China |
| Role | 唯一作者 + 通讯作者（presenter） |

---

## Title

LRLS: Role-Separated Exploration and Exploitation with a Scheduling Agent for Constrained Optimisation

## Abstract（EDAS 摘要框，纯文本，约 235 词）

Metaheuristics that alternate between exploration and exploitation usually make that switch with a scalar schedule - a temperature threshold, an entropy coefficient, or a cooling curve. We ask what changes when the switch is made by an agent instead. LRLS separates the two behaviours into heterogeneous roles: a high-entropy explorer population proposes candidate regions, a constraint-aware refiner population promotes them into verified feasible solutions, and a scheduler allocates budget between the two from global state. This paper contributes (i) an executable specification with a fixed state decomposition, six action primitives, a single reward structure and a hard-constraint safety layer; (ii) a dependency-free deterministic reference implementation; and (iii) a budget-matched evaluation against four baselines over five seeds. The result is deliberately not a speed claim: random search and a single-pool ablation reach 99% of the optimum 1.3-2.9x faster than LRLS. What role separation buys is constraint safety on the path - LRLS reaches the 99% threshold with zero hazard-zone evaluations in every profile and every seed, while every baseline pays 16-456 violations to reach the same quality, and a temperature-gated switch in the style of the Crayfish Optimization Algorithm is worse on both axes. We release the specification, the simulator and all experiment code.

## Keywords

constrained optimisation; exploration-exploitation; metaheuristics; multi-agent; constraint handling; reproducibility

## Topic（EDAS 下拉，按 CFP 主题表）

- Primary: **Constraint handling**
- Secondary: **Metaheuristics and hyper-heuristics**
- 备选（若需第三个）：Evolutionary reinforcement learning

---

## 稿件状态

- `paper/cec/cec-v1.pdf`：**4 页**，US Letter，双栏，IEEE 会议版式（上 .75in / 下 1in / 左右 .625in）
- 结构：Abstract · 1 Introduction · 2 Related Work · 3 Specification（3.1 问题定义 + Algorithm 1）· 4 Reference Implementation · 5 Experiments（5.1 Setup / 5.2 Results / 5.3 边界）· 6 Discussion · 7 Limitations · 8 Conclusion · References
- 图：Fig. 1（预算匹配对比，双面板）· Fig. 2（精炼者容量轨迹）
- 表：Table I（参数默认值）· II（四档 profile）· III（预算匹配结果）· IV（P4 逐 seed）
- 参考文献：8 条（COA / RL survey / SA / SAC / PPO / MAPPO / 本 preprint / 模拟器）
- 定位：**short paper（4 页）**。若要投 full paper（≤8 页，2-28 截稿），需再补约一倍内容（最值得补的是 hazard-gate 敏感性实验 ρ=0.25/0.35/0.45）

## 与期刊/预印本版的差异（避免重复发表争议）

| | 期刊版（13 页） | CEC 版（4 页） |
|---|---|---|
| 定位 | 规范 + 参考实现 + 完整实验 | 约束处理机制 + 预算匹配对比 |
| 内容 | 六节 + RoboZero 多机器人扩展 | 精简规范、算法框、核心实验、讨论 |
| 关系 | 技术报告（Zenodo DOI + Preprints.org 242857） | 会议短文，引用前者 [7] |

## 待办

- [x] 生成 4 页 IEEE 版式 PDF（US Letter）
- [x] 数学符号渲染（LaTeX → Unicode/HTML）
- [x] 图表按单栏宽度重做
- [x] 加参考文献与文内引用
- [ ] EDAS 账号（免费，需要能访问 EDAS 的网络）
- [ ] 上传 `cec-v1.pdf`，填标题/摘要/关键词/topic/作者
- [ ] 提交后下载 EDAS 生成的确认 PDF 核对
- [ ] 录用后填 IEEE eCopyright 与终稿

## 构建命令

```
python tools/make_cec_figs.py     # 单栏尺寸图（Fig.1 / Fig.2）
python tools/build_cec.py         # cec-v1.md -> cec-v1.html -> cec-v1.pdf
```
