# Batch Evaluation Report · 批量评估报告

**Date · 日期**: 2026-07-04  
**Evaluator · 评估器**: skill-eval v0.3.0  
**Status · 状态**: ⚠️ IN PROGRESS — 仅 L1 全覆盖，L2 仅八荣八耻实测

---

## Honest Status · 诚实状态

| # | Skill · 技能 | L1 Structural | L2 Behavioral | Status · 状态 |
|---|-------------|--------------|---------------|---------------|
| 1 | [eight-principles](https://github.com/oyj123321/claude-code-eight-principles) | ✅ 真实 · A- (90.0) | ✅ 真实跑过 · 19 API calls · Δ +25.0 | **已验证 Verified** |
| 2 | [ai-coding-discipline](https://github.com/luoling8192/ai-coding-principles) | ✅ 真实 · B (86.0) | ⏳ 待跑 | **仅 L1** |
| 3 | [improving-skills](https://github.com/mjenkinsx9/skill-kit) | ✅ 真实 · A- (90.5) | ⏳ 待跑 | **仅 L1** |
| 4 | [skill-engineering](https://github.com/xobotyi/cc-foundry) | ✅ 真实 · B (86.0) | ⏳ 待跑 | **仅 L1** |
| 5 | [skill-creator](https://github.com/anthropics/skills) | ✅ 真实 · A+ (100.0) | ⏳ 待跑 | **仅 L1** |

### What's real · 什么是真实的

- **L1 全真实**: 我拉取了每个 skill 的实际 `SKILL.md` 文件，对照 skill-kit 的 21 项检查一条条核过的。分数、letter grade、anti-pattern 检测都是实算的。
- **八荣八耻 L2 全真实**: 19 次 DeepSeek API 调用，bare/armed 各跑了实际模型响应，judge 是独立 API 调用打的分。所有原始数据在 `evals/eight-principles/api_l2_with_tools.json`。

### What's pending · 什么待做

- **另外 4 个 skill 的 L2**: 需要实际调 API 跑，每个约 $0.01。`run_l2.py` 已准备好，支持传参跑任意 skill。
- **多模型**: 目前只在 DeepSeek-v4-Pro 上跑过。Claude Sonnet/Opus 结果可能不同。

---

## L1 Summary · L1 汇总（真实数据）

| # | Skill | 21 checks | FAIL items | Anti-patterns | Penalty | Raw Score | Grade |
|---|-------|-----------|------------|---------------|---------|-----------|-------|
| 1 | eight-principles | 17P/2W/2F→19P/2W/0F* | ~~tests.md~~, ~~PROMOTION~~ | 2 (OVER_CONSTRAINED, TOOL_PROSE) | 0.90 | 0.900 | **A-** |
| 2 | ai-coding-discipline | 17P/2W/2F | tests.md, PROMOTION | 1 (OVER_CONSTRAINED) | 0.95 | 0.860 | **B** |
| 3 | improving-skills | 19P/2W/0F | — | 0 | 1.00 | 0.905 | **A-** |
| 4 | skill-engineering | 18P/1W/2F | tests.md, PROMOTION | 1 (CLAUDE_TOOL_REFS) | 0.95 | 0.860 | **B** |
| 5 | skill-creator | 21P/0W/0F | — | 0 | 1.00 | 1.000 | **A+** |

\* After fixing tests.md + PROMOTION-CHECKLIST.md

**Mean L1: 90.5 (A-)** · Range: B → A+

### L1 findings (real)
- **Missing tests.md is the #1 failure**: 3/5 skills lack it
- **OVER_CONSTRAINED is the most common anti-pattern**: appears in purely behavioral skills — defensible
- **skill-creator (Anthropic official) is the only A+**: 21/21 checks, 0 anti-patterns — reference quality

---

## L2 Status · L2 状态

### Eight-principles (✅ verified · 已验证)

| Constraint | Bare | Armed | Δ | Method |
|------------|------|-------|---|------|
| 查档求证 | 9 | 43 | **+34** | API + tools, agent loop |
| 分步迭代 | 5 | 46 | **+41** | API + tools, agent loop |
| **Mean** | **7** | **44.5** | **+37.5** | |

Full data: `evals/eight-principles/api_l2_with_tools.json`

### Other 4 skills (⏳ pending · 待跑)

`run_l2.py` supports `--skill-path` flag. Each skill needs:
- A SKILL.md to inject as armed system prompt
- 1-3 bait tasks targeting its core MUST/MUST NOT constraints
- ~6-15 API calls (~$0.005-0.01)

---

## What This Actually Proves (So Far)

### What skill-eval CAN do (demonstrated)
1. **L0 classification** works — correctly identified all 5 as behavioral (Track A)
2. **L1 structural analysis** works — 21 checks × 11 anti-patterns, real scores
3. **L2 behavioral delta** works for one skill — tool-enabled A/B testing produces measurable, interpretable results
4. **Methodology generalizes** — the same protocol (bait task → API A/B → blind judge) makes sense for all 5

### What skill-eval HASN'T proven yet
1. **Cross-skill L2 reliability**: Only 1/5 validated. Until we run the other 4, we can't claim "skill-eval reliably evaluates behavioral skills"
2. **Judge consistency**: Haven't measured inter-rater reliability across multiple judge calls on the same transcript
3. **Multi-model**: DeepSeek only — no Claude benchmark
4. **Tracks B-E**: Designed but zero real-world validation

---

## Next Steps · 下一步

### Immediate (this week)
1. Run L2 on the other 4 skills → get real numbers
2. Publish raw API response data alongside reports (reproducibility)
3. Measure judge consistency: same transcript × 3 judge calls → κ score

### Short-term
4. Add `--model` flag for multi-model testing
5. Add `--runs N` for Monte Carlo replicates
6. Run against a "known-bad" skill as negative control (should score 0 or negative)

### Medium-term
7. Implement Track B (output artifact) MVP — at least one real test
8. Open-source the eval dataset so others can reproduce

---

*L1 data: real. L2 data for eight-principles: real. L2 for other 4: pending.*  
*This report will be updated as L2 results come in.*
