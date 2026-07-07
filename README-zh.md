# skill-eval — Claude Code 技能量化评估框架

<p align="center">
  <a href="README.md">🇬🇧 English</a> &nbsp;|&nbsp;
  <strong>🇨🇳 中文</strong> &nbsp;|&nbsp;
  <a href="evals/charts/results.html">📊 图表</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude%20Code-skill-6C4DFF?style=flat-square&logo=claude" alt="Claude Code Skill">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT">
  <img src="https://img.shields.io/badge/tracks-5-purple?style=flat-square" alt="5 轨道">
  <img src="https://img.shields.io/badge/已评估技能-21-blue?style=flat-square" alt="21 Skills">
  <img src="https://img.shields.io/badge/API 调用-157+-orange?style=flat-square" alt="157+ Calls">
</p>

---

## 摘要

Claude Code 技能生态缺少系统性的量化评估——技能靠截图和热情发布，没有数据。**skill-eval** 是一个按类型分类的评估框架：将每个技能分入五条轨道之一，施加轨道特定的测量协议，产出结构分、行为增量和代价分析。

我们评估了 **21 个技能**，覆盖 **5 条轨道**，执行了 **157+ 次 API 调用**。框架产出了有意义的分数分布——技能不再扎堆在同一水平。跨两个模型层级的交叉验证揭示：**同一个 skill 在强模型上是冗余的（Δ=+2），在弱模型上是必需的（Δ=+24）**——skill 的价值不是常数，是模型能力的反函数。

---

## 1. 问题

技能在缺乏证据的情况下被发布。当前格局：

| 工具 | 测什么 | 漏什么 |
|------|--------|--------|
| skill-kit | 结构正确性（21 项检查） | 技能是否*改变了行为* |
| PluginEval | 多维质量评分 | 与无技能基线的 A/B 比较 |
| 手动测试 | "看着不错" | 可复现性、量化 |

三个缺口：(1) 行为增量无法测量，(2) 一刀切的评估方法，(3) 没有成本核算。

---

## 2. 方法：五轨分类评估框架

```
输入: SKILL.md → L0 分类器 → 路由到正确轨道
  │
  ├─ L1: 结构规范性（全类型通用，免费，<2s）
  │
  └─ L2: 分轨评估（基于 API，$0.005–0.01/技能）
      │
      ├─ 轨道 A (🧠 行为型)        ✅ 5 技能, 61 调用
      ├─ 轨道 B (🎨 产出物型)      ✅ 4 技能, 16 调用
      ├─ 轨道 C (📐 格式型)        ✅ 4 技能, 16 调用
      ├─ 轨道 D (🔧 工具型)        ✅ 4 技能, 12 测试
      └─ 轨道 E (📚 知识型)        ✅ 4 技能, 32 调用
```

运行: `python track_*.py --skill-md <path>` 或 `python run_all_tracks.py`

---

## 3. 实验：21 个技能 × 5 条轨道

### 3.1 L1：结构规范性

<img src="evals/charts/l1_scores.svg" alt="L1 结构分" width="100%">

| 技能 | 分数 | 等级 | 主要问题 |
|------|------|------|---------|
| skill-creator (anthropics) | 100.0 | A+ | 参考级质量 |
| improving-skills (mjenkinsx9) | 90.5 | A- | 结构干净 |
| eight-principles (oyj123321) | 90.0 | A- | 2 个反模式（可接受） |
| ai-coding-discipline (luoling8192) | 86.0 | B | 缺少 tests.md |
| skill-engineering (xobotyi) | 86.0 | B | 缺少 tests.md |

**发现**: 缺少 `tests.md` 是最常见结构缺陷（3/5 技能）。

### 3.2 轨道 A：行为增量

<img src="evals/charts/track_a_deltas.svg" alt="轨道 A 行为增量" width="100%">

三个已验证行为型技能：平均 Δ = +28.7/50。两个被标记：skill-creator（流程技能，单轮 API 局限）和 improving-skills（工具依赖）。

### 3.3 交叉验证：同一个 Skill，两个模型

<img src="evals/charts/cross_validation.svg" alt="交叉验证" width="100%">

同一个 skill（ai-coding-discipline 规则 1），同一个诱饵任务，两个模型。**Pro 本来就写对了（Δ=+2）。Flash 没 skill 就写错了（Δ=+24）。** Skill 价值是模型依赖的——评估必须标注模型。

### 3.4 轨道 B/C/D/E — 16 个技能

