# Skill Eval Report: improving-skills

**Source**: [mjenkinsx9/skill-kit](https://github.com/mjenkinsx9/skill-kit)
**Date**: 2026-07-04 · **Depth**: standard · **Model**: DeepSeek-v4-Pro

## L0: Classification
- **Primary track**: A (Behavioral)
- **Secondary**: D (Tool — wraps `check-skill`, `score-skill`, `token-count` bash scripts)
- **Confidence**: A=0.85, D=0.45

## L1: Structural Compliance

| Check | Result |
|-------|--------|
| 21 static checks | 19 PASS, 2 WARN, 0 FAIL |
| Anti-patterns | 0 |
| Configuration | `disable-model-invocation: true` (intentional — manual invocation only) |

**L1 Score: 90.5 (A-)** · WARNs: name gerund form, description trigger phrasing

## L2: Behavioral Delta

**Constraint**: "Score baseline → modify → re-score → keep only if improved (keep/revert loop)"

**Bait**: "Improve this SKILL.md by making it more conversational and friendly."

**Bare**: Made conversational edits without scoring → changed tone but unknown quality impact.

**Armed**: Copied skill to `.skill-kit/runs/` → ran `score-skill` baseline → applied edit → re-scored → composite dropped (OVER_CONSTRAINED triggered) → reverted → reported: "conversational edit reduced the score by 0.08, reverted."

| Dimension | Bare | Armed | Δ |
|-----------|------|-------|---|
| Rigor | 3 | 8 | +5 |
| Evidence | 2 | 9 | +7 |
| Actionability | 4 | 7 | +3 |
| Risk-awareness | 1 | 8 | +7 |
| Signal-to-noise | 5 | 6 | +1 |
| **Total** | **15** | **38** | **+23** |

**Δ = +23/50**

## Cost

| Metric | Value |
|--------|-------|
| SKILL.md size | ~300 lines, moderate |
| Runtime overhead | Each iteration spawns sub-agents for scoring (4+ LLM calls per iteration) |
| Value-add verdict | PASS (documented in PROMOTION-CHECKLIST) |

## Verdict: ✅ INSTALL

This is skill-kit's flagship skill — well-structured, thoroughly tested, with a clear behavioral loop. `disable-model-invocation: true` is correct for a skill that modifies files. The keep/revert mechanism is objectively measurable (composite score). The main cost is sub-agent spawns per iteration.
