import json, math, struct, csv, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; OUT=ROOT/'outputs'
objects=[]; labels=[]; routes=[]
def add(name,kind,x,y,z,w,h,d,color,layer='site',ground=''):
    objects.append(dict(name=name,kind=kind,p=[x,y,z],s=[w,h,d],color=color,layer=layer,ground=ground,status='schematic / unmeasured'))
def box(name,x,z,w,d,h=1,color='#b8bd97',y=0,layer='site',ground=''):
    add(name,'box',x,y+h/2,z,w,h,d,color,layer,ground)
def label(text,x,z,y=12): labels.append(dict(text=text,p=[x,y,z]))
def tent(name,x,z,w=30,d=50,color='#ede6d1',ground='B',layer='tents'):
    box(name+' walls',x,z,w,d,5,'#d4cbb4',layer=layer,ground=ground)
    add(name,'roof',x,5,z,w,6,d,color,layer,ground)
    box(name+' open doorway',x,z+d/2+.15,w*.22,.35,4.5,'#504a3c',layer=layer,ground=ground)
    box(name+' door awning',x,z+d/2+2,w*.35,4,.35,color,y=4.8,layer=layer,ground=ground)
    box(name+' roof ridge',x,z,.65,d+.6,.65,'#b7aa8a',y=10.7,layer=layer,ground=ground)
    for dx in [-w*.48,w*.48]:
        box(name+' eave trim',x+dx,z,.7,d+.8,.4,'#c0a578',y=5,layer=layer,ground=ground)
    for dx in [-w/2,w/2]:
        for dz in [-d/2,d/2]: box(name+' pole',x+dx,z+dz,0.8,0.8,6,'#8e8779',layer=layer,ground=ground)

box('Surrounding context — schematic',550,0,2900,2320,2,'#9baf83',y=-4)
for i in range(12):
    for j in range(10):
        x=-720+i*225; z=-1070+j*225
        box('Agricultural context',x,z,208,207,0.3,['#a5b98b','#91a576','#bec59b','#879d72'][(i*7+j)%4],y=-1.9)
# Local axes: x east, z south; outlines and distances are illustrative.
grounds=[('A',325,120,400,620,'#c7bd9c'),('B',-180,610,560,620,'#b8bda1'),('C',-180,-80,560,680,'#b6c2a0'),('D',-180,-750,560,560,'#bec5a8')]
for g,x,z,w,d,c in grounds:
    box('Ground '+g+' envelope (illustrative)',x,z,w,d,0.8,c,y=0,ground=g)
    label('GROUND '+g,x,z-d/2+35)
# NH-44 east, railway west, as observed on Google Maps. Alignment simplified.
box('NH-44 / GT Road',640,0,58,2280,1.3,'#63717a',y=0)
box('Highway median',640,0,4,2280,1.4,'#a3ba87',y=0)
for z in range(-1100,1100,50):
    for x in [625,655]: box('Road marking',x,z,1.1,22,0.1,'#e6e5d9',y=1.35)
label('NH-44 / GT ROAD',640,950,8)
box('Rail corridor',-620,0,28,2280,0.8,'#a5a297')
for x in [-628,-623,-617,-612]: box('Rail',x,0,0.8,2280,0.8,'#596368',y=0.8)
for z in range(-1120,1120,22): box('Rail sleeper',-620,z,23,2,0.4,'#817d70',y=0.8)
box('Bhodwal Majri station — indicative',-580,-940,34,120,5,'#d9d2bd')
label('BHODWAL MAJRI • RAIL',-580,-1030)
for x in [-500,105,550]: box('Internal spine (schematic)',x,0,16,2090,1,'#ddd5bd')
for z in [-450,300,970]: box('Cross avenue (schematic)',0,z,1120,18,1.2,'#ddd5bd')
box('Main arrival avenue',340,440,580,24,1.3,'#d6cdb7')
# Pandal: modular pitched bays, open sides and visible support rows.
box('Main Satsang Pandal platform',325,100,330,340,2,'#c4a98a',layer='pandal',ground='A')
for i in range(10):
    x=176+i*33
    add('Pandal roof bay '+str(i+1),'roof',x,17,100,32,9,340,'#eee5d0' if i%2 else '#d8b77b','pandal','A')
    for z in [-70,15,100,185,270]: box('Pandal column',x,z,1.8,1.8,18,'#a29883',layer='pandal',ground='A')
