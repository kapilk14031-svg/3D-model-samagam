import json, math, pathlib, numpy as np, trimesh

ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs'; OUT.mkdir(exist_ok=True)
objects=[]
colors={'stone':'#eae3d5','white':'#f5f5f2','roof':'#374151','glass':'#6ba5d6','grass':'#4a9c2a','tree':'#2d7a2e','bark':'#422817','paving':'#eae2d3','road':'#32373f','pink':'#e8739a','gold':'#f59e0b','proposal':'#d97706','seat':'#cbd5e1','dark':'#1f2937','context':'#94a3b8','flower':'#f43f5e','wood':'#b47b48','carpet':'#16a34a','light':'#fef08a','acoustic':'#e2e8f0'}
def add(name,p,s,mat='stone',shape='box',group='campus',rot=0):
    objects.append(dict(name=name,p=p,s=s,mat=mat,shape=shape,group=group,rot=rot))
def box(name,x,y,z,w,h,d,mat='stone',group='campus',rot=0):add(name,[x,y,z],[w,h,d],mat,group=group,rot=rot)
def cyl(name,x,y,z,r,h,mat='stone',group='campus'):add(name,[x,y,z],[r,h,r],mat,'cylinder',group)
def sphere(name,x,y,z,rx,ry,rz,mat='tree',group='campus'):add(name,[x,y,z],[rx,ry,rz],mat,'sphere',group)
box('Context ground • extent illustrative',-20,-.7,0,280,1,220,'grass','context')
box('Core compound • approximate satellite footprint',0,-.05,0,120,.4,120,'paving')
box('Assan–Thirana Road • schematic alignment',-18,.03,-67,270,.2,9,'road',rot=.12)
for x in range(-140,120,14):box('Road marking',x,.16,-67-x*.12,5,.02,.15,'white')
box('East approach lane',64,.1,-2,5,.2,137,'road')
for x in [-61,61]:box('Compound wall • boundary approximate',x,1,8,.5,2,105)
box('South boundary',0,1,62,122,2,.5)
box('North boundary west',-42,1,-61,38,2,.5)
box('North boundary east',34,1,-61,54,2,.5)
for x in [-20,-6]:box('Entry pier • position inferred',x,2.6,-61,1.4,5.2,1.4,'white')
box('Entry beam • shape indicative',-13,5.4,-61,16,1,1.5,'stone')
box('Entry driveway',-13,.22,-54,11,.15,18,'paving')
# West main roofed footprint. Identification and exact dimensions remain provisional.
box('Hall floor • ~42 x 66 m assumed envelope',-40,.5,-10,42,1,66,'wood')
box('Hall west wall',-61,5,-10,.5,9,66,'white')
box('Hall east wall',-19,5,-10,.5,9,66,'white','shell')
box('Hall north wall',-40,5,-43,42,9,.5,'white','shell')
box('Hall south wall',-40,5,23,42,9,.5,'white','shell')
box('Hall roof • assumed height',-40,9.8,-10,44,.7,68,'roof','roof')
for z in range(-38,24,8):
    for x in [-60.6,-19.4]:box('Hall glazing • arrangement illustrative',x,5,z,.2,2.4,4,'glass','shell')
box('Raised stage • recent photo reference; orientation inferred',-40,1.5,-35,34,1.2,10,'wood','interior')
box('Stage backdrop • photo inspired',-40,4.1,-39.6,25,4.8,.35,'pink','interior')
cyl('Meditation focal point',-40,5,-39.3,.7,.12,'gold','interior')
for i in range(5):box('Green carpet stage stair',-40,1.05+i*.12,-27.8-i*.6,7,.15+i*.24,.6,'carpet','interior')
for x in [-43.7,-36.3]:
    for z in [-27,-28,-29,-30]:cyl('Stair railing post',x,2.1,z,.045,1,'gold','interior')
    box('Stair handrail • indicative',x,2.7,-28.6,.07,.07,4,'gold','interior')
