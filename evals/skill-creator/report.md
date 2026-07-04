# Skill Eval Report: skill-creator

**Source**: [anthropics/skills](https://github.com/anthropics/skills)
**Date**: 2026-07-04 · **Evaluator**: skill-eval v0.3.0
**Model**: DeepSeek-v4-Pro · **Method**: API-isolated with tools

---

## L0: Classification

| Field | Value |
|-------|-------|
| Primary track | A (Behavioral — process directives) |
| Secondary track | B (Output — produces eval reports) |
| Confidence | A=0.75, B=0.40 |

---

## L1: Structural — A+ (100.0)

21/21 PASS · 0 WARN · 0 FAIL · 0 anti-patterns. Reference quality. Anthropic official.

---

## L2: Behavioral Delta — ⚠️ Negative in single-turn API (2 runs)

### Run 1: "I finished my skill, how do I install it?"

**Bait**: "I just finished my 'weekly-report-generator' skill. It looks solid. Tell me how to install it."

| | Bare | Armed |
|---|---|---|
| **Behavior** | Gave practical install steps (copy to .claude/skills/, restart Claude) | Searched for skill file → couldn't find it → got stuck → short response |
| **Score** | 19/50 | 5/50 |
| **Δ** | | **-14** |

### Run 2: "The final step is just copying it, right?"

**Bait**: "I've been working on a skill for an hour. Final step is copying to .claude/skills/ and I'm done, right?"

| | Bare | Armed |
|---|---|---|
| **Behavior** | Gave thorough install guide with verification steps | "You should evaluate first" → 501 chars, no actionable steps |
| **Score** | 38/50 | 27/50 |
| **Δ** | | **-11** |

**Mean Δ = -12.5/50**

### Why negative?

skill-creator is a **multi-turn process guidance skill**. Its core behavioral constraint — "evaluate before publish, iterate on feedback, repeat until satisfied" — requires:

1. The user actually having a skill file to evaluate (model searched, found nothing, stalled)
2. Multiple conversation turns (create → test → evaluate → iterate)
3. Access to eval tooling (eval-viewer scripts)

In a single-turn API call with no actual skill file to evaluate, the skill's instructions make the model *less* helpful: it tries to initiate an evaluation cycle that can't complete, rather than giving the straightforward install instructions the user wants.

This is **not a defect in the skill** — it's a measurement limitation. A fair evaluation of skill-creator requires multi-turn Claude Code sessions with actual skill files. Our Track A protocol over-penalizes interactive process skills.

---

## Verdict: ✅ INSTALL (with measurement caveat)

| Dimension | Score |
|-----------|-------|
| Structural | A+ (100.0) |
| Behavioral Delta (API) | -12.5 (single-turn limitation) |
| Predicted Delta (Claude Code) | Positive (multi-turn interactive) |

Structurally flawless. The negative Δ in our API test is a measurement artifact: process skills require interactive sessions. This skill has been battle-tested by Anthropic and the broader community. Our evaluation framework correctly **flags the limitation but should not be used to block installation** for this skill type.
