import json,math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]

def register(objects,colors,signs,labels):
    geo=json.loads((ROOT/'work/georeference.json').read_text(encoding='utf-8'))
    fit=np.array(geo['pixelToLonLat']); ex=geo['eastMetresPerDegree']; ny=geo['northMetresPerDegree']; origin=[geo['originLongitude'],geo['originLatitude']]
    def pixel(p):
        lon,lat=np.array([*p,1])@fit
        return np.array([(lon-origin[0])*ex,(origin[1]-lat)*ny])
    def ll(p):return [origin[0]+p[0]/ex,origin[1]-p[1]/ny]
    old=np.array([[-40,-10,1],[28,-45,1],[0,39,1]])
    target=np.array([pixel([585,400]),pixel([840,255]),pixel([750,590])]);glob=np.linalg.solve(old,target)
    def trans(p,m=glob):return np.array([p[0],p[1],1])@m
    features=[
      ('hall','Main auditorium roof / envelope',[[515,257],[659,251],[670,520],[526,526]],'campus','Estimated height; interior registration inferred'),
      ('garden','Central garden enclosure',[[720,331],[920,323],[928,506],[728,514]],'campus','Visible paths and lawns; not a legal boundary'),
      ('south','Southern building footprint union',[[525,546],[976,527],[982,654],[531,673]],'campus','Roof massing visible; internal room use not established'),
      ('rear','South rear roof wing',[[670,641],[982,628],[984,664],[672,677]],'campus','Roof outline manually digitised'),
      ('construction','Southwest annex / construction block',[[520,548],[645,543],[649,645],[524,650]],'campus','Registration of construction status inferred from photos'),
      ('west-a','West adjacent covered block A',[[321,264],[410,260],[423,564],[334,568]],'context','Ownership and height unverified'),
      ('west-b','West adjacent covered block B',[[217,318],[318,314],[330,604],[229,609]],'context','Ownership and height unverified'),
      ('west-c','West adjacent covered block C',[[109,326],[210,322],[223,618],[122,622]],'context','Partly obscured in screenshot; outline approximate'),
      ('east-blue','Eastern blue-roof building',[[1017,181],[1125,176],[1133,358],[1025,363]],'context','Ownership/use/height unverified'),
      ('red','Small red-roof structure',[[938,397],[967,396],[968,428],[939,429]],'campus','Function/date unverified'),
      ('industrial-east','Eastern industrial roof visible in screenshot',[[1250,155],[1370,150],[1385,443],[1265,448]],'context','Partial footprint; screen overlays obscure remaining extent'),
    ]
    footprints=[]
    for key,name,pts,group,note in features:
        pts=[pixel(p).tolist() for p in pts]
        footprints.append(dict(id=key,name=name,points=pts,group=group,status=note,source='Google Earth user screenshot with visible one-arcsecond graticule'))
    footprints.append(dict(id='pavilion',name='Lotus meditation pavilion circular plinth',points=[(pixel([840,255])+np.array([12*math.cos(a),12*math.sin(a)])).tolist() for a in np.linspace(0,math.tau,32,endpoint=False)],group='campus',status='Circular plinth read from image; height/detail based on photos',source='Graticule screenshot and ground photos'))
    def matrix_for(key,bounds):
        pts=np.array(next(f['points'] for f in footprints if f['id']==key));xmin,zmin,xmax,zmax=bounds
        u=(pts[1]-pts[0])/(xmax-xmin);v=(pts[3]-pts[0])/(zmax-zmin);offset=pts[0]-xmin*u-zmin*v
        return np.array([u,v,offset])
    hm=matrix_for('hall',[-61,-43,-19,23]);gm=matrix_for('garden',[1.5,-26,50.5,18])
    pc=pixel([840,255]); gate=pixel([685,215]);gdelta=gate-trans([-13,-61])
    transform_by_id={}
    removeprefix=('West covered block','West block ','West covered block roof rib','East block •','Unfinished multi-storey','Unfinished block column','Southwest service annex','South rear narrow roof wing','South rear wing roof')
    objects[:]=[o for o in objects if not o['name'].startswith(removeprefix)]
    def region(o):
        x,y,z=o['p'];n=o['name'];mat=o['mat']
        if n.startswith(('Hall ','Stage ','Raised stage','Meditation focal','Green carpet','Stair ','Sloping stainless','Lectern','Ceiling ','Hanging speaker','Speaker suspension','Square acoustic','Rear wall acoustic','Vertical curtain','Backdrop ','Central backdrop','Central emblem','Side exhibition','Low stage','Gold fascia','Fascia garland','Gold ceremonial','Ceremonial chair','White suspended','Scalloped frontage','Dark window frame','Window illuminated','Facade gold','Facade warm','Facade niche','Niche white','Classroom ','External black entry','Entrance stainless','Entrance handrail','Open glazed','Side entrance')) or o['group'] in ['seating','interior','ceiling'] or mat in ['sign-auditorium','sign-classroom','sign-literature']:
            return 'hall'
        if n.startswith(('Lotus ','Meditation pavilion','Pavilion ')):return 'pavilion'
        if n.startswith(('Central lawn','Lawn ','Garden cross','Garden large','Garden red border','Garden yellow border','Clipped garden')):return 'garden'
        if n.startswith(('Entry pier','Entry beam','Entry driveway','Open gate','Gate ','Entrance threshold','Entrance white')) or mat=='sign-gate':return 'gate'
        return 'global'
    def apply(o,m):
        p=trans([o['p'][0],o['p'][2]],m)
        # Dimensions are in each mesh's LOCAL axes. A side-facing arch's
        # width runs along world Z, so applying world-X scale left gaps.
        r=o['rot'];u=np.array([math.cos(r),-math.sin(r)])@m[:2];v=np.array([math.sin(r),math.cos(r)])@m[:2]
        o['p'][0],o['p'][2]=p.tolist();o['s'][0]*=np.linalg.norm(u);o['s'][2]*=np.linalg.norm(v);o['rot']=math.atan2(-u[1],u[0])
    for o in objects:
        r=region(o);oldp=o['p'].copy()
        if r=='hall':apply(o,hm)
        elif r=='garden':apply(o,gm)
        elif r=='pavilion':
            p=pc+(np.array([oldp[0],oldp[2]])-np.array([28,-45]))*1.045;o['p'][0],o['p'][2]=p.tolist();o['s'][0]*=1.045;o['s'][2]*=1.045
        else:
            apply(o,glob)
            if r=='gate':o['p'][0]+=gdelta[0];o['p'][2]+=gdelta[1]
        transform_by_id[o['name']]=r
    # Keep every sign's register consistent with its actual mesh placement.
    for s in signs:
        o=next(o for o in objects if o['mat']==s['key']);s['p']=o['p'].copy();s['rot']=o['rot'];s['size']=[o['s'][0],o['s'][1]];s['longitudeLatitude']=ll([o['p'][0],o['p'][2]])
    for i,l in enumerate(labels):
        p=trans([l[1][0],l[1][2]],hm if i==0 else glob);l[1][0],l[1][2]=p.tolist()
        if i==1:l[1][0],l[1][2]=pc.tolist()
    # Map listings checked directly on 20 Oct 2026. A business pin is not a
    # cadastral boundary or evidence of physical facade lettering.
    listings=[('Luft india',29.4133618,76.8499721),('BAMC Medical',29.4134342,76.8502209),('Birmi Industries Private Limited',29.4138875,76.8512636)]
    def listing_position(lat,lon,height=12):return [(lon-origin[0])*ex,height,(origin[1]-lat)*ny]
    labels[4]=['पश्चिमी इमारतें • नाम अपुष्ट',labels[4][1],'Three roofed buildings visible west of the auditorium. Official names and ownership are not verified; no service/business name assigned.']
    labels[5]=['Luft india (map listing)',listing_position(listings[0][1],listings[0][2],10),'Verified map listing beside the blue-roof building; exact legal roof association and facade lettering unverified.']
    labels[:]=[l for l in labels if not l[0].startswith(('Birmi Industries','Birmi Impex'))]
    for name,lat,lon in listings[1:]:labels.append([name+' (map listing)',listing_position(lat,lon,15),'Verified Google Maps listing position; no fabricated painted sign or ownership boundary.'])
    geo['verifiedMapListings']=[dict(name=n,latitude=lat,longitude=lon,source='Google Maps place listing selected directly, 2026-10-20',status='Listing pin only; cadastral ownership and facade text unverified') for n,lat,lon in listings]
    for f in footprints:
        if f['id']=='east-blue':
            f['name']='Blue-roof building beside Luft india map listing';f['status']='Nearby Luft india listing checked; ownership and exact roof association not established.'
        if f['id']=='industrial-east':
            f['name']='BAMC Medical • partial industrial roof beside verified map pin';f['status']='Map listing and BAMC roof lettering corroborate industrial context; legal boundary/height unverified.'
    colors.update({'redRoof':'#a55250','solar':'#344b5c','paverObject':'#d6d1c4'})
    def add(name,p,s,mat,group='campus',shape='box',rot=0):objects.append(dict(name=name,p=p,s=s,mat=mat,shape=shape,group=group,rot=rot))
    # Reconstruct the surrounding roof extents directly from the registered image.
    for f in footprints:
        if f['id'] not in ['west-a','west-b','west-c','east-blue','rear','red']:continue
        q=np.array(f['points']);c=q.mean(axis=0);w=np.linalg.norm(q[1]-q[0]);d=np.linalg.norm(q[3]-q[0]);angle=math.atan2(-(q[1]-q[0])[1],(q[1]-q[0])[0]);h={'red':3.1,'rear':7.6}.get(f['id'],7.5)
        add(f['name']+' • graticule registered',[c[0],h/2,c[1]],[w,h,d],'white' if f['group']=='campus' else 'context',f['group'],rot=angle)
        add(f['name']+' roof',[c[0],h+.15,c[1]],[w+.3,.3,d+.3],'redRoof' if f['id']=='red' else 'glass' if f['id']=='east-blue' else 'roof',f['group'],rot=angle)
        if f['id'].startswith('west'):
            for dz in np.arange(-d/2+2,d/2,6):add('Registered west roof seam',[c[0],h+.33,c[1]+dz],[w,.04,.07],'metal','context',rot=angle)
        if f['id']=='red':
            # Garden hut rotated 90 degrees clockwise per user request (clears front entrance from tree)
            rot_red = angle - math.pi / 2
            objects[:]=[o for o in objects if not o['name'].startswith(f['name'])]
            add(f['name']+' - graticule registered',[c[0],h/2,c[1]],[w,h,d],'white' if f['group']=='campus' else 'context',f['group'],rot=rot_red)
            add('Red garden hut pitched roof - satellite match inferred',[c[0],h,c[1]],[w+1.3,1.25,d+1.3],'redRoof',shape='hutRoof',rot=rot_red)
            def rot_hut(lx, lz):
                dx = lx * math.cos(rot_red) + lz * math.sin(rot_red)
                dz = -lx * math.sin(rot_red) + lz * math.cos(rot_red)
                return [c[0] + dx, c[1] + dz]
            p_front = rot_hut(0, d/2 + .05)
            add('Garden hut green frontage - video informed',[p_front[0],1.4,p_front[1]],[w,.9,.10],'carpet',rot=rot_red)
            for xx in [-w*.45,0,w*.45]:
                p_post = rot_hut(xx, d/2 + .25)
                add('Garden hut slim veranda post',[p_post[0],2,p_post[1]],[.1,2.2,.1],'carpet',rot=rot_red)
            for i in range(3):
                p_step = rot_hut(0, d/2 + 1.2 - i*.3)
                add('Garden hut front terracotta step',[p_step[0],.25+i*.16,p_step[1]],[w*.5,.2,.45],'redRoof',rot=rot_red)
    q=np.array(next(f['points'] for f in footprints if f['id']=='construction'));c=q.mean(axis=0);w=np.linalg.norm(q[1]-q[0]);d=np.linalg.norm(q[3]-q[0])
    for y in [2,5,8,11,14]:
        add('Southwest construction floor slab • registered footprint',[c[0],y,c[1]],[w,.3,d],'context')
        for xx in np.linspace(-w*.43,w*.43,4):
            for zz in [-d*.43,0,d*.43]:add('Southwest construction column',[c[0]+xx,y+1.3,c[1]+zz],[.5,2.6,.5],'context')
    # New 10:43 ZIP close-ups: concentric pavilion edges and the two small
    # panel banks on the blue roof. Positions share the existing registered frame.
    # Pavilion terraces are now modelled as connected tread solids in detail_lotus.
    q=np.array(next(f['points'] for f in footprints if f['id']=='east-blue'))
    u=q[1]-q[0];v=q[3]-q[0];angle=math.atan2(-u[1],u[0])
    for fu,fv in [(.43,.42),(.58,.56)]:
        for row in range(2):
            for col in range(3):
                p=q[0]+u*(fu+col*.026)+v*(fv+row*.025)
                add('Blue roof small solar module • 10:43 ZIP close-up',[p[0],7.86,p[1]],[.65,.07,1.05],'solar','context',rot=angle)
    # Light-coloured stacks are a satellite-date observation, not verified seats.
    for u in range(802,883,12):
        for v in range(425,478,12):
            if u<815 and v<450:continue
            p=pixel([u,v]);add('Light objects visible on satellite • type/date unverified',[p[0],.7,p[1]],[2,.9,2],'paverObject','snapshot')
    for u in [885,897]:
        for v in [356,369,382]:
            p=pixel([u,v]);add('Light satellite object cluster • function unverified',[p[0],.7,p[1]],[2,.9,2],'paverObject','snapshot')
    solar=[(550,503,20,8),(785,564,18,6),(923,554,14,6)]
    for u,v,wp,dp in solar:
        p=pixel([u,v]);add('Solar panel array • position read from satellite',[p[0],10.3 if u<600 else 9.7,p[1]],[wp*.26,.15,dp*.26],'solar','roof')
    roads=[]
    route_specs=[('main-road','Assan–Thirana Road',[[150,271],[500,199],[750,145],[1000,91],[1250,39],[1370,14]],9),('approach','Internal concrete approach',[[685,215],[691,359],[698,520]],10),('south-court','South building circulation court',[[698,520],[819,520],[968,508]],6),('east-lane','East perimeter lane',[[981,174],[985,350],[995,663]],4.5)]
    objects[:]=[o for o in objects if not o['name'].startswith(('Assan–Thirana Road','North boundary','Main inner concrete approach','Residential frontage turning court','East internal circulation strip','Inner approach low stone edge','Approach curb joint','Inner concrete transverse joint','Edge drain grille','Drain grille slat'))]
    for key,name,pixels,width in route_specs:
        pts=[pixel(p).tolist() for p in pixels];roads.append(dict(id=key,name=name,points=pts,width=width,status='Centreline manually digitised from displayed image; width estimated'))
        for p1,p2 in zip(np.array(pts),np.array(pts[1:])):
            delta=p2-p1;length=np.linalg.norm(delta);c=(p1+p2)/2;angle=math.atan2(delta[0],delta[1]);add(name+' • registered centreline',[c[0],.28,c[1]],[width,.15,length],'road' if key=='main-road' else 'paving','campus',rot=angle)
            if key=='main-road':
                # Continuous granular verges sit below the carriageway, matching
                # the unmarked rural road in the supplied satellite close-ups.
                perp=np.array([delta[1],-delta[0]])/length
                for side in [-1,1]:
                    edge=c+side*perp*(width/2+.55)
                    add('Main road earth shoulder • reference informed',[edge[0],.16,edge[1]],[1.15,.12,length+.05],'paving',rot=angle)
            if key!='main-road':
                perp=np.array([delta[1],-delta[0]])/length
                for side in [-1,1]:
                    edge=c+side*perp*(width/2+.1);add('Registered circulation curb edge',[edge[0],.4,edge[1]],[.18,.18,length],'stone',rot=angle)
    main=np.array(roads[0]['points'])
    def road_distance(p):
        return min(np.linalg.norm(p-(a+np.clip(np.dot(p-a,b-a)/np.dot(b-a,b-a),0,1)*(b-a))) for a,b in zip(main,main[1:]))
    # Old schematic northern enclosure walls crossed the newly registered road.
    # Split those walls and preserve only portions outside a clear road corridor.
    clipped=[]
    for o in objects:
        if o['name']!='North lower enclosure perimeter wall':continue
        clipped.append(o)
        axis=np.array([math.sin(o['rot']),math.cos(o['rot'])]);centre=np.array([o['p'][0],o['p'][2]])
        for a in np.arange(-o['s'][2]/2,o['s'][2]/2,1):
            length=min(1,o['s'][2]/2-a);p=centre+axis*(a+length/2)
            if road_distance(p)<6.5:continue
            add('Northern enclosure wall • clear of main road',[p[0],o['p'][1],p[1]],[o['s'][0],o['s'][1],length],o['mat'],'context',rot=o['rot'])
    objects[:]=[o for o in objects if o not in clipped]
    # Front boundary follows the image-side frontage and returns to the gate
    # piers rather than running diagonally across the main road.
    for chain in [[[515,230],[636,205],[642,215]],[[728,215],[740,185],[981,132]]]:
        pts=[pixel(p) for p in chain]
        for a,b in zip(pts,pts[1:]):
            d=b-a;c=(a+b)/2;length=np.linalg.norm(d);angle=math.atan2(d[0],d[1])
            add('Frontage boundary wall • image aligned',[c[0],1,c[1]],[.4,2,length],'stone',rot=angle)
            add('Frontage wall white coping',[c[0],2.06,c[1]],[.5,.12,length],'white',rot=angle)
    # Replace legacy side walls whose transformed ends stopped short of frontage.
    rear=next(o for o in objects if o['name']=='South boundary')
    centre=np.array([rear['p'][0],rear['p'][2]])
    axis=np.array([math.cos(rear['rot']),-math.sin(rear['rot'])])*rear['s'][0]/2
    rear_corners=[centre-axis,centre+axis]
    front_corners=[pixel([515,230]),pixel([981,132])]
    objects[:]=[o for o in objects if not o['name'].startswith(('Compound wall •','Compound wall pilaster','Compound wall coping'))]
    boundary_joins=[]
    for side,a,b in zip(['west','east'],front_corners,rear_corners):
        d=b-a;length=np.linalg.norm(d);c=(a+b)/2;angle=math.atan2(d[0],d[1])
        add('Compound side boundary • joined '+side+' frontage',[c[0],1,c[1]],[.5,2,length+.12],'stone',rot=angle)
        add('Compound side coping • joined '+side+' frontage',[c[0],2.06,c[1]],[.6,.12,length+.12],'white',rot=angle)
        for t in np.linspace(0,1,max(2,math.ceil(length/10)+1)):
            point=a+d*t;add('Compound side pilaster • '+side,[point[0],1.1,point[1]],[.7,2.2,.7],'stone',rot=angle)
        boundary_joins.append({'side':side,'front':a.tolist(),'rear':b.tolist(),'lengthMetres':float(length)})
    geo['boundaryJoins']=boundary_joins
    # User-marked empty strip behind/east of the lotus pavilion becomes lawn.
    grass_outline=np.array([[24,-73.5],[62.3,-80.8],[61,-36],[41,-36],[40,-50],[38,-63]],float)
    lo=grass_outline.min(axis=0);hi=grass_outline.max(axis=0);mid=(lo+hi)/2;span=hi-lo
    from geometry_profiles import extruded_polygon
    from detail_lotus_v8 import MESHES
    grass_mesh=extruded_polygon(((grass_outline-mid)/span).tolist())
    # XY outline / Z thickness -> XZ outline / Y thickness, preserving winding.
    import trimesh
    grass_mesh.apply_transform(trimesh.transformations.rotation_matrix(math.pi/2,[1,0,0]))
    MESHES['frontLotusGrassStrip']={'vertices':grass_mesh.vertices.tolist(),'faces':grass_mesh.faces.tolist()}
    add('Front east landscaped grass strip • user marked area',[mid[0],.20,mid[1]],[span[0],.04,span[1]],'grass',shape='frontLotusGrassStrip')
    geo['frontLotusGrassStrip']=grass_outline.tolist()
    # Gate apron meets the campus-side road edge without covering the carriageway.
    choices=[]
    for a,b in zip(main,main[1:]):
        v=b-a;q=a+np.clip(np.dot(gate-a,v)/np.dot(v,v),0,1)*v;choices.append((np.linalg.norm(q-gate),q))
    _,road_centre=min(choices,key=lambda x:x[0]);normal=gate-road_centre;normal/=np.linalg.norm(normal)
    tangent=np.array([normal[1],-normal[0]]);edge=road_centre+normal*(roads[0]['width']/2)
    apron=np.array([gate-tangent*7,edge-tangent*7,edge+tangent*7,gate+tangent*7])
    area=sum(apron[i,0]*apron[(i+1)%4,1]-apron[(i+1)%4,0]*apron[i,1] for i in range(4))
    if area<0:apron=apron[::-1]
    lo=apron.min(axis=0);hi=apron.max(axis=0);mid=(lo+hi)/2;span=hi-lo
    verts=[[float((x-mid[0])/span[0]),y,float((z-mid[1])/span[1])] for y in [-.5,.5] for x,z in apron]
    faces=[[0,1,2],[0,2,3],[4,6,5],[4,7,6]]
    for i in range(4):
        j=(i+1)%4;faces.extend([[i,j,j+4],[i,j+4,i+4]])
    from detail_lotus_v8 import MESHES
    MESHES['gateApronTrimmed']={'vertices':verts,'faces':faces}
    add('Main gate apron • stops at campus-side road edge',[mid[0],.27,mid[1]],[span[0],.14,span[1]],'paving',shape='gateApronTrimmed')
    geo['gateApronPolygon']=apron.tolist()
    geo['roadRevision']='Removed legacy crossing frontage wall; clipped north enclosure wall outside 6.5m road corridor; redrawn frontage returns, continuous entrance apron and earth shoulders. Width/detail estimated from supplied images.'
    # A true local-to-WGS84 frame is shared by model, signs and footprint GeoJSON.
    geo.update(globalPlanTransform=glob.tolist(),hallPlanTransform=hm.tolist(),gardenPlanTransform=gm.tolist(),gateDelta=gdelta.tolist(),pavilionCentre=pc.tolist(),footprints=footprints,roads=roads,
               accuracy='Displayed-graticule registration only. Fit residual measures internal consistency, not absolute position accuracy; screenshot pixels, digitisation, imagery age, geometry simplification and ground survey error remain.')
    out=ROOT/'outputs';(out/'georeference.json').write_text(json.dumps(geo,indent=2),encoding='utf-8')
    gj={'type':'FeatureCollection','features':[]}
    for f in footprints:
        ring=[ll(p) for p in f['points']];ring.append(ring[0]);gj['features'].append({'type':'Feature','id':f['id'],'properties':{k:v for k,v in f.items() if k!='points'},'geometry':{'type':'Polygon','coordinates':[ring]}})
    for r in roads:gj['features'].append({'type':'Feature','id':r['id'],'properties':{k:v for k,v in r.items() if k!='points'},'geometry':{'type':'LineString','coordinates':[ll(p) for p in r['points']]}})
    gj['features'].append({'type':'Feature','id':'origin-pin','properties':{'name':'Supplied Google Maps pin / model origin'},'geometry':{'type':'Point','coordinates':origin}})
    for i,p in enumerate(geo['verifiedMapListings']):
        gj['features'].append({'type':'Feature','id':f'verified-listing-{i+1}','properties':{k:v for k,v in p.items() if k not in ['latitude','longitude']},'geometry':{'type':'Point','coordinates':[p['longitude'],p['latitude']]}})
    (out/'site-footprints.geojson').write_text(json.dumps(gj,indent=2),encoding='utf-8')
    return objects,colors,signs,labels,geo