for x in range(-55,-24,2):box('Stage front flowers',x,2,-29.8,1.3,.45,.5,'flower','interior')
for x in [-51,-45.5,-40,-34.5,-29]:
    box('Stage sofa • photo inspired',x,2.5,-35,4.2,.7,1.5,'white','interior')
    box('Stage sofa back',x,3.15,-35.7,4.2,.7,.3,'white','interior')
for r in range(28):
    z=-20+r*1.4
    for c in range(30):
        x=-56.8+c*1.05+(3.1 if c>=15 else 0)
        box('Illustrative audience seat',x,1.3,z,.7,.15,.72,'seat','seating')
        box('Illustrative chair back',x,1.75,z+.34,.7,.78,.12,'seat','seating')
        for dx in [-.39,.39]:box('Chair armrest',x+dx,1.65,z,.07,.08,.7,'gold','seating')
box('Central aisle • photo inspired',-40.5,1.03,-1,2.4,.03,44,'paving','interior')
for x in [-60.6,-19.4]:
    for z in range(-36,23,4):
        box('Acoustic wall panels • photo inspired',x,6.3,z,.15,3,3.3,'acoustic','shell')
        box('Curtain below acoustic panels',x,3.1,z,.18,2,2.6,'stone','shell')
for z in range(-37,22,6):
    for x in range(-57,-20,6):box('Ceiling light panel • illustrative pattern',x,9.35,z,1.5,.05,1.5,'light','ceiling')
    for x in [-51,-29]:
        cyl('Speaker suspension',x,8.8,z,.04,1.1,'dark','ceiling')
        box('Hanging speaker • photo inspired',x,8.1,z,.4,.8,.5,'dark','ceiling')
box('Hall pink facade parapet • recent photos',-18.5,7.9,-10,1,1.1,66,'pink','shell')
for z in range(-38,24,8):
    box('Hall facade pilaster',-18.4,3.9,z,.8,7, .5,'stone','shell')
    add('Scalloped facade arch • simplified',[-18.2,4.9,z+4],[3.5,1.6,.3],'stone','arch','shell',math.pi/2)
    box('Facade warm uplight',-17.8,1.6,z,.15,.35,.4,'gold','shell')
# Lawn and pavilion positions read approximately from the aerial image.
box('Central lawn',26,.25,8,49,.25,44,'grass')
box('Lawn north path',26,.4,-17,50,.15,3,'stone')
box('Lawn south path',26,.4,33,50,.15,3,'stone')
box('Lawn west path',0,.4,8,3,.15,52,'stone')
box('Lawn east path',52,.4,8,3,.15,52,'stone')
cyl('Lotus pavilion circular plinth',32,.7,-45,11,1.1)
cyl('Lotus pavilion steps',32,1.4,-45,9.5,.6,'white')
cyl('Meditation pavilion drum • photo inspired',32,4.3,-45,6,5.2,'white')
for a in range(0,360,45):
    t=math.radians(a); x=32+6.05*math.cos(t);z=-45+6.05*math.sin(t)
    box('Pavilion glazing',x,4.4,z,1.8,3,.18,'glass',rot=-t+math.pi/2)
for a in range(0,360,30):
    t=math.radians(a); sphere('Lotus petal • stylised',32+7.5*math.cos(t),2.5,-45+7.5*math.sin(t),1.2,2,1.2,'pink')
sphere('Pavilion dome • stylised',32,7,-45,6.5,3.1,6.5,'white','roof')
cyl('Pavilion finial',32,10.4,-45,.2,1.1,'gold')
# South two-storey building facade based on Maps photos, divisions inferred.
box('South building ground floor',0,2.3,51,112,4.6,17,'white','shell')
box('South building upper floor',0,6.8,51,112,4.4,17,'white','shell')
box('South building roof',0,9.2,51,115,.5,19,'roof','roof')
box('Upper gallery rail',0,5.3,41.8,112,.8,.25,'stone')
for x in range(-52,57,8):
    box('Facade column',x,4.5,41.5,.65,9,.7,'stone')
    for y in [2,6.7]:box('Facade window',x+2,y,42.3,3,2,.2,'glass','shell')
