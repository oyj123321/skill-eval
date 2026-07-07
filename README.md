# skill-eval — A Quantitative Evaluation Framework for Claude Code Skills

<p align="center">
  <strong>🇬🇧 English</strong> &nbsp;|&nbsp;
  <a href="README-zh.md">🇨🇳 中文</a> &nbsp;|&nbsp;
  <a href="evals/charts/results.html">📊 Charts</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude%20Code-skill-6C4DFF?style=flat-square&logo=claude" alt="Claude Code Skill">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT">
  <img src="https://img.shields.io/badge/tracks-5-purple?style=flat-square" alt="5 Tracks">
  <img src="https://img.shields.io/badge/skills_evaluated-21-blue?style=flat-square" alt="21 Skills">
  <img src="https://img.shields.io/badge/API_calls-157+-orange?style=flat-square" alt="157+ API Calls">
</p>

---

## Abstract

The Claude Code skill ecosystem lacks systematic evaluation. Skills are published with screenshots and enthusiasm but no quantitative evidence. **skill-eval** is a type-aware evaluation framework that classifies every skill into one of five tracks, applies a track-specific measurement protocol, and produces structured reports with structural scores, behavioral deltas, and cost analysis.

We evaluated **21 skills** across **5 tracks** with **157+ API calls**. The framework produces meaningful score distributions — skills don't all score the same. Cross-validation across two model tiers revealed that **the same skill can be redundant on a strong model (Δ=+2) and essential on a weak one (Δ=+24)** — skill value is not a constant, it's an inverse function of model capability.

---

## 1. Problem

Skills are published without evidence. The current landscape:

| Tool | Measures | Misses |
|------|----------|--------|
| skill-kit `check-skill` | Structural correctness (21 checks) | Whether the skill *changes behavior* |
| PluginEval | Multi-dim quality scoring | A/B comparison to no-skill baseline |
| Manual testing | "Looks good to me" | Reproducibility, quantification |

Three gaps: (1) no behavioral delta measurement, (2) one-size-fits-all evaluation, (3) no cost accounting.

---

## 2. Method: 5-Track Type-Aware Framework

```
INPUT: SKILL.md → L0 Classifier → route to correct track(s)
  │
  ├─ L1: Structural Compliance (all types, free, <2s)
  │
  └─ L2: Tracked Evaluation (API-based, $0.005–0.01 per skill)
      │
      ├─ Track A (🧠 Behavioral)        ✅ 5 skills, 61 calls
      ├─ Track B (🎨 Output Artifact)   ✅ 4 skills, 16 calls
      ├─ Track C (📐 Format)            ✅ 4 skills, 16 calls
      ├─ Track D (🔧 Tool)              ✅ 4 skills, 12 tests
      └─ Track E (📚 Knowledge)         ✅ 4 skills, 32 calls
```

Run: `python track_*.py --skill-md <path>` or `python run_all_tracks.py`

---

## 3. Experiment: 21 Skills Across 5 Tracks

### 3.1 L1: Structural Compliance

<img src="evals/charts/l1_scores.svg" alt="L1 Structural Scores" width="100%">

| Skill | Score | Grade | Key Issue |
|-------|-------|-------|-----------|
| skill-creator (anthropics) | 100.0 | A+ | Reference quality |
| improving-skills (mjenkinsx9) | 90.5 | A- | Clean structure |
| eight-principles (oyj123321) | 90.0 | A- | 2 anti-patterns (defensible) |
| ai-coding-discipline (luoling8192) | 86.0 | B | Missing tests.md |
| skill-engineering (xobotyi) | 86.0 | B | Missing tests.md |

**Finding**: Missing `tests.md` is the #1 structural failure (3/5 skills).

### 3.2 Track A: Behavioral Delta

<img src="evals/charts/track_a_deltas.svg" alt="Track A Behavioral Deltas" width="100%">

| Skill | Bare Score | Armed Score | Δ / 50 | Verdict |
|-------|-----------|-------------|--------|---------|
| eight-principles | 5 | 46 | **+37.5** | ✅ fabrication→verification, chaos→decomposition |
| ai-coding-discipline | 11 | 39 | **+28.0** | ✅ silent masking→fail-fast |
| skill-engineering | 19.5 | 40 | **+20.5** | ✅ reference-dependence→self-sufficiency |
| skill-creator | 28.5 | 16 | **-12.5** | ⚠️ process skill, single-turn API limitation |
| improving-skills | — | — | **N/A** | ⚠️ tool-dependent, needs Track D |

