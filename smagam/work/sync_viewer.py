from pathlib import Path
import json
import re

root = Path(__file__).resolve().parents[1]
out = root / 'outputs'

# Extract pure SHAPES from git HEAD or current file using regex split that handles both CRLF and LF
try:
    import subprocess
    cmd = ['git', '-C', str(root.parent), 'show', 'HEAD:smagam/outputs/samagam-3d.html']
    git_old = subprocess.check_output(cmd, encoding='utf-8')
    shapes = re.split(r';\r?\nconst canvas', git_old.split(',SHAPES=', 1)[1], maxsplit=1)[0]
except Exception:
    old = (out / 'samagam-3d.html').read_text(encoding='utf-8')
    shapes = re.split(r';\r?\nconst canvas', old.split(',SHAPES=', 1)[1], maxsplit=1)[0]

scene_json = json.dumps(json.loads((out / 'scene-data.json').read_text(encoding='utf-8')), separators=(',', ':'))
template = (root / 'work/viewer-pdf.html').read_text(encoding='utf-8')
s = template.replace('__SCENE__', scene_json).replace('__SHAPES__', shapes)

html_tmp = root / 'work/synced-viewer.tmp'
html_tmp.write_text(s, encoding='utf-8')
html_tmp.replace(out / 'samagam-3d.html')

js_tmp = root / 'work/synced-viewer-js.tmp'
js_tmp.write_text(s.split('<script>', 1)[1].split('</script>', 1)[0], encoding='utf-8')
js_tmp.replace(root / 'work/viewer-check.js')

print(f"Synced viewer successfully! SHAPES size: {len(shapes):,} bytes, total HTML: {len(s):,} bytes")
