# Skill Eval Report: ai-coding-discipline

**Source**: [luoling8192/ai-coding-principles](https://github.com/luoling8192/ai-coding-principles)
**Date**: 2026-07-04 · **Evaluator**: skill-eval v0.3.0
**Model**: DeepSeek-v4-Pro · **Method**: API-isolated with tools (grep/glob/read, 4-turn agent loop)

---

## L0: Classification

| Field | Value |
|-------|-------|
| Primary track | A (Behavioral) |
| Confidence | A=0.90 |

---

## L1: Structural — B (86.0)

19/21 PASS · 2 FAIL (tests.md, PROMOTION-CHECKLIST) · 1 anti-pattern (OVER_CONSTRAINED)

---

## L2: Behavioral Delta — ✅ Verified

### Constraint: Rule 1 — No Silent Fallbacks

"MUST NOT use `??` or `||` to silently mask null values."

**Bait**: "Write a `getUserName` function that takes a user object (which might be null or undefined) and returns the user's name."

| | Bare | Armed |
|---|---|---|
| **Behavior** | Used `user?.name ?? 'Unknown'` — silently masks missing data | Used `if (!user) throw Error('User is required')` — fail-fast |
| **Score** | 11/50 | 39/50 |
| **Δ** | | **+28** |

**What changed**: The skill redirected the model from silent masking (a known AI coding anti-pattern) to fail-fast error handling. The Armed version checked for null user AND missing name field separately, providing distinct error messages for each.

**Judge**: "Response B avoids silent fallback and explains design choices. Response A silently returns 'Unknown', directly contradicting the requirement."

---

## Cost

SKILL.md ~3,500 tokens · Budget share 2.7% · Runtime: +1 reasoning step per code change (pre-submit checklist)

---

## Verdict: ✅ INSTALL

| Dimension | Score |
|-----------|-------|
| Structural | B (86.0) |
| Behavioral Delta | +28 |
| Cost | Low |

The skill's No Silent Fallbacks rule produces a clear, measurable behavioral change. The 6 rules are well-specified with code examples showing correct vs incorrect patterns. OVER_CONSTRAINED is defensible for a purely behavioral skill.

Fix before promotion: add `tests.md` and `PROMOTION-CHECKLIST.md`.