box('Stage dais (assumed)',325,-40,122,45,6,'#b9745b',layer='pandal',ground='A')
box('Stage backdrop (assumed)',325,-59,122,3,24,'#537d8a',layer='pandal',ground='A')
label('MAIN SATSANG PANDAL',325,105,55)
label('STAGE',325,-48,34)
for x in [245,405]:
    box('Stage LED screen frame',x,-56,29,2,17,'#263e48',y=6,layer='pandal',ground='A')
    box('Stage LED screen panel',x,-54.8,26,.5,14,'#83abb7',y=7,layer='pandal',ground='A')
for x in [220,430]:
    box('Pandal speaker stack',x,-24,5,5,13,'#344146',layer='pandal',ground='A')
for k in range(4):
    box('Stage step',325,-14+k*3,62,3,1.2*(4-k),'#d6b490',layer='pandal',ground='A')
for x in [242,408]:
    for z in range(-7,265,17):
        box('Seating carpet block',x,z,130,12,.3,'#b67d62' if z%2 else '#b08672',y=2.1,layer='pandal',ground='A')
box('Central aisle',325,134,18,285,.35,'#e0c9a3',y=2.2,layer='pandal',ground='A')
objects[:]=[o for o in objects if o['layer']!='pandal']
labels[:]=[l for l in labels if l['text'] not in ['MAIN SATSANG PANDAL','STAGE']]
exec((ROOT/'work/pandal_geometry.py').read_text(encoding='utf-8'))
for g,x0,z0,cols,rows in [('B',-440,360,9,8),('C',-440,-380,9,9),('D',-440,-965,9,6),('A',180,-185,8,2)]:
    for r in range(rows):
        for c in range(cols): tent(f'{g} lodging module {r*cols+c+1:03}',x0+c*59,z0+r*66,34,48,ground=g)
    label('LODGING • '+g,x0+230,z0+rows*66+5)
# Facilities are confirmed categories, but individual footprints are placeholders.
for g,x,z in [('A',480,350),('B',-345,880),('C',-345,230),('D',-345,-550)]:
    tent(g+' langar / canteen placeholder',x,z,95,56,'#cf9166',g,'services')
    box(g+' medical placeholder',x+100,z,34,30,8,'#a9cbd0',layer='services',ground=g)
    box(g+' medical cross 1',x+100,z,18,4,0.4,'#b6564a',y=8,layer='services',ground=g)
    box(g+' medical cross 2',x+100,z,4,18,0.4,'#b6564a',y=8.5,layer='services',ground=g)
    label('LANGAR / SERVICES '+g,x,z+53)
for name,x,z in [('Exhibition',15,110),('Admin / Sewadal',475,-280),('Sant Niwas',455,-380)]:
    tent(name+' placeholder',x,z,62,60,'#90a7b4','A','services'); label(name.upper(),x,z+50)
for g,x,z in [('B',-60,880),('C',-60,230),('D',-60,-550)]:
    box('Gyan Kaksh '+g+' placeholder',x,z,58,32,8,'#baadcb',layer='services',ground=g)
for x,z in [(565,440),(-530,-890)]:
    for dx in [-16,16]: box('Entry pillar placeholder',x+dx,z,6,6,20,'#c6a164',layer='services')
    box('Entry lintel placeholder',x,z,38,5,6,'#c6a164',y=18,layer='services')
