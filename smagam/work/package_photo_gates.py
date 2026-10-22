from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import shutil,zipfile
root=Path(__file__).resolve().parents[1];repo=root.parent;out=root/'outputs';delivery=repo/'outputs';work=root/'work'
notes='''\n## Gate 1 and Gate 2 photo reference — 22 October 2026\nGate G01 and G02 retain their PDF positions and numbering. Their former ceremonial arches are replaced by the supplied photograph's rectangular composition: cream piers, two dark-brown ribbed steel vehicle portals, a central flat-roof guard room with glazed/brown door, steps and mat, potted palms and floodlight fittings. Surrounding decorative trees/masts are kept outside the portal area. Dimensions remain illustrative because the photograph provides no measurements. Gate 3 and the other gates retain their previous design.\n\nUse Gate 1 · photo view / Gate 2 · photo view in the sidebar for a front view, or open the gate from the concept map. Open gates 1–2 / Close gates 1–2 swings the four leaves at each gate inward; AK collision geometry follows the selected state. The static GLB contains the closed reference appearance. Deployment and vehicle-view controls remain available.\n\nChecks: rebuilt HTML/GLB/data; JS syntax; both gates' cream piers, four brown leaves, guard room, door and palms; Gate 3 retention; all four portals block AK when closed and clear when open. Native browser checked both front views and open/close control with no console errors.\n'''
for name in ['README.md','verification.txt']:
 p=out/name;p.write_text(p.read_text(encoding='utf-8')+notes,encoding='utf-8')
(delivery/'GATE-1-2-UPDATE.md').write_text(notes,encoding='utf-8')
reference=Path('C:/Users/HP/Downloads/17925904661116994045007522882962 - Amar Singh.jpg')
if reference.is_file():shutil.copyfile(reference,out/'gate-reference-photo.jpg')
im=Image.new('RGB',(1400,490),'#f1ece0');d=ImageDraw.Draw(im)
try:font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',20)
except OSError:font=ImageFont.load_default()
for i,(file,title)in enumerate([('gate-1-photo-reference-view.jpg','GATE 1 · Photo-reference design'),('gate-2-photo-reference-view.jpg','GATE 2 · Photo-reference design')]):
 p=Image.open(delivery/file).convert('RGB');p.thumbnail((690,440));im.paste(p,(700*i+5,42));d.text((700*i+14,9),title,font=font,fill='#214b52')
im.save(delivery/'gate-1-2-photo-design-preview.jpg',quality=93)
new=['GATE-1-2-UPDATE.md','gate-reference-photo.jpg','gate-1-photo-reference-view.jpg','gate-2-photo-reference-view.jpg','gate-1-open-view.jpg','gate-1-2-photo-design-preview.jpg']
for name in new:
 if (delivery/name).is_file():shutil.copyfile(delivery/name,out/name)
new+=['source/'+name for name in ['photo_gate_geometry.py','clear_photo_gate_frontage.py','install_photo_gate_viewer.py','photo_gate_camera.py','test_photo_gates.py','test_photo_gate_walk.py','test-photo-gate-walk.cjs']]
archive=delivery/'samagam-3d-package.zip';temp=work/'updated-photo-gates-package.zip'
with zipfile.ZipFile(archive) as old,zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED) as z:
 for name in dict.fromkeys(old.namelist()+new):
  candidates=[work/name[7:]] if name.startswith('source/') else [out/name,delivery/name]
  p=next((p for p in candidates if p.is_file()),None)
  if p:z.write(p,name)
  elif name in old.namelist():z.writestr(name,old.read(name))
temp.replace(archive);shutil.copyfile(archive,out/'samagam-3d-package.zip')
print('Saved gate previews, update notes and refreshed package')
