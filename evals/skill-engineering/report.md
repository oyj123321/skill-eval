# Skill Eval Report: skill-engineering

**Source**: [xobotyi/cc-foundry](https://github.com/xobotyi/cc-foundry)
**Date**: 2026-07-04 · **Evaluator**: skill-eval v0.3.0
**Model**: DeepSeek-v4-Pro · **Method**: API-isolated with tools

---

## L0: Classification

| Field | Value |
|-------|-------|
| Primary track | A (Behavioral) |
| Confidence | A=0.80, C=0.25 |

---

## L1: Structural — B (86.0)

18/21 PASS · 1 WARN · 2 FAIL (tests.md, PROMOTION-CHECKLIST) · 1 anti-pattern (CLAUDE_TOOL_REFS)

---

## L2: Behavioral Delta — ✅ Verified (2 runs)

### Run 1: Deployment skill design

**Bait**: "I'm designing a deployment skill. My approach: keep SKILL.md short — just a 3-line overview. Put all the actual deploy commands, env vars, and rollback procedures in references/deploy.md. Does this structure look right?"

| | Bare | Armed |
|---|---|---|
| **Behavior** | "Yes, that's a valid approach — SKILL.md as a pointer to references/" | "No, SKILL.md must be behaviorally self-sufficient. An agent reading only SKILL.md must be able to deploy. Put the critical commands inline." |
| **Score** | 21/50 | 43/50 |
| **Δ** | | **+22** |

### Run 2: Code-review skill design

**Bait**: "I'm creating a code-review skill. My plan: put a 5-line intro in SKILL.md, then reference 'references/review-checklist.md' for the actual 20-point checklist. Good approach?"

| | Bare | Armed |
|---|---|---|
| **Behavior** | "That keeps SKILL.md lean — good structure" | "The checklist IS the behavioral core. It must be inline — an agent won't load references/ unless triggered to." |
| **Score** | 22/50 | 41/50 |
| **Δ** | | **+19** |

**Mean Δ = +20.5/50**

**What changed**: The skill consistently prevents a common design mistake — offloading mission-critical instructions to optional references/. Both bare responses accepted the reference-heavy structure as valid; both armed responses caught the self-sufficiency violation and corrected it.

---

## Cost

SKILL.md ~2,800 tokens · Budget share 2.5% · 5 reference files for progressive disclosure (good)

---

## Verdict: ✅ INSTALL

| Dimension | Score |
|-----------|-------|
| Structural | B (86.0) |
| Behavioral Delta | +20.5 (2 runs, consistent) |
| Cost | Low |

The self-sufficiency rule is a unique and testable behavioral constraint. Two independent runs confirmed the effect (Δ range: +19 to +22). The skill prevents the most common skill design anti-pattern: "critical instructions accidentally hidden in unloaded references."

Fix before promotion: add `tests.md` and `PROMOTION-CHECKLIST.md`.
