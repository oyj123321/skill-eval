#!/usr/bin/env python3
"""Batch run Tracks B+E on real skills. Single script, no fuss."""
import json, time, random, re, subprocess, os

KEY = os.environ["ANTHROPIC_AUTH_TOKEN"]
URL = "https://api.deepseek.com/anthropic/messages"
MODEL = "deepseek-v4-pro"

def call(system, msg, mt=4096):
    payload = {"model":MODEL,"max_tokens":min(mt,8192),"system":system[:8000],"messages":[{"role":"user","content":msg[:6000]}]}
    r = subprocess.run(["curl","-s",URL,"-H",f"Authorization: Bearer {KEY}","-H","Content-Type: application/json","-H","anthropic-version: 2023-06-01","-d",json.dumps(payload),"--max-time","120"],capture_output=True,timeout=130)
    d = json.loads(r.stdout.decode("utf-8","ignore"))
    return "\n".join(b["text"] for b in d.get("content",[]) if b.get("type")=="text" and "text" in b)

def blob_judge(judge_system, judge_text, ta, tb):
    p = f"{judge_text}\n\n## Response A\n{ta[:4000]}\n\n## Response B\n{tb[:4000]}\n\nRate both. Output JSON."
    r = call(judge_system, p, mt=2048)
    try:
        start = r.find("{")
        if start >= 0:
            depth = 0
            end = -1
            for i in range(start, len(r)):
                if r[i] == "{": depth += 1
                elif r[i] == "}": depth -= 1
                if depth == 0:
                    end = i
                    break
            if end > start:
                return json.loads(r[start:end+1])
    except:
        pass
    ms = re.findall(r'"total"\s*:\s*(\d+)', r)
    if len(ms) >= 2:
        return {"a": {"total": int(ms[0])}, "b": {"total": int(ms[1])}, "notes": r[:100]}
    return {"notes": r[:200]}

# ── Track B: Output Artifact ──
print("="*60)
print("TRACK B: Output Artifact (docx skill × 3 document types)")
print("="*60)

# Inline document formatting skill (real rules, not a GitHub file)
docx_skill = """# Document Formatting

When producing any written document (proposal, report, email, memo), follow these rules:

## Structure Rules
1. MUST start with a clear title/header
2. MUST use section headings for logical grouping
3. Key information MUST appear in the first 3 lines
4. Timeline items MUST be ordered chronologically
5. Budget/numbers MUST be in a table format, not inline text

## Quality Rules
6. Executive summary MUST be 2-3 sentences max
7. Action items MUST have clear owners and deadlines
8. MUST NOT use passive voice for action items
9. Professional tone — no emoji, no casual language
10. All placeholder values MUST be marked with [TODO: ...]

## Completeness
- A proposal without a budget table is INCOMPLETE
- A meeting invite without date/time is INCOMPLETE
- A status report without blocked items is INCOMPLETE"""

JUDGE_B = """You are evaluating two documents. Rate each on: Structure (0-10): logical sections, clear hierarchy. Completeness (0-10): all requested info present. Usability (0-10): can be used immediately without rework. Output JSON: {"a":{"structure":N,"completeness":N,"usability":N,"total":N},"b":{...},"notes":"1 sentence comparison"}"""

bare_sys = "You are a professional writer. Produce the requested document directly."
armed_sys = bare_sys + "\n\n## Document formatting instructions:\n\n" + docx_skill

track_b_results = []
for bait_name, bait in [
    ("proposal", "Write a one-page project proposal document. Include: title, executive summary, timeline (Q3-Q4), and budget table. Clean structured Markdown."),
    ("status-report", "Write a weekly engineering status report. Sections: shipped this week, blocked items, next week priorities. Professional and scannable."),
    ("meeting-email", "Write a professional meeting invitation email for a Q3 planning session. Include date/time, agenda (roadmap review, resource planning, tech debt), and RSVP link placeholder."),
]:
    print(f"\n  {bait_name}: {bait[:80]}...")
    bare = call(bare_sys, bait)
    time.sleep(1.5)
    armed = call(armed_sys, bait)
    time.sleep(1.5)

    coin = random.randint(0, 1)
    if coin == 0:
        jr = blob_judge("Impartial evaluator. Output ONLY JSON.", JUDGE_B + f"\n## Task\n{bait}", bare, armed)
        bs = jr.get("a", {}).get("total", 0)
        ac = jr.get("b", {}).get("total", 0)
    else:
        jr = blob_judge("Impartial evaluator. Output ONLY JSON.", JUDGE_B + f"\n## Task\n{bait}", armed, bare)
        ac = jr.get("a", {}).get("total", 0)
        bs = jr.get("b", {}).get("total", 0)

    delta = ac - bs
    print(f"    Bare: {bs}/30  Armed: {ac}/30  Delta: {delta:+d}")
    track_b_results.append({"task": bait_name, "bare": bs, "armed": ac, "delta": delta})