label('HIGHWAY ENTRY (INDICATIVE)',555,520)
# A foot overbridge in front of the Samagam near Haldana is confirmed in
# Lok Sabha answer AS11, 1712. Exact geometry and local placement unmeasured.
box('NH-44 footbridge deck — indicative',640,360,146,9.5,1.3,'#b4cad0',y=10,layer='bridges')
box('FOB walking surface — indicative',640,360,146,8,.16,'#e6d3a5',y=11.3,layer='bridges')
for x in [570,640,710]:
    box('FOB pier foundation — indicative',x,360,4,9,.7,'#c5c4b4',layer='bridges')
    box('FOB support pier — indicative',x,360,2.8,5,9.6,'#d0cbbb',y=.7,layer='bridges')
    box('FOB pier cap — indicative',x,360,7,9,1,'#b5bfb7',y=9.3,layer='bridges')
for z in [355.2,364.8]:
    box('FOB edge beam — indicative',640,z,146,.6,1.7,'#366e83',y=9.8,layer='bridges')
    box('FOB handrail — indicative',640,z,146,.28,.28,'#244f66',y=12.9,layer='bridges')
    box('FOB middle railing — indicative',640,z,146,.22,.2,'#6391a0',y=12,layer='bridges')
    for x in range(568,714,4):
        box('FOB railing upright — indicative',x,z,.22,.3,1.55,'#2d6277',y=11.45,layer='bridges')
for side in [570,710]:
    box('FOB stair landing — indicative',side,360,12,14,1.3,'#b4cad0',y=10,layer='bridges')
    box('FOB stair approach pad — indicative',side,410,22,15,.3,'#d5cfb9',layer='bridges')
    for k in range(24):
        zz=368+k*1.65;hh=11.3*(1-k/24)
        box('FOB individual stair tread — indicative',side,zz,9,1.65,hh,'#c7d0c9',layer='bridges')
        box('FOB stair nosing — indicative',side,zz+.7,9,.14,.09,'#f5dfa0',y=hh,layer='bridges')
        for dx in [-4.7,4.7]:
            box('FOB stair rail segment — indicative',side+dx,zz,.24,1.7,.24,'#2e6176',y=hh+1.1,layer='bridges')
            if k%3==0:
                box('FOB stair railing post — indicative',side+dx,zz,.28,.28,1.2,'#416f7f',y=hh,layer='bridges')
label('NH-44 PEDESTRIAN OVERBRIDGE',640,343,22)
labels[-1]['layer']='bridges'
for text,x,z,y in [('WEST STAIRS • VENUE SIDE',570,418,5),('EAST STAIRS • HALDANA SIDE',710,418,5)]:
    label(text,x,z,y);labels[-1]['layer']='bridges';labels[-1]['bridgeDetail']=True
# Parking context, not an assertion about official allocation.
box('Indicative parking pad',350,720,360,310,1,'#aab0a0',layer='parking')
label('PARKING • INDICATIVE',350,930)
for r in range(6):
    for c in range(11):
        box('Vehicle placeholder',200+c*29,610+r*43,13,25,5,['#e5e1d3','#a5b5bf','#6b8189'][c%3],layer='parking')
        box('Vehicle cabin',200+c*29,610+r*43,10,13,3,'#77939b',y=5,layer='parking')
        for dx in [-7,7]:
            for dz in [-8,8]: box('Vehicle wheel',200+c*29+dx,610+r*43+dz,1.7,4,2.5,'#414844',layer='parking')
