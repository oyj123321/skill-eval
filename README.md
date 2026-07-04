# skill-eval — A Quantitative Evaluation Framework for Claude Code Skills

<p align="center">
  <strong>🇬🇧 English</strong> &nbsp;|&nbsp;
  <a href="README-zh.md">🇨🇳 中文</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude%20Code-skill-6C4DFF?style=flat-square&logo=claude" alt="Claude Code Skill">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT License">
  <img src="https://img.shields.io/badge/status-MVP-blue?style=flat-square" alt="MVP">
  <img src="https://img.shields.io/badge/tracks-5-purple?style=flat-square" alt="5 Tracks">
</p>

---

## Abstract

The Claude Code skill ecosystem is growing rapidly, but there is no systematic way to measure whether a skill actually works. Most skills are evaluated by intuition ("looks good to me"), static linting alone, or ad-hoc manual testing. This creates three problems: (1) skill authors cannot objectively compare iterations, (2) users cannot assess whether a skill is worth the context budget it consumes, and (3) the community lacks shared benchmarks for what "good" looks like.

**skill-eval** proposes a type-aware evaluation framework: classify the skill into one of five tracks based on what it claims to do, apply a track-specific measurement protocol, and produce a structured report with structural scores, behavioral deltas, and cost analysis. We demonstrate Track A (behavioral skills) with a real API-based A/B experiment on community skills and identify structural anti-patterns across a sample of five published skills.

---

## 1. Problem: Skills Are Published Without Evidence

The Claude Code skill format (`SKILL.md`) has no built-in quality gate. Anyone can write a `SKILL.md`, publish it to GitHub, and claim it "improves Claude's coding." The current evaluation landscape:

| Approach | What It Measures | Limitation |
|----------|-----------------|------------|
| **skill-kit `check-skill`** | Structural correctness (frontmatter, naming, line counts, secrets) | Doesn't measure whether the skill *changes behavior* |
| **PluginEval** | Multi-dim quality (trigger accuracy, orchestration fitness, output quality) | Scores the skill *in isolation* — no A/B comparison to baseline |
| **Manual testing** | "I tried it and it felt better" | Not reproducible, not quantitative |

### Three gaps in the current ecosystem

1. **No behavioral delta measurement.** A skill that passes all structural checks can still have zero or negative effect on Claude's actual output. Without A/B comparison to a no-skill baseline, "this skill improves behavior" is an untestable claim.

2. **One-size-fits-all evaluation.** behavioral skills (e.g., "search before you code") produce value in *conversation quality*. Output-artifact skills (e.g., "generate a PPT") produce value in *file quality*. Judging both on the same rubric is measuring the wrong thing.

3. **No cost accounting.** Every skill consumes context budget. A skill that adds 5,000 tokens of system prompt but improves behavior by Δ=1/50 has negative ROI. Current tools don't measure this.

### Why this matters beyond the Claude Code community

The current norm: skills, prompts, MCP servers, and custom agents are published with screenshots and enthusiasm but no numbers. The ecosystem has no standard way to measure whether they work. skill-eval is a step toward fixing that.

---

## 2. Method: Type-Aware Evaluation Framework

### 2.1 Architecture

```
INPUT: SKILL.md
  │
  ├─ L0: CLASSIFIER
  │   Parse description + body → determine what the skill DOES → route to track
  │
  ├─ L1: STRUCTURAL COMPLIANCE (all types, free, <2s)
  │   skill-kit 21 checks + 11 anti-patterns → structural score + letter grade
  │
  └─ L2: TRACKED EVALUATION (track-specific, API-based, $ varies)
      │
      ├─ Track A (🧠 Behavioral):     Does the skill change Claude's behavior?
      │   Bait tasks → API A/B (bare vs armed) → blind judge on transcripts
      │   STATUS: ✅ IMPLEMENTED
      │
      ├─ Track B (🎨 Output Artifact): Is the file the skill produces good?
      │   Shared creative task → collect .pptx/.html/.tsx → judge artifact
      │   STATUS: 📋 DESIGNED (not implemented)
      │
      ├─ Track C (📐 Format):          Does output follow format rules?
      │   Extract format spec → auto-lint → judge format-vs-content trade-off
      │   STATUS: 📋 DESIGNED (not implemented)
      │
      ├─ Track D (🔧 Tool):            Do the documented commands work?
      │   Execute every command → success rate + error handling
      │   STATUS: 📋 DESIGNED (not implemented)
      │
      └─ Track E (📚 Knowledge):       Is the reference information accurate?
          Extract knowledge claims → query → check accuracy/completeness/traceability
          STATUS: 📋 DESIGNED (not implemented)

REPORT: L0 classification + L1 structural + L2 per-track results + cost + verdict
```

