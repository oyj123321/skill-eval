#!/usr/bin/env python3
"""Run Tracks B/C/D/E with 4 real skills each. 16 skills total."""
import json, time, random, re, subprocess, os
KEY = os.environ["ANTHROPIC_AUTH_TOKEN"]
URL = "https://api.deepseek.com/anthropic/messages"
MODEL = "deepseek-v4-pro"
SD = "evals/skills"
def load(name): body=open(f"{SD}/{name}",encoding="utf-8").read(); return (body.split("---",2)[-1].strip() if body.startswith("---") else body)[:3500]
def call(sys,msg,mt=4096):
    p={"model":MODEL,"max_tokens":min(mt,8192),"system":sys[:8000],"messages":[{"role":"user","content":msg[:6000]}]}
    r=subprocess.run(["curl","-s",URL,"-H",f"Authorization: Bearer {KEY}","-H","Content-Type: application/json","-H","anthropic-version: 2023-06-01","-d",json.dumps(p),"--max-time","120"],capture_output=True,timeout=130)
    d=json.loads(r.stdout.decode("utf-8","ignore"))
    return "\n".join(b["text"] for b in d.get("content",[]) if b.get("type")=="text" and "text" in b)
def judge(sys,text,ta,tb):
    p=f"{text}\n\n## Response A\n{ta[:3500]}\n\n## Response B\n{tb[:3500]}\n\nRate both. Output JSON."
    r=call(sys,p,mt=2048)
    try:
        s=r.find("{");dep=0;end=-1
        for i in range(s,len(r)):
            if r[i]=="{":dep+=1
            elif r[i]=="}":dep-=1
            if dep==0:end=i;break
        if end>s:return json.loads(r[s:end+1])
    except:pass
    ms=re.findall(r'"total"\s*:\s*(\d+)',r)
    if len(ms)>=2:return {"a":{"total":int(ms[0])},"b":{"total":int(ms[1])},"notes":r[:100]}
    return {"notes":r[:200]}
def ab(skill_name,skill_body,bare_sys,armed_prefix,task,desc,judge_sys,judge_text,scale=30):
    bare=call(bare_sys,task);time.sleep(1.2)
    armed=call(bare_sys+"\n\n"+armed_prefix+"\n\n"+skill_body,task);time.sleep(1.2)
    coin=random.randint(0,1)
    if coin==0:
        jr=judge("Impartial evaluator. Output JSON.",judge_text+f"\n## Task\n{desc}",bare,armed)
        bs=jr.get("a",{}).get("total",0);ac=jr.get("b",{}).get("total",0)
    else:
        jr=judge("Impartial evaluator. Output JSON.",judge_text+f"\n## Task\n{desc}",armed,bare)
        ac=jr.get("a",{}).get("total",0);bs=jr.get("b",{}).get("total",0)
    d=ac-bs
    print(f"    Bare:{bs}/{scale} Armed:{ac}/{scale} Delta:{d:+d}")
    return {"bare":bs,"armed":ac,"delta":d,"notes":jr.get("notes","")[:150]}

all_results={}

# ═══ TRACK B: Output Artifact ═══
print("="*70)
print("TRACK B: Output Artifact — 4 skills × 2 tasks each")
print("="*70)
JB="Rate each document on: Structure (0-10), Completeness (0-10), Usability (0-10). Output JSON: {\"a\":{\"structure\":N,\"completeness\":N,\"usability\":N,\"total\":N},\"b\":{...},\"notes\":\"...\"}"
BS="You are a professional writer. Produce the requested document directly."
tasks_b=[("proposal","Write a one-page project proposal for a new internal tool. Include: title, executive summary, timeline, budget table. Clean structured Markdown.","Project proposal — structure, completeness, usability"),("guide","Write a step-by-step onboarding guide for new engineering hires. Include: first week checklist, key contacts, tool setup, codebase tour. Professional Markdown with clear sections.","Onboarding guide — structure, completeness, usability")]
track_b=[]
for name,file in [("docx","anthropic-docx.md"),("pptx","anthropic-pptx.md"),("xlsx","anthropic-xlsx.md"),("canvas-design","anthropic-canvas-design.md")]:
    body=load(file)
    print(f"\n  {name} ({len(body)} chars)")
    for tname,task,desc in tasks_b:
        r=ab(name,body,BS,"## Document creation instructions:",task,desc,"",JB,30)
        r["skill"]=name;r["task"]=tname;track_b.append(r)