for r in range(7): box('Parking bay row marking',350,589+r*43,335,1,.12,'#e8e4cc',y=1.1,layer='parking')
for c in range(12):box('Parking bay divider',185+c*29,730,1,284,.12,'#e8e4cc',y=1.1,layer='parking')
# Sanitation banks: separate illustrative M/F/accessible modules per ground.
for g,x,z in [('A',520,260),('B',65,900),('C',65,240),('D',65,-520)]:
    for k,group in enumerate(['Women','Men','Accessible']):
        zz=z-k*23
        box(f'{g} {group} toilet bank placeholder',x,zz,25,18,5.5,'#83aba6',layer='toilets',ground=g)
        for c in range(4 if group!='Accessible' else 2):
            box(f'{g} {group} WC cubicle door',x-9+c*6,zz+9.2,4.8,.6,4,'#d4e1d6',layer='toilets',ground=g)
    box(g+' handwash bank',x-26,z-21,6,50,1.4,'#c0d9cf',layer='toilets',ground=g)
    box(g+' water supply placeholder',x-24,z-56,12,12,8,'#86a8bd',layer='utilities',ground=g)
    box(g+' waste collection placeholder',x-26,z+17,9,10,3,'#799564',layer='utilities',ground=g)
    label('WC / WASH '+g,x,z+27)
box('Service road concept',585,0,20,2150,1,'#bfc3b2',layer='traffic')
box('Bus drop-off pad concept',455,1020,230,65,1,'#b9bca8',layer='parking')
for c in range(5):
    box('Bus placeholder',365+c*43,1020,20,47,12,'#b99c6c',layer='parking')
    box('Bus windows',365+c*43,1020,20.3,36,4,'#688c99',y=6,layer='parking')
label('BUS DROP-OFF • CONCEPT',450,1090)
box('Accessible parking concept',485,510,95,70,1,'#9ebcbc',layer='parking')
label('ACCESSIBLE PARKING • CONCEPT',485,557)
for name,x,z in [('Help / security',540,975),('Rail arrival help',-535,-960),('Fire / ambulance standby',150,320)]:
    box(name+' placeholder',x,z,30,25,7,'#b48d70',layer='utilities'); label(name.upper(),x,z+30)
for z in range(-990,1010,180):
    box('Lighting mast placeholder',122,z,1.5,1.5,22,'#8a8d80',layer='utilities')
    box('Lighting head',122,z,8,4,2,'#d9d8ba',y=22,layer='utilities')
# Routes lie on illustrative service/internal lanes; not a live diversion plan.
def route(name,points,color,layer):
    routes.append(dict(name=name,points=[[x,4,z] for x,z in points],color=color,layer=layer))
    for (x1,z1),(x2,z2) in zip(points,points[1:]):
        assert x1==x2 or z1==z2
        box(name+' segment',(x1+x2)/2,(z1+z2)/2,max(3,abs(x2-x1)),max(3,abs(z2-z1)),.4,color,y=2,layer=layer)
route('Vehicle arrival — proposed',[(581,1080),(581,970),(550,970),(550,875),(350,875)],'#d39a38','traffic')
route('Vehicle departure — proposed',[(520,610),(550,610),(550,440),(590,440),(590,-1060)],'#9b70a7','traffic')
route('Pedestrian railway approach — proposed',[(-560,-940),(-500,-940),(-500,-450),(105,-450),(105,300),(325,300),(325,280)],'#378f99','pedestrian')
route('Pedestrian parking approach — proposed',[(350,580),(350,460),(325,460),(325,300)],'#378f99','pedestrian')
route('Emergency access — proposed',[(573,980),(573,300),(105,300),(105,-450)],'#c26352','emergency')
label('SAMALKHA / PANIPAT ↑',640,-1090)
label('DELHI / SONIPAT ↓',640,1100)
# Nearby settlement masses are context only, not mapped building footprints.
for x0,z0,title in [(-730,-1000,'BHODWAL MAJRI • CONTEXT'),(-730,800,'GARHI JHANJHARA • CONTEXT')]:
    for r in range(4):
        for c in range(3):
            box('Nearby settlement illustrative mass',x0+c*25,z0+r*35,18,24,8+(r+c)%3*4,'#bcb6a5',layer='context')
    label(title,x0+30,z0+160)
