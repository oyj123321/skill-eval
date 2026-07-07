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

Three verified behavioral skills: mean Δ = +28.7/50. Two flagged: skill-creator (process skill, single-turn API limitation) and improving-skills (tool-dependent).

### 3.3 Cross-Validation: Same Skill, Two Models

<img src="evals/charts/cross_validation.svg" alt="Cross-Validation" width="100%">

Same skill (ai-coding-discipline Rule 1), same bait, two models. **Pro already writes correct code (Δ=+2). Flash gets it wrong without the skill (Δ=+24).** Skill value is model-dependent — evaluations must report the model.

### 3.4 Tracks B/C/D/E — 16 Skills

| Track | Skills | Score Range | Key Finding |
|-------|--------|-------------|-------------|
| **B** Output | 4 | +3.0 to -5.5 | Format hurts creative docs, helps structured ones |
| **C** Format | 4 | +1.0 to -3.5 | Only actual format skills score positive |
| **D** Tool | 4 | 67% to 33% | 34-point pass rate spread |
| **E** Knowledge | 4 | +6.5 to -3.5 | skill-creator +6.5; non-knowledge skills negative |

<img src="evals/charts/track_b_deltas.svg" alt="Track B" width="48%">
<img src="evals/charts/track_e_deltas.svg" alt="Track E" width="48%">

### 3.5 Cost

Full evaluation of 21 skills: 157+ API calls, total cost ~$0.12 (DeepSeek-v4-pro). Average ~$0.006 per skill at standard depth.

---

## 4. Discussion

### What the Framework Demonstrates

1. **Structural quality varies meaningfully** (B to A+). The L1 score is a useful first-pass filter.

2. **All five tracks produce score spreads** — skills don't cluster. The framework discriminates.

3. **Skill value is model-dependent.** Same skill, same task: Δ=+2 on Pro, Δ=+24 on Flash. Skills are redundant on strong models, essential on weak ones.

4. **Output format constraints have asymmetric effects.** Strict rules hurt creative tasks (Track B Δ=-5.5) but help structured ones (+3.0).

5. **Only type-matched skills score positive on format/knowledge tracks.** General skills forced into the wrong rubric get negative deltas — the classifier works.

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
