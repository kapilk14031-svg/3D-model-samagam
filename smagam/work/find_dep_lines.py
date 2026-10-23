from pathlib import Path
p = Path("79-th-nirankari-sant-samagam-bhodwal/smagam/work/viewer-pdf.html")
lines = p.read_text(encoding="utf-8").splitlines()
print(f"Total lines: {len(lines)}")
for i in range(len(lines)):
    if 'depSeedUnits' in lines[i] or 'depClone' in lines[i] or 'DEPLOYMENT_SEED' in lines[i]:
        print(f"Line {i+1}: {lines[i][:100]}")
