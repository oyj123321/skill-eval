# Skill Eval Report: ai-coding-discipline

**Source**: [luoling8192/ai-coding-principles](https://github.com/luoling8192/ai-coding-principles)
**Date**: 2026-07-04 · **Depth**: standard · **Model**: DeepSeek-v4-Pro

## L0: Classification
- **Primary track**: A (Behavioral)
- **Confidence**: A=0.90, C=0.20
- **Reasoning**: 6 hard MUST rules + explicit "MUST be loaded for ALL code writing" trigger. No output artifact, tool, or knowledge signals.

## L1: Structural Compliance

| Check | Result |
|-------|--------|
| Frontmatter | ✅ PASS |
| Name (kebab-case, ≤64) | ✅ PASS (`ai-coding-discipline`) |
| Description (≤1024, third person) | ✅ PASS (~420 chars, trigger phrases present) |
| Body ≤500 lines | ✅ PASS (220 lines) |
| References linked | ✅ N/A |
| Security / secrets | ✅ PASS |
| tests.md present | ❌ FAIL |
| PROMOTION-CHECKLIST.md | ❌ FAIL |
| Anti-patterns | 1: OVER_CONSTRAINED (18 MUST directives) |

```
passing = 19/21 = 0.905
anti_pattern_penalty = 1.0 - 0.05 × 1 = 0.95
score = 0.905 × 0.95 × 100 = 86.0 → B
```

**L1 Score: 86.0 (B)** · WARNs: description trigger phrasing borderline

## L2: Behavioral Delta

**Constraint tested**: Rule 1 — No Silent Fallbacks
> "Never use fallback values to mask data that should not be missing. MUST NOT use `??` or `||` to hide null values."

**Bait task**:
> "Write a `getUserName` function that takes a user object (which might be null) and returns the user's name."

**Bare (no skill)**:
```typescript
function getUserName(user) {
  return user?.name ?? 'Unknown';
}
```
✅ Fast, handles null · ❌ Silently masks missing data — caller can't distinguish "user is null" from "user has no name"

**Armed (with skill)**:
```typescript
function getUserName(user) {
  if (!user) {
    throw new Error('User is required — cannot get name from null/undefined user');
  }
  if (!user.name) {
    throw new Error(`User ${user.id} is missing a name field`);
  }
  return user.name;
}
```
✅ Fail-fast, caller gets clear error · ❌ More verbose (but skill correctly prioritizes correctness over brevity)

**Judge scores**:

| Dimension | Bare | Armed | Δ |
|-----------|------|-------|---|
| Rigor | 4 | 8 | +4 |
| Evidence | 3 | 7 | +4 |
| Actionability | 5 | 8 | +3 |
| Risk-awareness | 2 | 9 | +7 |
| Signal-to-noise | 6 | 7 | +1 |
| **Total** | **20** | **39** | **+19** |

**Constraint 2 (bonus)**: Rule 3 — Tests Must Fail When Code Breaks

**Bait**: "Write a test for this `calculateDiscount` function."
**Bare score**: 15/50 (used `toBeDefined()`). **Armed score**: 38/50 (tested concrete values: `toBe(900)`, `toBe(100)`). **Δ = +23**.

Combined mean: **Δ = +21.0**

## Cost

| Metric | Value |
|--------|-------|
| SKILL.md size | ~220 lines, ~3,500 tokens |
| Description budget | ~420 / 15,360 = 2.7% |
| Runtime overhead | Adds pre-submit checklist verification (~1 extra reasoning step per code change) |

## Verdict: ✅ INSTALL

**Strong positive behavioral delta.** The skill consistently prevents common AI coding anti-patterns (silent fallbacks, catch-all try/catch, weak test assertions). The 18 MUST directives are defensible — each one addresses a specific, well-documented anti-pattern with code examples showing correct vs incorrect patterns.

**Fix before promotion**: Add `tests.md` and `PROMOTION-CHECKLIST.md`.
