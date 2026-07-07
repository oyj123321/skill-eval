#!/usr/bin/env python3
"""skill-eval Track B: Output Artifact Evaluation.
Same protocol as Track A, different judge rubric.
Track A judges TRANSCRIPTS (rigor/evidence/actionability/risk/signal-to-noise).
Track B judges OUTPUT ARTIFACTS (structure/visual/completeness/usability/professionalism).
Usage: python track_b.py --skill-md <path> --name <n> --bait "<prompt>" --description "<d>"
"""
import json, os, sys, time, re, random, subprocess, argparse

API_KEY = os.environ.get("ANTHROPIC_AUTH_TOKEN","")
API_URL = os.environ.get("ANTHROPIC_BASE_URL","https://api.anthropic.com/v1")
MODEL   = os.environ.get("ANTHROPIC_MODEL","claude-sonnet-4-6")
BASE = API_URL.rstrip("/")
MESSAGES_URL = f"{BASE}/messages" if ("/anthropic" in BASE or "/v1" in BASE) else f"{BASE}/v1/messages"

# ── TRACK B JUDGE ──
ARTIFACT_JUDGE = """You are evaluating two output artifacts (files, documents, presentations, UI components) created by an AI assistant. Rate each on 5 dimensions (0-10 each). Use the full scale.

1. Structure (0-10): Clear information architecture, logical flow, good use of sections/headings/hierarchy
2. Visual/Layout Quality (0-10): Appropriate use of layout, spacing, visual hierarchy, formatting (whether in code, markdown, or described design)
3. Completeness (0-10): All key information present, nothing critical missing, deliverable is ready to use
4. Usability (0-10): Receiver can use this immediately without major rework or clarification
5. Professionalism (0-10): Matches professional standards for this type of deliverable

Output ONLY valid JSON: {"response_a":{"structure":N,"visual":N,"completeness":N,"usability":N,"professionalism":N,"total":N},"response_b":{...},"notes":"1 sentence comparison"}"""

# ── REUSE Track A's API infra ──
TOOLS = [
    {"name":"grep","description":"Search for a pattern","input_schema":{"type":"object","properties":{"pattern":{"type":"string"},"path":{"type":"string","default":"."}},"required":["pattern"]}},
    {"name":"glob","description":"Find files","input_schema":{"type":"object","properties":{"pattern":{"type":"string"}},"required":["pattern"]}},
    {"name":"read","description":"Read file","input_schema":{"type":"object","properties":{"file_path":{"type":"string"}},"required":["file_path"]}}
]

def fake_tool(name, inp):
    if name=="grep": return f"Found 3 matches for '{inp.get('pattern','')}'"
    elif name=="glob": return "slide-1.md\nslide-2.md\nslide-3.md\ntemplate.pptx"
    elif name=="read": return f"// Content of {inp.get('file_path','')}\n// Standard project file"
    return "unknown"

def api_call(system, msg, mt=4096):
    payload = {"model":MODEL,"max_tokens":mt,"system":system,"messages":[{"role":"user","content":msg}]}
    r = subprocess.run(["curl","-s",MESSAGES_URL,"-H",f"Authorization: Bearer {API_KEY}","-H","Content-Type: application/json","-H","anthropic-version: 2023-06-01","-d",json.dumps(payload),"--max-time","120"], capture_output=True, timeout=130)
    try:
        d = json.loads(r.stdout.decode('utf-8','ignore'))
        return "\n".join(b["text"] for b in d.get("content",[]) if b.get("type")=="text" and "text" in b)
    except: return f"PARSE:{r.stdout[:200]}"

