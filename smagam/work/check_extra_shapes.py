from pathlib import Path
ROOT = Path("79-th-nirankari-sant-samagam-bhodwal/smagam")
lines = (ROOT / 'work/build_pdf_model.py').read_text(encoding='utf-8').splitlines()
for i, l in enumerate(lines):
    if 'extra_shapes' in l:
        print(f"Line {i+1}: {l}")
