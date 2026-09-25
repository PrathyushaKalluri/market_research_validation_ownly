#!/usr/bin/env python3
"""Parse the pre-registered KPI dictionary into structured rows."""
import re, os, json, csv

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "09_analysis", "kpi_system", "metric_dictionary.md")

txt = open(SRC, encoding="utf-8").read()
layer = None
out = []
for block in re.split(r"\n(?=#{2,3} )", txt):
    h = block.split("\n", 1)[0]
    if h.startswith("## Layer") or h.startswith("## "):
        m = re.match(r"## (.+)", h)
        if m and "Layer" in m.group(1): layer = m.group(1).strip()
        if not h.startswith("### "): continue
    m = re.match(r"### (K\d+[a-z]?) · (.+)", h)
    if not m: continue
    kid, rest = m.group(1), m.group(2)
    parts = [p.strip() for p in rest.split("·")]
    name = parts[0]
    prio = next((p for p in parts if re.match(r"^P\d$", p)), "")
    guard = next((p for p in parts if p.startswith("Guardrail")), "")
    star = "★" in rest
    def field(label):
        mm = re.search(r"- \*\*%s:\*\*\s*(.+?)(?=\n- \*\*|\n### |\Z)" % re.escape(label), block, re.S)
        return re.sub(r"\s+", " ", mm.group(1)).strip() if mm else ""
    out.append({
        "kpi_id": kid, "layer": layer or "", "name": name.replace("★", "").strip(),
        "priority": prio, "guardrail": guard.replace("Guardrail", "").strip(),
        "north_star": "Yes" if star else "No",
        "definition": field("Definition"), "formula": field("Formula"),
        "source": field("Source"), "evidence_level": field("Evidence level"),
        "denominator": field("Denominator"), "decision": field("Decision"),
        "high_means": field("High means"), "low_means": field("Low means"),
        "bias": field("Bias"),
    })

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "00_kpi_dictionary_prereg.csv"),
          "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
    w.writeheader(); w.writerows(out)

print(f"parsed {len(out)} pre-registered KPIs from metric_dictionary.md\n")
print(f"{'ID':6s} {'P':3s} {'G':3s} {'NAME':52s} EVIDENCE LEVEL")
print("-"*110)
for r in out:
    print(f"{r['kpi_id']:6s} {r['priority']:3s} {r['guardrail']:3s} {r['name'][:52]:52s} {r['evidence_level'][:34]}")
