from pathlib import Path
import zipfile
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[1];out=root/'outputs';work=root/'work';s=(work/'viewer-pdf.html').read_text(encoding='utf-8')
a=s.index('// Details for both deployed personnel');b=s.index('function depOfficerModelHit',a);(work/'officer_details.js').write_text(s[a:b],encoding='utf-8')
notes='''\n## Movement and nearby icons — 20 October 2026\nClick a moving deployed model or its original icon once to pause; click again to resume from the same route position. The duty card displays Paused / Moving and also offers a Pause / Resume button. This applies to rider, QRT, patrol, foot patrol, ambulance and fire-vehicle routes. Static models only open their details. Pause is a runtime control; reloading restarts normal route playback.\n\nWide overview shows all applicable icons in view. Close views automatically limit icons to the area around the camera focus; AK street view limits them to nearby positions. No duplicate officer-icon layer is added. Officer bodies remain directly clickable even when distant duty icons are hidden.\n\nVerification: native isolated patrol check confirmed click → Paused with unchanged icon position, second click → Moving with changed position. Main venue overview showed 128 icons, bridge close view 9 nearby icons. Unit tests covered pause/resume for six types, smooth route continuation, relocation while paused, static models, overview/zoom/street proximity. Temporary test drafts were not saved.\n'''
for name in ['README.md','deployment-guide.md']:
 p=out/name;p.write_text(p.read_text(encoding='utf-8')+notes,encoding='utf-8')
with (out/'verification.txt').open('a',encoding='utf-8') as f:f.write(notes)
im=Image.new('RGB',(1400,495),'#f3eee2');draw=ImageDraw.Draw(im)
try:font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',20)
except OSError:font=ImageFont.load_default()
for i,(name,title)in enumerate([('samagam-movement-pause.jpg','Click to pause / click again to resume'),('samagam-nearby-icons.jpg','Zoomed view: nearby icons only')]):
 p=Image.open(out/name).convert('RGB');p.thumbnail((690,440));im.paste(p,(i*700+5,45));draw.text((i*700+14,10),title,font=font,fill='#214b52')
im.save(out/'samagam-movement-icons-preview.jpg',quality=92)
archive=out/'samagam-3d-package.zip'
with zipfile.ZipFile(archive) as z:names=z.namelist()
names+=['samagam-movement-pause.jpg','samagam-nearby-icons.jpg','samagam-movement-icons-preview.jpg']+['source/'+n for n in ['click_pause_movement.py','nearby_icons.py','responsive_movement.py','test_pause_movement.py','test-pause-movement.cjs','test-nearby-icons.cjs','sync_viewer.py']]
temp=work/'updated-package.zip'
with zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED) as z:
 for name in dict.fromkeys(names):
  p=work/name[7:] if name.startswith('source/') else out/name
  if p.is_file():z.write(p,name)
temp.replace(archive)
print('Updated deliverables and package')
