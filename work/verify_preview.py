import json,struct,math,pathlib,zipfile
from PIL import Image,ImageDraw,ImageFont
P=pathlib.Path(__file__).resolve().parents[1]/'outputs'
b=(P/'samagam-schematic.glb').read_bytes();magic,version,total=struct.unpack_from('<III',b)
assert magic==0x46546c67 and version==2 and total==len(b)
n,t=struct.unpack_from('<II',b,12);g=json.loads(b[20:20+n]);assert t==0x4e4f534a
assert len(g['nodes'])==len(json.loads((P/'scene-data.json').read_text())['objects'])
for a in g['accessors']:
    v=g['bufferViews'][a['bufferView']];assert v['byteOffset']+v['byteLength']<=g['buffers'][0]['byteLength']
s=json.loads((P/'scene-data.json').read_text(encoding='utf-8'));assert all(o['s'][i]>0 for o in s['objects'] for i in range(3))
html=(P/'samagam-3d.html').read_text(encoding='utf-8');assert '__SCENE__' not in html and '__SHAPES__' not in html
# Static projection of the same mesh data, with correct foreground order.
ns={};exec((P.parent/'work/build_model.py').read_text().split('# GLB shares')[0].split("(OUT/'scene-data.json')")[0],{'__file__':str(P.parent/'work/build_model.py')},ns) if False else None
V=[[-.5,0,-.5],[.5,0,-.5],[.5,1,-.5],[-.5,1,-.5],[-.5,0,.5],[.5,0,.5],[.5,1,.5],[-.5,1,.5]]
F=[[0,3,2,1],[4,5,6,7],[0,1,5,4],[3,7,6,2],[0,4,7,3],[1,2,6,5]]
RV=[[-.5,0,-.5],[.5,0,-.5],[0,1,-.5],[-.5,0,.5],[.5,0,.5],[0,1,.5]];RF=[[0,2,1],[3,4,5],[0,3,5,2],[1,2,5,4],[0,1,4,3]]
im=Image.new('RGB',(1600,1320),'#e6ebdf');d=ImageDraw.Draw(im)
fontpath='C:/Windows/Fonts/segoeui.ttf'
font=ImageFont.truetype(fontpath,17);title=ImageFont.truetype(fontpath,34);sub=ImageFont.truetype(fontpath,20)
yaw=-.72;pitch=.83;scale=.44
def project(p):
    x,y,z=p;a=x*math.cos(yaw)+z*math.sin(yaw);q=-x*math.sin(yaw)+z*math.cos(yaw)
    return (800+a*scale,680+(q*math.sin(pitch)-y*math.cos(pitch))*scale,q*math.cos(pitch)+y*math.sin(pitch))
polys=[]
for oi,o in enumerate(s['objects']):
    vv,ff=(V,F) if o['kind']=='box' else (RV,RF)
    pp=[project([o['p'][i]+v[i]*o['s'][i]-(o['s'][i]/2 if i==1 and o['kind']=='box' else 0) for i in range(3)]) for v in vv]
    for fi,f in enumerate(ff):
        if o['layer']=='site' and fi!=3: continue
        pts=[pp[k] for k in f];area=sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(pts,pts[1:]+pts[:1]))
        if area>=0:continue
        shade=[.82,.9,.7,1.04,.77,.95][fi];c=o['color'];rgb=tuple(min(255,round(int(c[i:i+2],16)*shade)) for i in [1,3,5])
        key=(0,o['p'][1]) if o['layer']=='site' else (1,sum(p[2] for p in pts)/len(pts))
        polys.append((key,[(p[0],p[1]) for p in pts],rgb))
for key,pts,c in sorted(polys,key=lambda x:x[0]): d.polygon(pts,fill=c)
for r in s['routes']:
    pp=[project(p) for p in r['points']];d.line([(p[0],p[1]) for p in pp],fill=r['color'],width=4)
occupied=[]
for l in s['labels']:
    x,y,_=project(l['p']);text=l['text'].replace('↑','N').replace('↓','S');bb=d.textbbox((0,0),text,font=font);w=bb[2]+12;h=27;rect=(x-w/2,y-h/2,x+w/2,y+h/2)
    if any(rect[0]<r[2] and rect[2]>r[0] and rect[1]<r[3] and rect[3]>r[1] for r in occupied):continue
    occupied.append(rect);d.rectangle(rect,fill='#f8f6eb');d.text((x-w/2+6,y-h/2+1),text,font=font,fill='#264637')
d.rectangle((0,0,1600,135),fill='#173e34');d.text((40,23),'79th Nirankari Sant Samagam',font=title,fill='#f6f2e5');d.text((40,78),'Bhodwal Majri / NH-44  |  Schematic 3D draft  |  18 October 2026',font=sub,fill='#cbdcc9')
d.rectangle((0,1220,1600,1320),fill='#faf8ef');d.text((35,1234),'Tents / Pandal / Toilets / Parking / Foot overbridge / Proposed traffic routes',font=sub,fill='#244738');d.text((35,1270),'Illustrative geometry and routes. Exact positions, dimensions and official traffic plan are unverified.',font=sub,fill='#7b602d')
im.save(P/'samagam-overview.png')
with zipfile.ZipFile(P/'samagam-3d-package.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name in ['samagam-3d.html','samagam-3d-basic.html','samagam-schematic.glb','scene-data.json','model-inventory.csv','samagam-overview.png','README.md']:z.write(P/name,name)
print(f"Verified GLB header, {len(g['nodes'])} nodes, accessors, positive dimensions, HTML data injection. Preview and ZIP created.")
