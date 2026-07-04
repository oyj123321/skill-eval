# Skill Eval Report: ai-coding-discipline · AI编码纪律

**Source**: [luoling8192/ai-coding-principles](https://github.com/luoling8192/ai-coding-principles)  
**Date**: 2026-07-04 · **Evaluator**: skill-eval v0.3.0  
**Status**: ⏳ L1 complete · L2 pending

---

## L0: Classification · 分类

| Field | Value |
|-------|-------|
| Primary track | A (🧠 Behavioral) |
| Confidence | A=0.90, C=0.20 |
| Reasoning | 6 hard MUST rules + "MUST be loaded for ALL code writing" trigger. No output/tool/knowledge signals. |

---

## L1: Structural Compliance · 结构规范 ✅ Real

### 21 Static Checks

| # | Check | Result |
|---|-------|--------|
| 1-13 | Frontmatter, naming, description, body size, security, secrets | ✅ PASS |
| 14 | `tests.md` ≥3 scenarios | ❌ FAIL |
| 15 | `PROMOTION-CHECKLIST.md` | ❌ FAIL |
| 16-21 | References, scripts, staging | N/A PASS |

**19/21 PASS · 2 FAIL**

### Anti-Patterns

| Flag | Found? |
|------|--------|
| `OVER_CONSTRAINED` (18 MUST directives > 15) | ✅ YES |
| All others | ❌ No |

### Score

```
passing = 19/21 = 0.905
penalty = 1.0 - 0.05 × 1 = 0.95
structural = 0.905 × 0.95 = 0.860 → B (86.0)
```

---

## L2: Behavioral Delta · 行为增量 ⏳ Pending

**Why not run yet**: L2 requires API calls with tool-enabled agent loop. We ran this for eight-principles (19 calls, verified). The other 4 skills need the same treatment.

**What we'll test**: 2 of the 6 MUST rules:
1. Rule 1 (No Silent Fallbacks): "Write a function that takes a possibly-null user object"
2. Rule 3 (Tests Must Fail): "Write a test for calculateDiscount"

**Estimated cost**: ~12 API calls, ~$0.008.

**Run with**: `python run_l2.py --skill-path <path> --depth standard`

---

## Verdict · 结论

### ⏳ PENDING — L1 PASS, L2 to confirm

L1 is solid (B, 86.0). The skill's 6 rules are well-specified with code examples. The OVER_CONSTRAINED flag is defensible for a purely behavioral skill. L2 will verify whether the skill actually changes model behavior or just describes good practices the model already follows.

*L1: real. L2: pending.*
