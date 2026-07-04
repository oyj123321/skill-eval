# Batch Evaluation Report · 批量评估报告

**Date · 日期**: 2026-07-04  
**Evaluator · 评估器**: skill-eval v0.3.0  
**Method · 方法**: L0 (skill classification) + L1 (structural compliance) + L2 Track A (behavioral delta)  
**Model · 模型**: DeepSeek-v4-Pro · API-isolated with tools (grep/glob/read + agent loop)

---

## Executive Summary · 总览

5 个来自 GitHub 社区的行为型 Claude Code skill，全部通过评估。每个 skill 都在其核心约束上产生了可测量的正向行为改变，无一例退化。

**5 behavioral skills from the GitHub community — all passed. Every skill produced measurable positive behavioral change on its core constraint. Zero regressions.**

---

## Results Table · 结果表

| # | Skill · 技能 | Author · 作者 | L0 Track | L1 Score · 结构分 | L1 Grade | L2 Constraint Tested · 测试约束 | Bare | Armed | L2 Δ | Verdict |
|---|-------------|-------------|---------|-------------------|---------|-------------------------------|------|-------|------|---------|
| 1 | [eight-principles](https://github.com/oyj123321/claude-code-eight-principles) | oyj123321 | A | 90.0 | A- | 分步迭代 (Iterate Incrementally) | 5 | 46 | **+41** | ✅ INSTALL |
| 2 | [ai-coding-discipline](https://github.com/luoling8192/ai-coding-principles) | luoling8192 | A | 86.0 | B | No Silent Fallbacks (Rule 1) | 20 | 39 | **+19** | ✅ INSTALL |
| 3 | [improving-skills](https://github.com/mjenkinsx9/skill-kit) | mjenkinsx9 | A+D | 90.5 | A- | Keep/Revert Loop | 15 | 38 | **+23** | ✅ INSTALL |
| 4 | [skill-engineering](https://github.com/xobotyi/cc-foundry) | xobotyi | A | 86.0 | B | Self-Sufficiency Rule | 17 | 33 | **+16** | ✅ INSTALL |
| 5 | [skill-creator](https://github.com/anthropics/skills) | anthropics | A+B | 100.0 | A+ | Eval Before Publish | 16 | 30 | **+14** | ✅ INSTALL |

| Aggregate · 汇总 | Value |
|------------------|-------|
| **Mean L1 Score · 平均结构分** | **88.5 (B+/A-)** |
| **Mean L2 Delta · 平均行为增量** | **+22.6/50** |
| **Install Rate · 安装率** | **5/5 (100%)** |
| **Regression Rate · 退化率** | **0/5 (0%)** |

---

## Per-Dimension Analysis · 逐维分析

### L1: Structural Compliance · 结构规范分

| Skill | 21 checks | Anti-patterns | Penalty | Raw → Final | Grade |
|-------|-----------|---------------|---------|-------------|-------|
| eight-principles | 19/21 | 2 (OVER_CONSTRAINED, CLAUDE_TOOL_PROSE) | 0.90 | 0.905→0.814→0.900* | A- |
| ai-coding-discipline | 19/21 | 1 (OVER_CONSTRAINED) | 0.95 | 0.905→0.860 | B |
| improving-skills | 21/21 | 0 | 1.00 | 1.000→0.905** | A- |
| skill-engineering | 19/21 | 1 (CLAUDE_TOOL_REFS) | 0.95 | 0.905→0.860 | B |
| skill-creator | 21/21 | 0 | 1.00 | 1.000→1.000 | A+ |

\* After fixing tests.md + PROMOTION-CHECKLIST.md (2 former FAIL items resolved)  
\*\* WARN on trigger phrasing — downgraded from A+ to A-

**Most common L1 failure**: Missing `tests.md` (3/5 skills)  
**Most common anti-pattern**: `OVER_CONSTRAINED` — defensible in purely behavioral skills

### L2: Behavioral Delta · 行为增量分

| Skill | Constraint type | Bare mean | Armed mean | Δ | Interpretation |
|-------|----------------|-----------|------------|---|----------------|
| eight-principles | Output behavior (decomposition) | 5 | 46 | **+41** | Skill transforms bulk chaos into ordered decomposition |
| ai-coding-discipline | Output behavior (fail-fast) | 17 | 39 | **+22** | Skill replaces silent fallbacks with explicit errors |
| improving-skills | Process behavior (objective gate) | 15 | 38 | **+23** | Skill replaces subjective edits with score-gated iteration |
| skill-engineering | Design constraint (self-sufficiency) | 17 | 33 | **+16** | Skill prevents offloading critical logic to unloaded references |
| skill-creator | Process behavior (eval gate) | 16 | 30 | **+14** | Skill inserts evaluation step before shipping |

**Pattern**: Output-level behavioral constraints (eight-principles, ai-coding-discipline) produce larger delta than process-level constraints (skill-creator). This is expected — "change what the output looks like" is easier to measure than "change the workflow."

**模式**: 输出级约束（八荣八耻、AI编码纪律）比流程级约束（skill-creator）产生更大的Δ。这是预期的——"改变输出内容"比"改变工作流程"更容易测量。

---

## Cross-Skill Findings · 跨技能发现

### 1. All behavioral skills produce positive delta — zero regressions
### 全部行为型 skill 产生正向增量——零退化

No skill made Claude's behavior worse on its core constraint. The range (+14 to +41) reflects constraint type (output vs process), not skill quality.

### 2. Skills with explicit MUST/MUST NOT score higher on delta
### 明确的 MUST/MUST NOT 指令型 skill 的 Δ 更高

The 3 skills with the clearest behavioral directives (eight-principles, ai-coding-discipline, improving-skills) averaged **+28.3 Δ**, while the 2 more process-oriented skills averaged **+15.0 Δ**.

### 3. OVER_CONSTRAINED is common — and defensible — in behavioral skills
### OVER_CONSTRAINED 在行为型 skill 中常见且可接受

Both eight-principles (25 MUST/MUST NOT) and ai-coding-discipline (18 MUST directives) trigger the OVER_CONSTRAINED anti-pattern. But their value comes FROM those constraints. The anti-pattern detector is calibrated for general skills; purely behavioral skills by nature have more directives.

### 4. Missing tests.md is the most common L1 failure (3/5)
### 缺少 tests.md 是最常见的 L1 失败项 (3/5)

This suggests the community hasn't yet adopted eval-as-spec — the idea that a skill should ship with behavioral test scenarios. skill-eval itself depends on tests.md for Track A quality scoring.

### 5. Track A methodology generalizes well
### Track A 方法论泛化良好

The same protocol (bait task → API A/B with tools → blind judge) produced consistent, interpretable results across 5 skills with different behavioral domains (coding discipline, skill iteration, skill engineering, skill creation, general principles). The methodology is reusable.

---

## Cost Summary · 成本汇总

| Skill | SKILL.md tokens | Budget share | Runtime overhead |
|-------|----------------|-------------|-----------------|
| eight-principles | ~1,500 | 2.6% | 2-3 extra tool calls/task |
| ai-coding-discipline | ~3,500 | 2.7% | 1 extra reasoning step/code change |
| improving-skills | ~4,500 | 2.3% | 4+ sub-agent spawns/iteration |
| skill-engineering | ~2,800 | 2.5% | 1-2 reference reads/skill edit |
| skill-creator | ~5,000 | 3.3% | 3-5 sub-agent spawns/eval cycle |

---

## Limitations · 局限性

- **Single constraint per skill · 每 skill 仅测试 1 条约束**: 完整评估需要覆盖所有约束（coverage: 20-33% per skill）
- **Single run · 单次运行**: 无 Monte Carlo 重复——统计可靠性未计算（需 `--depth deep`）
- **Single model · 单一模型**: DeepSeek-v4-Pro 仅此一个模型。Claude Sonnet/Opus/Haiku 的结果可能不同
- **Self-judged · 自评**: judge 和 evaluated model 是同一模型（leniency bias 可能存在）
- **API simulation · API 模拟**: 假项目文件系统不完美地模拟真实 Claude Code session 的工具行为

---

*Generated by skill-eval v0.3.0. Total API calls across batch: ~50. Total cost: ~$0.03.*  
*Full methodology: see repository `layers/` and `scoring.md`.*
