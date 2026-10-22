"""Apply the user's 22 October red/yellow/green screenshot layout in registered coordinates."""
import json, math
from pathlib import Path
import numpy as np
from geometry_profiles import extruded_polygon
from detail_lotus_v8 import MESHES

ROOT=Path(__file__).resolve().parents[1]

def apply_layout(objects,colors,geo):
    ref=json.loads((ROOT/'work/helipad-layout-reference.json').read_text(encoding='utf-8'))
    transform=np.array(ref['imageToRegisteredPixel']);fit=np.array(geo['pixelToLonLat'])
    def world(p):
        uv=np.array([*p,1])@transform;lon,lat=np.array([*uv,1])@fit
        return np.array([(lon-geo['originLongitude'])*geo['eastMetresPerDegree'],(geo['originLatitude']-lat)*geo['northMetresPerDegree']])
    h=geo['helipadProposal'];old=np.array(h['centre']);centre=world(ref['helipadImagePixel']);route=[world(p) for p in ref['routeImagePixels']]
    forward=route[1]-centre;forward/=np.linalg.norm(forward)
    old_forward=-np.array(h['alignmentAxis']);old_heading=math.atan2(*old_forward);heading=math.atan2(*forward);turn=heading-old_heading
    c,s=math.cos(turn),math.sin(turn)
    def move(p):
        q=np.array(p)-old
        return centre+np.array([c*q[0]+s*q[1],-s*q[0]+c*q[1]])
    remove=('Proposed vehicle access','Link road ')
    objects[:]=[o for o in objects if not o['name'].startswith(remove)]
    for o in objects:
        if o['group']=='helipad' and not ('red-carpet' in o['name'].lower() or 'main gate to auditorium' in o['name']):
            o['p'][0],o['p'][2]=move([o['p'][0],o['p'][2]]).tolist();o['rot']+=turn
    # Begin the silver path at the circular rim rather than cutting across the H marking.
    a,b=route[0],route[1];v=b-a;w=a-centre
    roots=np.roots([np.dot(v,v),2*np.dot(w,v),np.dot(w,w)-16.35**2])
    candidates=[float(t.real) for t in roots if abs(t.imag)<1e-7 and 0<=t.real<=1]
    if candidates:route[0]=a+v*max(candidates)
    # Connect to the FIELD-side edge of the existing main road, never over its carriageway.
    road=np.array(geo['roads'][0]['points']);last=route[-1];near=[]
    for a,b in zip(road,road[1:]):
        v=b-a;t=np.clip(np.dot(last-a,v)/np.dot(v,v),0,1);p=a+t*v
        near.append((np.linalg.norm(last-p),p,v/np.linalg.norm(v)))
    _,road_mid,tangent=min(near,key=lambda e:e[0]);normal=np.array([tangent[1],-tangent[0]])
    if np.dot(last-road_mid,normal)<0:normal=-normal
    edge=road_mid+normal*geo['roads'][0]['width']/2
    last_direction=route[-1]-route[-2];last_direction/=np.linalg.norm(last_direction)
    route[-1]+=last_direction*np.dot(edge-route[-1],normal)/np.dot(last_direction,normal)
    width=5.5;half=width/2;directions=[(b-a)/np.linalg.norm(b-a) for a,b in zip(route,route[1:])]
    left=[];right=[]
    for i,p in enumerate(route):
        if i in (0,len(route)-1):n=np.array([directions[0 if i==0 else -1][1],-directions[0 if i==0 else -1][0]]);offset=n*half
        else:
            n0=np.array([directions[i-1][1],-directions[i-1][0]]);n1=np.array([directions[i][1],-directions[i][0]]);n=n0+n1;n/=np.linalg.norm(n);offset=n*half/np.dot(n,n1)
        left.append(p-offset);right.append(p+offset)
    for side in [left,right]:side[-1]+=last_direction*np.dot(edge-side[-1],normal)/np.dot(last_direction,normal)
    polygon=np.array(left+right[::-1]);low=polygon.min(axis=0);span=polygon.max(axis=0)-low;mid=low+span/2
    mesh=extruded_polygon((polygon-mid)/span)
    MESHES['userSilverHelipadRoad']={'vertices':mesh.vertices[:,[0,2,1]].tolist(),'faces':mesh.faces[:,::-1].tolist()}
    colors.update(helipadSilverRoad='#bcc2c7',helipadGateMetal='#8e9aa4',helipadGatePier='#e2e5e7',helipadLaneMark='#707b84')
    def add(name,p,size,mat,shape='box',rot=0):
        objects.append(dict(name=name,p=list(map(float,p)),s=list(map(float,size)),mat=mat,shape=shape,group='helipad',rot=float(rot)))
    add('Silver helipad access road • yellow-line alignment',[mid[0],.15,mid[1]],[span[0],.30,span[1]],'helipadSilverRoad','userSilverHelipadRoad')
    for edge_points in [left,right]:
        for a,b in zip(edge_points,edge_points[1:]):
            delta=b-a;p=(a+b)/2
            add('Silver road flush edge strip',[p[0],.312,p[1]],[.12,.016,np.linalg.norm(delta)],'padRoadCurb',rot=math.atan2(*delta))
    for a,b in zip(route,route[1:]):
        delta=b-a;length=np.linalg.norm(delta);direction=delta/length
        for distance in np.arange(3,length-2,6):
            p=a+direction*distance;add('Silver road subtle centre dash',[p[0],.317,p[1]],[.15,.018,2.0],'helipadLaneMark',rot=math.atan2(*direction))
    gate=world(ref['gateImagePixel']);gate_dir=directions[1];side=np.array([gate_dir[1],-gate_dir[0]]);gate_heading=math.atan2(*gate_dir)
    for sign in [-1,1]:
        hinge=gate+side*sign*3.13
        add('Helipad access gate silver pier • green mark',[hinge[0],1.6,hinge[1]],[.38,3.2,.38],'helipadGatePier')
        add('Helipad access gate pier cap',[hinge[0],3.25,hinge[1]],[.48,.12,.48],'helipadGateMetal')
        # Park both leaves open along the road edges, keeping its full width clear.
        leaf=hinge-gate_dir*1.35
        for y in [.58,1.25,2.0]:add('Helipad access gate open leaf rail',[leaf[0],y,leaf[1]],[.075,.075,2.7],'helipadGateMetal',rot=gate_heading)
        for d in np.linspace(.08,2.62,13):
            p=hinge-gate_dir*d;add('Helipad access gate open leaf vertical bar',[p[0],1.3,p[1]],[.035,1.5,.035],'helipadGateMetal')
    add('Helipad entry gate header • green mark',[gate[0],3.55,gate[1]],[6.65,.40,.25],'helipadGateMetal',rot=gate_heading)
    # Keep pad floodlights clear of the newly marked access path.
    def path_distance(p):
        distances=[]
        for a,b in zip(route,route[1:]):
            v=b-a;t=np.clip(np.dot(p-a,v)/np.dot(v,v),0,1);distances.append(np.linalg.norm(p-a-t*v))
        return min(distances)
    objects[:]=[o for o in objects if not (o['name'].startswith('Perimeter floodlight') and path_distance(np.array([o['p'][0],o['p'][2]]))<3.4)]
    # Remove any schematic northern wall blocks that cross the new connection.
    objects[:]=[o for o in objects if not(o['name'].startswith('Northern enclosure wall') and path_distance(np.array([o['p'][0],o['p'][2]]))<3.2)]
    h.update(status='User-marked red-dot helipad and silver access road, 22 October 2026',centre=centre.tolist(),helicopterCentre=centre.tolist(),alignmentAxis=(-forward).tolist(),gateToCentreMetres=float(np.linalg.norm(centre-np.array(h['gate']))),rightShiftMetres=None,rightShiftReference='Superseded by the user-marked screenshot location',corners=[move(p).tolist() for p in h['corners']],vehicleAccess=[route[0].tolist(),route[-1].tolist()],vehicleAccessPolyline=[p.tolist() for p in route],vehicleAccessPolygon=polygon.tolist(),mainRoadJoinEdge=[left[-1].tolist(),right[-1].tolist()],vehicleAccessWidthMetres=width,vehicleAccessMaterial='Silver grey',roadConnectionCentre=road_mid.tolist(),accessGate=dict(centre=gate.tolist(),roadHeading=gate_heading,clearWidth=5.5,displayState='Open',sourceImagePixel=ref['gateImagePixel']),userLayoutRegistration=ref)
    campus_gate=np.array(h['gate']);approach=[]
    for a,b in zip(road,road[1:]):
        v=b-a;t=np.clip(np.dot(campus_gate-a,v)/np.dot(v,v),0,1);p=a+t*v;approach.append((np.linalg.norm(p-campus_gate),p))
    h['campusRoadCentre']=min(approach,key=lambda e:e[0])[1].tolist()
    # Agricultural context digitised from the same supplied marked screenshot.
    colors.update(helipadFieldDry='#9c875e',helipadFieldStubble='#aa956c',helipadFieldGreen='#79835a',helipadFurrow='#807050',helipadBuilding='#d3cec0',helipadRoof='#b3b0a7')
    def context_poly(name,pixels,mat,y=.04,height=.035):
        q=np.array([world(p) for p in pixels]);lo=q.min(axis=0);span=q.max(axis=0)-lo;mid=lo+span/2
        mesh=extruded_polygon((q-mid)/span);key='helipadContext'+str(len(MESHES))
        MESHES[key]={'vertices':mesh.vertices[:,[0,2,1]].tolist(),'faces':mesh.faces[:,::-1].tolist()}
        add(name,[mid[0],y,mid[1]],[span[0],height,span[1]],mat,key)
        objects[-1]['group']='context'
        return q
    parcels=[('Left approach field north',[(242,108),(316,108),(316,181),(246,181)],'helipadFieldDry'),('Left approach field south',[(255,285),(316,285),(314,334),(258,345)],'helipadFieldStubble'),('Right approach field west',[(340,105),(389,108),(388,320),(340,332)],'helipadFieldStubble'),('Right approach field east',[(399,8),(518,15),(518,314),(398,320)],'helipadFieldDry')]
    for name,pixels,mat in parcels:
        q=context_poly(name,pixels,mat)
        a,b,c,d=q
        for t in np.arange(.035,.99,.055):
            v0=a*(1-t)+b*t;v1=d*(1-t)+c*t;dv=v1-v0;mid=(v0+v1)/2
            add(name+' cultivated furrow',[mid[0],.067,mid[1]],[.10,.012,np.linalg.norm(dv)],'helipadFurrow',rot=math.atan2(*dv));objects[-1]['group']='context'
    # Low white building visible in the distant left landscaped plot; heights estimated.
    for name,pixels in [('Left distant building front wing',[(29,148),(83,149),(82,165),(29,164)]),('Left distant building return wing',[(28,164),(44,164),(44,219),(28,220)])]:
        q=context_poly(name,pixels,'helipadBuilding',1.8,3.6)
        context_poly(name+' flat roof',pixels,'helipadRoof',3.68,.16)
        a,b=q[0],q[1];dv=b-a;length=np.linalg.norm(dv)
        for t in np.arange(.12,.94,.17):
            pt=a+dv*t
            add(name+' dark window',[pt[0],2.0,pt[1]],[1.1,1.15,.08],'dark',rot=math.atan2(-dv[1],dv[0]));objects[-1]['group']='context'
    h['surroundingsUpdate']={'source':'Marked satellite screenshot 2026-10-22 151630.png','fields':'Four agricultural parcels either side of access with cultivated rows','leftBuilding':'Low L-shaped building in left landscaped plot; screenshot footprint, estimated height and window spacing'}
    h['previousLocationReplaced']=True
    geo['helipadProposal']=h
    (ROOT/'outputs/helipad-layout-registration.json').write_text(json.dumps(ref,indent=2),encoding='utf-8')
    return objects,colors,geo
