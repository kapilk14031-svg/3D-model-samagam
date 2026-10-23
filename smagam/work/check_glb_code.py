from pathlib import Path

p = Path("79-th-nirankari-sant-samagam-bhodwal/smagam/work/build_pdf_model.py")
lines = p.read_text(encoding="utf-8").splitlines()
for i, l in enumerate(lines):
    if "samagam-schematic.glb" in l or "export_glb" in l or "glb" in l.lower():
        print(f"Line {i+1}: {l[:120]}")
