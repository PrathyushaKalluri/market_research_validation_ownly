#!/usr/bin/env python3
"""Validate dce_design_matrix.csv (stdlib only).

Checks:
  1. Structure: 2 alternatives per task; 6 tasks + 1 dominance task per block.
  2. Dominance: no alternative dominates the other, except in the dominance-check task
     (where A must dominate B).
  3. Purity: a 'price_vs_X' task varies ONLY price and attribute X; the cheaper
     alternative must be worse on X (otherwise the pair is dominated).
  4. Tag counts per block (>= 2 price_vs_reliability required for RSS).
  5. Level balance per attribute: overall and per block (dominance task excluded).
  6. Position balance: how often the cheaper alternative is shown as A.
  7. Implausible 'super-profile' excluded (235 / 25 min / 1 late / most / auto_24h).
Run:  python3 dce_check.py [path/to/dce_design_matrix.csv]
Exit code 1 if any hard check fails.
"""
import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("dce_design_matrix.csv")

# Utility direction: higher score = better for the respondent.
REST_RANK = {"few": 0, "some": 1, "most": 2}
REFUND_RANK = {"case_by_case": 0, "auto_24h": 1}
ATTRS = ["price", "eta_min", "late_in_10", "restaurants", "refund"]
TAG_ATTR = {
    "price_vs_eta": "eta_min",
    "price_vs_reliability": "late_in_10",
    "price_vs_assortment": "restaurants",
    "price_vs_refund": "refund",
}
SUPER_PROFILE = ("235", "25", "1", "most", "auto_24h")


def goodness(row):
    """Per-attribute 'goodness' vector (bigger = better)."""
    return {
        "price": -int(row["price"]),
        "eta_min": -int(row["eta_min"]),
        "late_in_10": -int(row["late_in_10"]),
        "restaurants": REST_RANK[row["restaurants"]],
        "refund": REFUND_RANK[row["refund"]],
    }


def dominates(a, b):
    ga, gb = goodness(a), goodness(b)
    return all(ga[k] >= gb[k] for k in ATTRS) and any(ga[k] > gb[k] for k in ATTRS)


def main():
    rows = list(csv.DictReader(PATH.open()))
    tasks = defaultdict(dict)
    for r in rows:
        tasks[(r["block"], r["task"])][r["alt"]] = r

    errors, notes = [], []
    tag_counts = defaultdict(Counter)
    levels_all = {k: Counter() for k in ATTRS}
    levels_block = defaultdict(lambda: {k: Counter() for k in ATTRS})
    cheaper_pos = defaultdict(Counter)

    print(f"Matrix: {PATH.name}  rows={len(rows)}  tasks={len(tasks)}\n")
    print("1-3) Per-task checks")
    for (block, task), alts in sorted(tasks.items(), key=lambda x: (x[0][0], int(x[1]["A"]["position"]))):
        if set(alts) != {"A", "B"}:
            errors.append(f"block {block} {task}: needs exactly A and B")
            continue
        a, b = alts["A"], alts["B"]
        tag = a["purpose_tag"]
        tag_counts[block][tag] += 1
        varying = [k for k in ATTRS if a[k] != b[k]]
        dom_ab, dom_ba = dominates(a, b), dominates(b, a)
        status = "ok"
        if tag == "dominance_check":
            if not dom_ab:
                errors.append(f"block {block} {task}: dominance task but A does not dominate B")
                status = "FAIL"
        else:
            if dom_ab or dom_ba:
                errors.append(f"block {block} {task}: dominated pair")
                status = "FAIL"
            for alt in (a, b):
                for k in ATTRS:
                    levels_all[k][alt[k]] += 1
                    levels_block[block][k][alt[k]] += 1
            cheaper = "A" if int(a["price"]) < int(b["price"]) else "B"
            cheaper_pos[block][cheaper] += 1
            if tag in TAG_ATTR:
                expected = {"price", TAG_ATTR[tag]}
                if set(varying) != expected:
                    errors.append(f"block {block} {task}: {tag} should vary only {sorted(expected)}, varies {varying}")
                    status = "FAIL"
            elif tag == "multi" and len(varying) < 3:
                errors.append(f"block {block} {task}: multi task varies only {varying}")
                status = "FAIL"
        for alt in (a, b):
            if tuple(alt[k] for k in ATTRS) == SUPER_PROFILE:
                errors.append(f"block {block} {task}: implausible super-profile used")
                status = "FAIL"
        price_gap = abs(int(a["price"]) - int(b["price"]))
        print(f"  block {block} pos {a['position']} {task:<4} {tag:<22} varies={','.join(varying):<42} "
              f"price_gap=Rs{price_gap:<3} dominated={'A>B' if dom_ab else ('B>A' if dom_ba else 'no')}  [{status}]")

    print("\n4) Tag counts per block")
    for block in sorted(tag_counts):
        print(f"  block {block}: {dict(tag_counts[block])}")
        if tag_counts[block]["price_vs_reliability"] < 2:
            errors.append(f"block {block}: fewer than 2 price_vs_reliability tasks")
        n_main = sum(v for k, v in tag_counts[block].items() if k != "dominance_check")
        if n_main != 6 or tag_counts[block]["dominance_check"] != 1:
            errors.append(f"block {block}: expected 6 tasks + 1 dominance task, got {dict(tag_counts[block])}")

    print("\n5) Level counts across both blocks (appearances; dominance task excluded)")
    for k in ATTRS:
        print(f"  {k:<12} {dict(sorted(levels_all[k].items()))}")
    for block in sorted(levels_block):
        print(f"  -- block {block}")
        for k in ATTRS:
            counts = levels_block[block][k]
            print(f"     {k:<12} {dict(sorted(counts.items()))}")
    for k in ATTRS:
        c = levels_all[k]
        if c and max(c.values()) > 3 * min(c.values()):
            notes.append(f"imbalance warning: {k} max/min appearances > 3 ({dict(c)})")

    print("\n6) Cheaper alternative shown as A vs B (main tasks)")
    for block in sorted(cheaper_pos):
        print(f"  block {block}: {dict(cheaper_pos[block])}")
        if abs(cheaper_pos[block]["A"] - cheaper_pos[block]["B"]) > 2:
            notes.append(f"block {block}: cheaper option position unbalanced")

    print("\nSUMMARY")
    for n in notes:
        print("  NOTE:", n)
    if errors:
        for e in errors:
            print("  ERROR:", e)
        sys.exit(1)
    print("  All hard checks passed.")


if __name__ == "__main__":
    main()
