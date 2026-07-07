#!/usr/bin/env python3
"""Track C: Format Compliance. Give a format spec + bait task → measure format adherence rate."""
import json, os, sys, time, re, random, subprocess

API_KEY = os.environ.get("ANTHROPIC_AUTH_TOKEN","")
MODEL   = os.environ.get("ANTHROPIC_MODEL","deepseek-v4-pro")
URL     = "https://api.deepseek.com/anthropic/messages"

def call(system, msg, mt=4096):
    payload = {"model":MODEL,"max_tokens":min(mt,8192),"system":system[:8000],"messages":[{"role":"user","content":msg[:6000]}]}
    r = subprocess.run(["curl","-s",URL,"-H",f"Authorization: Bearer {API_KEY}","-H","Content-Type: application/json","-H","anthropic-version: 2023-06-01","-d",json.dumps(payload),"--max-time","120"],capture_output=True,timeout=130)
    d = json.loads(r.stdout.decode('utf-8','ignore'))
    return "\n".join(b["text"] for b in d.get("content",[]) if b.get("type")=="text" and "text" in b)

def judge_format(task, rules, ta, tb):
    p = f"""## Format Rules
{rules}

## Task
{task}

## Response A
{ta[:5000]}

## Response B
{tb[:5000]}

Rate each response. Format adherence (0-5): does it follow every rule? Content quality (0-5): is the information good? Trade-off (0-10): overall, which is better considering format constraints? Output JSON: {{"a":{{"format":N,"content":N,"overall":N}},"b":{{...}},"notes":"..."}}"""
    r = call("You are an impartial format evaluator. Output ONLY JSON.", p, mt=2048)
    try:
        start = r.find('{'); depth = 0; end = -1
        for i in range(start, len(r)):
            if r[i]=='{': depth+=1
            elif r[i]=='}': depth-=1
            if depth==0: end=i; break
        if end>start: return json.loads(r[start:end+1])
    except: pass
    return {"notes":r[:200]}

# ── Track C Demo: commit-message-format skill ──
FORMAT_SKILL = """# Commit Message Format

All commit messages MUST follow the conventional commits format:
- Structure: `<type>(<scope>): <description>`
- Types: feat, fix, docs, style, refactor, test, chore
- Scope is optional but recommended
- Description MUST be lowercase, no period at end
- Body MUST be separated by blank line
- Breaking changes MUST include `BREAKING CHANGE:` in body
- MUST NOT use generic descriptions like "updates", "fixes", "changes"
"""

BAITS = [
    "Write a commit message for: I fixed a bug in the user login where passwords with special characters caused a 500 error. The fix validates and sanitizes input before hashing.",
    "Write a commit message for: I added pagination to the search results API. The default page size is 20, with a max of 100. Includes new query params `page` and `limit`.",
    "Write a commit message for: I restructured the database module — split the monolithic db.js into separate files for connections, queries, migrations. No behavior changes."
]

bare_sys = "You are a software developer. Write the requested commit message."
armed_sys = bare_sys + "\n\n## Commit Message Rules:\n\n" + FORMAT_SKILL

results = []
for i, bait in enumerate(BAITS):
    print(f"Task {i+1}: {bait[:80]}...")
    bare = call(bare_sys, bait)
    time.sleep(1.5)
    armed = call(armed_sys, bait)
    time.sleep(1.5)

    coin = random.randint(0,1)
    if coin==0:
        jr = judge_format(bait, FORMAT_SKILL[:2000], bare, armed)
        bs = jr.get("a",{}).get("overall",0); ac = jr.get("b",{}).get("overall",0)
    else:
        jr = judge_format(bait, FORMAT_SKILL[:2000], armed, bare)
        ac = jr.get("a",{}).get("overall",0); bs = jr.get("b",{}).get("overall",0)

    delta = ac - bs
    print(f"  Bare: {bs}/10  Armed: {ac}/10  Delta: {delta:+d}  |  {jr.get('notes','')[:120]}")
    results.append({"task":i+1,"bare_score":bs,"armed_score":ac,"delta":delta})

print(f"\nTrack C: Mean Delta = {sum(r['delta'] for r in results)/len(results):+.1f}/10")

os.makedirs("evals/track-c-demo", exist_ok=True)
json.dump(results, open("evals/track-c-demo/results.json","w",encoding="utf-8"), indent=2)
print("Saved to evals/track-c-demo/results.json")
