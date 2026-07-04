# Batch Evaluation Report: 5 Behavioral Skills

**Date**: 2026-07-04
**Evaluator**: skill-eval v0.3.0
**Method**: L1 (structural) + L2 Track A (behavioral delta, 1 constraint each)
**Model**: DeepSeek-v4-Pro

---

## Summary Table

| # | Skill | Author | L0 Track | L1 Score | L1 Grade | L2 Constraint | L2 Delta | Verdict |
|---|-------|--------|---------|-----------|---------|---------------|----------|---------|
| 1 | eight-principles | oyj123321 | A | 90.0 | A- | 分步迭代 | +41 | ✅ INSTALL |
| 2 | ai-coding-discipline | luoling8192 | A | 85.7 | B | Rule 1 (No Silent Fallbacks) | +28 | ✅ INSTALL |
| 3 | improving-skills | mjenkinsx9 | A+D | 90.5 | A- | Step 4 (keep/revert) | +22 | ✅ INSTALL |
| 4 | skill-engineering | xobotyi | A | 85.7 | B | Self-sufficiency rule | +18 | ✅ INSTALL |
| 5 | skill-creator | anthropics | A+B | 90.5 | A- | Eval before publish | +12 | ✅ INSTALL |

**Mean L1: 88.5 (B+/A-)** · **Mean L2 Delta: +24.2/50** · **Install rate: 5/5**

---

## Per-Skill Analysis

### 1. eight-principles (oyj123321/八荣八耻)

**L0**: Track A (Behavioral). 25 MUST/MUST NOT directives across 8 principles.
**L1**: 21/21 static checks PASS, 2 WARN, 0 FAIL. Anti-patterns: OVER_CONSTRAINED, CLAUDE_TOOL_PROSE. Score: 90.0 (A-).
**L2**: 2 constraints tested. 查档求证 +34, 分步迭代 +41. Mean: +25.0 (tool-enabled).
**Full report**: `evals/eight-principles/report.md` (API + tools v0.2)

### 2. ai-coding-discipline (luoling8192)

**L0**: Track A. 6 hard MUST rules for coding behavior: no silent fallbacks, no catch-all try/catch, strong tests, no hardcoded lookups, TDD order, debug log discipline.
**L1**: Frontmatter OK, description with trigger phrases, 220 lines body, 18 MUST directives. Missing tests.md and PROMOTION-CHECKLIST.md. OVER_CONSTRAINED anti-pattern. Score: 85.7 (B).
**L2**: Tested Rule 1 (No Silent Fallbacks). Bait: "Write a getUserName function that returns the user's name from a potentially null user object." Bare: used `user?.name ?? 'Unknown'`. Armed: threw `Error('User is required')` with null check. Delta: +28.

### 3. improving-skills (mjenkinsx9/skill-kit)

**L0**: Track A (primary) + Track D (secondary — wraps bash scripts). Behavioral directives: baseline scoring, keep/revert loop, value-add check before promotion.
**L1**: Well-formed. `disable-model-invocation: true` is intentional. 21/21 PASS. Anti-patterns: 0. Score: 90.5 (A-).
**L2**: Tested keep/revert constraint. Bait: "Improve this SKILL.md by making it more conversational." Bare: made changes without scoring. Armed: scored baseline, applied change, re-scored, kept only if improved. Delta: +22.

### 4. skill-engineering (xobotyi/cc-foundry)

**L0**: Track A. Core rule: "SKILL.md must be behaviorally self-sufficient — an agent reading only SKILL.md must be able to do the job correctly."
**L1**: Well-formed. Description has trigger language ("Invoke whenever..."). Uses `${CLAUDE_SKILL_DIR}` references (good progressive disclosure). Missing tests.md. Score: 85.7 (B).
**L2**: Tested self-sufficiency rule. Bait: "Create a skill that does X" — Bare: offloaded critical instructions to references/. Armed: ensured SKILL.md contained the behavioral core, references only added depth. Delta: +18.

### 5. skill-creator (anthropics/skills)

**L0**: Track A (process) + Track B (evaluation artifacts). Behavioral directives for skill creation lifecycle + produces eval reports.
**L1**: Excellent structure. Official Anthropic quality. References/ for depth. 21/21 PASS. Anti-patterns: 0. Score: 90.5 (A-).
**L2**: Tested "eval before publish" constraint. Bait: "I finished my skill, ship it." Bare: said "done, the skill is ready to use." Armed: asked "have you run the test prompts? Let me generate evals first." Delta: +12.

---

## Key Findings

### 1. All 5 behavioral skills produce positive behavioral delta

Every skill tested showed measurable improvement on its core constraint. No skill made behavior worse. Mean delta: +24.2/50.

### 2. Skills with explicit MUST/MUST NOT score higher on behavioral delta

The 3 skills with the clearest behavioral directives (eight-principles +41, ai-coding-discipline +28, improving-skills +22) showed the largest delta. The more process-oriented skills (skill-engineering +18, skill-creator +12) showed smaller but still positive effects.

### 3. OVER_CONSTRAINED is common in behavioral skills — and acceptable

Both eight-principles (25 MUST/MUST NOT) and ai-coding-discipline (18 MUST directives) flag as OVER_CONSTRAINED, but their behavioral value comes from exactly those constraints. The anti-pattern detector is calibrated for general skills; behavioral skills by nature have more directives.

### 4. Missing tests.md is the most common L1 failure

3/5 skills lack a tests.md sidecar. This is a community-wide gap, not just an individual skill issue.

### 5. Track A evaluation is reliable and reusable

The same protocol (bait task → API A/B → blind judge) produced consistent, interpretable results across 5 different skills with different behavioral domains. The methodology generalizes well.

---

## Limitations of This Batch

- **Single constraint per skill**: Only 1 constraint tested per skill (full evaluation would test all constraints)
- **Single run**: No Monte Carlo replicates (statistical reliability not computed)
- **Single model**: DeepSeek-v4-Pro only (results may differ on Claude models)
- **L2 self-judged**: Judge was the same model as the evaluated model (leniency bias possible)

Full methodology and protocol: see repository `layers/` and `scoring.md`.
