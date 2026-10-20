import json, math, struct, csv, pathlib, re, zipfile
from pdf_plan_data import *
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'outputs'
objects=[];labels=[];routes=[];extra_shapes={};current=''
exec((ROOT/'work/pandal_geometry.py').read_text(encoding='utf-8').split('def pb(')[0])
def add(name,kind,x,y,z,w,h,d,color,layer='site',ground=''):
    objects.append(dict(name=name,kind=kind,p=[x,y,z],s=[w,h,d],color=color,layer=layer,ground=ground,status='PDF relative position; height and scale illustrative',featureId=current))
def box(name,x,z,w,d,h=1,color='#b8bd97',y=0,layer='site',ground=''):
    add(name,'box',x,y+h/2,z,w,h,d,color,layer,ground)
def line(name,pts,width,h,color,layer,y=0):
    for a,b in zip(pts,pts[1:]):
        dx=b[0]-a[0];dz=b[2]-a[2];length=math.hypot(dx,dz)
        if length<.01:continue
        box(name,(a[0]+b[0])/2,(a[2]+b[2])/2,length,width,h,color,y,layer)
        objects[-1]['rotY']=-math.atan2(dz,dx)
def polygon(name,points,color,layer,height=.35):
    key='poly'+str(len(extra_shapes));pts=[planpoint(*p) for p in points]
    vs=[[p[0],y,p[2]] for y in [0,height] for p in pts];n=len(pts)
    fs=[list(range(n-1,-1,-1)),list(range(n,2*n))]+[[i,(i+1)%n,(i+1)%n+n,i+n] for i in range(n)]
    extra_shapes[key]=[vs,fs];add(name,key,0,0,0,1,1,1,color,layer)
def loc(f):
    if f.get('bbox'):
        u,v,r,b=f['bbox'];return (u+r)/2,(v+b)/2
    if f.get('path'):return tuple(sum(p[k] for p in f['path'])/len(f['path']) for k in [0,1])
    return None