box('Central entrance glass',0,2.3,41.9,8,4.1,.2,'glass','shell')
box('Central portico frame',0,5,40.7,13,9.5,1.2,'stone','shell')
box('Front steps',0,.35,38,14,.5,5,'stone')
for x in [-42,-17,15,42]:box('Solar panel • photo inspired',x,9.8,51,9,.25,4,'glass','roof',rot=0)
# Context buildings are visible nearby but ownership/function cannot be verified.
box('West covered block A • ownership/use unverified',-94,4.8,21,18,9.6,119,'context','context')
box('West block A roof',-94,9.8,21,20,.5,121,'roof','context')
box('West covered block B • ownership/use unverified',-119,4,3,26,8,74,'context','context')
box('West block B roof',-119,8.3,3,28,.5,76,'roof','context')
box('East block • ownership/use unverified',91,3.4,-44,29,6.8,44,'context','context')
for y in [2,5,8,11,14]:
    box('Unfinished multi-storey block • seen in local photos; position approximate',51,y,47,19,.4,16,'context','context')
    for x in [42,48,54,60]:box('Unfinished block column',x,y+1.2,47,.7,2.5,16,'context','context')
for x,z in [(-5,-25),(54,-45),(54,-25),(54,6),(54,22),(-54,35),(-34,35),(30,36),(-75,-54),(-85,-54)]:
    cyl('Landscape tree trunk',x,1.6,z,.35,3,'bark');sphere('Landscape tree canopy',x,4.4,z,2.3,3.1,2.3)
# Event overlay deliberately independent from existing geometry.
for name,x,w,mat in [('VVIP lounge • proposed',-40,22,'proposal'),('Reception • proposed',-14,23,'proposal'),('Medical / support • proposed',13,23,'proposal'),('Dining / service • proposed',40,22,'proposal')]:
    box(name,x,.8,51,w,.15,14,mat,'event')
    box('Proposed room partition',x+w/2,2.3,51,.15,3,14,'proposal','event')
    if x==-40:
        for z in [47,55]:box('Lounge sofa • proposed',x,1.5,z,12,1.2,1.4,'white','event')
        box('Lounge table • proposed',x,1.3,51,7,.7,2,'gold','event')
    elif x==40:
        for z in [47,52,56]:box('Dining table • proposed',x,1.3,z,12,.5,1.8,'white','event')
    else:box('Reception/support desk • proposed',x,1.6,51,9,1.2,2,'white','event')
box('Reception canopy • proposed',-9,3,-52,6,.25,4,'proposal','event')
for x in [-12,-6]:cyl('Canopy post • proposed',x,1.6,-52,.1,2.8,'proposal','event')
for i in range(4):
    x=-51+i*5.5
    box('Indicative visitor parking bay • feasibility unverified',x,.36,-53,4.6,.05,7,'proposal','event')
    box('Parked vehicle • illustrative',x,1.3,-53,2,1.7,4.3,'dark','event')
# Refine core spacing against closer 20 m scale satellite inspection.
for o in objects:
    if o['p'][2]>=38 and o['p'][2]<=56 and o['group'] not in ['context'] and (o['name'].startswith(('South building','Upper gallery','Facade column','Facade window','Central entrance','Central portico','Front steps','Solar panel','VVIP lounge','Reception •','Medical /','Dining /','Proposed room','Lounge ','Dining table','Reception/support'))):
        o['p'][2]-=12
    if o['name'].startswith(('Central lawn','Lawn ')):
        o['p'][2]-=12
    if o['name'].startswith(('Lotus pavilion','Meditation pavilion','Pavilion ','Lotus petal')):
        o['p'][0]-=4
