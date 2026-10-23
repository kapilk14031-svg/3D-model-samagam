from pathlib import Path
ROOT = Path("79-th-nirankari-sant-samagam-bhodwal/smagam")
OUT = ROOT / 'outputs'
old = (OUT / 'samagam-3d.html').read_text(encoding='utf-8')
if ',SHAPES=' in old:
    p = old.split(',SHAPES=', 1)[1]
    print("Start:", p[:100])
    end_marker = ';\nconst canvas' if ';\nconst canvas' in p else ';const canvas'
    print("End marker found:", end_marker in p)
    shapes_str = p.split(end_marker, 1)[0]
    print("End:", shapes_str[-100:])
