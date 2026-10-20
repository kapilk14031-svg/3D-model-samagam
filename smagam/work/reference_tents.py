"""Dense accommodation blocks inspired by the user-supplied 75th Samagam image.

The image is a different event/year and has no measured correspondence to the
79th traffic plan. Only its tent-block/lane/colour treatment is adapted here.
"""
current='';sleeping_tent_centres=[]
reference_sectors=[
 ('B1','#a15464',[[320,691],[405,676],[463,744],[528,825],[528,850],[320,850]]),
 ('B2','#4f7e9a',[[438,638],[615,453],[635,431],[635,705],[493,705]]),
 ('B3','#608d70',[[319,857],[355,857],[355,944],[453,950],[453,1045],[475,1063],[631,1023],[631,852],[537,852],[537,932],[319,932]]),
 ('C1','#608d70',[[730,581],[834,581],[834,707],[730,707]]),
 ('C2','#a15464',[[750,433],[834,433],[834,497],[750,497]]),
 ('C3','#4f7e9a',[[750,516],[834,516],[834,557],[750,557]]),
 ('C4','#a15464',[[752,337],[875,337],[875,410],[752,410]]),
 ('C5','#608d70',[[854,583],[888,583],[888,665],[854,665]]),
 ('D1','#4f7e9a',[[857,188],[956,187],[968,213],[1026,203],[1027,237],[859,272],[850,254],[850,225],[863,217]]),
 ('D2','#a15464',[[912,303],[946,303],[946,410],[912,410]]),
 ('D3','#608d70',[[963,435],[1006,435],[1006,549],[963,549]]),
 ('D4','#4f7e9a',[[1070,307],[1081,307],[1081,520],[1070,520]]),
 ('E1','#a15464',[[1102,397],[1119,397],[1119,455],[1102,455]]),
 ('E2','#608d70',[[1155,478],[1191,478],[1191,504],[1155,504]]),
 ('E3','#4f7e9a',[[1111,314],[1179,314],[1179,382],[1111,382]]),
 ('E4','#608d70',[[1069,300],[1350,300],[1318,355],[1318,404],[1212,508],[1140,609],[1070,604]]),
 # Second coverage pass: previously omitted large interior parcels. Roads,
 # occupied facilities and individual source boundaries still exclude tents.
 ('A1','#608d70',[[303,415],[708,341],[410,640],[314,653]]),
 ('B4','#a15464',[[438,638],[738,332],[738,562],[635,562],[635,705],[493,705]]),
 ('B5','#4f7e9a',[[465,836],[632,836],[632,1020],[472,1060],[465,1035]]),
 ('C6','#4f7e9a',[[753,331],[895,300],[895,563],[855,563],[855,706],[735,706],[735,576],[748,576]]),
 ('D5','#608d70',[[907,584],[1040,584],[1041,663],[1038,770],[911,770]]),
 ('D6','#a15464',[[1229,151],[1348,143],[1375,260],[1230,266]]),
 ('E5','#a15464',[[1094,686],[1234,699],[1234,735],[1095,730]]),
]
def ref_inside(p,poly):
    hit=False
    for a,b in zip(poly,poly[1:]+poly[:1]):
        if (a[1]>p[1])!=(b[1]>p[1]) and p[0]<(b[0]-a[0])*(p[1]-a[1])/(b[1]-a[1])+a[0]:hit=not hit
    return hit
def ref_distance(p,a,b):
    dx=b[0]-a[0];dy=b[1]-a[1];length=dx*dx+dy*dy
    t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/length))
    return math.hypot(p[0]-a[0]-t*dx,p[1]-a[1]-t*dy)*PLAN_SCALE
occupied=[];linear=[]
for f in features:
    if f['kind'] in ['building','toilets','parking','pandal','station','alighting','plot']:
        bb=f['bbox'];poly=f['path'] or [[bb[0],bb[1]],[bb[2],bb[1]],[bb[2],bb[3]],[bb[0],bb[3]]]
        occupied.append(poly)
    if f.get('path') and f['kind'] in ['road','internal_road','rail','wall','utility']:
        clearance={'road':25,'internal_road':12,'rail':13,'wall':7,'utility':15}[f['kind']]
        linear.extend((a,b,clearance) for a,b in zip(f['path'],f['path'][1:]))