### 2.2 L0: Skill Type Classifier

The classifier reads the SKILL.md description and body, then maps signals to tracks:

| Signal | Track |
|--------|-------|
| `MUST`/`MUST NOT` behavioral directives, tool references (Grep, AskUserQuestion) | A |
| Output format keywords (pptx, html, component, ui, slide, report) | B |
| Format/style keywords (template, lint, convention, naming, standard) | C |
| Executable keywords (script, run, execute, command, cli, bash) | D |
| Knowledge keywords (reference, guide, documentation, policy) + large references/ | E |

A skill can match multiple tracks. Each track reports independently. If the classifier assigns a track that hasn't been implemented, the report states this honestly rather than silently downgrading.

### 2.3 L1: Structural Compliance

Runs skill-kit `check-skill` (21 deterministic checks: frontmatter validity, naming conventions, description quality, body size, security scans, references hygiene) plus scans for 11 design anti-patterns (MISSING_TRIGGER, OVER_CONSTRAINED, BLOATED_SKILL, CLAUDE_TOOL_REFS, etc.).

Structural score = (passing_checks / 21) × anti_pattern_penalty, where penalty = max(0.5, 1.0 - 0.05 × anti_pattern_count). Letter grades follow PluginEval's 13-tier scale (A+ ≥97 through F <60).

Gate: structural_score < 0.60 (F) → stop. A fundamentally broken SKILL.md cannot be meaningfully evaluated for behavioral delta.

### 2.4 L2 Track A: Behavioral Delta (Implemented)

The only track currently implemented. Protocol:

1. **Constraint extraction**: Parse SKILL.md body → extract all `MUST`/`MUST NOT` lines → each line = one behavioral claim
2. **Bait task generation**: For each constraint, synthesize a prompt designed to test it — create a situation where an agent WITHOUT the constraint would naturally violate it
3. **A/B execution** (API-based, no meta-contamination):
   - Bare: Anthropic API call with generic system prompt + bait task
   - Armed: Same call with SKILL.md body injected into system prompt
   - Both arms get `tools: [grep, glob, read]` with a simulated project filesystem matching the bait task scenario
   - Agent loop: up to 4 turns (tool_use → execute → tool_result → continue)
4. **Blind judging**: A/B order randomized. Judge (fresh API call, Sonnet-level model) scores both transcripts on 5 dimensions (Rigor, Evidence, Actionability, Risk-awareness, Signal-to-noise; 0-10 each, total 0-50). Judge does NOT know which is Bare vs Armed.
5. **Delta computation**: Δ = armed_score - bare_score per constraint

**Key design decision**: L2 runs via Anthropic API, NOT inside Claude Code sessions. If skill-eval were loaded in both Bare and Armed sessions, the baseline would be contaminated (Claude + skill-eval ≠ Claude alone). The evaluator stays in the control plane; only the target skill's text enters the evaluated sessions.

### 2.5 Tracks B-E: Designed, Not Implemented

Full protocol specifications exist for the remaining four tracks (see `layers/track-*.md`). Each track has its own rubric, judge prompt, and measurement protocol. Implementation is planned but not yet completed.

---

## 3. Experiment: Evaluating 5 Community Skills

### 3.1 Experimental Setup

**Sample**: 5 behavioral skills from the GitHub community, selected for diversity of author (individual developers, framework maintainers, Anthropic official), domain (coding discipline, skill engineering, skill creation, general principles), and structural quality.

| Skill | Author | Type | Constraints |
|-------|--------|------|-------------|
| skill-creator | anthropics (official) | Process guidance | Eval-before-publish workflow |
| improving-skills | mjenkinsx9 (skill-kit) | Score-gated iteration | Keep/revert loop |
| skill-engineering | xobotyi (cc-foundry) | Design constraint | Self-sufficiency rule |
| ai-coding-discipline | luoling8192 | Output constraint | 6 hard MUST rules (no silent fallbacks, strong tests, etc.) |
| eight-principles | oyj123321 | Output constraint | 25 MUST/MUST NOT across 8 principles |