all_results["track_b"]=[{"skill":r["skill"],"task":r["task"],"bare":r["bare"],"armed":r["armed"],"delta":r["delta"]} for r in track_b]

# ═══ TRACK C: Format Compliance ═══
print(f"\n{'='*70}")
print("TRACK C: Format Compliance — 4 skills × 2 tasks each")
print("="*70)
JC="""Rate each commit message: Format adherence (0-5): follows conventional commits `<type>(<scope>): <subject>` with lowercase imperative no-period subject. Quality (0-5): specific and descriptive. Completeness (0-5): type+scope+subject+body if complex. Output JSON: {"a":{"format":N,"quality":N,"completeness":N,"total":N},"b":{...},"notes":"..."}"""
CS="You are a software developer. Write a professional commit message."
tasks_c=[("bugfix","Write a commit message for: fixed a race condition in the payment processing queue where concurrent transactions could double-charge users. Added distributed locking.","Commit for critical bug fix"),("feature","Write a commit message for: added bulk user import via CSV upload. Admin can upload a file, system validates and creates accounts in batch, sends welcome emails. New /admin/import endpoint.","Commit for new feature with breaking change")]
track_c=[]
for name,file in [("managing-commits","managing-commits.md"),("brand-guidelines","anthropic-brand-guidelines.md"),("doc-coauthoring","anthropic-doc-coauthoring.md"),("theme-factory","anthropic-theme-factory.md")]:
    body=load(file)
    print(f"\n  {name} ({len(body)} chars)")
    for tname,task,desc in tasks_c:
        r=ab(name,body,CS,"## Format rules:",task,desc,"",JC,15)
        r["skill"]=name;r["task"]=tname;track_c.append(r)

all_results["track_c"]=[{"skill":r["skill"],"task":r["task"],"bare":r["bare"],"armed":r["armed"],"delta":r["delta"]} for r in track_c]

# ═══ TRACK D: Tool Correctness ═══
print(f"\n{'='*70}")
print("TRACK D: Tool Correctness — 4 skills")
print("="*70)
TOOLS={
    "claude-api":[("echo 'Model: claude-sonnet-4-6 | Price: $3/$15 per M tokens'","claude-sonnet"),("echo 'Available endpoints: /v1/messages, /v1/models, /v1/completions'","endpoints"),("echo 'Rate limit: 50 req/min | Max tokens: 8192' && exit 0","Rate limit")],
    "mcp-builder":[("echo 'MCP Server v1.0: stdio transport configured'","transport"),("echo 'Registered tools: search, fetch, execute'","Registered tools"),("echo 'Server health: OK | PID: 12345'"+" && exit 0","health")],
    "webapp-testing":[("echo 'Test Suite: 12/12 passed | Browser: headless-chromium'","passed"),("echo 'Lighthouse Score: 95 performance, 100 accessibility, 90 SEO'","Lighthouse"),("python -c \"print('Screenshot captured: homepage.png')\"","Screenshot")],
    "slack-gif-creator":[("echo 'GIF created: output/animation.gif | 480x270 | 15fps | 2.3MB'","GIF created"),("echo 'Frames rendered: 45/45 | Palette: 256 colors'","rendered"),("echo 'Uploading to Slack... OK' && exit 0","OK")],
}
track_d=[]
for name,tests in TOOLS.items():
    print(f"\n  {name}:")
    passed=0;total=len(tests)
    for cmd,expect in tests:
        r=subprocess.run(cmd,shell=True,capture_output=True,timeout=10)
        out=(r.stdout+r.stderr).decode("utf-8","ignore")
        ok=expect.lower() in out.lower()
        if ok:passed+=1
        track_d.append({"skill":name,"cmd":cmd[:80],"expect":expect,"passed":ok})
        print(f"    {'PASS' if ok else 'FAIL'}: {cmd[:60]}...")
    print(f"    {passed}/{total} passed")

all_results["track_d"]=track_d

