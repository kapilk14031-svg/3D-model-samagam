from pathlib import Path
ROOT = Path("79-th-nirankari-sant-samagam-bhodwal/smagam")
OUT = ROOT / 'outputs'
lines = (OUT / 'samagam-3d.html').read_text(encoding='utf-8').splitlines()
print(f"Total lines: {len(lines)}")
for i in range(min(30, len(lines))):
    l = lines[i]
    if 'SHAPES=' in l or 'canvas=' in l:
        print(f"Line {i+1}: {l[:150]}")
