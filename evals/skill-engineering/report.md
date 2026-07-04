# Skill Eval Report: skill-engineering · 技能工程设计

**Source**: [xobotyi/cc-foundry](https://github.com/xobotyi/cc-foundry)  
**Date**: 2026-07-04 · **Evaluator**: skill-eval v0.3.0  
**Status**: ⏳ L1 complete · L2 pending

---

## L0: Classification · 分类

| Field | Value |
|-------|-------|
| Primary track | A (🧠 Behavioral) |
| Confidence | A=0.80, C=0.25 |

---

## L1: Structural Compliance · 结构规范 ✅ Real

### 21 Static Checks

| # | Check | Result |
|---|-------|--------|
| 1-13 | Frontmatter through secrets | ✅ PASS |
| 14 | `tests.md` | ❌ FAIL |
| 15 | `PROMOTION-CHECKLIST.md` | ❌ FAIL |
| 16-21 | References, staging | ✅ PASS |

**18/21 PASS · 1 WARN · 2 FAIL**

### Anti-Patterns

| Flag | Found? |
|------|--------|
| `CLAUDE_TOOL_REFS` (backticked `${CLAUDE_SKILL_DIR}` paths) | ✅ YES |
| All others | ❌ No |

### Score

```
passing = 19/21 = 0.905
penalty = 1.0 - 0.05 × 1 = 0.95
structural = 0.905 × 0.95 = 0.860 → B (86.0)
```

Notable: excellent progressive disclosure via 5 reference files covering spec/creation/evaluation/iteration/advanced patterns.

---

## L2: Behavioral Delta · 行为增量 ⏳ Pending

**What we'll test**: The self-sufficiency rule — "SKILL.md must be behaviorally self-sufficient without references."
**Bait task**: "Create a deployment skill — put overview in SKILL.md, details in references/deploy.md"
**Estimated cost**: ~6 API calls, ~$0.005.

---

## Verdict · 结论

### ⏳ PENDING — L1 B, L2 to confirm

Strong structural design with good progressive disclosure. The self-sufficiency rule is unique and testable. Needs L2 to verify it actually changes how Claude structures skills.

*L1: real. L2: pending.*