box('Garden cross path north-south • satellite visible',23,.43,-4,2,.12,44,'stone')
box('Garden cross path east-west • satellite visible',26,.44,-4,49,.12,2,'stone')
for z in range(-30,26,8):
    for x in [-9,55]:
        cyl('Garden bollard lamp • local photo reference',x,.85,z,.12,1.3,'dark')
        sphere('Garden lamp globe',x,1.55,z,.32,.28,.32,'light')
for x,z in [(0,-25),(51,-23),(52,17),(1,18),(-9,30)]:
    cyl('Palm trunk • local photo reference',x,3,z,.25,5.5,'bark')
    for angle in range(0,360,60):
        a=math.radians(angle)
        add('Palm frond • simplified',[x+1.6*math.cos(a),6,z+1.6*math.sin(a)],[2.6,.23,.55],'tree','sphere','campus',-a)
for x in [-57,-23]:
    box('Stage decorative pillar • photo inspired',x,4.1,-38.5,.7,4,.8,'gold','interior')
box('Lectern • photo inspired',-54,2.85,-32,1.2,1.5,.9,'wood','interior')
for z in range(-37,23,4):
    for y in [5.1,6.2,7.3]:
        for x in [-60.4,-19.6]:box('Acoustic panel grid • photo inspired',x,y,z,.12,.85,3.5,'white','shell')
