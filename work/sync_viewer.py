from pathlib import Path
import json
root=Path(__file__).resolve().parents[1];out=root/'outputs'
old=(out/'samagam-3d.html').read_text(encoding='utf-8');shapes=old.split(',SHAPES=',1)[1].split(';\nconst canvas',1)[0]
s=(root/'work/viewer-pdf.html').read_text(encoding='utf-8').replace('__SCENE__',json.dumps(json.loads((out/'scene-data.json').read_text(encoding='utf-8')),separators=(',',':'))).replace('__SHAPES__',shapes)
html_tmp=root/'work/synced-viewer.tmp';html_tmp.write_text(s,encoding='utf-8');html_tmp.replace(out/'samagam-3d.html')
js_tmp=root/'work/synced-viewer-js.tmp';js_tmp.write_text(s.split('<script>',1)[1].split('</script>',1)[0],encoding='utf-8');js_tmp.replace(root/'work/viewer-check.js')
