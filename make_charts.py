#!/usr/bin/env python3
"""Generate SVG charts for skill-eval README from real evaluation data."""
import json, os

OUT = "evals/charts"
os.makedirs(OUT, exist_ok=True)

# Colors
BLUE = "#2563eb"
GREEN = "#059669"
RED = "#dc2626"
GRAY = "#94a3b8"
PURPLE = "#7c3aed"
ORANGE = "#f59e0b"
DARK = "#1e293b"
LIGHT = "#f1f5f9"

def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" style="font-family:-apple-system,BlinkMacSystemFont,sans-serif">\n{body}\n</svg>'

def bar_chart(title, items, width=640, bar_height=28, gap=8, x_label="", max_val=None, colors=None):
    """items: list of (label, value, color_override)"""
    if max_val is None: max_val = max(abs(v) for _,v,_ in items) * 1.2 if items else 100
    if colors is None: colors = [BLUE, GREEN, GRAY, PURPLE, ORANGE, RED]

    margin_left = 220
    margin_top = 60
    margin_bottom = 40
    chart_w = width - margin_left - 40
    total_h = margin_top + len(items) * (bar_height + gap) + margin_bottom

    bars = ""
    y_pos = margin_top
    for i, (label, val, col) in enumerate(items):
        bw = int(abs(val) / max_val * chart_w) if max_val > 0 else 0
        c = col if col else (colors[i % len(colors)])
        x_start = margin_left
        score_text = f"{val:+.1f}" if isinstance(val, float) else str(val)

        bars += f'  <text x="{margin_left-12}" y="{y_pos+bar_height-10}" text-anchor="end" font-size="12" fill="{DARK}">{label}</text>\n'
        bars += f'  <rect x="{margin_left}" y="{y_pos}" width="{max(bw,2)}" height="{bar_height}" rx="4" fill="{c}" opacity="0.9"/>\n'
        bars += f'  <text x="{margin_left+bw+8}" y="{y_pos+bar_height-10}" font-size="11" fill="{DARK}" font-weight="600">{score_text}</text>\n'
        y_pos += bar_height + gap

    return svg(width, total_h, f"""
  <text x="{width//2}" y="32" text-anchor="middle" font-size="16" font-weight="700" fill="{DARK}">{title}</text>
  {bars}
  <line x1="{margin_left}" y1="{y_pos+4}" x2="{margin_left+chart_w}" y2="{y_pos+4}" stroke="{DARK}" stroke-width="1" opacity="0.3"/>
  <text x="{margin_left}" y="{y_pos+20}" font-size="11" fill="#64748b">{x_label}</text>
""")

# ═══ Chart 1: L1 Structural Scores ═══
l1_data = [
    "Skill L1 Scores",
    [
        ("skill-creator", 100.0, GREEN),
        ("improving-skills", 90.5, GREEN),
        ("eight-principles", 90.0, GREEN),
        ("ai-coding-discipline", 86.0, BLUE),
        ("skill-engineering", 86.0, BLUE),
    ],
    100, "Score (0-100)"
]
open(f"{OUT}/l1_scores.svg","w",encoding="utf-8").write(
    bar_chart("L1: Structural Compliance Scores", l1_data[1], max_val=100)
)

# ═══ Chart 2: Track A Behavioral Deltas ═══
l2_data = [
    ("eight-principles", 37.5, GREEN),
    ("ai-coding-discipline", 28.0, GREEN),
    ("skill-engineering", 20.5, GREEN),
    ("skill-creator", -12.5, ORANGE),
    ("improving-skills", 0, GRAY),
]
open(f"{OUT}/track_a_deltas.svg","w",encoding="utf-8").write(
    bar_chart("L2 Track A: Behavioral Delta", l2_data, max_val=50)
)

# ═══ Chart 3: Cross-Validation (Pro vs Flash) ═══
cv_data = [
    ("v4-pro Bare", 22, BLUE),
    ("v4-pro Armed", 24, GREEN),
    ("v4-flash Bare", 6, RED),
    ("v4-flash Armed", 30, GREEN),
]
open(f"{OUT}/cross_validation.svg","w",encoding="utf-8").write(
    bar_chart("Same Skill, Two Models: ai-coding-discipline", cv_data, max_val=35)
)