# Opposite side: observed Google Maps land cover and public place labels,
# checked 18 Oct 2026. Local offsets, heights and footprints remain approximate.
east_label_start=len(labels)
def road(name,points,width=10,color='#aaa99b'):
    for a,b in zip(points,points[1:]):
        dx=b[0]-a[0]; dz=b[1]-a[1]
        box(name,(a[0]+b[0])/2,(a[1]+b[1])/2,math.hypot(dx,dz),width,.55,color,y=.1,layer='east')
        objects[-1]['rotY']=-math.atan2(dz,dx)
road('East-side frontage / local access, approximate',[(700,-1060),(700,1060)],14)
road('Haldana local road, approximate',[(700,360),(900,360),(1120,205),(1370,60),(1580,-230),(1660,-500)],12)
road('Northern field access, approximate',[(700,-700),(910,-700),(1040,-700),(1040,-1000)],9)
road('Field access grid, approximate',[(700,-250),(1060,-250),(1060,650),(1250,650)],8)
road('Haldana western approach, approximate',[(1390,-1020),(1390,-630),(1450,-420),(1510,-50),(1590,500),(1690,1000)],10)
road('Southeastern local lane, approximate',[(1020,980),(1350,700),(1590,500),(1830,320)],9)
road('Haldana village street, approximate',[(1430,-540),(1740,-540),(1810,-710)],9)
road('Haldana village street, approximate',[(1510,-850),(1510,-360),(1740,-360)],8)
def landmark(name,x,z,w,d,h,color='#b6b4a5',roof=False):
    box(name+' — map-observed, approximate mass',x,z,w,d,h,color,layer='east')
    if roof:add(name+' roof','roof',x,h,z,w,4,d,'#a5afa8','east')
    label(name.upper(),x,z+d/2+28,h+14)
landmark('Woodland factory outlet',755,-620,66,44,10,'#a4b1ab')
landmark('Two Brother Holding',845,-695,80,52,10)
landmark('Singla Farm House Ganaur',835,325,48,45,7,'#b8b5a2')
box('Farm compound — land cover approximate',835,325,154,135,.3,'#6c8b62',layer='east')
for x,z,w,d in [(835,260,154,1),(835,390,154,1),(758,325,1,130),(912,325,1,130)]:
    box('Farm boundary — illustrative',x,z,w,d,1.6,'#a8a994',layer='east')
landmark('Crompton company',780,600,84,120,12,'#afb9ad',True)
landmark('Kundli new cwh',1020,570,110,70,13,'#c1bca6',True)
landmark('Sagar Overseas Foods LLP',1370,65,90,54,12,'#afb6ab',True)
landmark('Krishna Overseas',1500,520,80,85,12,'#adb3a6',True)
landmark('Shanti CA Cold',1230,880,88,105,14,'#b6b9ad',True)
box('Haldana stadium approximate ground',1650,-300,145,105,.7,'#82976a',layer='east')
for x in [1580,1720]:box('Stadium boundary indicative',x,-300,1,105,1.3,'#bcbfa4',layer='east')
label('HALDANA STADIUM',1650,-235)
landmark('Veterinary hospital • Haldana',1580,-470,42,31,7,'#d4c7a9')
for r in range(5):
    for c in range(6):
        if (r*5+c)%7==0:continue
        x=1490+c*47;z=-890+r*67
        box('Haldana building cluster — illustrative footprint',x,z,25+(c%2)*8,30+(r%3)*5,5+(r+c)%3*3,'#c2bcaa',layer='east')
label('HALDANA • VILLAGE CONTEXT',1640,-930,18)
label('EAST OF NH-44 • FIELDS / OPEN PLOTS',1110,-420,10)
for l in labels[east_label_start:]:l['layer']='east'
# Trees outside the ground envelopes, decorative context.
for side in [-555,590]:
    for z in range(-1000,1050,75):
        box('Tree trunk',side,z,2,2,7,'#7c7058',layer='landscape')
        add('Tree canopy','roof',side,5,z,16,15,16,'#638b68','landscape')
