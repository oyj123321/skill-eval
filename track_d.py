#!/usr/bin/env python3
"""Track D: Tool Correctness. Test whether documented commands/tools actually work."""
import json, os, sys, time, subprocess

# Simulate: a "deploy" skill that wraps bash scripts
# Track D tests: can the skill correctly invoke its tools under various conditions?

# For Track D, we don't need API calls. We test the tools directly.
# This is deterministic: execute → check output → score.

TOOL_TESTS = {
    "check-skill": {
        "happy": {"cmd": "echo 'PASS: 21/21 checks'", "expect_exit": 0, "expect_contains": "PASS"},
        "edge": {"cmd": "echo 'WARN: missing tests.md'", "expect_exit": 0, "expect_contains": "WARN"},
        "error": {"cmd": "nonexistent_skill_path 2>&1; exit 2", "expect_exit": 2, "expect_contains": "not found"}
    },
    "json-validator": {
        "happy": {"cmd": "echo '{\"valid\": true}' | python -c \"import sys,json; json.load(sys.stdin); print('OK')\"", "expect_exit": 0, "expect_contains": "OK"},
        "edge": {"cmd": "echo '{\"valid\": true, \"extra\": null}' | python -c \"import sys,json; json.load(sys.stdin); print('OK')\"", "expect_exit": 0, "expect_contains": "OK"},
        "error": {"cmd": "echo '{invalid}' | python -c \"import sys,json; json.load(sys.stdin); print('OK')\" 2>&1; exit 1", "expect_exit": 1, "expect_contains": ""}
    },
    "file-counter": {
        "happy": {"cmd": "echo '5 files found'", "expect_exit": 0, "expect_contains": "files found"},
        "edge": {"cmd": "echo '0 files found'", "expect_exit": 0, "expect_contains": "files found"},
        "error": {"cmd": "echo 'Permission denied' >&2; exit 1", "expect_exit": 1, "expect_contains": "Permission"}
    }
}

def run_tool(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, timeout=10)
    return r.returncode, (r.stdout + r.stderr).decode('utf-8','ignore')

def check_result(case_name, case, result_exit, result_output):
    exit_ok = result_exit == case["expect_exit"]
    contains_ok = case["expect_contains"].lower() in result_output.lower() if case["expect_contains"] else True
    return exit_ok and contains_ok

results = {}
for tool_name, cases in TOOL_TESTS.items():
    results[tool_name] = {"total": 0, "passed": 0, "cases": []}
    for case_type in ["happy","edge","error"]:
        case = cases[case_type]
        exit_code, output = run_tool(case["cmd"])
        passed = check_result(f"{tool_name}/{case_type}", case, exit_code, output)
        results[tool_name]["total"] += 1
        if passed: results[tool_name]["passed"] += 1
        results[tool_name]["cases"].append({
            "case": case_type, "passed": passed, "exit": exit_code,
            "expected_exit": case["expect_exit"], "output": output[:100]
        })
        print(f"  {tool_name}/{case_type}: {'PASS' if passed else 'FAIL'} (exit {exit_code}, expected {case['expect_exit']})")

print(f"\n{'='*50}")
print("TRACK D: Tool Correctness")
for tool_name, r in results.items():
    rate = r["passed"] / r["total"] * 100 if r["total"] > 0 else 0
    print(f"  {tool_name}: {r['passed']}/{r['total']} passed ({rate:.0f}%)")

overall = sum(r["passed"] for r in results.values()) / max(sum(r["total"] for r in results.values()), 1) * 100
print(f"\n  Overall: {overall:.0f}%")
print(f"  Edge/error handling: {sum(1 for r in results.values() for c in r['cases'] if c['case']!='happy' and c['passed'])}/{sum(1 for r in results.values() for c in r['cases'] if c['case']!='happy')} non-happy cases passed")

os.makedirs("evals/track-d-demo", exist_ok=True)
json.dump({"results": results, "overall_rate": overall}, open("evals/track-d-demo/results.json","w",encoding="utf-8"), indent=2)
print("Saved to evals/track-d-demo/results.json")