**Mean Δ = +28.7/50** (3 output-constraining skills). **Score spread = 50 points** — from +37.5 to -12.5.

### 3.3 Cross-Validation: Same Skill, Two Models

<img src="evals/charts/cross_validation.svg" alt="Cross-Validation" width="100%">

Same skill (ai-coding-discipline Rule 1), same bait, two models. **Pro already writes correct code (Δ=+2). Flash gets it wrong without the skill (Δ=+24).** Skill value is model-dependent — evaluations must report the model.

### 3.4 Track B: Output Artifact (4 skills, 16 API calls)

Tests whether a skill improves the quality of *documents it produces*.

<img src="evals/charts/track_b_deltas.svg" alt="Track B" width="100%">

| Skill | Proposal Δ | Guide Δ | Mean Δ / 30 | Notes |
|-------|-----------|---------|-------------|-------|
| xlsx | +7 | -1 | **+3.0** | Structured spreadsheet format helps |
| pptx | -3 | +3 | **0.0** | Neutral — presentation rules don't change output much |
| docx | -1 | -9 | **-5.0** | Strict document rules constrain creative proposals |
| canvas-design | -5 | -6 | **-5.5** | Design rules can't produce canvas output in API mode |

**Score spread = 8.5 points**. Format constraints hurt creative docs (-9Δ) but help structured ones (+7Δ).

### 3.5 Track C: Format Compliance (4 skills, 16 API calls)

Tests whether a skill enforces *output format rules* — conventional commit format.

<img src="evals/charts/track_c_deltas.svg" alt="Track C" width="100%">

| Skill | Bugfix Δ | Feature Δ | Mean Δ / 15 | Notes |
|-------|---------|----------|-------------|-------|
| managing-commits | +3 | -1 | **+1.0** | Actual commit-format skill — positive |
| brand-guidelines | 0 | 0 | **0.0** | Visual reference — format rules irrelevant |
| doc-coauthoring | -8 | +1 | **-3.5** | Writing process skill, not format skill |
| theme-factory | -7 | 0 | **-3.5** | UI theme skill, not format skill |

**Score spread = 4.5 points**. Only the actual format skill scores positive. General skills forced into wrong rubric get negative deltas.

### 3.6 Track D: Tool Correctness (4 skills, 12 tool tests)

Tests whether documented commands execute correctly.

<img src="evals/charts/track_d_passrates.svg" alt="Track D" width="100%">

| Skill | Tests | Pass Rate | Failed Cases |
|-------|-------|-----------|-------------|
| webapp-testing | 2/3 | **67%** | Test suite output format |
| mcp-builder | 2/3 | **67%** | Health check exit code |
| claude-api | 1/3 | **33%** | Model pattern, rate limit output |
| slack-gif-creator | 1/3 | **33%** | File output, frame count |

**Score spread = 34 points**. Deterministic — no LLM judge. Edge cases fail more than happy paths.

### 3.7 Track E: Knowledge Accuracy (4 skills, 32 API calls)

Tests whether reference knowledge produces more accurate answers than general model knowledge.

<img src="evals/charts/track_e_deltas.svg" alt="Track E" width="100%">

| Skill | Query 1 Δ | Query 2 Δ | Mean Δ / 20 | Notes |
|-------|----------|----------|-------------|-------|
| skill-creator | +7 | +6 | **+6.5** | Structured process knowledge matches queries |
| frontend-design | 0 | +1 | **+0.5** | Common CSS — model already knows |
| internal-comms | -3 | -3 | **-3.0** | Skill body too short (1,098 chars) |
| algorithmic-art | 0 | -7 | **-3.5** | Niche art — body adds noise, not signal |

**Score spread = 10.0 points**. Common knowledge Δ≈0. Structured process knowledge largest positive. Short/niche skills negative.

### 3.8 Cross-Validation + Cost

**Same skill, two models**: ai-coding-discipline Rule 1 — Δ=+2 on Pro, Δ=+24 on Flash. Skill value is model-dependent.

**Cost**: 157+ API calls, ~$0.12 total (DeepSeek-v4-pro). ~$0.006 per skill.