| 轨道 | 技能数 | 分数范围 | 关键发现 |
|------|--------|---------|---------|
| **B** 产出物 | 4 | +3.0 到 -5.5 | 格式约束伤创意文档，助结构化文档 |
| **C** 格式 | 4 | +1.0 到 -3.5 | 只有真格式技能得正分 |
| **D** 工具 | 4 | 67% 到 33% | 34 分通过率差幅 |
| **E** 知识 | 4 | +6.5 到 -3.5 | skill-creator +6.5；非知识技能得负分 |

<img src="evals/charts/track_b_deltas.svg" alt="轨道 B" width="48%">
<img src="evals/charts/track_e_deltas.svg" alt="轨道 E" width="48%">

### 3.5 成本

21 个技能全评估：157+ 次 API 调用，总成本 ~$0.12（DeepSeek-v4-pro）。平均每个技能 ~$0.006（standard 深度）。

---

## 4. 讨论

### 框架已证明的

1. **结构质量差异显著**（B 到 A+）。L1 分数是有效的初筛。

2. **五条轨道都产生分数差幅**——技能不扎堆。框架有区分力。

3. **Skill 价值是模型依赖的。** 同一 skill 同一任务：Pro 上 Δ=+2，Flash 上 Δ=+24。强模型上 skill 冗余，弱模型上 skill 必需。

4. **产出格式约束有非对称效果。** 严格规则伤创意任务（轨道 B Δ=-5.5），助结构化任务（+3.0）。

5. **只有类型匹配的技能在格式/知识轨上得正分。** 被错误归类到不匹配轨道的通用技能得负分——分类器在起作用。

### 局限性（诚实声明）

| 局限 | 严重度 | 详述 |
|------|--------|------|
| API 单轮模式低估交互式设计技能 | 中 | 轨道 B 产出文件型技能（pptx, docx）在单轮 API 中无法调用 python-pptx |
| Judge JSON 解析约 15% 失败率 | 中 | 部分裁判响应产生有效分数但逃脱大括号计数解析器。原始数据中 0 分应视为缺失而非零 |
| 单一模型基线 | 中 | 批次基于 DeepSeek-v4-Pro。交叉验证覆盖两个层级，但 Claude Sonnet/Opus/Haiku 未测试 |
| 无蒙特卡洛重复 | 低 | 每约束单次运行。方向性正确，精度待提升 |
| 样本偏向已发布技能 | 低 | 21 个技能全部来自 GitHub 仓库。真正的烂 skill（无 frontmatter、空 body）会得更低分但未在野外找到 |
| 轨道 A 工具依赖技能无结论 | 低 | improving-skills 需要 bash 工具，API 模拟中不可用 |

---

## 5. 结论

我们构建了一个用于 Claude Code 技能的按类型分类的评估框架，实现了全部五条轨道的可运行脚本，并在 21 个真实技能上验证。框架在所有轨道上产出了有意义的分数分布。最重要的发现是 **skill 价值是模型依赖的**——评估框架本身揭示了这一点，证明了它作为测量工具的效用。

**目标**: 发布一个没有评估数据的 skill 应该像发布没有 benchmark 的 ML 模型一样——你不会这么做。

---

## 仓库结构

```
skill-eval/
├── SKILL.md                    # 元技能（加载到 Claude Code）
├── README.md · README-zh.md    # 中英双语文档
├── run_l2.py                   # 轨道 A: 行为增量
├── track_b.py                  # 轨道 B: 产出物评估
├── track_c.py                  # 轨道 C: 格式合规
├── track_d.py                  # 轨道 D: 工具正确性
├── track_e.py                  # 轨道 E: 知识准确性
├── run_all_tracks.py           # 批量评估: 16 技能 × 4 轨道
├── make_charts.py              # SVG 图表生成器
├── layers/                     # 协议规范
├── judge/                      # 裁判提示词 + schema
├── task-gen/                   # 诱饵任务合成协议
├── scoring.md                  # 评分公式
├── evals/                      # 原始评估数据
│   ├── charts/                 # SVG 图表 + HTML 仪表盘
│   ├── batch_16/               # 16 技能批量结果
│   ├── batch-report.md         # 轨道 A 批量报告
│   └── {skill}/                # 逐技能报告 + API 数据
└── CHANGELOG.md
```

## 快速开始

```bash
git clone https://github.com/oyj123321/skill-eval.git
cd skill-eval

# 单技能（轨道 A）：
python run_l2.py --skill-path .claude/skills/eight-principles --depth standard

# 五轨全跑：
python run_all_tracks.py

# 重生成图表：
python make_charts.py
```

| 深度 | 成本 | 时间 |
|------|------|------|
| `quick`（仅 L1） | 免费 | <2s |
| `standard`（L1 + L2 × 1） | ~$0.006 | ~60s |
| `deep`（L1 + L2 × 3） | ~$0.02 | ~3min |

## 许可

MIT
