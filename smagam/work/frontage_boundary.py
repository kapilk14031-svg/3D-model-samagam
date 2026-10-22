"""User-requested venue frontage wall, half the height of the main decorative gates."""
current=''
gate_top=max(o['p'][1]+o['s'][1]*(.5 if o['kind']=='box' else 1) for o in objects if o['layer']=='gates' and not o.get('userAdded'))
frontage_height=gate_top/2
highway=next(f for f in features if f['id']=='H01')['path']
def source_at(u):
    for a,b in zip(highway,highway[1:]):
        if a[0]<=u<=b[0]:
            t=(u-a[0])/(b[0]-a[0]);return [u,a[1]+(b[1]-a[1])*t]
raw=[source_at(295)]+[p for p in highway if 295<p[0]<1320]+[source_at(1320)]
frontage=offset_path([planpoint(*p) for p in raw],-25.5)
stations=[0]
for a,b in zip(frontage,frontage[1:]):stations.append(stations[-1]+math.dist(a,b))
def project(point):
    best=None
    for j,(a,b) in enumerate(zip(frontage,frontage[1:])):
        dx=b[0]-a[0];dz=b[2]-a[2];ll=math.hypot(dx,dz)
        t=max(0,min(1,((point[0]-a[0])*dx+(point[2]-a[2])*dz)/(ll*ll)))
        q=[a[0]+t*dx,0,a[2]+t*dz];distance=math.dist([point[0],0,point[2]],q)
        if best is None or distance<best[0]:best=(distance,stations[j]+t*ll,[dx/ll,dz/ll])
    return best
# Align the photo gates to the actual frontage polyline before cutting its openings.
# Keep the printed PDF coordinates as source data; move the rendered gate assembly,
# leaf pivots, label and feature world anchor together.
for gate in [f for f in features if f['id'] in ['G01','G02','G03']]:
    old=list(gate['world']);_,station,tangent=project(old)
    for j,(lo,hi) in enumerate(zip(stations,stations[1:])):
        if lo-1e-6<=station<=hi+1e-6:
            t=(station-lo)/(hi-lo);centre=[frontage[j][i]+t*(frontage[j+1][i]-frontage[j][i]) for i in range(3)];break
    angle=math.atan2(-tangent[1],tangent[0])
    if math.cos(angle+math.pi/2)<0:angle+=math.pi
    delta=angle+math.pi/2;ca=math.cos(delta);sa=math.sin(delta)
    def align_point(p):
        dx=p[0]-old[0];dz=p[2]-old[2]
        return [centre[0]+dx*ca+dz*sa,p[1],centre[2]-dx*sa+dz*ca]
    for o in objects:
        if o['featureId']!=gate['id']:continue
        o['p']=align_point(o['p']);o['rotY']=o.get('rotY',0)+delta
        if 'photoLeaf' in o:o['photoLeaf']['pivot']=align_point(o['photoLeaf']['pivot'])
        o['status']+='; gate plane aligned to highway boundary wall'
    for label in labels:
        if label.get('featureId')==gate['id']:label['p']=align_point(label['p'])
    gate['world']=[centre[0],old[1],centre[2]]
    gate['gateAlignment']={'sourceWorld':old,'angle':angle,'station':station,'boundaryCentre':centre,'tangent':tangent}
openings=[]
for f in [f for f in features if f['id'] in ['G01','G02','G03','G04']]:
    u,v=loc(f);centre=f['world'] if f.get('gateAlignment') else planpoint(u,v);dist,station,tangent=project(centre);radius=0
    for o in objects:
        if o['featureId']!=f['id']:continue
        ca=math.cos(o.get('rotY',0));sa=math.sin(o.get('rotY',0))
        for sx,sz in [[-.5,-.5],[.5,-.5],[.5,.5],[-.5,.5]]:
            xx=sx*o['s'][0];zz=sz*o['s'][2];px=o['p'][0]+xx*ca+zz*sa-centre[0];pz=o['p'][2]-xx*sa+zz*ca-centre[2]
            radius=max(radius,abs(px*tangent[0]+pz*tangent[1]))
    gap=0 if f.get('gateAlignment') else 3.5
    openings.append([station-radius-gap,station+radius+gap,f['id']])
for title,u,v in [('P1 access',303,1126),('P4 outer access',1313,878)]:
    _,station,_=project(planpoint(u,v));openings.append([station-17,station+17,title])
for f in [f for f in features if f['id'] in ['H03','H04']]:
    centre=f['world'];_,station,_=project(centre);openings.append([station-15,station+15,f['id']+' underpass access'])
spans=[]
for lo,hi,title in sorted(openings):
    lo=max(0,lo);hi=min(stations[-1],hi)
    if spans and lo<=spans[-1][1]:spans[-1][1]=max(hi,spans[-1][1])
    else:spans.append([lo,hi])
def at(station):
    for j,(lo,hi) in enumerate(zip(stations,stations[1:])):
        if lo-1e-6<=station<=hi+1e-6:
            t=(station-lo)/(hi-lo);return [frontage[j][i]+t*(frontage[j+1][i]-frontage[j][i]) for i in range(3)]
kept=[];cursor=0
for lo,hi in spans:
    if lo-cursor>1:kept.append([cursor,lo])
    cursor=max(cursor,hi)
if stations[-1]-cursor>1:kept.append([cursor,stations[-1]])
start=len(objects)
for lo,hi in kept:
    points=[at(lo)]+[p for p,t in zip(frontage,stations) if lo<t<hi]+[at(hi)]
    line('USER ADDED / Highway frontage wall',points,1.3,frontage_height-.5,'#8e795d','frontage')
    line('USER ADDED / Highway boundary coping',points,1.9,.5,'#c3ae84','frontage',frontage_height-.5)
    for distance in [lo,hi]+[lo+j*32 for j in range(1,int((hi-lo)/32)+1)]:
        p=at(distance);box('USER ADDED / Frontage wall pier',p[0],p[2],2.2,2.2,frontage_height,'#a58b65',0,'frontage')
for o in objects[start:]:
    o['userAdded']=True;o['status']='User-requested highway boundary; height equals half main gate height; gaps reserved at source gates and access roads'
frontage_info=dict(height=frontage_height,main_gate_height=gate_top,side='venue side of NH44',source_span=[295,1320],clearance_from_highway_centre=25.5,openings=openings,wall_station_intervals=kept)
labels.append(dict(text='HIGHWAY BOUNDARY / HALF GATE HEIGHT',p=[frontage[2][0],frontage_height+5,frontage[2][2]],layer='frontage',userAdded=True))
print('Highway frontage boundary height:',round(frontage_height,3),'with',len(openings),'gate/access openings')