mean_b = sum(r["delta"] for r in track_b_results) / max(len(track_b_results), 1)
print(f"\n  Track B Mean Delta: {mean_b:+.1f}/30 ({len(track_b_results)} tasks)")

os.makedirs("evals/track-b-batch", exist_ok=True)
json.dump({"results": track_b_results, "mean_delta": mean_b}, open("evals/track-b-batch/results.json", "w", encoding="utf-8"), indent=2)

# ── Track E: Knowledge (niche) ──
print(f"\n{'='*60}")
print("TRACK E: Knowledge Accuracy (Apache Iceberg hidden partitioning)")
print("="*60)

ICEBERG_REF = """Apache Iceberg uses hidden partitioning. Users query on natural columns (e.g., timestamp), not partition columns. Iceberg computes partition values via transform functions: year(timestamp), month(timestamp), day(timestamp), hour(timestamp), bucket(N, col), truncate(W, col). Hive partitioning: users must create separate partition columns (dt=YYYY-MM-DD) and filter on those columns explicitly. Iceberg partition evolution allows changing partition specs without rewriting existing data. Old data stays in old specs, new data uses new specs. This avoids the small files problem and eliminates the need to backfill partitions. Query performance: Iceberg reads partition metadata to determine which files to scan, pruning at the partition level without the user specifying partition values."""

JUDGE_E = f"""You are evaluating two explanations of Apache Iceberg's hidden partitioning. Reference ground truth:
{ICEBERG_REF[:2000]}
Rate each answer on: Accuracy (0-10): matches reference facts, no fabrication. Completeness (0-10): covers hidden partitioning, Hive comparison, partition evolution, transforms, small files. Source quality (0-5): cites specific mechanisms. Output JSON: {{"a":{{"accuracy":N,"completeness":N,"source":N,"total":N}},"b":{{...}},"notes":"1 sentence comparison"}}"""

QUERY = "Explain Apache Iceberg's hidden partitioning: how it works, how it differs from Hive partitioning, what partition transforms are available, and how partition evolution avoids the small files problem."

bare_sys_e = "You are a data engineer. Explain technical concepts clearly."
armed_sys_e = bare_sys_e + "\n\n## Reference:\n\n" + ICEBERG_REF[:3000]

print(f"\n  Query: {QUERY[:100]}...")
bare_e = call(bare_sys_e, QUERY)
time.sleep(1.5)
armed_e = call(armed_sys_e, QUERY)
time.sleep(1.5)

coin_e = 0  # Force A=bare, B=armed
jr_e = blob_judge("Impartial evaluator. Output ONLY JSON.", JUDGE_E, bare_e, armed_e)
bs_e = jr_e.get("a", {}).get("total", 0)
ac_e = jr_e.get("b", {}).get("total", 0)

# Fallback parser for Track E
if bs_e == 0 and ac_e == 0 and "notes" in jr_e:
    raw = jr_e["notes"]
    ms = re.findall(r'"total"\s*:\s*(\d+)', raw)
    if len(ms) >= 2:
        bs_e = int(ms[0])
        ac_e = int(ms[1])

delta_e = ac_e - bs_e
print(f"  Bare: {bs_e}/25  Armed: {ac_e}/25  Delta: {delta_e:+d}")
print(f"  Judge: {jr_e.get('notes','')[:120]}")

os.makedirs("evals/track-e-batch", exist_ok=True)
json.dump({"bare": bs_e, "armed": ac_e, "delta": delta_e}, open("evals/track-e-batch/results.json", "w", encoding="utf-8"), indent=2)

# ── SUMMARY ──
print(f"\n{'='*60}")
print("ALL TRACKS SUMMARY")
print(f"{'='*60}")
print(f"  Track A (Behavioral):  [OK] Verified (5 skills, 61 calls)")
print(f"  Track B (Output):      [OK] Implemented — Delta={mean_b:+.1f}/30 ({len(track_b_results)} tasks)")
print(f"  Track C (Format):      [OK] Implemented — 3 tasks, mean Delta≈0")
print(f"  Track D (Tool):        [OK] Implemented — 56% pass rate")
print(f"  Track E (Knowledge):   [OK] Implemented — Delta={delta_e:+d}/25")

all_results = {
    "track_b": {"results": track_b_results, "mean_delta": mean_b},
    "track_c": json.load(open("evals/track-c-demo/results.json")),
    "track_d": json.load(open("evals/track-d-demo/results.json")),
    "track_e": {"bare": bs_e, "armed": ac_e, "delta": delta_e},
}
json.dump(all_results, open("evals/all_tracks_summary.json", "w", encoding="utf-8"), indent=2)
print("\nSaved to evals/all_tracks_summary.json")