exec((ROOT/'work/road_details.py').read_text(encoding='utf-8'))
exec((ROOT/'work/underpass_details.py').read_text(encoding='utf-8'))
exec((ROOT/'work/facility_details.py').read_text(encoding='utf-8'))
exec((ROOT/'work/gate_details.py').read_text(encoding='utf-8'))
exec((ROOT/'work/residence_details.py').read_text(encoding='utf-8'))
exec((ROOT/'work/office_details.py').read_text(encoding='utf-8'))
exec((ROOT/'work/petrol_details.py').read_text(encoding='utf-8'))
exec((ROOT/'work/station_details.py').read_text(encoding='utf-8'))
box('Plan terrain',-150,0,1950,2500,2,'#9b805c',-3)
for f in features:
    current=f['id'];k=f['kind'];uv=loc(f)
    f['representation']='indexed source annotation'
    if not uv:continue
    x,_,z=planpoint(*uv);f['world']=[x,8,z]
    layer={'pandal':'pandal','parking':'parking','toilets':'toilets','road':'context','internal_road':'context','rail':'context','wall':'context','flyover':'bridges','underpass':'bridges','utility':'utilities','village':'east','gate':'gates'}.get(k,'services')
    f['layer']=layer
    if k not in ['symbols','metadata']:
        labels.append(dict(text=f['id']+' · '+f['name'],p=[x,18,z],layer=layer,featureId=current))
    if f.get('path') and k in ['road','internal_road','rail','wall','utility']:
        p=[planpoint(*q) for q in f['path']];width=36 if k=='road' else 12 if k=='internal_road' else 5 if k=='rail' else 1.8
        if k in ['road','internal_road']:
            detailed_road(f,p,width);f['representation']='Continuous traced road mesh; illustrative surface and lane detailing';continue
        line(f['name'],p,width,1.1 if k!='wall' else .35 if current=='W29' else 2.6,'#566362' if k=='road' else '#d7cfba' if k=='internal_road' else '#68685a',layer)
        if k=='rail':
            for a,b in zip(p,p[1:]):
                length=math.dist(a,b)
                for t in range(0,int(length),9):
                    v=[a[i]+(b[i]-a[i])*t/length for i in range(3)];box('Railway sleeper',v[0],v[2],7,1,.15,'#b5a787',1.2,layer)
        if k=='utility':
            for p0 in p:
                box('HT tower',p0[0],p0[2],3,3,24,'#777d76',0,layer);box('HT crossarm',p0[0],p0[2],12,1,1,'#777d76',20,layer)
        f['representation']='3D traced polyline';continue
    if k=='flyover':
        p=[planpoint(*q) for q in f['path']];detailed_flyover(p)
        f['representation']='Continuous flyover deck, sloped ramps, lane markings, parapets and supports; assumed structure';continue
    if k in ['point','village','symbols','metadata'] or f['id'] in ['B11','B23']:continue
    if f.get('bbox'):
        u,v,r,b=f['bbox'];w=(b-v)*PLAN_SCALE;d=(r-u)*PLAN_SCALE;poly=[[u,v],[r,v],[r,b],[u,b]]
    else:
        poly=f['path'];p=[planpoint(*q) for q in poly];w=max(q[0] for q in p)-min(q[0] for q in p);d=max(q[2] for q in p)-min(q[2] for q in p)
    if k=='pandal':
        # Fit the canopy in the narrowest section of the traced pandal footprint.
        # The former polygon-average centre pushed the rectangular roof toward NH44.
        w*=.86
        x=min(q[0] for q in p)+w/2+4
        z=(min(q[2] for q in p)+max(q[2] for q in p))/2
        f['world']=[x,8,z]
        f['detail']+='; roof narrowed and inset to keep clear of NH44'
        for l in labels:
            if l.get('featureId')==current:l['p'][0]=x;l['p'][2]=z
    if k in ['parking','plot','alighting','pandal']:
        polygon(f['name'],poly,{'parking':'#c0b99f','plot':'#9b9e7b','alighting':'#b5c3bd','pandal':'#d5c49a'}[k],layer)
    elif k=='underpass':
        corrected_underpass(f,x,z,w,d)
    elif k=='gate':
        premium_gate(f,x,z,w,d)
    elif current=='H05':
        detailed_station(f,x,z,w,d)
    elif current=='B15':
        indian_oil_pump(f,x,z,w,d)
    elif current=='B03':
        four_floor_office(f,x,z,w,d)
    elif current=='B13':
        modern_residence(f,x,z,w,d)
    else:
        h=4 if k=='toilets' else 6
        box(f['name'],x,z,max(w,3),max(d,3),h,'#73a9a5' if k=='toilets' else '#c5b694',0,layer)
        add(f['name']+' roof','roof',x,h,z,max(w,3),3,max(d,3),'#e8dfc9',layer)
        if k=='toilets':
            for xx in range(int(-w/2+3),int(w/2),6):box('Toilet cubicle door',x+xx,z+d/2+.1,3,.2,3,'#477e7c',.1,layer)
    if k in ['building','toilets'] and current not in ['B13','B03','B15']:detailed_facility(f,x,z,max(w,3),max(d,3),h)
    if k=='parking':
        vp=[planpoint(*q) for q in poly]
        def inside(px,pz):
            hit=False
            for aa,bb in zip(vp,vp[1:]+vp[:1]):
                if (aa[2]>pz)!=(bb[2]>pz) and px<(bb[0]-aa[0])*(pz-aa[2])/(bb[2]-aa[2])+aa[0]:hit=not hit
            return hit
        bike=current=='P04';heavy=current in ['P02','P03','P06'];stepx=5 if bike else 16;stepz=7 if bike else 29 if heavy else 20
        count=0
        for dx in range(int(-w*.38),int(w*.4),stepx):
            for dz in range(int(-d*.38),int(d*.4),stepz):
                px=x+dx;pz=z+dz;bus=heavy and count%3!=2
                hw,hd=(1.6,2.5) if bike else (5,11) if bus else (4,7)
                if all(inside(px+sx*hw,pz+sz*hd) for sx in [-1,1] for sz in [-1,1]):
                    parked_vehicle(f,px,pz,bus,bike,count);count+=1
    if k=='pandal':
        # Canopy follows the source envelope; decorative architecture is illustrative.
        nx=48;nz=72;vs=[];fs=[]
        def canopy_height(xx,zz):
            arch=math.sqrt(max(0,1-(xx*2)**2))
            # Fabric sags softly between repeated longitudinal support lines.
            sag=.025*math.sin((zz+.5)*math.pi*12)**2*arch
            folds=.0035*math.sin(xx*math.pi*38)*math.sin((zz+.5)*math.pi)*arch
            return arch-sag+folds
        for iz in range(nz+1):
            zz=iz/nz-.5
            for j in range(nx+1):
                xx=j/nx-.5;vs.append([xx,canopy_height(xx,zz),zz])
        for iz in range(nz):
            for j in range(nx):
                a=iz*(nx+1)+j;fs.append([a,a+nx+1,a+nx+2,a+1])
        extra_shapes['fabriccanopy']=[vs,fs]
        # Narrow stitched seams sit on the curved fabric, inside its footprint.
        seamv=[];seamf=[]
        for sx in [-.375,-.25,-.125,0,.125,.25,.375]:
            first=len(seamv)
            for iz in range(nz+1):
                zz=iz/nz-.5
                for xx in [sx-.0017,sx+.0017]:seamv.append([xx,canopy_height(xx,zz)+.003,zz])
            for iz in range(nz):
                a=first+iz*2;seamf.append([a,a+2,a+3,a+1])
        extra_shapes['canopystitch']=[seamv,seamf]
        bays=1;bw=w/bays
        for n in range(bays):
            xx=x-w/2+bw*(n+.5);add('Pandal curved fabric roof','fabriccanopy',xx,20,z,bw,16,d,'#f6edda','pandal');objects[-1]['part']='roof'
            add('Pandal raised stitched fabric seams','canopystitch',xx,20,z,bw,16,d,'#a77b42','pandal');objects[-1]['part']='roof'
            for zz in [z-d/2,z+d/2]:
                add('Scalloped wine fabric valance','valance',xx,17,zz,bw,3,1,'#804952','pandal');objects[-1]['part']='roof'
                box('Golden canopy border',xx,zz,bw,1.3,.35,'#dac48b',20,'pandal')
                for j in range(16):
                    q1=j/16-.5;q2=(j+1)/16-.5
                    a=[xx+q1*bw,20+16*math.sqrt(max(0,1-(q1*2)**2)),zz]
                    b=[xx+q2*bw,20+16*math.sqrt(max(0,1-(q2*2)**2)),zz]
                    # Roof ribs follow the curved fabric silhouette.
                    dx=b[0]-a[0];dy=b[1]-a[1];length=math.hypot(dx,dy)
                    box('Curved canopy rib',(a[0]+b[0])/2,zz,length,.6,.5,'#c6b58d',(a[1]+b[1])/2,'pandal')
                    angle=math.atan2(dy,dx);objects[-1]['quaternion']=[0,0,math.sin(angle/2),math.cos(angle/2)]
                for dx in range(int(-bw/2+4),int(bw/2),8):box('Fabric hanging trim',xx+dx,zz,.6,1,2.6,'#c5a36c',13.5,'pandal')
        for xx in [x-w/2+1,x+w/2-1]:
            for zz in range(int(z-d/2+3),int(z+d/2-2),35):box('Pandal support column',xx,zz,1,1,20,'#15191c',0,'pandal')
        box('Pandal carpet',x,z,w*.94,d*.92,.2,'#bda17c',.7,'pandal')
        for row in range(4):
            for col in range(9):
                xx=x-w*.27+col*w*.078;zz=z-d*.36+row*d*.235
                box('Illustrative seating carpet panel',xx,zz,w*.065,d*.19,.15,'#a96061',1,'pandal')
        for zz in [z-d*.31,z+d*.31]:
            add('Illustrative stage arch','arch',x-w*.4,5,zz,8,11,d*.18,'#dcc68e','pandal');objects[-1]['rotY']=1.5707963
        for zz in [z-d/2-5,z+d/2+5]:
            for j in range(12):
                xx=x-w/2+12+j*(w-24)/11
                box('Decorative planter',xx,zz,3,3,2,'#9c8d6d',0,'pandal')
                add('Decorative topiary','ellipsoid',xx,2,zz,5,5,5,'#648268','pandal')
                box('Warm architectural light post',xx,zz,.5,.5,9,'#8d9c92',0,'pandal')
                add('Lantern diffuser','ellipsoid',xx,9,zz,1.5,1.4,1.5,'#f0d6a0','pandal')
        box('Central aisle',x,z,9,d,.25,'#8d4247',1,'pandal')
        box('Illustrative stage platform',x-w*.33,z,w*.22,d*.8,2,'#b69d69',1,'pandal')
        box('Illustrative stage backdrop',x-w*.43,z,2,d*.78,11,'#416c6c',3,'pandal')
        for zz in [z-d*.34,z+d*.34]:box('Stage display screen',x-w*.415,zz,1,d*.15,5,'#305860',7,'pandal')
    f['representation']='3D footprint and illustrative structure'
    if k=='pandal':enhance_pandal(f,x,z,w,d)
