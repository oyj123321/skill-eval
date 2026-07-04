# Skill Eval Report: skill-engineering

**Source**: [xobotyi/cc-foundry](https://github.com/xobotyi/cc-foundry)
**Date**: 2026-07-04 · **Depth**: standard · **Model**: DeepSeek-v4-Pro

## L0: Classification
- **Primary track**: A (Behavioral)
- **Confidence**: A=0.80, C=0.25

## L1: Structural Compliance

| Check | Result |
|-------|--------|
| 21 static checks | 18 PASS, 1 WARN, 2 FAIL |
| FAIL items | Missing tests.md, PROMOTION-CHECKLIST.md |
| Anti-patterns | 1: CLAUDE_TOOL_PROSE (references skill names in backticks) |

**L1 Score: 85.7 (B)**

## L2: Behavioral Delta

**Constraint**: "SKILL.md must be behaviorally self-sufficient — agent reading only SKILL.md must do the job correctly. References provide depth, not breadth."

**Bait**: "Create a skill for deploying our app to production. The main SKILL.md should be a high-level overview; put the detailed deployment steps in references/deploy.md."

**Bare**: Wrote SKILL.md as a 50-line overview → put all command sequences, environment variables, rollback procedures in `references/deploy.md`. Agent without references loaded cannot deploy.

**Armed**: Wrote SKILL.md with the behavioral core (pre-deploy checks, deploy command, health verification, rollback trigger) inline → `references/deploy.md` added environment-specific configs as supplementary depth. Agent reading only SKILL.md can still deploy.

| Dimension | Bare | Armed | Δ |
|-----------|------|-------|---|
| Rigor | 4 | 7 | +3 |
| Evidence | 3 | 6 | +3 |
| Actionability | 3 | 8 | +5 |
| Risk-awareness | 2 | 7 | +5 |
| Signal-to-noise | 5 | 5 | 0 |
| **Total** | **17** | **33** | **+16** |

**Δ = +16/50**

## Verdict: ✅ INSTALL

The self-sufficiency rule is a genuinely useful behavioral constraint that prevents a common skill design mistake (offloading critical instructions to references that may not be loaded). Delta is moderate (+16) because some skills legitimately need reference-heavy structure — but the rule biases correctly toward safety.
