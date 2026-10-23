from pathlib import Path
ROOT = Path("79-th-nirankari-sant-samagam-bhodwal/smagam")
out = ROOT / 'outputs'
old = (out / 'samagam-3d.html').read_text(encoding='utf-8')
parts = old.split(',SHAPES=', 1)
print("Has ,SHAPES=:", len(parts) > 1)
if len(parts) > 1:
    sub = parts[1].split(';\nconst canvas', 1)
    print("Has ;\\nconst canvas:", len(sub) > 1)
    if len(sub) == 1:
        print("Does NOT have ;\\nconst canvas!")
        # It didn't find ;\\nconst canvas, so sub[0] was the ENTIRE REST OF THE FILE!
        print("Length of sub[0]:", len(sub[0]))
        print("Last 200 chars of sub[0]:", sub[0][-200:])
