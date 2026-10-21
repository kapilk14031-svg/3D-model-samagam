"""User-requested concept: lawn-sized field area, 100 m across from gate."""
import json
import math
from pathlib import Path
import numpy as np

def add_helipad(objects,colors,geo):
    colors.update(helipadSurface='#59636b',helipadEdge='#d6cbaa',heliWhite='#e6edf0',heliBlue='#1e4c6b',heliGlass='#173646',heliMetal='#424c53',heliNavRed='#df3e36',heliNavGreen='#39b77d',redCarpet='#a92035')
    def add(name,p,s,mat,shape='box',rot=0):
        objects.append(dict(name=name,p=list(map(float,p)),s=list(map(float,s)),mat=mat,shape=shape,group='helipad',rot=float(rot)))
    g=np.array([-13.,1.,-61.]);m=np.array(geo['globalPlanTransform']);gate=np.array([g[0],g[2],1])@m;gate+=np.array(geo['gateDelta'])
    road=np.array(geo['roads'][0]['points']);candidates=[]
    for a,b in zip(road,road[1:]):
        v=b-a;t=np.clip(np.dot(gate-a,v)/np.dot(v,v),0,1);p=a+t*v;candidates.append((np.linalg.norm(p-gate),p,v/np.linalg.norm(v)))
    _,roadpoint,u=min(candidates,key=lambda x:x[0]);outward=roadpoint-gate;outward/=np.linalg.norm(outward)
    right_shift=8.0
    original_outward=outward.copy();original_right=u.copy()
    centre=gate+outward*math.sqrt(100**2-right_shift**2)+u*right_shift
    outward=(centre-gate)/100
    u=np.array([-outward[1],outward[0]])
    lawn=np.array(next(f['points'] for f in geo['footprints'] if f['id']=='garden'))
    width=np.linalg.norm(lawn[1]-lawn[0]);depth=np.linalg.norm(lawn[3]-lawn[0])
    v1=lawn[1]-lawn[0];v2=lawn[3]-lawn[0];area=abs(v1[0]*v2[1]-v1[1]*v2[0]);depth=area/width
    # Rectangle follows road tangent. It is a concept footprint, not land ownership.
    zaxis=-outward;angle=math.atan2(-u[1],u[0])
    add('Proposed helipad field area • central-lawn-sized',[centre[0],.22,centre[1]],[width,.22,depth],'helipadSurface',rot=angle)
    for x in [-width/2,width/2]:
        p=centre+u*x;add('Proposed helipad edge',[p[0],.35,p[1]],[.18,.04,depth],'helipadEdge',rot=angle)
    for z in [-depth/2,depth/2]:
        p=centre+zaxis*z;add('Proposed helipad edge',[p[0],.35,p[1]],[width,.04,.18],'helipadEdge',rot=angle)
    radius=min(width,depth)*.34
    for k in range(64):
        t=2*math.pi*k/64;p=centre+radius*np.array([math.cos(t),math.sin(t)])
        add('Helipad white circular marking',[p[0],.36,p[1]],[radius*2*math.pi/64+.05,.035,.35],'heliWhite',rot=math.pi/2-t)
    for x in [-2.1,2.1]:
        p=centre+u*x;add('Helipad H upright',[p[0],.37,p[1]],[.8,.04,7],'heliWhite',rot=angle)
    add('Helipad H crossbar',[centre[0],.37,centre[1]],[5,.04,.8],'heliWhite',rot=angle)
    # User correction: field approach is vehicle access only; carpet is inside campus.
    helicopter_scale=1.45
    heli=centre+outward*4-u*(1.9*helicopter_scale)
    road_start=centre-outward*(depth/2-1)
    # Trim each side of the connector at the field-side edge of the main road.
    direction=gate-road_start;direction/=np.linalg.norm(direction)
    side=np.array([direction[1],-direction[0]])
    road_edge=roadpoint+original_outward*(geo['roads'][0]['width']/2)
    def end_at_road(start):
        t=np.dot(road_edge-start,original_outward)/np.dot(direction,original_outward)
        return start+direction*t
    ends=[end_at_road(road_start-side*2.75),end_at_road(road_start+side*2.75)]
    road_end=(ends[0]+ends[1])/2
    polygon=np.array([road_start-side*2.75,ends[0],ends[1],road_start+side*2.75])
    signed=sum(polygon[i,0]*polygon[(i+1)%4,1]-polygon[(i+1)%4,0]*polygon[i,1] for i in range(4))
    if signed<0:polygon=polygon[::-1]
    lo=polygon.min(axis=0);hi=polygon.max(axis=0);mid=(lo+hi)/2;span=hi-lo
    vertices=[[float((x-mid[0])/span[0]),y,float((z-mid[1])/span[1])] for y in [-.5,.5] for x,z in polygon]
    faces=[[0,1,2],[0,2,3],[4,6,5],[4,7,6]]
    for i in range(4):
        j=(i+1)%4;faces.extend([[i,j,j+4],[i,j+4,i+4]])
    from detail_lotus_v8 import MESHES
    MESHES['helipadAccessTrimmed']={'vertices':vertices,'faces':faces}
    add('Proposed vehicle access • stops at main road edge',[mid[0],.30,mid[1]],[span[0],.12,span[1]],'paving','helipadAccessTrimmed')
    drive=road_end-road_start
    # Opening in the schematic field enclosure for the proposed vehicle approach.
    def approach_distance(o):
        p=np.array([o['p'][0],o['p'][2]]);t=np.clip(np.dot(p-road_start,drive)/np.dot(drive,drive),0,1);return np.linalg.norm(p-road_start-t*drive)
    objects[:]=[o for o in objects if not (o['name'].startswith('Northern enclosure wall') and approach_distance(o)<3.4)]
    # Short boarding carpet only: helicopter door to edge of vehicle access.
    helicopter_exit=heli+u*(1.9*helicopter_scale)
    road_normal=np.array([drive[1],-drive[0]])/np.linalg.norm(drive)
    if np.dot(road_normal,u)<0:road_normal=-road_normal
    boarding_end=road_start.copy()
    boarding_delta=boarding_end-helicopter_exit;boarding_centre=(helicopter_exit+boarding_end)/2
    add('Short red carpet • helicopter to vehicle road only',[boarding_centre[0],.36,boarding_centre[1]],[2.4,.025,np.linalg.norm(boarding_delta)],'redCarpet',rot=math.atan2(boarding_delta[0],boarding_delta[1]))
    # Carpet is restricted to the user's gate-to-auditorium route inside campus.
    steps=sorted([o for o in objects if o['name'].startswith('External black entry step')],key=lambda o:o['p'][1])
    entry_z=steps[0]['p'][2];turn=np.array([gate[0],entry_z]);foot=np.array([steps[0]['p'][0]+steps[0]['s'][0]/2,entry_z])
    carpet_route=[gate.tolist(),turn.tolist(),foot.tolist()]
    for a,b in [(gate,turn),(turn,foot)]:
        d=b-a;c=(a+b)/2;add('Proposed red carpet • main gate to auditorium',[c[0],.38,c[1]],[2.4,.025,np.linalg.norm(d)],'redCarpet',rot=math.atan2(d[0],d[1]))
    for step in steps:
        p=step['p'];add('Auditorium red-carpet stair tread',[p[0],p[1]+step['s'][1]/2+.015,p[2]],[step['s'][0],.025,2.4],'redCarpet',rot=step['rot'])
    top=steps[-1];jambs=[o for o in objects if o['name'].startswith('Side entrance metal jamb')];door_x=sum(o['p'][0] for o in jambs)/len(jambs)
    add('Auditorium red-carpet entrance landing',[(top['p'][0]+door_x)/2,top['p'][1]+top['s'][1]/2+.015,entry_z],[abs(top['p'][0]-door_x),.025,2.4],'redCarpet')
    carpet_route.append([door_x,entry_z])
    # Static civilian helicopter with cabin, glazing, doors, rotor and skids.
    facing=-outward;yaw=math.atan2(-facing[0],-facing[1]);c,s=math.cos(yaw),math.sin(yaw)
    def part(name,p,size,mat,shape='box',r=0):
        x,y,z=p;x*=helicopter_scale;z*=helicopter_scale;y=.33+(y-.54)*helicopter_scale;add('Parked helicopter • '+name,[heli[0]+c*x+s*z,y,heli[1]-s*x+c*z],[v*helicopter_scale for v in size],mat,shape,yaw+r)
    part('rounded fuselage',[0,2.2,0],[1.35,1.22,3.35],'heliWhite','sphereSmooth')
    part('blue belly',[0,1.55,.15],[1.22,.55,2.95],'heliBlue','sphereSmooth')
    part('cockpit glazing',[0,2.45,-2.4],[1.12,.78,1.2],'heliGlass','sphereSmooth')
    part('cockpit centre frame',[0,2.45,-3.61],[.055,1.25,.06],'heliWhite')
    for side in [-1,1]:
        for z in [-.5,1.05]:
            part('side cabin window',[side*1.40,2.55,z],[1.25,.65,.035],'heliGlass','rounded',math.pi/2)
        part('door handle',[side*1.45,1.95,.55],[.04,.05,.32],'heliMetal')
        part('door rear seam',[side*1.41,2.12,1.82],[.025,1.35,.025],'heliBlue')
        part('landing skid',[side*1.52,.6,.2],[.12,.12,5.9],'heliMetal','rounded')
        for z in [-1.5,1.5]:part('skid support',[side*1.13,1,z],[.12,.85,.12],'heliMetal')
    part('engine housing',[0,3.3,1.05],[.85,.45,1.7],'heliBlue','sphereSmooth')
    for side in [-1,1]:part('engine exhaust',[side*.7,3.25,2],[.24,.22,.65],'heliMetal','sphereSmooth')
    part('main rotor mast',[0,3.95,.25],[.13,1.05,.13],'heliMetal','cylinder')
    part('rotor hub',[0,4.49,.25],[.36,.16,.36],'heliMetal','cylinder')
    for k in range(4):
        a=k*math.pi/2+.2;x=3.6*math.cos(a);z=.25+3.6*math.sin(a)
        part('stationary main rotor blade',[x,4.53,z],[6.6,.07,.22],'heliMetal',r=-a)
        part('rotor blade white tip',[6.65*math.cos(a),4.55,.25+6.65*math.sin(a)],[.45,.045,.24],'heliWhite',r=-a)
    part('tail boom',[0,2.28,5.6],[.32,.34,3.5],'heliWhite','sphereSmooth')
    part('vertical tail fin',[0,3.05,8.55],[.18,2.25,1.35],'heliBlue')
    part('tail stabilizer',[0,2.3,7.7],[2.8,.12,.65],'heliWhite')
    part('tail rotor vertical',[.3,3,8.55],[.1,2.4,.15],'heliMetal')
    part('tail rotor horizontal',[.3,3,8.55],[.1,.15,2.4],'heliMetal')
    # Cabin seals, sliding-door tracks, footboards and mechanical fittings.
    for side in [-1,1]:
        for z in [-1.23,1.82]:part('sliding door vertical seal',[side*1.41,2.2,z],[.045,1.5,.045],'heliMetal')
        for y in [1.47,2.96]:part('sliding door guide track',[side*1.41,y,.3],[.055,.045,3.05],'heliMetal')
        part('boarding footboard',[side*1.68,.98,.1],[.42,.12,1.6],'heliMetal','rounded')
        for z in [-.5,-.2,.1,.4,.7]:part('footboard grip rib',[side*1.68,1.05,z],[.4,.025,.035],'heliBlue')
        part('skid curved nose',[side*1.52,.72,-2.69],[.08,.18,.36],'heliMetal','sphereSmooth')
        part('skid end cap',[side*1.52,.6,3.1],[.09,.08,.12],'heliMetal','sphereSmooth')
        part('navigation light',[side*1.38,2.18,1.75],[.075,.07,.1],'heliNavRed' if side<0 else 'heliNavGreen','sphereSmooth')
        for z in [.8,1.05,1.3,1.55,1.8]:part('engine cooling grille',[side*.83,3.4,z],[.035,.25,.045],'heliMetal')
        for z in [-.9,-.3,.3,.9,1.5]:part('cabin lower rivet',[side*1.29,1.51,z],[.025,.025,.025],'heliWhite','sphereSmooth')
    part('nose search lamp',[0,1.65,-3.02],[.22,.16,.18],'heliWhite','sphereSmooth')
    part('roof beacon',[0,3.78,1.35],[.1,.12,.1],'heliNavRed','sphereSmooth')
    part('roof antenna',[0,3.85,2.25],[.025,.75,.025],'heliMetal')
    for side in [-1,1]:
        part('mast brace',[side*.31,3.78,.25],[.12,.6,.14],'heliMetal')
        part('rotor grip housing',[side*.43,4.48,.25],[.62,.14,.19],'heliMetal')
    part('tail rotor hub',[.38,3,8.55],[.12,.2,.2],'heliWhite','sphereSmooth')
    for y,z in [(4.1,8.55),(1.9,8.55),(3,7.45),(3,9.65)]:part('tail rotor safety tip',[.32,y,z],[.13,.18,.18],'heliWhite')
    corners=[(centre+u*x+zaxis*z).tolist() for x,z in [(-width/2,-depth/2),(width/2,-depth/2),(width/2,depth/2),(-width/2,depth/2)]]
    proposal=dict(status='Proposed visual arrangement; site/flight suitability not verified',gate=gate.tolist(),centre=centre.tolist(),gateToCentreMetres=float(np.linalg.norm(centre-gate)),rightShiftMetres=right_shift,rightShiftReference='Looking outward from main gate',originalOutwardAxis=original_outward.tolist(),originalRightAxis=original_right.tolist(),widthMetres=float(width),depthMetres=float(depth),areaSquareMetres=float(area),corners=corners,helicopterCentre=heli.tolist(),helicopterDisplayScale=helicopter_scale,alignmentAxis=outward.tolist(),carpet=carpet_route,carpetDestination='Auditorium side entrance',vehicleAccess=[road_start.tolist(),road_end.tolist()],vehicleAccessEnd='Main road field-side edge',vehicleAccessPolygon=polygon.tolist(),mainRoadJoinEdge=[ends[0].tolist(),ends[1].tolist()],vehicleAccessWidthMetres=5.5,helipadBoardingCarpet=[helicopter_exit.tolist(),boarding_end.tolist()])
    geo['helipadProposal']=proposal
    root=Path(__file__).resolve().parents[1]
    (root/'outputs/helipad-proposal.json').write_text(json.dumps(proposal,indent=2),encoding='utf-8')
    (root/'outputs/georeference.json').write_text(json.dumps(geo,indent=2),encoding='utf-8')
    return objects,colors,geo
