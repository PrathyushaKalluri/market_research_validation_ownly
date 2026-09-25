"""
06_export.py — renders each dashboard tab to PNG and the whole deck to PDF
using headless Chrome, then trims trailing whitespace from each PNG.
"""
import os
import subprocess
import sys

from PIL import Image, ImageChops

ROOT = "/Users/klprathyusha/Sem 3/Project/Ownly"
FD = f"{ROOT}/final_dashboard"
EXP = f"{FD}/exports"
os.makedirs(EXP, exist_ok=True)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

TABS = [
    ("t1", "01_business_problem"), ("t2", "02_kpi_driver_tree"),
    ("t3", "03_marketing_metrics"), ("t4", "04_switching_equation"),
    ("t5", "05_price_switch_fit"), ("t6", "06_market_reality"),
    ("t7", "07_assortment_availability"), ("t8", "08_awareness_trial"),
    ("t9", "09_trial_retention"), ("t10", "10_challenger_failures"),
    ("t11", "11_evidence_matrix"), ("t12", "12_propositions"),
    ("t13", "13_gtm_decision"), ("t14", "14_hypothesis_decision"),
]

W, H = 1500, 3600
BG = (242, 235, 221)


def trim(path, pad=28):
    im = Image.open(path).convert("RGB")
    bg = Image.new("RGB", im.size, BG)
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()
    if bbox:
        bottom = min(im.height, bbox[3] + pad)
        im.crop((0, 0, im.width, bottom)).save(path, optimize=True)
    return Image.open(path).size


if not os.path.exists(CHROME):
    sys.exit("Chrome not found")

for tid, name in TABS:
    out = f"{EXP}/{name}.png"
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                    f"--screenshot={out}", f"--window-size={W},{H}",
                    "--virtual-time-budget=4000",
                    f"file://{FD}/index.html?tab={tid}"],
                   capture_output=True, timeout=120)
    if os.path.exists(out):
        sz = trim(out)
        print(f"  {name}.png  {sz[0]}x{sz[1]}")
    else:
        print(f"  !! failed {name}")

pdf = f"{FD}/Ownly_Gachibowli_GTM_Dashboard.pdf"
subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                f"--print-to-pdf={pdf}", "--no-pdf-header-footer",
                "--virtual-time-budget=8000", f"file://{FD}/index.html"],
               capture_output=True, timeout=180)
print(f"\nPDF: {pdf}  ({os.path.getsize(pdf)/1024:.0f} KB)" if os.path.exists(pdf) else "PDF failed")
