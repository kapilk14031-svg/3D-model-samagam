from pathlib import Path

p = Path("79-th-nirankari-sant-samagam-bhodwal/smagam/work/build_pdf_model.py")
lines = p.read_text(encoding="utf-8").splitlines()
print(f"Total lines in build_pdf_model: {len(lines)}")
for i, l in enumerate(lines[-35:]):
    print(f"Line {len(lines)-34+i}: {l}")
