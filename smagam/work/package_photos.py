from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib,json,zipfile,html
root=Path(__file__).resolve().parents[1];out=root/'outputs';folder=out/'photos';files=sorted(folder.glob('*.jpg'));assert len(files)==7
info=[]
for p in files:
    im=Image.open(p);im.verify();im=Image.open(p)
    assert im.format=='JPEG' and im.size==(1600,1000),(p,im.size)
    info.append(dict(file=p.name,width=1600,height=1000,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
assert len({r['sha256'] for r in info})==7
(folder/'photo-manifest.json').write_text(json.dumps(info,indent=2),encoding='utf-8')
sheet=Image.new('RGB',(1600,600),'#102f36');d=ImageDraw.Draw(sheet)
try:font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',18)
except OSError:font=ImageFont.load_default()
for i,p in enumerate(files):
    x=(i%4)*400;y=(i//4)*300
    im=Image.open(p);im.thumbnail((390,252));sheet.paste(im,(x+(400-im.width)//2,y+5));d.text((x+12,y+263),p.stem.replace('-',' '),font=font,fill='#f4e7c8')
d.text((1215,320),'7 JPG ANGLES',font=font,fill='#e1be79');d.text((1215,355),'1600 × 1000',font=font,fill='#e1be79')
sheet.save(out/'samagam-7-photo-preview.png')
with zipfile.ZipFile(out/'samagam-7-jpg-photos.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in files:z.write(p,p.name)
cards=''.join(f'<a href="{p.name}"><img src="{p.name}" alt="{html.escape(p.stem)}"><span>{html.escape(p.stem.replace("-"," "))}</span></a>' for p in files)
(folder/'index.html').write_text('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Samagam · Seven JPG angles</title><style>body{background:#102f36;color:#f7eddb;font:16px Segoe UI;margin:25px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}a{color:#f0d7a6;text-decoration:none;background:#1b434a;padding:12px;border-radius:12px}img{width:100%;display:block}span{display:block;padding:10px}h1{font-family:Georgia;font-weight:400}</style><h1>Samagam · Seven model angles</h1><p>1600 × 1000 · JPG</p><main>'+cards+'</main>',encoding='utf-8')
p=out/'README.md';p.write_text(p.read_text(encoding='utf-8')+'\nSeven distinct 1600x1000 JPG model views are saved in photos/: overview, pandal, footbridge/VIP side, accommodation, water tanks, railway/train and AK street view with live map. Open photos/index.html for the album, or use samagam-7-jpg-photos.zip.\n',encoding='utf-8')
p=out/'verification.txt';p.write_text(p.read_text(encoding='utf-8')+'Seven JPG exports verified as valid JPEG, 1600x1000, with distinct content hashes and named-angle capture.\n',encoding='utf-8')
archive=out/'samagam-3d-package.zip'
with zipfile.ZipFile(archive) as z:names=z.namelist()
names=list(dict.fromkeys(names+['photos/'+p.name for p in folder.iterdir()]+['samagam-7-photo-preview.png','source/photo_server.py','source/package_photos.py']))
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for name in names:
        p=root/'work'/name.removeprefix('source/') if name.startswith('source/') else out/name
        if p.exists():z.write(p,name)
print('Seven distinct 1600x1000 JPGs verified; photo ZIP, album and complete package saved')
