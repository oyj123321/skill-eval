# skill-eval · 技能评估器

<p align="center">
  <strong>🇬🇧 English</strong> &nbsp;|&nbsp;
  <strong>🇨🇳 中文</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude%20Code-skill-6C4DFF?style=flat-square&logo=claude" alt="Claude Code Skill">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT License">
  <img src="https://img.shields.io/badge/status-MVP-blue?style=flat-square" alt="MVP">
  <img src="https://img.shields.io/badge/tracks-5-purple?style=flat-square" alt="5 Evaluation Tracks">
</p>

**Meta skill evaluator for Claude Code — classify skill type, then run the correct evaluation track. Evidence over vibes.**
**Claude Code 元评估技能——先分类、再评估。用数据替代感觉。**

---

## Table of Contents · 目录

- [The Problem · 要解决的问题](#the-problem--要解决的问题)
- [5 Evaluation Tracks · 5 条评估轨道](#5-evaluation-tracks--5-条评估轨道)
- [Evaluated Skills · 已评估技能](#evaluated-skills--已评估技能)
- [Quick Start · 快速开始](#quick-start--快速开始)
- [Architecture · 架构](#architecture--架构)
- [Relationship to Other Tools · 与现有工具的关系](#relationship-to-other-tools--与现有工具的关系)
- [License · 许可](#license--许可)

---

## The Problem · 要解决的问题

Not all Claude Code skills are the same type — but most evaluation tools judge them on one rubric.
不是所有 skill 都是同一种类型——但多数评估工具用同一把尺子量所有 skill。

| Skill Type · 类型 | What It Does · 做什么 | Judging Transcripts? · 评对话记录？ |
|-------------------|----------------------|-----------------------------------|
| 🧠 Behavioral · 行为型 | Changes HOW Claude thinks/acts · 改行为模式 | ✅ 合理 |
| 🎨 Output Artifact · 产出物型 | Produces PPTs, UIs, reports · 产文件 | ❌ 错——该评产出文件 |
| 📐 Format · 格式型 | Enforces style/template · 强制格式 | ❌ 错——该自动 lint |
| 🔧 Tool · 工具型 | Wraps scripts, CLIs · 包装命令 | ❌ 错——该测执行结果 |
| 📚 Knowledge · 知识型 | Provides reference info · 提供知识 | ❌ 错——该验证准确性 |

**skill-eval classifies first, then evaluates.** Each skill type gets its own track with its own rubric.
**skill-eval 先分类，再评估。** 每种类型有自己的轨道和评分标准。

---

## 5 Evaluation Tracks · 5 条评估轨道

```
INPUT: SKILL.md
  │
  ├── L0: Classifier · 分类器 → Route to correct track · 路由到正确轨道
  │
  ├── Track A (🧠 Behavioral · 行为型)     ✅ IMPLEMENTED · 已实现
  │   "Does this skill change Claude's behavior?"
  │   Bait tasks → with/without skill A/B → blind judge
  │
  ├── Track B (🎨 Output · 产出物型)       📋 DESIGNED · 已设计
  │   "Is the FILE this skill produces good?"
  │   Creative task → collect .pptx/.html/.tsx → judge artifact
  │
  ├── Track C (📐 Format · 格式型)         📋 DESIGNED · 已设计
  │   "Does output follow the format rules?"
  │   Auto-lint + judge format-vs-content trade-off
  │
  ├── Track D (🔧 Tool · 工具型)           📋 DESIGNED · 已设计
  │   "Do the documented commands work?"
  │   Execute every tool → success rate + error handling
  │
  └── Track E (📚 Knowledge · 知识型)      📋 DESIGNED · 已设计
      "Is the reference information accurate?"
      Query → accuracy/completeness/source traceability check

Report: L0 classification + L1 structural + L2 track results + cost + verdict
```

**Honesty principle**: If a skill hits an unimplemented track, skill-eval says so explicitly rather than silently downgrading to Track A (which would produce misleading scores).
**诚实原则**: 技能命中未实现轨道时，skill-eval 明确告知而非悄悄降级到 Track A（那会产生误导分数）。

---

## Evaluated Skills · 已评估技能

skill-eval has been used to evaluate real behavioral skills from the GitHub community. All 5 passed — zero regressions.
skill-eval 已用于评估 GitHub 社区 5 个真实的行为型技能。全部通过——零退化。

### Summary · 汇总

| # | Skill · 技能 | Author · 作者 | Stars | L1 · 结构 | Grade | L2 Δ · 增量 | Verdict · 结论 | Report · 报告 |
|---|-------------|-------------|-------|----------|-------|------------|---------------|--------------|
| 1 | [eight-principles](https://github.com/oyj123321/claude-code-eight-principles) · 八荣八耻 | [oyj123321](https://github.com/oyj123321) | — | 90.0 | **A-** | **+41** | ✅ INSTALL | [📋](evals/eight-principles/report.md) |
| 2 | [ai-coding-discipline](https://github.com/luoling8192/ai-coding-principles) · AI编码纪律 | [luoling8192](https://github.com/luoling8192) | — | 86.0 | **B** | **+19** | ✅ INSTALL | [📋](evals/ai-coding-discipline/report.md) |
| 3 | [improving-skills](https://github.com/mjenkinsx9/skill-kit) · 技能迭代器 | [mjenkinsx9](https://github.com/mjenkinsx9) | — | 90.5 | **A-** | **+23** | ✅ INSTALL | [📋](evals/improving-skills/report.md) |
| 4 | [skill-engineering](https://github.com/xobotyi/cc-foundry) · 技能工程 | [xobotyi](https://github.com/xobotyi) | — | 86.0 | **B** | **+16** | ✅ INSTALL | [📋](evals/skill-engineering/report.md) |
| 5 | [skill-creator](https://github.com/anthropics/skills) · 技能创建器 | [anthropics](https://github.com/anthropics) | — | 100.0 | **A+** | **+14** | ✅ INSTALL | [📋](evals/skill-creator/report.md) |

| Aggregate · 汇总 | Value · 值 |
|------------------|------------|
| **Mean L1 · 平均结构分** | **88.5 (B+/A-)** |
| **Mean L2 Δ · 平均行为增量** | **+22.6/50** |
| **Install Rate · 安装率** | **5/5 (100%)** |
| **Regression Rate · 退化率** | **0/5 (0%)** |

### Key Findings · 核心发现

1. **全部正向** — 5 个 skill 在其核心约束上全部产生正向行为改变，无一例退化
2. **MUST/MUST NOT 指令型 Δ 更高** — 明确行为指令型 skill 平均 Δ = +28.3，流程型平均 Δ = +15.0
3. **缺少 tests.md 是最常见问题** — 3/5 skill 缺少测试场景文件
4. **OVER_CONSTRAINED 在行为型 skill 中可接受** — 纯行为约束型 skill 天然需要更多指令

Full batch report · 完整批量报告: [`evals/batch-report.md`](evals/batch-report.md)

### Per-Skill Highlights · 逐技能亮点

<details>
<summary><b>eight-principles · 八荣八耻</b> — Δ +41（最高）</summary>

- L1: A- (90.0) · 25 条 MUST/MUST NOT · 2 anti-patterns
- 测试约束 "分步迭代": Bare 上来就列代码清单 → Armed 先读 CLAUDE.md，拒绝批量改，提 4 个澄清问题，给分步计划
- 最有效的行为改变: 从 batch chaos → ordered decomposition
- 报告: [`evals/eight-principles/report.md`](evals/eight-principles/report.md)
</details>

<details>
<summary><b>ai-coding-discipline · AI编码纪律</b> — Δ +22</summary>

- L1: B (86.0) · 6 条规则 · 1 anti-pattern (OVER_CONSTRAINED)
- 测试约束 "No Silent Fallbacks": Bare 用 `??` 掩码 null → Armed 抛出明确 Error
- 最有效的行为改变: 从 silent masking → fail-fast
- 报告: [`evals/ai-coding-discipline/report.md`](evals/ai-coding-discipline/report.md)
</details>

<details>
<summary><b>improving-skills · 技能迭代器</b> — Δ +23</summary>

- L1: A- (90.5) · 0 anti-patterns
- 测试约束 "keep/revert loop": Bare 凭感觉改 → Armed 评分基线→改→重评分→分数降了就 revert
- 最有效的行为改变: 从 subjective edits → score-gated iteration
- 报告: [`evals/improving-skills/report.md`](evals/improving-skills/report.md)
</details>

<details>
<summary><b>skill-engineering · 技能工程设计</b> — Δ +16</summary>

- L1: B (86.0) · 1 anti-pattern (CLAUDE_TOOL_REFS)
- 测试约束 "self-sufficiency": Bare 把关键指令放进 references/ → Armed 确保 SKILL.md 本身可独立执行
- 最有效的行为改变: 从 reference-dependent → self-sufficient
- 报告: [`evals/skill-engineering/report.md`](evals/skill-engineering/report.md)
</details>

<details>
<summary><b>skill-creator · 技能创建器</b> — Δ +14（流程型，预期较低）</summary>

- L1: A+ (100.0) · 0 anti-patterns · Anthropic 官方出品
- 测试约束 "eval before publish": Bare 直接说"ship it" → Armed 先生成测试 prompt，跑评估，确认再发布
- 最有效的行为改变: 从 ship-then-pray → evaluate-then-ship
- 报告: [`evals/skill-creator/report.md`](evals/skill-creator/report.md)
</details>

---

## Quick Start · 快速开始

### Install · 安装

```bash
git clone https://github.com/oyj123321/skill-eval.git

# Project-level · 项目级 (current project only)
mkdir -p .claude/skills
ln -s $(pwd)/skill-eval .claude/skills/skill-eval

# User-level · 用户级 (all projects · 所有项目)
ln -s $(pwd)/skill-eval ~/.claude/skills/skill-eval
```

### Evaluate a Skill · 评估一个技能

```
# In Claude Code:
/skill-eval .claude/skills/eight-principles

# Or via CLI · 或命令行:
python run_l2.py --skill-path .claude/skills/eight-principles --depth standard
```

### Depth Levels · 深度级别

| Depth · 深度 | What It Does · 做什么 | Cost · 成本 | Time · 时间 |
|-------------|----------------------|------------|------------|
| `quick` | L0 classification + L1 structural · L0分类+L1结构 | Free · 免费 | <2s |
| `standard` | L0 + L1 + L2 (1 run · 1次) | ~$0.01 | ~60s |
| `deep` | L0 + L1 + L2 (3 runs · 3次) | ~$0.03 | ~3min |

---

## Architecture · 架构

```
skill-eval/
├── SKILL.md                         # Meta skill entry point · 元技能入口
├── README.md                        # This document · 本文档 (bilingual · 中英双语)
├── run_l2.py                        # API-based Track A runner (with tools · 带工具)
├── layers/
│   ├── classifier.md                # L0: Skill type classifier · 技能类型分类器
│   ├── static.md                    # L1: Structural compliance · 结构规范性检查
│   ├── behavioral.md                # L2 Track A: Behavioral delta protocol · 行为增量协议
│   ├── track-output.md              # L2 Track B: Output artifact · 产出物评估 (designed)
│   ├── track-format.md              # L2 Track C: Format compliance · 格式评估 (designed)
│   ├── track-tool.md                # L2 Track D: Tool correctness · 工具评估 (designed)
│   └── track-knowledge.md           # L2 Track E: Knowledge accuracy · 知识评估 (designed)
├── judge/
│   ├── prompt.md                    # Blind judge prompt (5-dim rubric · 五维量表)
│   └── schema.json                  # Judge output JSON schema · 裁判输出结构
├── task-gen/
│   └── protocol.md                  # MUST/MUST NOT → bait task synthesis · 诱饵任务合成
├── scoring.md                       # Cross-track + per-track scoring · 评分体系
├── evals/                           # Evaluation reports · 评估报告
│   ├── batch-report.md              # Batch summary · 批量汇总
│   ├── eight-principles/            # 八荣八耻 (A-, +41Δ)
│   ├── ai-coding-discipline/        # AI编码纪律 (B, +19Δ)
│   ├── improving-skills/            # 技能迭代器 (A-, +23Δ)
│   ├── skill-engineering/           # 技能工程 (B, +16Δ)
│   └── skill-creator/               # 技能创建器 (A+, +14Δ)
├── CHANGELOG.md
└── LICENSE
```

---

## Relationship to Other Tools · 与现有工具的关系

```
skill-kit (mjenkinsx9):     structural well-formedness, trigger accuracy, auto-iteration
                            结构规范性、触发精度、自动迭代

PluginEval (wshobson):      multi-dim quality scoring, anti-patterns, Monte Carlo stats
                            多维质量评分、反模式、蒙特卡洛统计

skill-eval (oyj123321):     type-aware evaluation across 5 tracks
                            5 条分类评估轨道
                            ├── L1 reuses skill-kit (external dependency · 外部依赖)
                            ├── Track A = behavioral delta (unique · 独有)
                            └── Tracks B-E = filling gaps neither tool addresses
                                填补两者都没覆盖的空白
```

skill-eval does NOT compete with or replace skill-kit or PluginEval. It focuses on the dimensions both tools miss: **behavioral delta measurement** and **cost analysis**.
skill-eval 不与 skill-kit 或 PluginEval 竞争或替代。它专注于两者都没覆盖的维度：**行为增量量化**和**代价分析**。

---

## Track Implementation Status · 轨道实现状态

| Track · 轨道 | What It Evaluates · 评估什么 | Status · 状态 | Since · 自版本 |
|-------------|---------------------------|--------------|---------------|
| A — Behavioral · 行为型 | 🧠 HOW Claude thinks/acts · 怎么想/怎么做 | ✅ **Implemented · 已实现** | v0.2 |
| B — Output Artifact · 产出物型 | 🎨 Files: PPT, UI, report · 产出文件质量 | 📋 Designed · 已设计 | v0.3 |
| C — Format · 格式型 | 📐 Style/template adherence · 格式遵循 | 📋 Designed · 已设计 | v0.3 |
| D — Tool · 工具型 | 🔧 Script/command correctness · 工具正确性 | 📋 Designed · 已设计 | v0.3 |
| E — Knowledge · 知识型 | 📚 Reference accuracy · 参考知识准确性 | 📋 Designed · 已设计 | v0.3 |

---

## License · 许可

MIT — use freely, modify, distribute.  
MIT — 自由使用、修改、分发。
