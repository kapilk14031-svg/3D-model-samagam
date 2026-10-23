from pathlib import Path
ROOT = Path("79-th-nirankari-sant-samagam-bhodwal/smagam")
OUT = ROOT / 'outputs'
lines = (OUT / 'samagam-3d.html').read_text(encoding='utf-8').splitlines()
for i, l in enumerate(lines):
    if 'SHAPES=' in l:
        print(f"Line {i+1} has SHAPES=: length {len(l)}, starts with: {l[:80]}")