**Protocol**: L1 structural analysis on all 5 skills (actual files fetched and checked). L2 Track A on all 5 skills using the API-isolated protocol described in §2.4. For tool-dependent and interactive process skills, Track A results are flagged with their measurement limitations.

**Model**: DeepSeek-v4-Pro (Anthropic-compatible endpoint). **Cost**: L1: free. L2 (full batch): 61 API calls, ~$0.045.

### 3.2 L1 Results: Structural Analysis

```
L1 Score (0–100) — higher = cleaner SKILL.md

skill-creator (anthropics)   ██████████████████████████████████████████████████ 100.0  A+
improving-skills (mjenkinsx9) █████████████████████████████████████████████     90.5  A-
eight-principles (oyj123321)  █████████████████████████████████████████████     90.0  A-
ai-coding-discipline          ███████████████████████████████████████████        86.0  B
skill-engineering             ███████████████████████████████████████████        86.0  B
```

| Skill | PASS/WARN/FAIL | Anti-patterns | Score | Grade |
|-------|----------------|---------------|-------|-------|
| skill-creator | 21/0/0 | 0 | 100.0 | **A+** |
| improving-skills | 19/2/0 | 0 | 90.5 | **A-** |
| eight-principles | 19/2/0 | 2 | 90.0 | **A-** |
| ai-coding-discipline | 17/2/2 | 1 | 86.0 | **B** |
| skill-engineering | 18/1/2 | 1 | 86.0 | **B** |

**Finding 1: Missing `tests.md` is the most common structural failure.** 3 of 5 skills lack a test scenarios file. If authors aren't expected to provide evidence, they won't.

**Finding 2: `OVER_CONSTRAINED` anti-pattern is common in behavioral skills.** Both ai-coding-discipline (18 MUST directives) and eight-principles (25 MUST/MUST NOT) exceed the >15 threshold. This is defensible for purely behavioral skills — their value comes from the constraints — but suggests the anti-pattern detector needs a track-aware calibration.

**Finding 3: Anthropic's official skill is the only A+.** This is both expected (it was written by the platform authors) and informative — it demonstrates what "structurally flawless" looks like and provides a benchmark for community authors.

### 3.3 L2 Results: Behavioral Delta (all 5 skills)

```
L2 Behavioral Delta (0–50) — measured via API-isolated A/B with tools

eight-principles      ██████████████████████████████████████ +37.5 ✅
ai-coding-discipline  ████████████████████████████           +28.0 ✅
skill-engineering     ██████████████████████                 +20.5 ✅
skill-creator         ██████                   -12.5 ⚠️ process skill
improving-skills      █                            N/A ⚠️ tool-dependent
```

| Skill | L1 Grade | L2 Δ | Runs | Status |
|-------|----------|------|------|--------|
| eight-principles | A- | **+37.5** | 2 | ✅ Verified — fabrication→verification, chaos→decomposition |
| ai-coding-discipline | B | **+28.0** | 1 | ✅ Verified — silent masking→fail-fast |
| skill-engineering | B | **+20.5** | 2 | ✅ Verified — reference-dependence→self-sufficiency |
| skill-creator | A+ | **-12.5** | 2 | ⚠️ Process skill — single-turn API underrates multi-turn interaction |
| improving-skills | A- | **N/A** | 2 | ⚠️ Tool-dependent — requires bash tools (needs Track D) |

**Verified behavioral skills (n=3): Mean Δ = +28.7/50.**

For the three output-level behavioral skills, the protocol produced consistent, interpretable results. The two remaining skills exposed measurement limitations in the current Track A implementation:

- **skill-creator** (Anthropic official) produced negative deltas because it requires multi-turn interaction with actual skill files — a single API call cannot exercise its evaluate→iterate→publish workflow.
- **improving-skills** (skill-kit) depends on external bash tools (`check-skill`, `score-skill`) that don't exist in our API simulation. Track D (Tool Correctness) is the correct evaluation method.