box('South rear narrow roof wing • satellite footprint',14,3.8,54,89,7.6,9,'white')
box('South rear wing roof',14,7.8,54,91,.4,10,'roof','roof')
box('Southwest service annex • satellite footprint',-49,3,43,16,6,26,'white','shell')
box('Southwest service annex roof',-49,6.2,43,17,.4,27,'roof','roof')
labels=[['Auditorium*',[-40,12,-10],'Dadi Chandramani Universal Peace Auditorium interior supported by local photos/videos; placement and dimensions approximate.'],['Lotus meditation',[28,12,-45],'Exterior form supported by public photographs; size estimated.'],['Central lawn',[28,2,-4],'Position estimated from satellite view.'],['South building',[0,12,39],'Two-storey facade supported by public photos. Room uses unverified.'],['West blocks*',[-108,12,12],'Visible nearby roofed blocks; ownership and use unverified.'],['East block*',[91,10,-44],'Visible nearby building; ownership and use unverified.']]
from refine_scene import refine
objects,colors=refine(objects,colors)
from detail_surroundings import detail
objects,colors,signs=detail(objects,colors)
labels[0][0]='Dadi Chandermani Auditorium';labels[3][0]='Dadi Prakashmani Residential Complex'
labels.extend([['North landscaped plot*',[-165,7,-155],'Satellite context; site ownership and function unverified.'],['Birmi Industries (map listing)*',[201,15,37],'Google Maps listing; approximate context footprint, not a verified physical facade sign.'],['Birmi Impex (map listing)*',[335,15,12],'Google Maps listing; approximate context footprint, not a verified physical facade sign.']])
labels.append(['Gyan Mansarovar campus',[0,18,0],'Core compound; detailed photo/video-informed reconstruction.'])
from geometry_profiles import paint_and_architecture,SCALLOP,extruded_polygon
objects,colors=paint_and_architecture(objects,colors)
from detail_lotus_v8 import refine_lotus,DOME,MESHES
objects,colors,signs=refine_lotus(objects,colors,signs)
from detail_photo_buildings import improve
objects=improve(objects)
from detail_side_gates import improve_gate
objects=improve_gate(objects)
from detail_youtube import improve as youtube_details
objects,colors=youtube_details(objects,colors)
from correct_stage_stairs import correct as correct_stage_stairs
objects=correct_stage_stairs(objects)
from register_scene import register
objects,colors,signs,labels,georeference=register(objects,colors,signs,labels)
from detail_helipad import add_helipad
objects,colors,georeference=add_helipad(objects,colors,georeference)
data={'objects':objects,'colors':colors,'labels':labels,'origin':{'latitude':29.413077,'longitude':76.848831,'coordinateFrame':'local metres, +X east, +Z south; schematic alignment'},'assumptions':{'geometry':'Satellite/photo informed schematic, not survey or photogrammetry','hall':[42,66,9.8],'coreCompound':[120,120],'audienceSeatsIllustrated':320,'seatCountIsCapacity':False,'event':'All room assignments, partitions, parking and furniture are proposals','heights':'Estimated; not measured','boundary':'Approximate visual core only; legal ownership not verified'},'sources':[{'title':'Google Maps: supplied venue pin, satellite and public photographs','url':'https://maps.app.goo.gl/JG881XSsXu1Vi61L9?g_st=aw','accessed':'2026-10-20'},{'title':'Brahma Kumaris Panipat: auditorium name and event report','url':'https://panipat.bk.ooo/?p=2036','note':'Search-indexed report identifies Dadi Chandramani Universal Peace Auditorium; exact roofed footprint not established.'}]}
data['assumptions']['audienceSeatsIllustrated']=840
data['signs']=signs
data['georeference']=georeference
hallq=np.array(next(f['points'] for f in georeference['footprints'] if f['id']=='hall'));data['assumptions']['hall']=[float(np.linalg.norm(hallq[1]-hallq[0])),float(np.linalg.norm(hallq[3]-hallq[0])),9.8]
data['profiles']={'scallopedSpandrel':SCALLOP,'lotusDome':DOME,'lotusMeshes':MESHES}
data['origin']['coordinateFrame']='WGS84 registered local metres: +X east, +Y up, +Z south; origin is the supplied Maps pin; altitude unknown.'
data['assumptions']['geometry']='Displayed Google Earth graticule registered reconstruction. Footprints manually digitised; elevations and unobserved details estimated, not surveyed.'
data['assumptions']['hallAlignment']='Revised toward southern residential end from gate-to-portico/side-entry photo-video sequence; still not a measured registration.'
data['assumptions']['surroundings']='Schematic satellite massing of adjoining agricultural parcels, industrial roofs, landscaped enclosure and diagonal rural road (confirmed using standard Google Maps view); ownership not established.'
data['sources'].append({'title':'User supplied WhatsApp Unknown 2026-10-20 at 9.45.02 AM.zip','photos':65,'videos':9,'review':'All photo contact sheets and 147 frames covering nine full video durations at 2-second intervals plus first/last frames reviewed; no audio transcription.','observations':['Scalloped frontage with pink parapet','Classroom signage','Portico and glass entrance','Raised stage with green carpet stairs','Cream chairs with arms and centre aisle','Acoustic wall panels','Ceiling light grid and suspended speakers','Landscaped paths and lotus pavilion','Unfinished multi-storey block visible near building','Side entrance near stage shown continuously in video 9','Green stage fascia with gold trim','Metal-framed upholstered seats with rounded backs','Pleated beige curtains','Two stage lighting crossbars','Large slab garden path and red/yellow peripheral paving']})
data['sources'].append({'title':'User supplied WhatsApp Unknown 2026-10-20 at 10.43.32 AM.zip','photos':11,'videos':0,'review':'All eleven Google Earth screenshot images visually reviewed at full resolution. Satellite capture date unknown; phone time is not imagery date.','observations':['Concentric pavilion terraces','Small solar panel banks on blue roof','Approach and eastern circulation lanes','Southern roof arrays and adjacent fields','Wider industrial roofs and BAMC roof lettering'],'limits':'Adds satellite context; no new measured height, ground facade, gate paint, interior photograph or survey control.'})
data['sources'].append({'title':'12 new architectural references: screenshots 110115–110332, 110902 and Retreat-centre-Panipat-5.jpg','review':'All inspected; several depict 2016–2022 historical states. Updated lotus curved petal courses, open entrance, fan stair, front garden; balcony/roof rails; both pedestrian side gates.','limits':'Counts/dimensions estimated. Current 2026 finish/signs take precedence. Health-centre footprint not verified; separate facade study supplied.'})
data['sources'].extend([{'title':'Brahma Kumaris Panipat garden short','url':'https://www.youtube.com/shorts/Z506BEp8GG4','review':'Seven approximate positions over 12.34 seconds; garden, lanterns and red-roof hut compared.'},{'title':'Gyan Mansarovar campus tour','url':'https://www.youtube.com/watch?v=qjMKc4im7YQ','review':'33 targeted timestamp views across 25:29; auto-captions used as navigation only. See YOUTUBE-DETAIL-REVIEW.md for coverage and unresolved lettering.'}])
data['assumptions']['meditationInterior']='Partial older-tour reconstruction; object arrangement approximate. Portrait/artwork and unresolved donation-box text not reproduced.'
data['assumptions']['stageAccess']='User site correction: two side staircases, left and right; no central stage staircase. Widths, rises and railing dimensions remain estimated.'
(OUT/'model-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'work/signs.json').write_text(json.dumps(signs,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'observed-signage.json').write_text(json.dumps(signs,ensure_ascii=False,indent=2),encoding='utf-8')
import subprocess
subprocess.run(['powershell','-NoProfile','-ExecutionPolicy','Bypass','-File',str(ROOT/'work/render_signs.ps1')],check=True)
scene=trimesh.Scene()
base={'box':trimesh.creation.box(), 'sphere':trimesh.creation.icosphere(subdivisions=1), 'cylinder':trimesh.creation.cylinder(radius=1,height=1,sections=20)}
base['sphereSmooth']=trimesh.creation.icosphere(subdivisions=2)
base['torus']=trimesh.creation.torus(major_radius=1,minor_radius=.09,major_sections=24,minor_sections=8)
base['sign']=trimesh.Trimesh(vertices=[[-.5,-.5,0],[.5,-.5,0],[.5,.5,0],[-.5,.5,0]],faces=[[0,1,2],[0,2,3]],process=False)
base['spandrel']=extruded_polygon(SCALLOP)
base['lotusDome']=trimesh.creation.revolve(np.array(DOME),sections=64)
base['lotusDome'].apply_transform(trimesh.transformations.rotation_matrix(-math.pi/2,[1,0,0]))
for name,mesh in MESHES.items():
    base[name]=trimesh.Trimesh(vertices=mesh['vertices'],faces=mesh['faces'],process=False)
leaf=[[-.5,-.5],[-.5,-.1],[-.3,.4],[0,1],[.3,.4],[.5,-.1],[.5,-.5]]
v=[[x,y,z] for z in [-.5,.5] for x,y in leaf];n=len(leaf);f=[]
for j in range(n):
    k=(j+1)%n;f.extend([[j,k,k+n],[j,k+n,j+n]])
for j in range(1,n-1):f.extend([[0,j+1,j],[n,n+j,n+j+1]])
base['petal']=trimesh.Trimesh(vertices=v,faces=f,process=False)
outline=[]
for cx,cy,a0 in [(.34,.34,0),(-.34,.34,90),(-.34,-.34,180),(.34,-.34,270)]:
    for j in range(5):
        a=math.radians(a0+j*22.5);outline.append([cx+.16*math.cos(a),cy+.16*math.sin(a)])
v=[[x,y,z] for z in [-.5,.5] for x,y in outline];n=len(outline);f=[]
for j in range(n):
    k=(j+1)%n;f.extend([[j,k,k+n],[j,k+n,j+n]])
for j in range(1,n-1):f.extend([[0,j+1,j],[n,n+j,n+j+1]])
base['rounded']=trimesh.Trimesh(vertices=v,faces=f,process=False)
# trimesh cylinders use Z as vertical; rotate to glTF Y-up.
base['cylinder'].apply_transform(trimesh.transformations.rotation_matrix(math.pi/2,[1,0,0]))
verts=[];faces=[]
for k in range(17):
    a=k*math.pi/16
    for r,z in [(1,-.5),(.82,-.5),(1,.5),(.82,.5)]:verts.append([r*math.cos(a),r*math.sin(a),z])
for k in range(16):
    j=k*4;n=j+4
    for a,b,c,d in [(j,n,n+1,j+1),(j+2,j+3,n+3,n+2),(j,j+2,n+2,n),(j+1,n+1,n+3,j+3)]:faces.extend([[a,b,c],[a,c,d]])
base['arch']=trimesh.Trimesh(vertices=verts,faces=faces,process=False)
from PIL import Image
from material_textures import create as create_material_textures
surface_textures=create_material_textures(OUT)
for shape,mat in set((o['shape'],o['mat']) for o in objects):
    m=base[shape].copy();rgba=list(bytes.fromhex(colors[mat][1:]))+[255]
    if shape=='sign':
        material=trimesh.visual.material.PBRMaterial(name=mat,baseColorTexture=Image.open(OUT/'sign-textures'/f'{mat}.png').convert('RGBA'),baseColorFactor=[255,255,255,255],roughnessFactor=1,doubleSided=True)
        m.visual=trimesh.visual.TextureVisuals(uv=[[0,0],[1,0],[1,1],[0,1]],material=material)
    elif mat in surface_textures:
        axes=[0,2] if mat=='wood' else [2,1] if mat=='acoustic' else [0,1]
        uv=m.vertices[:,axes].copy();lo=uv.min(axis=0);span=np.maximum(np.ptp(uv,axis=0),.001);uv=(uv-lo)/span
        material=trimesh.visual.material.PBRMaterial(name=mat,baseColorTexture=surface_textures[mat],baseColorFactor=[255,255,255,255],roughnessFactor=.92 if mat!='wood' else .72)
        m.visual=trimesh.visual.TextureVisuals(uv=uv,material=material)
    else:m.visual=trimesh.visual.ColorVisuals(m,vertex_colors=np.tile(rgba,(len(m.vertices),1)))
    scene.geometry[shape+'_'+mat]=m
for i,o in enumerate(objects):
    t=trimesh.transformations.translation_matrix(o['p']) @ trimesh.transformations.rotation_matrix(o['rot'],[0,1,0]) @ trimesh.transformations.rotation_matrix(o.get('tilt',0),[1,0,0]) @ trimesh.transformations.rotation_matrix(o.get('rz',0),[0,0,1]) @ np.diag(o['s']+[1])
    scene.graph.update(frame_to=f"{o['group']}__{i}__{o['name']}",matrix=t,geometry=o['shape']+'_'+o['mat'],metadata={'status':o['group']})
import struct
blob=scene.export(file_type='glb');jn=struct.unpack('<I',blob[12:16])[0];tree=json.loads(blob[20:20+jn]);tree['asset']['extras']={'georeference':{'crs':'EPSG:4326','origin':data['origin'],'axes':'+X east,+Y up,+Z south','eastMetresPerDegree':georeference['eastMetresPerDegree'],'northMetresPerDegree':georeference['northMetresPerDegree'],'status':'screenshot-graticule registered; altitude and absolute survey accuracy unknown'}}
jblob=json.dumps(tree,separators=(',',':')).encode();jblob+=b' '*((-len(jblob))%4);tail=blob[20+jn:];(OUT/'gyan-mansarovar-concept.glb').write_bytes(struct.pack('<4sII',b'glTF',2,20+len(jblob)+len(tail))+struct.pack('<I4s',len(jblob),b'JSON')+jblob+tail)
(ROOT/'work'/'scene-inline.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
print(f'{len(objects)} objects; GLB written')
