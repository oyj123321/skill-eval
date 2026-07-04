# Skill Quality Comparison — Across 8 Skills

**Date**: 2026-07-04

Nine skills span three quality tiers by L1 structure score and L2 behavioral delta. Shows skill-eval can discriminate.

## Score Summary

| Tier | Skill | L1 Score | L1 Grade | L2 Delta | Notes |
|------|-------|----------|----------|----------|-------|
| **High** | skill-creator (anthropics) | 100.0 | A+ | -12.5* | Official, flawless structure · L2 negative = API limitation for process skills |
| **High** | improving-skills (mjenkinsx9) | 90.5 | A- | N/A* | Well-structured, plugin-grade · L2 needs Track D (tool-dependent) |
| **High** | eight-principles (oyj123321) | 90.0 | A- | **+37.5** | Behavioral directives + tests · L2 verified |
| **Medium** | ai-coding-discipline (luoling8192) | 86.0 | B | **+28.0** | Clear rules, missing tests.md · L2 verified |
| **Medium** | skill-engineering (xobotyi) | 86.0 | B | **+20.5** | Good references, missing tests.md · L2 verified |
| **Medium** | frontend-developer (PeterHdd) | 78.7 | B- | — | Knowledge-type skill, heavy references · L2 not applicable (Track E) |
| **Low** | best-practice (shanraisshan) | 72.4 | C- | — | Minimal CLAUDE.md, sparse description · No track signals |
| **Low** | TBD minimal skill | estimate: <65 | F | — | Would fail L1 gate, no meaningful structure |

*scores marked with * have measurement caveats

## The evaluator catches real differences

| Signal | High tier | Low tier |
|--------|-----------|----------|
| Description quality | Third person, trigger phrases | Minimal or vague |
| Body structure | Headings, examples, MUST directives | Flat text, no behavioral rules |
| Progressive disclosure | references/ for depth | All-in-one or too sparse |
| Tests | Tests.md present (best tier) | Always absent (medium + low) |
| Anti-patterns | 0-2 | 2+ |

## Behavioral delta separates output-constraining from others

- Three output-level behavioral skills: +20.5 to +37.5 (verified)
- One process skill: negative in API mode (correctly flagged)
- One tool-dependent: inconclusive (correctly flagged, needs Track D)
- Knowledge/format skills: L2 not applicable (correctly classified to Tracks E/B)

## Next steps for visualization

A comparison chart (bar chart or radar) showing:
- L1 structure scores (8 skills)
- L2 deltas (3 verified behavioral skills)
- Anti-pattern counts colored by severity
