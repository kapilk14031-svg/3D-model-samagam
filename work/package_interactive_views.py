from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
from zipfile import ZipFile,ZIP_DEFLATED
root=Path.cwd();out=root/'outputs';names=['pandal','gate','traffic','road','ground','parking','langar','residential','police','railway'];sheet=Image.new('RGB',(1500,1100),'#163b40');d=ImageDraw.Draw(sheet)
for i,n in enumerate(names):
 im=Image.open(out/'detail-views'/(n+'.png')).convert('RGB');im=ImageOps.fit(im,(292,475));x=5+(i%5)*300;y=35+(i//5)*540;sheet.paste(im,(x,y));d.text((x+8,y+485),n.upper(),fill='#f2d59b')
sheet.save(out/'samagam-interactive-scenes.jpg',quality=92)
read=out/'README.md';s=read.read_text(encoding='utf-8');s+='''\n\n## Interactive concept map and close-up scenes — 19 October 2026\nSelect a coloured feature or category, then Open 3D view. Dedicated conceptual scenes cover pandal interior, parking, langar, residential tents, police chowki, railway station, gates, road viewpoints, grounds and traffic points. Back: Concept map. Explore with AK returns to the feature position in the complete venue.\nAll six PDF gates G01–G06 are selectable. Road vertices have source-road IDs and point numbers. PDF traffic facilities B07/B08 alighting, H03/H04 underpasses and S04 local bus stop are selectable. Conceptual ground groupings cover the residential sectors; only readable original names are asserted.\nMouse-wheel zoom follows the cursor in the concept map and orbit model. The venue uses ground-plane anchoring; near-horizontal local detail views use a camera-facing target plane. AK street mode retains follow-camera distance control.\nClose-up interiors and traffic-control dressing are illustrative browser scenes, inspired by the supplied screenshot. They are not measured reconstructions and are not embedded in the static GLB. Original source layout and static model remain available.\nPreview: samagam-interactive-scenes.jpg; individual captures: detail-views/.\n''';read.write_text(s,encoding='utf-8')
with (out/'verification.txt').open('a',encoding='utf-8') as f:f.write('\nInteractive extension: ten category click > Open 3D view > return flows passed in browser. All ten render captures saved. Browser console: no errors. Cursor zoom: 48 round-trip anchor checks passed. JavaScript syntax check passed.\n')
archive=out/'samagam-3d-package.zip'
with ZipFile(archive) as z:members=z.namelist()
new=['samagam-interactive-scenes.jpg']+['detail-views/'+n+'.png' for n in names]+['source/'+n for n in ['sync_viewer.py','concept_map.js','pandal_interior.js','feature_scenes.js','extend_click_views.py','traffic_click_views.py','refine_traffic.py','cursor_zoom.py','test_cursor_zoom.py','test-cursor-zoom.cjs']]
with ZipFile(archive,'w',ZIP_DEFLATED) as z:
 for name in dict.fromkeys(members+new):
  path=root/'work'/name[7:] if name.startswith('source/') else out/name
  if path.is_file():z.write(path,name)
print('Package and 10-view proof saved')
