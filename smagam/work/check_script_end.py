from pathlib import Path
p = Path("79-th-nirankari-sant-samagam-bhodwal/smagam/work/viewer-pdf.html")
lines = p.read_text(encoding="utf-8").splitlines()
for i in range(len(lines)-15, len(lines)):
    print(f"Line {i+1}: {lines[i]}")
