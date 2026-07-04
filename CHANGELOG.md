# Changelog

## [0.3.0] — 2026-07-04

### Added
- L0: Skill type classifier (5-track: Behavioral/Output/Format/Tool/Knowledge)
- Track B design: Output artifact evaluation (judge the file, not the conversation)
- Track C design: Format compliance evaluation (auto-lint + trade-off analysis)
- Track D design: Tool correctness evaluation (execute + measure)
- Track E design: Knowledge accuracy evaluation (accuracy/completeness/source traceability)
- Multi-track skill support (single skill can span multiple tracks)
- `layers/classifier.md`: classification signals + algorithm
- `layers/track-output.md`, `layers/track-format.md`, `layers/track-tool.md`, `layers/track-knowledge.md`: full design docs

## [0.2.0] — 2026-07-04

### Added
- API-based L2 with TOOLS (grep, glob, read + agent loop + simulated project FS)
- Tool gap resolution: behavioral delta now measures execution, not just intention

### Fixed
- DeepSeek API response parsing (thinking blocks, dual text format)
- Judge JSON extraction with regex fallback

## [0.1.0] — 2026-07-04

### Added
- L1: Structural compliance (skill-kit 21 checks + 11 anti-patterns)
- L2 Track A: Behavioral delta (API-based A/B, blind judge, 5-dim rubric)
- Task generation protocol: MUST/MUST NOT → bait tasks
- Meta-contamination isolation: skill-eval runs in control plane, not in evaluated sessions
- 3-dim scoring: structural + behavioral_delta + cost
- Dogfood evaluation of eight-principles skill