raise_highway_at_underpasses()
exec((ROOT/'work/reference_tents.py').read_text(encoding='utf-8'))
exec((ROOT/'work/vip_gate.py').read_text(encoding='utf-8'))
exec((ROOT/'work/frontage_boundary.py').read_text(encoding='utf-8'))
exec((ROOT/'work/p5_parking.py').read_text(encoding='utf-8'))
exec((ROOT/'work/foot_overbridge.py').read_text(encoding='utf-8'))
exec((ROOT/'work/realistic_environment.py').read_text(encoding='utf-8'))
exec((ROOT/'work/railway_train.py').read_text(encoding='utf-8'))
exec((ROOT/'work/water_supply.py').read_text(encoding='utf-8'))
amusement_info={'status':'Removed at user request; R18 rear parcel now contains reference-style residential tents'}
exec((ROOT/'work/aligned_routes.py').read_text(encoding='utf-8'))
for route_index,route in enumerate(plan_routes):
    current=route['id'];p=road_aligned_route(route,route_index)
    chunks=[[]]
    for q in p:
        if chunks[-1] and math.dist(chunks[-1][-1],q)>12:chunks.append([])
        chunks[-1].append(q)
    for part in chunks:
        if len(part)<2:continue
        ribbon(route['id']+' road-aligned path',part,.55,.035,route['color'],'traffic')
        routes.append(dict(name=route['id'],points=part,color=route['color'],layer='traffic',width=.55,status='Visual route family snapped to schematic road axes; not turn-by-turn guidance'))