---

## 4. Discussion

### What the Framework Demonstrates

1. **Structural quality varies meaningfully** (B to A+). L1 score is a useful first-pass filter (3.1).

2. **Track A discriminates behavioral skills across a 50-point range** (+37.5 to -12.5). Output-level constraints show the largest deltas (3.2).

3. **Track B captures format-vs-creativity trade-off.** Rules that help a spreadsheet (+7Δ) hurt a creative proposal (-9Δ). API-only mode underrates interactive file-generation skills (3.4).

4. **Track C identifies mismatched skills.** Only the actual commit-format skill scored positive; three general skills scored negative when forced into the format rubric (3.5).

5. **Track D catches real tool failures.** Deterministic pass/fail testing reveals a 33-67% range with edge cases failing more than happy paths (3.6).

6. **Track E separates common from niche knowledge.** Common CSS rules show Δ≈0 (model already knows); structured process knowledge shows +6.5 (model doesn't know); niche/short skills score negative (3.7).

7. **Skill value is model-dependent.** Same skill: Δ=+2 on Pro, Δ=+24 on Flash (3.8).

### Limitations (Honest)

| Limitation | Severity | Detail |
|-----------|----------|--------|
| API-only mode underrates interactive design skills | Medium | Track B skills that generate files (pptx, docx) can't call python-pptx in single-turn API |
| Judge JSON parsing ~15% failure rate | Medium | Some judge responses produce valid scores that escape the brace-counting parser. Scores of 0 in raw data should be treated as missing, not zero |
| Single model baseline | Medium | Batch run on DeepSeek-v4-Pro. Cross-validation on 2 tiers, but Claude Sonnet/Opus/Haiku untested |
| No Monte Carlo replicates | Low | Single run per constraint. Directional, not precise |
| Sample biased toward published skills | Low | All 21 skills from GitHub repos. Truly broken skills (no frontmatter, empty body) would score lower but weren't found in the wild |
| Track A tool-dependent skills inconclusive | Low | improving-skills requires bash tools not available in API simulation |

---

## 5. Conclusion

We built a type-aware evaluation framework for Claude Code skills, implemented all five tracks with working runners, and validated them on 21 real skills. The framework produces meaningful score distributions across all tracks. The most important finding is that **skill value is model-dependent** — the evaluation framework itself revealed this, proving its utility as a measurement tool.

**The goal**: publishing a skill without eval data should feel like publishing an ML model without benchmark scores — you don't do it.

---

## Repository Structure

```
skill-eval/
├── SKILL.md                    # Meta skill (load into Claude Code)
├── README.md · README-zh.md    # Bilingual documentation
├── run_l2.py                   # Track A: Behavioral delta
├── track_b.py                  # Track B: Output artifact
├── track_c.py                  # Track C: Format compliance
├── track_d.py                  # Track D: Tool correctness
├── track_e.py                  # Track E: Knowledge accuracy
├── run_all_tracks.py           # Batch eval: 16 skills × 4 tracks
├── make_charts.py              # SVG chart generator
├── layers/                     # Protocol specifications
│   ├── classifier.md · static.md · behavioral.md
│   └── track-{output,format,tool,knowledge}.md
├── judge/                      # Judge prompts + schema
├── task-gen/                   # Bait task synthesis protocol
├── scoring.md                  # Scoring formulas
├── evals/                      # Raw evaluation data
│   ├── charts/                 # SVG charts + HTML dashboard
│   ├── batch_16/               # 16-skill batch results
│   ├── batch-report.md         # Track A batch report
│   └── {skill}/                # Per-skill reports + API data
└── CHANGELOG.md
```

## Quick Start

```bash
git clone https://github.com/oyj123321/skill-eval.git
cd skill-eval

# Single skill (Track A):
python run_l2.py --skill-path .claude/skills/eight-principles --depth standard

# All five tracks on one skill:
python run_all_tracks.py  # reads from evals/skills/

# Regenerate charts:
python make_charts.py
```

| Depth | Cost | Time |
|-------|------|------|
| `quick` (L1 only) | Free | <2s |
| `standard` (L1 + L2 × 1) | ~$0.006 | ~60s |
| `deep` (L1 + L2 × 3) | ~$0.02 | ~3min |

## License

MIT
