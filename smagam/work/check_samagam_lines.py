from pathlib import Path
p = Path("79-th-nirankari-sant-samagam-bhodwal/smagam/outputs/samagam-3d.html")
lines = p.read_text(encoding="utf-8").splitlines()
print(f"Total lines in samagam-3d.html: {len(lines)}")
for i in range(830, 850):
    if i < len(lines):
        print(f"Line {i+1}: {lines[i][:110]}")
