from pathlib import Path
import json,subprocess,numpy as np,trimesh
from PIL import Image
root=Path(__file__).resolve().parents[1];out=root/'outputs';dest=out/'health-centre-reference';dest.mkdir(exist_ok=True)
signs=[dict(key='health-hindi',lines=['दादी जानकी','पॉजिटिव हेल्थ केयर सेन्टर, ज्ञान मानसरोवर, थिराना, पानीपत -132103'],size=[15,1.4],bg='#e4e7dd',fg='#a25839'),dict(key='health-english',lines=['DADI JANKI','Positive Health Care Centre','Organised by','GYAN MANSAROVAR, PANIPAT'],size=[3,1.25],bg='#e3e9e0',fg='#884c4e')]
records=root/'work/health-signs.json';records.write_text(json.dumps(signs,ensure_ascii=False),encoding='utf8')
subprocess.run(['powershell','-NoProfile','-ExecutionPolicy','Bypass','-File',str(root/'work/render_signs.ps1'),'-RecordsPath',str(records),'-OutputDirectory',str(dest)],check=True)
scene=trimesh.Scene()
def box(name,p,s,color):
 m=trimesh.creation.box(extents=s);m.visual.vertex_colors=np.tile(list(bytes.fromhex(color))+[255],(len(m.vertices),1));m.apply_translation(p);scene.add_geometry(m,node_name=name)
box('White single-storey facade study • footprint/depth/height estimated',[0,2.4,0],[16,4.8,6],'eeeee4')
box('Projecting flat roof',[0,4.85,.2],[16.5,.25,6.8],'e4e5dc')
box('Door recess',[0,1.75,3.02],[2.7,3.4,.08],'626c6c')
for x in [-5.1,5.1]:
 box('Side window',[x,2.1,3.04],[2,2.5,.08],'8b9692')
 for dx in [-1,0,1]:box('White window frame',[x+dx,2.1,3.12],[.06,2.55,.09],'eeeeea')
 box('Window transom',[x,2.7,3.12],[2,.07,.09],'eeeeea')
for x in [-1.35,0,1.35]:box('White door jamb',[x,1.75,3.12],[.07,3.45,.09],'eeeeea')
for y in [.08,1.25,2.9,3.45]:box('White door transom',[0,y,3.12],[2.75,.07,.09],'eeeeea')
for key,p,s in [('health-hindi',[0,4.5,3.65],[15.7,.8,1]),('health-english',[0,3.75,3.18],[3,.6,1])]:
 m=trimesh.Trimesh(vertices=[[-.5,-.5,0],[.5,-.5,0],[.5,.5,0],[-.5,.5,0]],faces=[[0,1,2],[0,2,3]],process=False)
 m.visual=trimesh.visual.TextureVisuals(uv=[[0,0],[1,0],[1,1],[0,1]],material=trimesh.visual.material.PBRMaterial(baseColorTexture=Image.open(dest/f'{key}.png'),doubleSided=True))
 m.apply_transform(trimesh.transformations.translation_matrix(p)@np.diag(s+[1]));scene.add_geometry(m,node_name=key)
for x in [-6.6,-4.8,4.8,6.6]:box('Front sill',[x,.82,3.18],[.4,.1,.18],'e4e5dc')
(out/'dadi-janki-health-centre-facade-study.glb').write_bytes(scene.export(file_type='glb'))
(dest/'README.txt').write_text('Standalone facade study from Screenshot 110248 (Jan 2022). NO georeference or campus placement is assigned. Only the visible front is supported; dimensions, depth and unseen sides are illustrative. Sign spellings follow the visible source; lettering colours approximated. Roof icons, worn paint, door advertisements and small illegible labels are not exact replicas. No connection to a particular satellite roof has been established.',encoding='utf8')
print('Standalone health-centre facade GLB written; no geographic placement assigned.')
