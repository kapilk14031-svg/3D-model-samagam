from pathlib import Path
ROOT = Path("79-th-nirankari-sant-samagam-bhodwal/smagam")
OUT = ROOT / 'outputs'
lines = (OUT / 'samagam-3d.html').read_text(encoding='utf-8').splitlines()
l = lines[143] # 0-indexed 144
idx = l.index(',SHAPES=')
print("Before SHAPES=:", l[idx-50:idx])
print("After SHAPES=:", l[idx+8:idx+150])
print("End of line 144:", l[-100:])
if len(lines) > 144:
    print("Line 145 starts with:", lines[144][:80])
