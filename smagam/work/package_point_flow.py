from pathlib import Path
import zipfile
root=Path(__file__).resolve().parents[1];out=root/'outputs';work=root/'work'
s=(work/'viewer-pdf.html').read_text(encoding='utf-8');start=s.index('// Point-first deployment wizard.');end=s.index('// Screen-space',start)
(work/'point_first_deployment.js').write_text(s[start:end],encoding='utf-8')
addition='''\n## Point-first deployment\nDuty deployment opens the panel and activates placement on the model. Click a place → choose the duty/model. Officer, barricade, Naka, Machaan and Morcha appear at that place as an unsaved preview. QRT, rider and patrol ask for a path; the clicked location is the first point. Add route points and choose Preview movement. Save changes commits the deployment to the local plan; Cancel draft restores the previous plan. Existing objects remain clickable and draggable. Edit details, delete and change position/path are available after saving; changing a position/path also previews before Save changes. The panel keeps the searchable supplied roster, advanced force fields and backups.\n\nNative verification: static placement, explicit Save and reload persistence, later deletion; QRT route request, animated preview and cancel without persistence. Temporary test deployments removed.\n'''
for name in ['deployment-guide.md','README.md']:
 p=out/name;p.write_text(p.read_text(encoding='utf-8')+addition,encoding='utf-8')
with (out/'verification.txt').open('a',encoding='utf-8') as f:f.write(addition)
archive=out/'samagam-3d-package.zip'
with zipfile.ZipFile(archive) as z:names=z.namelist()
names+=['samagam-point-deployment.jpg','source/point_first_deployment.js','source/install_point_first.py','source/finish_point_flow.py']
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for name in dict.fromkeys(names):
  p=work/name[7:] if name.startswith('source/') else out/name
  if p.is_file():z.write(p,name)
print('Point-first flow packaged; production HTML clean')
