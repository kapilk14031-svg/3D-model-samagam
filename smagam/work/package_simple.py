from pathlib import Path
import zipfile
from PIL import Image
root=Path(__file__).resolve().parents[1];out=root/'outputs';work=root/'work'
addition='''\n## Simple controls update\nChoose a duty, then Place / Move on map. Click a model or pictogram for its small duty card. New duty opens a short object picker. The focused editor hides the full list; All duties returns to search. Strength, shift timing, coordinates, full staff and backup controls are collapsed. The first officer name/rank can be edited directly.\n\nFor rider, QRT or patrol car: Draw / change path, click road points, Start movement. Movement turns on automatically, and the camera opens at the vehicle. Speed/return/loop remain under route settings. All three use the same tested route animation. Native browser verified a patrol car moving along its assigned route, with a matching moving car icon; the temporary test model was removed.\n'''
for name in ['deployment-guide.md','README.md']:
 p=out/name;p.write_text(p.read_text(encoding='utf-8')+addition,encoding='utf-8')
s=(work/'viewer-pdf.html').read_text(encoding='utf-8')
start=s.index('// Editable local duty plan.');end=s.index('// Direct 3D duty-object picking',start)
(work/'deployment_panel.js').write_text(s[start:end],encoding='utf-8')
pic=Image.open(out/'deployment-preview/DEP-B-M-1.png').convert('RGB');pic.thumbnail((1500,950));pic.save(out/'samagam-simple-deployment-preview.jpg',quality=92)
archive=out/'samagam-3d-package.zip'
with zipfile.ZipFile(archive) as z:names=z.namelist()
names+=['samagam-simple-deployment-preview.jpg','source/simplify_deployment.py','source/compact_deployment.py']
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for name in dict.fromkeys(names):
  p=work/name[7:] if name.startswith('source/') else out/name
  if p.is_file():z.write(p,name)
print('Final simplified model packaged')
