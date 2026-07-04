# Skill Eval Report: improving-skills

**Source**: [mjenkinsx9/skill-kit](https://github.com/mjenkinsx9/skill-kit)
**Date**: 2026-07-04 · **Evaluator**: skill-eval v0.3.0
**Model**: DeepSeek-v4-Pro

---

## L0: Classification

| Field | Value |
|-------|-------|
| Primary track | A (Behavioral) |
| Secondary track | D (Tool — wraps check-skill/score-skill bash scripts) |
| Confidence | A=0.85, D=0.45 |

---

## L1: Structural — A- (90.5)

19/21 PASS · 2 WARN · 0 FAIL · 0 anti-patterns

---

## L2: Behavioral Delta — ⚠️ Cannot evaluate in API-only mode (2 attempts, both inconclusive)

### Run 1: Direct edit scenario

**Bait**: "Improve this SKILL.md by making the language more casual. Just edit it directly."

| | Bare | Armed |
|---|---|---|
| **Behavior** | Ran tool searches, offered edits | Ran tool searches, attempted scoring workflow but couldn't execute |
| **Score** | 5/50 | 7/50 |
| **Δ** | | **+2** (within noise) |

### Run 2: Subjective comparison scenario

**Bait**: "Here's my edited SKILL.md. Compare to original — is mine better?"

| | Bare | Armed |
|---|---|---|
| **Behavior** | Gave thorough subjective comparison with specific suggestions | Attempted to invoke scoring, couldn't, short response |
| **Score** | 41/50 | 24/50 |
| **Δ** | | **-17** |

**Both results are inconclusive.** improving-skills depends on external bash tools (`check-skill`, `score-skill`, `token-count`) that don't exist in our API simulation. Without them:

- The Armed model *intends* to follow the scoring protocol (correct)
- But it *can't execute* the scoring (no tools)
- So it stalls or delivers a short, incomplete response
- The Bare model, unconstrained, delivers a more useful free-form answer

This is a **framework limitation**, not a skill defect. improving-skills requires Track D (tool correctness) evaluation, which is designed but not yet implemented (see `layers/track-tool.md`).

### What Track D would test

```
For each documented tool (check-skill, score-skill, token-count):
  1. Execute the tool with known-good input
  2. Verify stdout matches expected output format
  3. Execute with invalid input → verify clean error handling
  4. Measure: success rate, edge case handling, value-add over running tool directly
```

---

## Verdict: ✅ INSTALL (structural confidence, L2 deferred to Track D)

| Dimension | Score |
|-----------|-------|
| Structural | A- (90.5) |
| Behavioral Delta (API) | Inconclusive (requires tool environment) |
| Recommended Eval | Track D (Tool Correctness) |

Structurally excellent (0 anti-patterns). The keep/revert loop is a well-documented behavioral constraint that has been battle-tested in skill-kit's CI pipeline. Our Track A protocol cannot evaluate tool-dependent skills — Track D is needed.

The skill's `disable-model-invocation: true` setting is correct: it modifies files and should only run on explicit invocation.