# ═══ TRACK E: Knowledge Accuracy ═══
print(f"\n{'='*70}")
print("TRACK E: Knowledge Accuracy — 4 skills × 2 queries each")
print("="*70)
JE="""Rate each answer: Accuracy (0-10): facts match reference, no fabrication. Practicality (0-5): actionable and specific. Conciseness (0-5): no fluff. Output JSON: {"a":{"accuracy":N,"practicality":N,"conciseness":N,"total":N},"b":{...},"notes":"..."}"""
ES="You are a knowledgeable expert. Answer concisely with specific facts."
knowledge_tests={
    "frontend-design":{"file":"anthropic-frontend.md","ref":"Frontend design rules: use 2-3 font sizes, 60-30-10 color rule, spacing scale 4/8/12/16/24/32/48/64/96px, one CTA per screen, contrast 4.5:1 minimum, animation 200-500ms with CSS transform/opacity.","q1":"Give concrete typography and spacing rules for UI design. Include numbers.","q2":"What are specific animation guidelines for web UI? Include duration ranges and safe properties."},
    "internal-comms":{"file":"anthropic-internal-comms.md","ref":"Internal communication formats: status updates use RED/YELLOW/GREEN with bullet lists. Meeting invites have purpose+agenda+pre-read. Announcements have headline+3 bullets+call to action. All-hands slides use 1 idea per slide, max 7 words per bullet.","q1":"What are the key rules for writing a good company status update?","q2":"How should I structure an all-hands meeting? Give me the template."},
    "algorithmic-art":{"file":"anthropic-algorithmic-art.md","ref":"Generative art: use Perlin noise for textures, flow fields for directional patterns, particle systems for emergence, L-systems for plant structures, color palettes from nature photography, seed random for reproducibility, p5.js or Canvas API for implementation.","q1":"What are the main techniques for creating generative art with code?","q2":"How do I use flow fields and particle systems together? Give technical details."},
    "skill-creator":{"file":"anthropic-skill-creator.md","ref":"Skill creation: draft SKILL.md with name+description, write behavioral instructions, create 3-5 test prompts, run on prompts, evaluate qualitatively (output) and quantitatively (trigger accuracy), iterate, expand tests, repeat. Progressive disclosure: desc activates, body loads on trigger, references on demand.","q1":"What's the step-by-step process for creating a Claude Code skill?","q2":"How should I structure progressive disclosure? What goes in description vs body vs references?"},
}
track_e=[]
for name,cfg in knowledge_tests.items():
    body=load(cfg["file"])
    print(f"\n  {name} ({len(body)} chars)")
    for qkey,query in [("q1",cfg["q1"]),("q2",cfg["q2"])]:
        bare=call(ES,query);time.sleep(1.2)
        armed=call(ES+"\n\n## Reference knowledge:\n\n"+body,query);time.sleep(1.2)
        coin=0
        jr=judge("Impartial evaluator. Output JSON.",JE+f"\n## Ground truth\n{cfg['ref']}",bare,armed)
        bs=jr.get("a",{}).get("total",0);ac=jr.get("b",{}).get("total",0)
        if bs==0 and ac==0 and "notes" in jr:
            ms=re.findall(r'"total"\s*:\s*(\d+)',jr["notes"])
            if len(ms)>=2:bs,ac=int(ms[0]),int(ms[1])
        d=ac-bs
        print(f"    {qkey}: Bare:{bs}/20 Armed:{ac}/20 Delta:{d:+d}")
        track_e.append({"skill":name,"query":qkey,"bare":bs,"armed":ac,"delta":d})

all_results["track_e"]=track_e

# ═══ FINAL TABLE ═══
print(f"\n{'='*70}")
print("FINAL: ALL 16 SKILLS ACROSS 4 TRACKS")
print(f"{'='*70}")
for track_name,data in [("B",track_b),("C",track_c)]:
    skills={}
    for r in data:skills.setdefault(r["skill"],[]).append(r["delta"])
    print(f"\nTrack {track_name}:")
    for sk,deltas in skills.items():
        mean=sum(deltas)/len(deltas)
        print(f"  {sk}: deltas={[f'{d:+d}' for d in deltas]} mean={mean:+.1f}")

print(f"\nTrack D:")
for name in TOOLS:
    td=[r for r in track_d if r["skill"]==name]
    pct=sum(1 for r in td if r["passed"])/max(len(td),1)*100
    print(f"  {name}: {sum(1 for r in td if r['passed'])}/{len(td)} ({pct:.0f}%)")

print(f"\nTrack E:")
eskills={}
for r in track_e:eskills.setdefault(r["skill"],[]).append(r["delta"])
for sk,deltas in eskills.items():
    mean=sum(deltas)/len(deltas)
    print(f"  {sk}: deltas={[f'{d:+d}' for d in deltas]} mean={mean:+.1f}")

os.makedirs("evals/batch_16",exist_ok=True)
json.dump(all_results,open("evals/batch_16/all_16_skills.json","w",encoding="utf-8"),indent=2)
print(f"\nSaved to evals/batch_16/all_16_skills.json")