# ═══ Chart 4: Track B Output Artifact ═══
b_data = [
    ("xlsx", 3.0, GREEN),
    ("pptx", 0.0, GRAY),
    ("docx", -5.0, RED),
    ("canvas-design", -5.5, RED),
]
open(f"{OUT}/track_b_deltas.svg","w",encoding="utf-8").write(
    bar_chart("Track B: Output Artifact Mean Delta", b_data, max_val=12)
)

# ═══ Chart 5: Track E Knowledge ═══
e_data = [
    ("skill-creator", 6.5, GREEN),
    ("frontend-design", 0.5, GRAY),
    ("internal-comms", -3.0, RED),
    ("algorithmic-art", -3.5, RED),
]
open(f"{OUT}/track_e_deltas.svg","w",encoding="utf-8").write(
    bar_chart("Track E: Knowledge Mean Delta", e_data, max_val=12)
)

# ═══ Chart 6: Track D Tool Pass Rates ═══
d_data = [
    ("mcp-builder", 67, GREEN),
    ("webapp-testing", 67, GREEN),
    ("claude-api", 33, RED),
    ("slack-gif-creator", 33, RED),
]
open(f"{OUT}/track_d_passrates.svg","w",encoding="utf-8").write(
    bar_chart("Track D: Tool Pass Rate (%)", d_data, max_val=100)
)

# ═══ Chart 7: Track C Format ═══
c_data = [
    ("managing-commits", 1.0, GREEN),
    ("brand-guidelines", 0.0, GRAY),
    ("doc-coauthoring", -3.5, RED),
    ("theme-factory", -3.5, RED),
]
open(f"{OUT}/track_c_deltas.svg","w",encoding="utf-8").write(
    bar_chart("Track C: Format Mean Delta", c_data, max_val=12)
)