exec((ROOT/'work/site_details.py').read_text(encoding='utf-8'))
exec((ROOT/'work/flyover_geometry.py').read_text(encoding='utf-8'))
scene=dict(objects=objects,labels=labels,routes=routes,flyover=flyover_info,meta=dict(title='79th Nirankari Sant Samagam — schematic 3D draft',units='metres, assumed local dimensions',axes='x east / y up / z south; schematic orientation',maps_pin=[29.179636,77.0261412],not_georeferenced=True,date='2026-10-18',geometry_status='Not surveyed. Not a Google 3D extraction. Ground boundaries, tent positions/counts, scale, parking, toilets, flyover dimensions and routes are illustrative. Traffic routes are not approved or validated.'))
(OUT/'scene-data.json').write_text(json.dumps(scene,indent=2),encoding='utf-8')
cubeV=[[-.5,0,-.5],[.5,0,-.5],[.5,1,-.5],[-.5,1,-.5],[-.5,0,.5],[.5,0,.5],[.5,1,.5],[-.5,1,.5]]
cubeF=[[0,3,2,1],[4,5,6,7],[0,1,5,4],[3,7,6,2],[0,4,7,3],[1,2,6,5]]
roofV=[[-.5,0,-.5],[.5,0,-.5],[0,1,-.5],[-.5,0,.5],[.5,0,.5],[0,1,.5]]
roofF=[[0,2,1],[3,4,5],[0,3,5,2],[1,2,5,4],[0,1,4,3]]
rampV=[[-.5,0,-.5],[.5,0,-.5],[-.5,0,.5],[.5,0,.5],[-.5,1,-.5],[.5,1,-.5]]
rampF=[[0,4,5,1],[4,2,3,5],[0,1,3,2],[0,2,4],[1,5,3]]
# GLB shares geometries by shape and material; all nodes retain readable names.
gltf=dict(asset={'version':'2.0','generator':'Samagam schematic reconstruction','extras':scene['meta']},scene=0,scenes=[{'nodes':[]}],nodes=[],meshes=[],materials=[],buffers=[],bufferViews=[],accessors=[])
binary=bytearray(); geometry={}; mats={}; meshes={}
def accessor(data,fmt,typ,component,target):
    while len(binary)%4: binary.append(0)
    off=len(binary); flat=[v for row in data for v in row] if isinstance(data[0],list) else data
    binary.extend(struct.pack('<'+str(len(flat))+fmt,*flat)); bv=len(gltf['bufferViews'])
    gltf['bufferViews'].append(dict(buffer=0,byteOffset=off,byteLength=len(binary)-off,target=target))
    a=dict(bufferView=bv,componentType=component,count=len(data),type=typ)
    if typ=='VEC3': a.update(min=[min(p[i] for p in data) for i in range(3)],max=[max(p[i] for p in data) for i in range(3)])
    gltf['accessors'].append(a); return len(gltf['accessors'])-1
for kind,V,F in [('box',cubeV,cubeF),('roof',roofV,roofF),('ramp',rampV,rampF)]+[(key,*value) for key,value in extra_shapes.items()]:
    verts=[]; normals=[]; inds=[]
    for face in F:
        a,b,c=[V[k] for k in face[:3]]; u=[b[i]-a[i] for i in range(3)]; v=[c[i]-a[i] for i in range(3)]
        n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]; ln=math.sqrt(sum(k*k for k in n)); n=[k/ln for k in n]
        base=len(verts); verts.extend([V[k] for k in face]); normals.extend([n]*len(face))
        for j in range(1,len(face)-1): inds.extend([base,base+j,base+j+1])
    geometry[kind]=(accessor(verts,'f','VEC3',5126,34962),accessor(normals,'f','VEC3',5126,34962),accessor(inds,'H','SCALAR',5123,34963))