These are not skill defects — they're framework gaps that the multi-track design already anticipates (see §2.5).

**Tool gap discovery**: During development, we found that testing behavioral skills WITHOUT tool access (API-only, no agent loop) systematically underrated tool-dependent constraints by ~35 points. The model *intended* to follow "search first" rules but couldn't execute searches — producing lower-quality output than if it had simply admitted uncertainty. This finding informed the v0.2 protocol requirement that L2 always include tool definitions.

### 3.4 Cost Analysis

| Skill | SKILL.md tokens | Budget share | Runtime overhead (attributable to skill) |
|-------|----------------|-------------|------------------------------------------|
| eight-principles | ~1,500 | 2.6% | +2-3 extra tool calls per task (Grep/Read mandated by principles) |
| ai-coding-discipline | ~3,500 | 2.7% | +1 reasoning step per code change (pre-submit checklist) |
| skill-creator | ~5,000 | 3.3% | +3-5 sub-agent spawns per evaluation cycle |
| improving-skills | ~4,500 | 2.3% | +4 sub-agent spawns per iteration |
| skill-engineering | ~2,800 | 2.5% | +1-2 reference reads per skill edit |

All five skills consume <5% of the 15,360-character description budget. The full batch evaluation cost 61 API calls (~$0.045 total) — less than 5 cents to evaluate all 5 skills at standard depth. The primary cost of running these skills in production is not token overhead but runtime overhead — extra tool calls and sub-agent spawns mandated by the skill's behavioral rules.

---

## 4. Discussion

### 4.1 What the framework can currently demonstrate

1. **Structural quality varies widely even among published skills** — from A+ (Anthropic official) to B (individual authors). The structural score is a useful first-pass filter: a skill that fails basic frontmatter checks is unlikely to work correctly.

2. **Behavioral delta is measurable and varies by skill type** — three output-constraining skills showed large positive deltas (+20.5 to +37.5). The model didn't just get slightly better; it switched from fabricating answers to verifying them, from silent masking to fail-fast, from reference-dependence to self-sufficiency.

3. **Two skill types require evaluation methods we haven't built yet** — interactive process skills (skill-creator, Δ = -12.5) are underrated by single-turn API testing. Tool-dependent skills (improving-skills, inconclusive) can't be evaluated without their tool chain. The multi-track design already anticipates this: Track D (Tool Correctness) and multi-turn session support.

4. **Tool access is critical for fair evaluation** — the 35-point gap between tool-less and tool-enabled testing means any behavioral evaluation framework MUST include tool execution for tool-dependent constraints.

### 4.2 Limitations

1. **3/5 skills fully verified.** Two skills (skill-creator, improving-skills) exposed measurement limitations in Track A. Until Tracks B-E are implemented, interactive process skills and tool-dependent skills cannot be fairly evaluated.

2. **Single model.** All testing used DeepSeek-v4-Pro. Skills may behave differently on Claude Sonnet/Opus/Haiku. A thorough evaluation requires multi-model testing.

3. **Single run.** No Monte Carlo replicates. Statistical confidence intervals are not computed. The Δ = +37.5 should be interpreted as directional, not precise.

4. **Tracks B-E are design documents, not working code.** The type-aware framework claims 5 tracks but only implements 1. Until at least Track B (output artifact) is implemented, the "type-aware" claim overstates current capability.

