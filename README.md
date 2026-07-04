# skill-eval — Meta Skill Evaluator for Claude Code

<p align="center">
  <img src="https://img.shields.io/badge/Claude%20Code-skill-6C4DFF?style=flat-square&logo=claude" alt="Claude Code Skill">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT License">
  <img src="https://img.shields.io/badge/status-MVP-blue?style=flat-square" alt="MVP">
</p>

**Evaluate any Claude Code skill with evidence.** Classify the skill type, then run the correct evaluation track.

---

## The Problem

Not all skills are the same type, but most evaluation tools judge them on one rubric:

| Skill Type | What It Does | Judging Conversational Transcripts? |
|-----------|-------------|-------------------------------------|
| 🧠 Behavioral | Changes HOW Claude thinks/acts | ✅ Makes sense |
| 🎨 Output Artifact | Produces PPTs, UIs, reports | ❌ Wrong — judge the FILE |
| 📐 Format | Enforces style/template/structure | ❌ Wrong — auto-lint the output |
| 🔧 Tool | Wraps scripts, APIs, CLIs | ❌ Wrong — measure correctness |
| 📚 Knowledge | Provides reference information | ❌ Wrong — verify accuracy |

skill-eval **classifies first, then evaluates** — each skill type gets its own evaluation track.

---

## 5 Evaluation Tracks

```
L0: CLASSIFIER → reads SKILL.md → routes to correct track(s)

Track A (🧠 Behavioral)     ✅ IMPLEMENTED
  "Does this skill change Claude's behavior?"
  Bait tasks → with/without skill A/B → blind judge

Track B (🎨 Output Artifact) 📋 DESIGNED
  "Is the FILE this skill produces good?"
  Creative task → collect .pptx/.html/.tsx → judge artifact

Track C (📐 Format)          📋 DESIGNED
  "Does output follow the format rules?"
  Auto-lint + judge format-vs-content trade-off

Track D (🔧 Tool)            📋 DESIGNED
  "Do the documented commands work?"
  Execute every tool → success rate + error handling

Track E (📚 Knowledge)       📋 DESIGNED
  "Is the reference information accurate?"
  Query → check accuracy/completeness/source traceability
```

---

## Quick Start

### Install

```bash
git clone https://github.com/oyj123321/skill-eval.git
# Link into your project
mkdir -p .claude/skills
ln -s $(pwd)/skill-eval .claude/skills/skill-eval
```

### Evaluate a Skill

```
# In Claude Code:
/skill-eval .claude/skills/eight-principles

# Or via CLI:
python run_l2.py --skill-path .claude/skills/eight-principles --depth standard
```

### Depth Levels

| Depth | What It Does | Cost | Time |
|-------|-------------|------|------|
| `quick` | L0 classification + L1 structural | Free | <2s |
| `standard` | L0 + L1 + L2 (1 run) | ~$0.01 | ~60s |
| `deep` | L0 + L1 + L2 (3 runs) | ~$0.03 | ~3min |

---

## Evaluated Skills

skill-eval has been used to evaluate real skills from the community:

| Skill | Type | L1 Score | L2 Delta | Verdict |
|-------|------|----------|----------|---------|
| [eight-principles](https://github.com/oyj123321/claude-code-eight-principles) | Track A | A- (90.0) | +25.0/50 | ✅ INSTALL |
| *(more coming)* |

See `evals/` for full reports.

---

## Architecture

```
skill-eval/
├── SKILL.md                    # Meta skill (Claude Code entry point)
├── README.md                   # This document
├── run_l2.py                   # API-based Track A runner (with tools)
├── layers/
│   ├── classifier.md           # L0: Skill type classifier
│   ├── static.md               # L1: Structural compliance checks
│   ├── behavioral.md           # L2 Track A: Behavioral delta protocol
│   ├── track-output.md         # L2 Track B: Output artifact (designed)
│   ├── track-format.md         # L2 Track C: Format compliance (designed)
│   ├── track-tool.md           # L2 Track D: Tool correctness (designed)
│   └── track-knowledge.md      # L2 Track E: Knowledge accuracy (designed)
├── judge/
│   ├── prompt.md               # Blind judge prompt (5-dim rubric)
│   └── schema.json             # Judge output JSON schema
├── task-gen/
│   └── protocol.md             # MUST/MUST NOT → bait task synthesis
├── scoring.md                  # Cross-track + per-track scoring
├── evals/                      # Evaluation reports
├── CHANGELOG.md
└── LICENSE
```

## Relationship to Other Tools

```
skill-kit:      structural well-formedness, trigger accuracy, auto-iteration
PluginEval:     multi-dim quality scoring, anti-patterns, Monte Carlo stats
skill-eval:     type-aware evaluation across 5 tracks
                └── L1 reuses skill-kit (external dependency)
                └── Track A = behavioral delta (unique)
                └── Tracks B-E = filling gaps neither tool addresses
```

## License

MIT — use freely, modify, distribute.