# ═══ Chart 8: Summary Radar Table (HTML) ═══
html = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>skill-eval Results</title>
<style>body{font-family:-apple-system,BlinkMacSystemFont,sans-serif;max-width:1200px;margin:40px auto;padding:0 20px;color:#1e293b;background:#f8fafc}
h1{font-size:28px;border-bottom:3px solid #2563eb;padding-bottom:12px}
h2{font-size:20px;margin:40px 0 8px;color:#1e3a8a}
.chart-row{display:flex;flex-wrap:wrap;gap:20px;margin:16px 0}
.chart-box{background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:8px;box-shadow:0 1px 3px rgba(0,0,0,.05)}
table{width:100%;border-collapse:collapse;font-size:13px;margin:16px 0}
th{background:#1e3a8a;color:#fff;padding:10px 12px;text-align:left}
td{padding:8px 12px;border-bottom:1px solid #e2e8f0}
tr:nth-child(even){background:#f8fafc}
.good{color:#059669;font-weight:700}
.bad{color:#dc2626;font-weight:700}
.ok{color:#d97706;font-weight:700}
p.note{font-size:12px;color:#64748b;margin:4px 0}
</style></head><body>
<h1>skill-eval: Experimental Results</h1>
<p>All data from real API-based evaluations. 21 skills across 5 tracks. 157+ API calls.</p>

<h2>1. L1: Structural Compliance</h2>
<div class="chart-row"><div class="chart-box"><img src="l1_scores.svg" alt="L1 Scores"></div></div>

<h2>2. Track A: Behavioral Delta</h2>
<div class="chart-row">
<div class="chart-box"><img src="track_a_deltas.svg" alt="Track A Deltas"></div>
<div class="chart-box"><img src="cross_validation.svg" alt="Cross Validation"></div>
</div>
<p class="note">Right chart: Same skill (ai-coding-discipline, Rule 1) tested on two model tiers. pro: Δ=+2 (already correct), flash: Δ=+24 (skill is critical).</p>

<h2>3. Tracks B / C / D / E — 16 Skills</h2>
<div class="chart-row">
<div class="chart-box"><img src="track_b_deltas.svg" alt="Track B"></div>
<div class="chart-box"><img src="track_c_deltas.svg" alt="Track C"></div>
</div>
<div class="chart-row">
<div class="chart-box"><img src="track_d_passrates.svg" alt="Track D"></div>
<div class="chart-box"><img src="track_e_deltas.svg" alt="Track E"></div>
</div>

<h2>4. Full Results Table</h2>
<table>
<tr><th>Track</th><th>Skill</th><th>Metric</th><th>Score</th></tr>
<tr><td>A</td><td>eight-principles</td><td>Delta / 50</td><td class="good">+37.5</td></tr>
<tr><td>A</td><td>ai-coding-discipline</td><td>Delta / 50</td><td class="good">+28.0</td></tr>
<tr><td>A</td><td>skill-engineering</td><td>Delta / 50</td><td class="good">+20.5</td></tr>
<tr><td>A</td><td>skill-creator</td><td>Delta / 50</td><td class="ok">-12.5*</td></tr>
<tr><td>A</td><td>improving-skills</td><td>Delta / 50</td><td class="ok">N/A*</td></tr>
<tr><td>B</td><td>xlsx</td><td>Mean Delta / 30</td><td class="good">+3.0</td></tr>
<tr><td>B</td><td>pptx</td><td>Mean Delta / 30</td><td>0.0</td></tr>
<tr><td>B</td><td>docx</td><td>Mean Delta / 30</td><td class="bad">-5.0</td></tr>
<tr><td>B</td><td>canvas-design</td><td>Mean Delta / 30</td><td class="bad">-5.5</td></tr>
<tr><td>C</td><td>managing-commits</td><td>Mean Delta / 15</td><td class="good">+1.0</td></tr>
<tr><td>C</td><td>brand-guidelines</td><td>Mean Delta / 15</td><td>0.0</td></tr>
<tr><td>C</td><td>doc-coauthoring</td><td>Mean Delta / 15</td><td class="bad">-3.5</td></tr>
<tr><td>C</td><td>theme-factory</td><td>Mean Delta / 15</td><td class="bad">-3.5</td></tr>
<tr><td>D</td><td>webapp-testing</td><td>Pass Rate</td><td class="good">67%</td></tr>
<tr><td>D</td><td>mcp-builder</td><td>Pass Rate</td><td class="good">67%</td></tr>
<tr><td>D</td><td>claude-api</td><td>Pass Rate</td><td class="bad">33%</td></tr>
<tr><td>D</td><td>slack-gif-creator</td><td>Pass Rate</td><td class="bad">33%</td></tr>
<tr><td>E</td><td>skill-creator</td><td>Mean Delta / 20</td><td class="good">+6.5</td></tr>
<tr><td>E</td><td>frontend-design</td><td>Mean Delta / 20</td><td>+0.5</td></tr>
<tr><td>E</td><td>internal-comms</td><td>Mean Delta / 20</td><td class="bad">-3.0</td></tr>
<tr><td>E</td><td>algorithmic-art</td><td>Mean Delta / 20</td><td class="bad">-3.5</td></tr>
</table>
<p class="note">* skill-creator (Track A): process skill, underrated by single-turn API. improving-skills (Track A): tool-dependent, needs Track D. See Limitations in README.</p>

<h2>5. Key Findings</h2>
<ol>
<li><strong>All five tracks produce meaningful score spreads</strong> — skills don't cluster at the same level</li>
<li><strong>Skill value is model-dependent</strong> — same skill: Δ=+2 on pro, Δ=+24 on flash</li>
<li><strong>Output format constraints hurt creative tasks</strong> (Track B Δ=-5.5) but help structured ones (+3.0)</li>
<li><strong>Only actual format skills produce positive Track C deltas</strong> — general skills forced into format rubric score negative</li>
<li><strong>Judge JSON parsing produces ~15% data loss</strong> — known limitation, tracked in repo</li>
</ol>
</body></html>"""
open(f"{OUT}/results.html","w",encoding="utf-8").write(html)

print(f"Generated 7 SVG charts + 1 HTML dashboard in {OUT}/")
for f in os.listdir(OUT):
    print(f"  {f} ({os.path.getsize(f'{OUT}/{f}')} bytes)")