# User-requested dark-brown railway track and sleepers.
for o in objects:
    if o['featureId']=='H06':o['color']='#493025' if o['name']=='Railway sleeper' else '#38291f'
# Golden-brown pandal fabric with warm golden illumination.
gold_bay=0
for o in objects:
    if o['layer']!='pandal':continue
    if o['name']=='Pandal curved fabric roof':
        o['color']='#b78743' if gold_bay%2==0 else '#c69a55';gold_bay+=1
    elif 'fabric valance' in o['name'] or 'wine fabric valance' in o['name']:o['color']='#805230'
    elif 'Golden canopy border' in o['name']:o['color']='#d6b16a'
    if any(term in o['name'].lower() for term in ['canopy rib','support column','tent truss','tie beam','guy line']):o['color']='#15191c'
# User-requested facility identification colours.
for o in objects:
    if o['featureId'] in ['B09','B10','B11','B12']:
        if o['kind']=='roof':o['color']='#163b66'
        elif o['name']=='LANGAR':o['color']='#284d76'
        elif 'canopy' in o['name'] or 'veranda' in o['name']:o['color']='#1d456f'
        elif 'eave fascia' in o['name']:o['color']='#527498'
    elif o['featureId']=='B17':
        if o['kind']=='roof' or 'canopy' in o['name'] or 'eave fascia' in o['name']:o['color']='#244f87'
        elif o['name']=='POLICE CHOWKI' or 'corner trim' in o['name']:o['color']='#b43545'
        elif 'entrance door' in o['name'] or 'window mullion' in o['name']:o['color']='#285b9d'
# Threefold boundary-wall height; the low internal pandal divider is not a boundary wall.
boundary_ids={f['id'] for f in features if f['kind']=='wall' and f['id']!='W29'}
for o in objects:
    if o['featureId'] in boundary_ids:
        o['p'][1]*=3;o['s'][1]*=3
        o['status']+='; boundary wall height multiplied by 3 at user request'
# User-requested vertical emphasis; footprints and source positions stay fixed.
height_factors={f['id']:(1.25 if f['kind']=='pandal' else 1.30) for f in features if f['kind'] in ['pandal','building','toilets','station']}
for o in objects:
    factor=height_factors.get(o['featureId'])
    if not factor:continue
    if 'quaternion' in o:
        # Bake a world-vertical stretch for sloped truss members without moving their x/z endpoints.
        qx,qy,qz,qw=o.pop('quaternion');vv=[]
        for xx,yy,zz in [[-.5,-.5,-.5],[.5,-.5,-.5],[.5,.5,-.5],[-.5,.5,-.5],[-.5,-.5,.5],[.5,-.5,.5],[.5,.5,.5],[-.5,.5,.5]]:
            xx*=o['s'][0];yy*=o['s'][1];zz*=o['s'][2]
            tx=2*(qy*zz-qz*yy);ty=2*(qz*xx-qx*zz);tz=2*(qx*yy-qy*xx)
            vv.append([o['p'][0]+xx+qw*tx+qy*tz-qz*ty,(o['p'][1]+yy+qw*ty+qz*tx-qx*tz)*factor,o['p'][2]+zz+qw*tz+qx*ty-qy*tx])
        key='heightdetail'+str(len(extra_shapes));extra_shapes[key]=[vv,[[0,3,2,1],[4,5,6,7],[0,1,5,4],[3,7,6,2],[0,4,7,3],[1,2,6,5]]]
        o['kind']=key;o['p']=[0,0,0];o['s']=[1,1,1]
    else:o['p'][1]*=factor;o['s'][1]*=factor
    o['status']+='; user-requested illustrative vertical emphasis'