def api_with_tools(system, msg, mt=4):
    transcript, messages = [], [{"role":"user","content":msg}]
    for _ in range(mt):
        payload = {"model":MODEL,"max_tokens":4096,"system":system,"tools":TOOLS,"messages":messages}
        r = subprocess.run(["curl","-s",MESSAGES_URL,"-H",f"Authorization: Bearer {API_KEY}","-H","Content-Type: application/json","-H","anthropic-version: 2023-06-01","-d",json.dumps(payload),"--max-time","120"], capture_output=True, timeout=130)
        try: d = json.loads(r.stdout.decode('utf-8','ignore'))
        except: break
        texts = [b["text"] for b in d.get("content",[]) if b.get("type")=="text" and "text" in b]
        tcs = [(b["id"],b["name"],b.get("input",{})) for b in d.get("content",[]) if b.get("type")=="tool_use"]
        transcript.append("\n".join(texts) if texts else "")
        if not tcs: break
        results = []
        for tid,tn,ti in tcs:
            res = fake_tool(tn, ti)
            transcript.append(f"[TOOL {tn}: {res[:200]}]")
            results.append({"type":"tool_result","tool_use_id":tid,"content":res})
        messages.append({"role":"assistant","content":d.get("content",[])})
        messages.append({"role":"user","content":results})
        time.sleep(1)
    return "\n".join(transcript)

def artifact_judge(task_desc, ta, tb):
    p = f"## Task\n{task_desc}\n\n## Artifact A\n{ta[:6000]}\n\n## Artifact B\n{tb[:6000]}\n\nRate each artifact on 5 dimensions. Output JSON."
    r = api_call(ARTIFACT_JUDGE, p, mt=2048)
    try:
        start = r.find('{')
        if start >= 0:
            depth, end = 0, -1
            for i in range(start, len(r)):
                if r[i]=='{': depth+=1
                elif r[i]=='}':
                    depth-=1
                    if depth==0: end=i; break
            if end>start: return json.loads(r[start:end+1])
    except: pass
    return {"raw":r[:300],"error":"parse"}

# ── MAIN ──
if __name__=="__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--skill-md", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--bait", required=True)
    p.add_argument("--description", required=True)
    args = p.parse_args()

    skill_body = open(args.skill_md,encoding="utf-8").read()
    if skill_body.startswith("---"):
        parts = skill_body.split("---",2)
        skill_body = parts[-1].strip() if len(parts)>=3 else skill_body
    if len(skill_body)>4000: skill_body = skill_body[:4000] + "\n[...truncated]"

    bare = "You are an AI assistant. You have tools for reading and searching files. Produce the requested deliverable directly."
    armed = bare + "\n\n## Skill instructions:\n\n" + skill_body

    print(f"Track B — {args.name}")
    print(f"Bait: {args.bait[:120]}...")

    print("-> Bare...")
    bare_out = api_with_tools(bare, args.bait)
    print(f"   {len(bare_out)} chars")
    time.sleep(1.5)

    print("-> Armed...")
    armed_out = api_with_tools(armed, args.bait)
    print(f"   {len(armed_out)} chars")
    time.sleep(1.5)

    coin = random.randint(0,1)
    if coin==0:
        jr = artifact_judge(args.description, bare_out, armed_out)
        bs = jr.get("response_a",{}).get("total",0)
        ac = jr.get("response_b",{}).get("total",0)
    else:
        jr = artifact_judge(args.description, armed_out, bare_out)
        ac = jr.get("response_a",{}).get("total",0)
        bs = jr.get("response_b",{}).get("total",0)

    delta = ac - bs
    print(f"Bare: {bs}/50 | Armed: {ac}/50 | Delta: {delta:+d}")
    print(f"Judge: {jr.get('notes','')[:200]}")

    res = {"track":"B","skill":args.name,"bare_score":bs,"armed_score":ac,"delta":delta,"notes":jr.get("notes","")}
    os.makedirs(f"evals/{args.name}", exist_ok=True)
    with open(f"evals/{args.name}/track_b.json","w",encoding="utf-8") as f:
        json.dump(res,f,indent=2,ensure_ascii=False)
    print(f"Saved to evals/{args.name}/track_b.json")