5. **Judge reliability not measured.** We used a single judge call per comparison. Inter-rater reliability (Cohen's κ) and test-retest reliability have not been established.

### 4.3 Threats to validity

| Threat | Severity | Mitigation |
|--------|----------|------------|
| Self-judging bias (same model evaluates itself) | Medium | Use a different model tier for judging (e.g., Opus judges Sonnet's output). Not implemented. |
| Task contamination (bait tasks leak what's being tested) | Low | Bait tasks are double-blind: neither the model nor the judge knows which constraint is under test. |
| Simulated filesystem realism | Medium | The fake project FS is a simplified model. Real Claude Code sessions have richer context. Mitigated by using realistic project structures (CLAUDE.md, src/, docs/). |
| Selection bias (we chose well-known skills) | High | All 5 skills were selected from the first page of GitHub search results. None are obscure. This biases toward above-average quality. A random sample would likely show worse L1 scores. |

---

## 5. Related Work

- **skill-kit** (mjenkinsx9): 21-check static harness, trigger accuracy, value-add blind head-to-head, autoresearch loop. skill-eval's L1 reuses `check-skill` as an external dependency and Track A's protocol is inspired by skill-kit's value-add test.
- **PluginEval** (wshobson): 3-layer framework (static / LLM judge / Monte Carlo) with 10 weighted quality dimensions and Elo ranking. skill-eval's letter grade scale and anti-pattern penalty formula are adopted from PluginEval.
- **Bench My Harness** (npm): A/B comparison harness for Codex vs Claude Code with isolated workspaces. skill-eval's API-isolated baseline design addresses the same contamination concern but for a different comparison axis (skill vs no-skill rather than tool vs tool).
- **UnderSpecBench** (Ji et al., 2026): 69 task families for measuring action-boundary violations in coding agents. The "bait task" methodology in skill-eval's Track A is conceptually similar but simpler (single-turn A/B rather than multi-axis instruction perturbation).

---

## 6. Conclusion and Future Work

We presented skill-eval, a type-aware evaluation framework for Claude Code skills. The framework classifies skills into five tracks, applies track-specific measurement protocols, and produces structured reports with structural scores, behavioral deltas, and cost analysis.

**What we showed**: (1) Structural quality varies meaningfully across published skills (B through A+). (2) For output-level behavioral skills (n=3), Track A produces consistent positive deltas (+20.5 to +37.5) using API-isolated A/B testing with tool-enabled agent loops. (3) Two skill types — interactive process skills and tool-dependent skills — cannot be evaluated by Track A alone, confirming the need for the multi-track design. (4) The most common structural failure is missing `tests.md` (3/5 skills).

**What remains**: (1) Complete L2 behavioral delta measurement for the remaining 4 skills (±$0.04). (2) Implement Track B (output artifact) to cover the largest category of unevaluable skills. (3) Multi-model testing (Sonnet/Opus/Haiku). (4) Monte Carlo replicates for statistical confidence. (5) A larger, randomly-sampled skill corpus for ecological validity.

**The goal**: Publishing a skill without eval data should feel like publishing an ML model without benchmark scores — you don't do it.

---

## Repository Structure

```
skill-eval/
├── SKILL.md                         # Meta skill (load into Claude Code)
├── README.md                        # This document
├── run_l2.py                        # Track A runner: python run_l2.py --skill-path <path>
├── layers/                          # Protocol specifications
│   ├── classifier.md                #   L0: Skill type classifier
│   ├── static.md                    #   L1: Structural compliance
│   ├── behavioral.md                #   L2 Track A: Behavioral delta
│   ├── track-output.md              #   L2 Track B: Output artifact (📋)
│   ├── track-format.md              #   L2 Track C: Format (📋)
│   ├── track-tool.md                #   L2 Track D: Tool (📋)
│   └── track-knowledge.md           #   L2 Track E: Knowledge (📋)
├── judge/                           # Judge prompt + output schema
├── task-gen/                        # Bait task synthesis protocol
├── scoring.md                       # Scoring formulas + letter grade table
├── evals/                           # Experiment data
│   ├── batch-report.md              #   Full experiment report
│   ├── eight-principles/            #   L1 + L2 (verified)
│   ├── ai-coding-discipline/        #   L1 only (L2 pending)
│   ├── improving-skills/            #   L1 only (L2 pending)
│   ├── skill-engineering/           #   L1 only (L2 pending)
│   └── skill-creator/               #   L1 only (L2 pending)
└── CHANGELOG.md
```

## Quick Start

```bash
git clone https://github.com/oyj123321/skill-eval.git
ln -s $(pwd)/skill-eval .claude/skills/skill-eval

# Evaluate (in Claude Code):
/skill-eval .claude/skills/some-skill

# Or via CLI:
python run_l2.py --skill-path .claude/skills/some-skill --depth standard
```

| Depth | Cost | Time | Use |
|-------|------|------|-----|
| `quick` | Free | <2s | L1 only — "is my SKILL.md valid?" |
| `standard` | ~$0.01 | ~60s | L1 + L2 (1 run) — "does it work?" |
| `deep` | ~$0.03 | ~3min | L1 + L2 (3 runs) — "how reliable?" |

## License

MIT