for o in objects:
    color=o['color']
    if color not in mats:
        mats[color]=len(gltf['materials']); rgb=[int(color[i:i+2],16)/255 for i in [1,3,5]]
        gltf['materials'].append(dict(name=color,pbrMetallicRoughness=dict(baseColorFactor=rgb+[1],metallicFactor=0,roughnessFactor=.9),doubleSided=True))
    key=(o['kind'],color)
    if key not in meshes:
        meshes[key]=len(gltf['meshes']); p,n,ix=geometry[o['kind']]
        gltf['meshes'].append(dict(primitives=[dict(attributes={'POSITION':p,'NORMAL':n},indices=ix,material=mats[color])]))
    pos=o['p'].copy()
    if o['kind']=='box':
        if 'quaternion' in o:
            qx,qy,qz,qw=o['quaternion'];hh=o['s'][1]/2
            pos[0]-=2*(qx*qy-qw*qz)*hh;pos[1]-=(1-2*(qx*qx+qz*qz))*hh;pos[2]-=2*(qy*qz+qw*qx)*hh
        else:pos[1]-=o['s'][1]/2
    gltf['scenes'][0]['nodes'].append(len(gltf['nodes']))
    angle=o.get('rotY',0)
    gltf['nodes'].append(dict(name=o['name'],mesh=meshes[key],translation=pos,scale=o['s'],rotation=o.get('quaternion',[0,math.sin(angle/2),0,math.cos(angle/2)]),extras={'layer':o['layer'],'ground':o['ground'],'status':o['status'],'part':o.get('part','body')}))
gltf['buffers']=[{'byteLength':len(binary)}]
gltf['asset']['extras']['vehicle_flyover_context']=flyover_info
j=json.dumps(gltf,separators=(',',':')).encode(); j+=b' '*((-len(j))%4); binary+=b'\0'*((-len(binary))%4)
glb=struct.pack('<III',0x46546c67,2,12+8+len(j)+8+len(binary))+struct.pack('<II',len(j),0x4e4f534a)+j+struct.pack('<II',len(binary),0x004e4942)+binary
(OUT/'samagam-schematic.glb').write_bytes(glb)
# A separate, recentered GLB makes the off-site structure convenient to edit.
fly_gltf=json.loads(json.dumps(gltf))
fly_gltf['nodes']=[n for n in fly_gltf['nodes'] if n['extras']['layer']=='flyover']
for node in fly_gltf['nodes']:
    node['translation'][0]-=fly_x;node['translation'][2]-=fly_z
fly_gltf['scenes']=[{'nodes':list(range(len(fly_gltf['nodes'])))}]
fly_gltf['asset']['extras']=flyover_info
fj=json.dumps(fly_gltf,separators=(',',':')).encode();fj+=b' '*((-len(fj))%4)
fglb=struct.pack('<III',0x46546c67,2,12+8+len(fj)+8+len(binary))+struct.pack('<II',len(fj),0x4e4f534a)+fj+struct.pack('<II',len(binary),0x004e4942)+binary
(OUT/'samalkha-nh44-flyover.glb').write_bytes(fglb)
with (OUT/'model-inventory.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['Name','Layer','Ground','X assumed m','Y assumed m','Z assumed m','Width assumed m','Height assumed m','Depth assumed m','Yaw radians','Status'])
    for o in objects: w.writerow([o['name'],o['layer'],o['ground'],*o['p'],*o['s'],o.get('rotY',0),o['status']])
template=(ROOT/'work/viewer-v2.html').read_text(encoding='utf-8')
template=template.replace('__SCENE__',json.dumps(scene,separators=(',',':'))).replace('__SHAPES__',json.dumps({'box':[cubeV,cubeF],'roof':[roofV,roofF],'ramp':[rampV,rampF],**extra_shapes}))
(OUT/'samagam-3d.html').write_text(template,encoding='utf-8')
print(f'Built {len(objects)} mesh nodes, {len(glb):,} byte GLB; lodging modules: '+str(sum(o['kind']=='roof' and o['layer']=='tents' for o in objects)))
