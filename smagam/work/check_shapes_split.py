from pathlib import Path
ROOT = Path("79-th-nirankari-sant-samagam-bhodwal/smagam")
v = (ROOT / 'work/viewer-pdf.html').read_text(encoding='utf-8')
for l in v.splitlines():
    if '__SHAPES__' in l or 'const canvas' in l:
        print(repr(l[:80]))