gate_centres=[loc(f) for f in features if f['kind']=='gate']
def vacant(u,v):
    points=[[u,v]]+[[u+du,v+dv] for du,dv in [(-3.3,-2.6),(3.3,-2.6),(3.3,2.6),(-3.3,2.6)]]
    if any(ref_inside(p,poly) for poly in occupied for p in points):return False
    if any(ref_distance([u,v],a,b)<c for a,b,c in linear):return False
    if any(math.hypot(u-a,v-b)*PLAN_SCALE<35 for a,b in gate_centres):return False
    x,_,z=planpoint(u,v)

    return True
sector_palettes = {
    # Sector B (Ground B)
    'B1': {'roof': '#c85a6e', 'roof2': '#b84e62', 'ridge': '#e88295', 'wall': '#f2e8ea'}, # Rose Maroon
    'B2': {'roof': '#3f78a8', 'roof2': '#356a96', 'ridge': '#6fa8db', 'wall': '#e4ebf2'}, # Royal Blue
    'B3': {'roof': '#3d8e5a', 'roof2': '#337d4e', 'ridge': '#68ba85', 'wall': '#e4f2e9'}, # Emerald Green
    'B4': {'roof': '#c98a36', 'roof2': '#b87b2c', 'ridge': '#ebb25e', 'wall': '#f5ede0'}, # Warm Gold / Ochre
    'B5': {'roof': '#6859a4', 'roof2': '#5b4c94', 'ridge': '#9585d6', 'wall': '#ece9f5'}, # Deep Violet
    # Sector C (Ground C)
    'C1': {'roof': '#2f8252', 'roof2': '#267347', 'ridge': '#5cb582', 'wall': '#e2f2e8'}, # Forest Green
    'C2': {'roof': '#b54152', 'roof2': '#a33646', 'ridge': '#db6e7f', 'wall': '#f5e4e7'}, # Crimson Red
    'C3': {'roof': '#2b8596', 'roof2': '#227483', 'ridge': '#5eb6c7', 'wall': '#e2f0f2'}, # Cyan / Teal
    'C4': {'roof': '#c26532', 'roof2': '#b05928', 'ridge': '#e68f5e', 'wall': '#f5ece4'}, # Terracotta / Orange
    'C5': {'roof': '#5e8538', 'roof2': '#527530', 'ridge': '#8eb568', 'wall': '#edf2e4'}, # Olive Green
    'C6': {'roof': '#3368a6', 'roof2': '#2b5a92', 'ridge': '#659bdb', 'wall': '#e4ecf5'}, # Cobalt Blue
    # Sector D (Ground D)
    'D1': {'roof': '#4688b5', 'roof2': '#3c79a3', 'ridge': '#75b5e3', 'wall': '#e6f0f7'}, # Sky Blue
    'D2': {'roof': '#a63c6c', 'roof2': '#94325e', 'ridge': '#d16a98', 'wall': '#f5e4ee'}, # Berry Magenta
    'D3': {'roof': '#4d8a64', 'roof2': '#427a56', 'ridge': '#7ab591', 'wall': '#e6f2eb'}, # Sage Green
    'D4': {'roof': '#2d8085', 'roof2': '#247075', 'ridge': '#5eb2b8', 'wall': '#e3eff0'}, # Ocean Teal
    'D5': {'roof': '#4f8f42', 'roof2': '#447f38', 'ridge': '#7cc26e', 'wall': '#e8f5e4'}, # Spring Green
    'D6': {'roof': '#80447c', 'roof2': '#723a6e', 'ridge': '#ab6ea7', 'wall': '#f2e6f0'}, # Plum Purple
    # Sector A & E
    'A1': {'roof': '#b88d3d', 'roof2': '#a67d32', 'ridge': '#dbb163', 'wall': '#f5eee2'}, # Golden Amber
    'E1': {'roof': '#b05048', 'roof2': '#9e443c', 'ridge': '#d97d75', 'wall': '#f5e7e6'}, # Coral Red
    'E2': {'roof': '#3e8f6e', 'roof2': '#347d5f', 'ridge': '#6ec29f', 'wall': '#e4f5ed'}, # Mint Green
    'E3': {'roof': '#4a7294', 'roof2': '#3e6280', 'ridge': '#7aa2c7', 'wall': '#e6edf2'}, # Steel Blue
    'E4': {'roof': '#327c5e', 'roof2': '#296b50', 'ridge': '#61b08f', 'wall': '#e3f2ec'}, # Viridian Green
    'E5': {'roof': '#8a3a4c', 'roof2': '#7a3140', 'ridge': '#b56274', 'wall': '#f2e4e7'}, # Rich Burgundy
}
counts={};seen=[]
for sector,color,poly in reference_sectors:
    u0=min(p[0] for p in poly);u1=max(p[0] for p in poly);v0=min(p[1] for p in poly);v1=max(p[1] for p in poly)
    count=0
    for row,v in enumerate(range(int(v0)+5,int(v1)-3,8)):
        if row%6==5:continue # cross aisles between compact reference blocks
        for col,u in enumerate(range(int(u0)+5,int(u1)-3,10)):
            if col%5==4:continue # longitudinal access lanes
            if not all(ref_inside([u+du,v+dv],poly) for du,dv in [(-3.3,-2.6),(3.3,-2.6),(3.3,2.6),(-3.3,2.6)]):continue
            if not vacant(u,v):continue
            pal = sector_palettes.get(sector, {'roof': color, 'roof2': color, 'ridge': '#ffffff', 'wall': '#f2eee6'})
            roof_color = pal['roof'] if count % 2 == 0 else pal['roof2']
            x,_,z=planpoint(u,v)
            if any(abs(x-a)<8 and abs(z-b)<10 for a,b in seen):continue
            seen.append([x,z]);num=len(sleeping_tent_centres)+1;before=len(objects)
            name=f'REFERENCE ACCOMMODATION / {sector}-{count+1:03}'
            box(name+' canvas walls',x,z,6.4,8.6,2.3,pal['wall'],.1,'tents')
            add(name+f' {sector} ridge tent','roof',x,2.4,z,6.8,2.05,9.0,roof_color,'tents');objects[-1]['part']='roof'
            box(name+' reference block colour fascia',x,z+4.52,6.85,.16,.35,color,2.1,'tents')
            box(name+' entrance flap',x,z+4.34,1.5,.08,1.85,'#686050',.15,'tents')
            for side in [-1,1]:
                box(name+' slender canvas support',x+side*3.05,z+4.12,.09,.09,2.4,'#827b68',.1,'tents')
            box(name+' entrance threshold',x,z+4.28,1.65,.38,.08,'#9e9175',.1,'tents')
            box(name+' ridge seam',x,z,.22,9.1,.1,pal['ridge'],4.43,'tents');objects[-1]['part']='roof'
            for o in objects[before:]:
                o['userAdded']=True;o['referenceSector']=sector;o['status']='User-added accommodation concept adapted from low-resolution 75th Samagam image; not an official 79th tent allocation or surveyed position'
            sleeping_tent_centres.append(dict(number=num,sector=sector,camp='REFERENCE '+sector,p=[x,0,z],source_uv=[u,v],footprint=[6.8,9.0],roof=roof_color,reference_year='75th Samagam image; adapted to 79th traffic-plan geometry'))
            count+=1
    counts[sector]=count
    # Coloured block identifiers follow the drawing's pink, blue and green grouping style.
    if count and sector in ['B2','B3','C1','C4','D1','D3','E3','E4']:
        cu=sum(p[0] for p in poly)/len(poly);cv=sum(p[1] for p in poly)/len(poly);p=planpoint(cu,cv,13)
        group={'B':'GROUND-B','C':'GROUND-C','D':'GROUND-D'}.get(sector[0],'RESIDENTIAL TENTS')
        labels.append(dict(text=group,p=p,layer='tents',userAdded=True))
print('Reference-style residential tents:',len(sleeping_tent_centres),'; sectors:',counts)
reference_tent_info=dict(reference='Screenshot 2026-10-19 062833.png',event_on_reference='75th Nirankari Sant Samagam',status='User-requested visual adaptation; original image is low resolution; exact small labels and tent allocations not transcribed',tent_count=len(sleeping_tent_centres),sectors=counts,black_tents_replaced=True)
