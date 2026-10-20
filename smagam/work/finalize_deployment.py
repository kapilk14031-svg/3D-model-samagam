from pathlib import Path
import json,csv,zipfile
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[1];out=root/'outputs';work=root/'work'
s=(work/'viewer-pdf.html').read_text(encoding='utf-8')
start=s.index('// Direct 3D duty-object picking, anchored dragging and officer identity cards.')
end=s.index('// Screen-space',start)
(work/'deployment_direct_drag.js').write_text(s[start:end],encoding='utf-8')
plan=json.loads((out/'samagam-duty-deployment.json').read_text(encoding='utf-8'))
assert len(plan['units'])==162
with (out/'samagam-duty-deployment.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['ID','Duty','Type','Ground','Position','Shift','Main force','Women (included)','Incharge (separate)','Extra','Start','End','Notes'])
 for u in plan['units']:
  for k,v in u['shifts'].items():w.writerow([u['id'],u['title'],u['type'],u.get('ground',''),u.get('position'),k,v.get('force'),v.get('female'),v.get('incharge'),v.get('extra'),v.get('start',''),v.get('end',''),u.get('notes','')+' '+v.get('notes','')])
guide='''# Police deployment controls

Open samagam-3d.html and choose Duty deployment.

- Machaan, Morcha, QRT, rider, patrol car ya officer ke **3D body par click** karein: duty card khulega.
- Body par left mouse button daba kar drag karein: position badlegi aur local draft save hoga. Chhota icon bhi drag kar sakte hain.
- Moving rider/car drag ke dauran rukta hai; release par uska poora assigned route nayi position par shift hokar resume hota hai.
- Camera pan ke liye khaali ground drag karein; object ke upar Shift/right-drag camera ka alternate control hai.
- Officer card mein assigned naam, rank, role, shift aur duty dikhti hai. Naam na diya ho to Name not assigned dikhega.
- Edit officer / duty → staff field: Name | Rank | Role | Shift | Contact, har officer alag line mein. Save ke baad Create individual staff icons se alag clickable officer models banayein.
- Add, duplicate, delete, Undo, numeric X/Y/Z, rotation aur scale panel mein hain. Place on model se point select karke shift karein.
- Rider/QRT/patrol ke liye Draw route → model par points → Finish route. Speed aur loop/return editable hain.
- Models/icons, har model type, animation aur shift ke toggles diye hain.
- JSON export/import se backup aur transfer; CSV se shift-wise review. Browser ka local draft usi browser mein rehta hai.

Supplied roster ke 162 records retained hain. 33 off-site/unconfirmed points unplaced hain; panel se location dein. Main force, women subset, separate incharge aur extra staff alag fields hain. Unknown numbers/shifts blank hain. QRT-4 night incharge aur duplicate A-14 ki uncertainty notes mein retained hai. Positions conceptual hain. New routes manually assign karne hain; source mein na diye routes invent nahi kiye.

Static GLB mein dynamic deployment/interiors nahi hain; interactive HTML mein ye features available hain.
'''
(out/'deployment-guide.md').write_text(guide,encoding='utf-8')
readme=out/'README.md';text=readme.read_text(encoding='utf-8');text+='''\n## Editable police deployment — 19 October 2026\n162 supplied duty records, editable shifts/strength and separate incharges, models, staff identities, routes and local persistence. Directly click a deployed 3D body for its identity/duty card; drag the body to relocate it. Moving vehicle routes translate with the model. Individual staff markers remain included within their parent strength. Unknown names are explicitly unassigned. See deployment-guide.md; samagam-duty-deployment.json is the positioned backup and CSV is the shift review. 33 off-site/unconfirmed records remain unplaced for user positioning.\n\nMachaan, Morcha and barricades have HARYANA POLICE signs. Rider/QRT/patrol routes support animation. NH44 paths now retain a 1.35 CSS-pixel minimum core at overview scales with a restrained glow, above the road surface.\n\nVerified: 162-record seed/count semantics, unknown shift handling, female subset validation, route animation/return/translation, individual-marker counting, 3D ray picking and misses, JavaScript syntax. Native browser verified CRUD, route animation/persistence, icon dragging, direct Machaan body click/drag and Undo; no console errors.\n''';readme.write_text(text,encoding='utf-8')
with (out/'verification.txt').open('a',encoding='utf-8') as f:f.write('\nDeployment: PASS 162-record roster and shift/strength invariants; route return and relocation; child marker counts; direct 3D ray picking six model types and misses; JS syntax. Native UI PASS direct model click/drag and Undo, CRUD, moving rider route, local reload persistence, separate staff markers, final JSON export; no browser console errors. NH44 minimum-pixel path core visible in overview.\n')
tiles=[('DEP-B-M-1.png','MACHAAN · editable 3D duty post'),('DEP-B-MO-1.png','MORCHA · Haryana Police'),('DEP-SP-N5.png','NAKA · barricades and officers'),('DEP-overview.png','NH44 · route lines and deployment')]
im=Image.new('RGB',(1600,1080),'#f3eee2');d=ImageDraw.Draw(im)
try:font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',21)
except OSError:font=ImageFont.load_default()
for i,(file,title) in enumerate(tiles):
 p=Image.open(out/'deployment-preview'/file).convert('RGB');p.thumbnail((780,485));x=10+(i%2)*800;y=15+(i//2)*540;d.text((x+10,y),title,font=font,fill='#214754');im.paste(p,(x+(780-p.width)//2,y+36))
im.save(out/'samagam-police-deployment-preview.jpg',quality=92)
archive=out/'samagam-3d-package.zip'
with zipfile.ZipFile(archive) as z:members=z.namelist()
new=['deployment-guide.md','samagam-duty-deployment.json','samagam-duty-deployment.csv','deployment-supplied-roster.json','samagam-police-deployment-preview.jpg']+['deployment-preview/'+n for n,_ in tiles]
new+=['source/'+n for n in ['deployment_panel.js','deployment_direct_drag.js','readable_route_paths.js','build_deployment_seed.py','deployment-seed.json','test_deployment.py','test-deployment.cjs','test_deployment_picking.py','test-deployment-picking.cjs']]
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for name in dict.fromkeys(members+new):
  p=work/name[7:] if name.startswith('source/') else out/name
  if p.is_file():z.write(p,name)
print('Saved guide, CSV, preview and refreshed package; 162 records')
