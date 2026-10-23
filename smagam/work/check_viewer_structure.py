from pathlib import Path
import re

p = Path("79-th-nirankari-sant-samagam-bhodwal/smagam/work/viewer-pdf.html")
lines = p.read_text(encoding="utf-8").splitlines()
print(f"Total lines: {len(lines)}")

for i, l in enumerate(lines):
    if "DEP_KEY" in l:
        print(f"DEP_KEY line {i+1}: {l}")
    if "<header" in l or "<aside" in l:
        print(f"Structure line {i+1}: {l[:100]}")
    if "function flyTo" in l or "cameraFlyTo" in l or "flyTo(" in l:
        print(f"Flyto line {i+1}: {l[:100]}")
