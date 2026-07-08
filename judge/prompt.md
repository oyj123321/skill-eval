# Judge Prompt — Behavioral Delta Evaluation

## Template

Replace `{TRANSCRIPT_A}`, `{TRANSCRIPT_B}`, and `{TASK_DESCRIPTION}` before use.

```
You are an impartial evaluator. Your job is to compare two responses from an AI
coding assistant and rate each on 6 dimensions (5 quality dimensions + 1 confidence).

## The Task

{TASK_DESCRIPTION}

## Response A

{TRANSCRIPT_A}

## Response B

{TRANSCRIPT_B}

## Instructions

Rate Response A and Response B separately on each of the 6 dimensions below.
Use the full 0-10 scale — don't cluster around 5.

### Dimension 1: Rigor (0-10)
Depth and correctness of reasoning.
- 0: Surface-level, no reasoning steps shown
- 5: Adequate reasoning but misses important edge cases
- 10: Thorough, multi-step reasoning that anticipates edge cases

### Dimension 2: Evidence (0-10)
Concrete, sourced proof — not bare assertion.
- 0: Pure assertion with no support ("X is true because I say so")
- 5: Some evidence but incomplete ("X might be true, see this one example")
- 10: Verifiable claims backed by specific sources, citations, or code references

### Dimension 3: Actionability (0-10)
A clear, falsifiable next step the user can act on.
- 0: Vague or no actionable output ("You should think about this more")
- 5: Suggests a general direction but no concrete step
- 10: Specifies exact commands, file paths, or API calls; user can act immediately

### Dimension 4: Risk-awareness (0-10)
Surfaces real risks — legal, adoption, competition, economic, technical.
- 0: Ignores risks entirely; only mentions positives
- 5: Flags one risk category but misses others
- 10: Comprehensive risk analysis across multiple categories with mitigation suggestions

### Dimension 5: Signal-to-noise (0-10)
Insight per line — scaffolding, filler, or repetition counts against.
- 0: Mostly boilerplate, introductions, summaries, "let me know if..."
- 5: Mix of substance and filler; about 50/50
- 10: Dense with insight; every line carries information; no filler

### Dimension 6: Confidence (0-10) — NEW
How confident are you in this score? This is NOT about the response quality — it's about how certain your own judgment is.
- 0: Not confident at all. The response is ambiguous or could be scored completely differently by another judge.
- 3: Low confidence. Multiple reasonable interpretations possible.
- 5: Moderate confidence. Clear direction but debatable specifics.
- 8: High confidence. Strong signal, minor room for interpretation.
- 10: Certain. The response unambiguously hits every anchor on this dimension.

## Examples of False Positives

Before finalizing your scores, check against these common false-positive patterns:

- **Brevity ≠ low quality.** A shorter response that directly answers the question is not worse than a longer one. Do not penalize conciseness.
- **Tool calls without results ≠ incompetence.** If the environment lacks tools (grep, read), a response that tries to search but can't is demonstrating the right intent. Judge the intent, not the tool availability.
- **Tone differences ≠ quality differences.** A casual tone is not worse than a formal one. Judge substance, not style.
- **Pre-existing patterns ≠ skill effect.** If both responses do the same good thing (e.g., both use conventional commit format), the skill didn't help but it also didn't hurt. Score both fairly.
- **Confidence in wrong answer ≠ good answer.** A response that is confidently wrong scores 0 on Rigor regardless of how authoritative it sounds. Fabrication is fabrication.

## Output Format

Respond with ONLY this JSON structure (no other text):

{
  "response_a": {
    "rigor": <0-10>,
    "evidence": <0-10>,
    "actionability": <0-10>,
    "risk_awareness": <0-10>,
    "signal_to_noise": <0-10>,
    "confidence": <0-10>,
    "total": <sum of first 5 dimensions, 0-50>
  },
  "response_b": {
    "rigor": <0-10>,
    "evidence": <0-10>,
    "actionability": <0-10>,
    "risk_awareness": <0-10>,
    "signal_to_noise": <0-10>,
    "confidence": <0-10>,
    "total": <sum of first 5 dimensions, 0-50>
  },
  "notes": "<1 sentence comparison: which was better and why, or 'comparable'>"
}
```

## Design Notes

The 6-dimension rubric is inspired by Anthropic's official code-review plugin architecture
(parallel multi-agent → adversarial verification → confidence filter), adapted for skill evaluation:

- Dimensions 1-5 measure response quality (WHAT changed)
- Dimension 6 measures judgment certainty (HOW sure are we)
- The "Examples of False Positives" section is a direct adaptation of code-review's
  false-positive guard — it catches the most common judge errors we observed in
  157+ real API evaluations (brevity penalty, tool-gap penalty, tone bias)
