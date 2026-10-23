from pathlib import Path
p = Path("79-th-nirankari-sant-samagam-bhodwal/smagam/work/viewer-pdf.html")
lines = p.read_text(encoding="utf-8").splitlines()
for i, l in enumerate(lines):
    if "data-view" in l or "VIEWS" in l or "VIEWS[" in l or "VIEWS =" in l or "VIEWS=" in l:
        print(f"Line {i+1}: {l[:120]}")
    if "function cameraFlyTo" in l or "flyTo" in l:
        print(f"Line {i+1}: {l[:120]}")
