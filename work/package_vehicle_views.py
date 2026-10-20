from pathlib import Path
import zipfile
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[1];out=root/'outputs';work=root/'work'
s=(work/'viewer-pdf.html').read_text(encoding='utf-8');a=s.index('// Vehicle-mounted first-person');b=s.index('// Point-first deployment wizard.',a);(work/'vehicle_views.js').write_text(s[a:b],encoding='utf-8')
notes='''\n## Rider / QRT / patrol camera views — 20 October 2026\nClick a deployed rider, QRT or patrol car (or its icon), then choose FPV view or Third-person view in its duty card. FPV looks from rider/driver height along the route; the selected vehicle body is hidden in FPV to keep the view clear. Third person follows behind the visible bike/car. Camera position and turns are smoothed.\n\nInside vehicle view: drag to look around, scroll or +/− to zoom, switch FPV / Third person, Pause / Resume, Reset camera, Exit vehicle view or Esc. The scene fits the available screen height. Entering a vehicle view resumes an assigned paused route; switching camera modes preserves the current pause state. With no route, the camera remains mounted at the parked vehicle and shows No route. Draw a route to enable movement. Exiting restores the previous model camera.\n\nVerification: native camera-option card on the real QRT-1; isolated production-code checks of FPV and third person for rider, QRT and patrol; drag look-around/reset; Pause and camera-switch pause preservation; Exit restores normal view. No console errors. Unit checks cover vehicle/heading camera transforms, zoom, route displacement, short-angle smoothing; existing click-picking, pause/resume and nearby-icon regressions pass. Verification fixtures used a separate local-storage key; the user deployment plan was preserved.\n'''
for name in ['README.md','deployment-guide.md']:
 p=out/name;p.write_text(p.read_text(encoding='utf-8')+notes,encoding='utf-8')
with (out/'verification.txt').open('a',encoding='utf-8') as f:f.write(notes)
im=Image.new('RGB',(1400,495),'#f4f0e5');d=ImageDraw.Draw(im)
try:font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',20)
except OSError:font=ImageFont.load_default()
for i,(name,title)in enumerate([('samagam-rider-third-person.jpg','RIDER · Third-person follow'),('samagam-vehicle-fpv.jpg','PATROL · First-person view')]):
 p=Image.open(out/name).convert('RGB');p.thumbnail((690,440));im.paste(p,(700*i+5,45));d.text((700*i+14,10),title,font=font,fill='#214b52')
im.save(out/'samagam-vehicle-views-preview.jpg',quality=92)
archive=out/'samagam-3d-package.zip'
with zipfile.ZipFile(archive) as z:names=z.namelist()
names+=['samagam-vehicle-views-preview.jpg','samagam-rider-third-person.jpg','samagam-rider-fpv.jpg','samagam-qrt-fpv.jpg','samagam-qrt-third-person.jpg','samagam-patrol-third-person.jpg','samagam-vehicle-fpv.jpg']+['source/'+n for n in ['vehicle_views.js','test_vehicle_views.py','test-vehicle-views.cjs','install_vehicle_views.py','refine_vehicle_camera.py','finish_vehicle_views.py']]
temp=work/'updated-vehicle-package.zip'
with zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED) as z:
 for name in dict.fromkeys(names):
  p=work/name[7:] if name.startswith('source/') else out/name
  if p.is_file():z.write(p,name)
temp.replace(archive)
print('Saved vehicle view preview, guide and updated package')
