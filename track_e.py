#!/usr/bin/env python3
"""skill-eval Track E: Knowledge Accuracy Evaluation.
Tests whether a knowledge/reference skill improves factual accuracy and completeness.
Usage: python track_e.py --skill-md <path> --name <n> --query "<q>" --reference "<known facts>"
"""
import json, os, sys, time, re, random, subprocess, argparse

API_KEY = os.environ.get("ANTHROPIC_AUTH_TOKEN","")
API_URL = os.environ.get("ANTHROPIC_BASE_URL","https://api.anthropic.com/v1")
MODEL   = os.environ.get("ANTHROPIC_MODEL","claude-sonnet-4-6")
BASE = API_URL.rstrip("/")
MESSAGES_URL = f"{BASE}/messages" if ("/anthropic" in BASE or "/v1" in BASE) else f"{BASE}/v1/messages"

KNOWLEDGE_JUDGE = """You are evaluating whether an AI assistant's answer to a knowledge question is accurate, complete, and well-sourced. Rate on 5 dimensions (0-10 each).

Reference information (ground truth):
{reference}

1. Accuracy (0-10): Every factual claim matches the reference. Penalize fabricated claims heavily.
2. Completeness (0-10): All relevant reference information surfaced. Nothing critical omitted.
3. Source Traceability (0-10): Claims cite specific sections/files from the provided knowledge base.
4. Confidence Calibration (0-10): Overconfident on missing info = bad. Over-cautious on known info = also bad. Calibrated uncertainty matters.
5. Synthesis (0-10): Synthesized across multiple knowledge sources into a coherent answer, not copy-pasted.

Output ONLY valid JSON: {"response_a":{"accuracy":N,"completeness":N,"traceability":N,"confidence":N,"synthesis":N,"total":N},"response_b":{...},"notes":"1 sentence comparison"}"""

def api_call(system, msg, mt=4096):
    payload = {"model":MODEL,"max_tokens":min(mt,8192),"system":system[:8000],"messages":[{"role":"user","content":msg[:12000]}]}
    r = subprocess.run(["curl","-s",MESSAGES_URL,"-H",f"Authorization: Bearer {API_KEY}","-H","Content-Type: application/json","-H","anthropic-version: 2023-06-01","-d",json.dumps(payload),"--max-time","120"], capture_output=True, timeout=130)
    out = r.stdout.decode('utf-8','ignore')
    if not out.strip(): return "EMPTY"
    try:
        d = json.loads(out)
        texts = [b["text"] for b in d.get("content",[]) if b.get("type")=="text" and "text" in b]
        # Also check for thinking (some models output thinking only when the prompt is complex)
        thinkings = [b.get("thinking","") for b in d.get("content",[]) if b.get("type")=="thinking"]
        result = "\n".join(texts)
        if not result.strip() and thinkings:
            result = thinkings[-1]  # last thinking block might contain the answer
        return result if result.strip() else f"EMPTY_TEXT (content_blocks={len(d.get('content',[]))})"
    except Exception as e:
        return f"PARSE:{out[:200]} err={e}"

def judge(reference, task, ta, tb):
    p = KNOWLEDGE_JUDGE.replace("{reference}", reference[:3000])
    p += f"\n\n## Question\n{task}\n\n## Answer A\n{ta[:5000]}\n\n## Answer B\n{tb[:5000]}\n\nRate each on 5 dimensions. Output JSON."
    r = api_call("You are an impartial evaluator. Output ONLY valid JSON.", p, mt=2048)
    # Debug: print first 300 chars of judge response
    if r and not r.startswith("PARSE"):
        print(f"   [Judge raw: {r[:150]}...]")
    try:
        start = r.find('{')
        if start >= 0:
            depth, end = 0, -1
            for i in range(start, len(r)):
                if r[i]=='{': depth+=1
                elif r[i]=='}': depth-=1
                if depth==0: end=i; break
            if end>start:
                obj = json.loads(r[start:end+1])
                if "response_a" in obj:
                    return obj
    except Exception as e:
        print(f"   [Judge parse error: {e}]")
    return {"raw":r[:500] if r else "EMPTY","error":"parse"}

if __name__=="__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--skill-md", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--query", required=True)
    p.add_argument("--reference", required=True, help="Ground truth facts")
    args = p.parse_args()

    skill_body = open(args.skill_md,encoding="utf-8").read()
    if skill_body.startswith("---"):
        parts = skill_body.split("---",2)
        skill_body = parts[-1].strip() if len(parts)>=3 else skill_body
    if len(skill_body)>4000: skill_body = skill_body[:4000] + "\n[...truncated]"

    bare = "You are an AI assistant. Answer the user's question directly using your general knowledge."
    armed = bare + "\n\n## Reference knowledge:\n\n" + skill_body

    print(f"Track E — {args.name}")
    print(f"Query: {args.query[:120]}...")

    print("-> Bare (general knowledge)...")
    bare_ans = api_call(bare, args.query)
    print(f"   {len(bare_ans)} chars")
    time.sleep(1.5)

    print("-> Armed (with reference)...")
    armed_ans = api_call(armed, args.query)
    print(f"   {len(armed_ans)} chars")
    time.sleep(1.5)

    coin = random.randint(0,1)
    if coin==0:
        jr = judge(args.reference, args.query, bare_ans, armed_ans)
        bs = jr.get("response_a",{}).get("total",0)
        ac = jr.get("response_b",{}).get("total",0)
    else:
        jr = judge(args.reference, args.query, armed_ans, bare_ans)
        ac = jr.get("response_a",{}).get("total",0)
        bs = jr.get("response_b",{}).get("total",0)

    # Fallback: if brace-counting failed, try regex
    if bs==0 and ac==0 and "raw" in jr:
        raw = jr["raw"]
        ms = re.findall(r'"total"\s*:\s*(\d+)', raw)
        if len(ms)>=2:
            bs2, ac2 = int(ms[0]), int(ms[1])
            if coin==1: bs2, ac2 = ac2, bs2
            bs, ac = bs2, ac2

    delta = ac - bs
    print(f"Bare: {bs}/50 | Armed: {ac}/50 | Delta: {delta:+d}")
    notes = jr.get('notes','')
    if not notes: notes = jr.get('raw','')[:150]
    print(f"Judge: {notes}")

    res = {"track":"E","skill":args.name,"bare_score":bs,"armed_score":ac,"delta":delta,"notes":jr.get("notes","")}
    os.makedirs(f"evals/{args.name}", exist_ok=True)
    with open(f"evals/{args.name}/track_e.json","w",encoding="utf-8") as f:
        json.dump(res,f,indent=2,ensure_ascii=False)
    print(f"Saved to evals/{args.name}/track_e.json")