for l in labels:
    if l.get('featureId') in height_factors:l['p'][1]=max(l['p'][1],48 if l['layer']=='pandal' else 20)
meta=dict(title='79th Nirankari Sant Samagam — PDF traffic plan reconstruction',units='assumed local scale; not measured',axes='x east / y up / z south; source rotated north-up',maps_pin=[29.179636,77.0261412],not_georeferenced=True,date='2026-10-19',geometry_status='Source plan relative layout. Heights, architecture and scale illustrative. Unclear scan labels explicitly flagged. Route overlays are traced diagram families, not approved navigation.')
meta['reference_accommodation']=reference_tent_info
meta['amusement_zone']=amusement_info
meta['p5_parking']=p5_info
meta['s04_footbridge']=footbridge_info
meta['underpasses']=underpass_nav
meta['railway_train']=train_info
meta['water_supply']=water_info
meta['highway_boundary']=frontage_info
meta['vip_access']='PDF has invited guests / VIP parking and green route L11, without a separately named VIP gate. An additional user-proposed VIP gate is modelled at I-PARKING near Gate 2.'
meta['ground_finish']='Illustrative grass, dry turf and exposed soil shading in the interactive viewer; not mapped land-cover evidence. GLB retains a grass-coloured base surface.'
flyover_info={'local_anchor':planpoint(1100,950),'status':'Local Gate 3 flyover marked in PDF; structure illustrative'}
meta['sleeping_tents']={'status':'User-added proposal, not source PDF inventory','count':len(sleeping_tent_centres),'regions':sorted({t['camp'] for t in sleeping_tent_centres})}
(OUT/'sleeping-tent-layout.json').write_text(json.dumps(sleeping_tent_centres,indent=2),encoding='utf-8')
scene=dict(objects=objects,labels=labels,routes=routes,features=features,flyover=flyover_info,meta=meta)
(OUT/'scene-data.json').write_text(json.dumps(scene,indent=2),encoding='utf-8')
(OUT/'pdf-detail-register.json').write_text(json.dumps(features,indent=2),encoding='utf-8')
with (OUT/'pdf-detail-register.csv').open('w',newline='',encoding='utf-8-sig') as fp:
    wr=csv.writer(fp);wr.writerow(['ID','PDF label','Category','Source page','Detail','Reading status','Model representation'])
    for f in features:wr.writerow([f['id'],f['name'],f['kind'],1,f['detail'],f['status'],f['representation']])
# Reuse the verified GLB mesh exporter, without its former off-site flyover export.
src=(ROOT/'work/build_model.py').read_text(encoding='utf-8');export=src[src.index('cubeV='):src.index('# A separate, recentered GLB')]
export=export.replace('doubleSided=True))',"doubleSided=True,emissiveFactor=([min(1,c*1.65+.06) for c in rgb] if color in {r['color'] for r in plan_routes} else [0,0,0])))")
export=export.replace('else [0,0,0]',"else ([.35,.19,.045] if color in ['#b78743','#c69a55'] else [0,0,0])")
export=export.replace('else [0,0,0]',"else ([.45,.13,.015] if color in ['#b94d18','#dc7b24','#f0a044'] else [0,0,0])")
export=export.replace("(OUT/'samagam-schematic.glb').write_bytes(glb)", "(ROOT/'work/updated-model.glb').write_bytes(glb); (ROOT/'work/updated-model.glb').replace(OUT/'samagam-schematic.glb')")
exec(export)
template=(ROOT/'work/viewer-pdf.html').read_text(encoding='utf-8')
template=template.replace('__SCENE__',json.dumps(scene,separators=(',',':'))).replace('__SHAPES__',json.dumps({'box':[cubeV,cubeF],'roof':[roofV,roofF],'ramp':[rampV,rampF],**extra_shapes}))
(OUT/'samagam-3d.html').write_text(template,encoding='utf-8')
assert len({f['id'] for f in features})==len(features)
assert all(f['representation'] for f in features)
with (OUT/'model-inventory.csv').open('w',newline='',encoding='utf-8-sig') as fp:
    wr=csv.writer(fp);wr.writerow(['Feature ID','Mesh name','Layer','Status'])
    for o in objects:wr.writerow([o['featureId'],o['name'],o['layer'],o['status']])
print(len(features),'source entries;',len(objects),'mesh nodes;',len(glb),'GLB bytes')
