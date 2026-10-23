from pathlib import Path
p = Path("79-th-nirankari-sant-samagam-bhodwal/smagam/work/viewer-pdf.html")
lines = p.read_text(encoding="utf-8").splitlines()
for i, l in enumerate(lines):
    if "depSeedUnits" in l or "samagam-duty-deployment" in l or "deployment-seed" in l:
        print(f"Line {i+1}: {l[:140]}")
