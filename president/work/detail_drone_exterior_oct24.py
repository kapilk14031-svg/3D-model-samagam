"""24 October drone-reference exterior detail pass. No editor or simulation logic."""
import math,json
from pathlib import Path
import numpy as np
from detail_lotus_v8 import MESHES
from geometry_profiles import extruded_polygon
ROOT=Path(__file__).resolve().parents[1]
def improve(objects,colors,geo):
 colors.update(droneSoil='#aa9578',droneSlab='#e3dfd3',droneConcrete='#a7a99f',droneCable='#343a3c',droneBrick='#a66f58',droneRoof='#b6b4ab',dronePink='#d9acbb',droneLeaf='#486b3b',droneMetal='#7d898c')
 def add(n,p,s,mat,shape='box',group='context',rot=0,rz=0):
  objects.append(dict(name='Drone reference • '+n,p=[float(v) for v in p],s=[float(v) for v in s],mat=mat,shape=shape,group=group,rot=float(rot),rz=float(rz)))
 def line(n,a,b,w,mat,group='context'):
  a=np.array(a);b=np.array(b);d=b-a;length=np.linalg.norm(d);yaw=math.atan2(d[0],d[2]);tilt=-math.atan2(d[1],math.hypot(d[0],d[2]))
  add(n,(a+b)/2,[w,w,length],mat,group=group,rot=yaw);objects[-1]['tilt']=tilt
 def poly(n,points,y,h,mat,group='context'):
  q=np.array(points);lo=q.min(axis=0);span=q.max(axis=0)-lo;mid=(lo+q.max(axis=0))/2;m=extruded_polygon((q-mid)/span);key='droneExterior'+str(len(MESHES));MESHES[key]=dict(vertices=m.vertices[:,[0,2,1]].tolist(),faces=m.faces[:,::-1].tolist());add(n,[mid[0],y,mid[1]],[span[0],h,span[1]],mat,key,group)
 h=geo['helipadProposal'];route=np.array(h['vehicleAccessPolyline']);gate=np.array(h['accessGate']['centre'])
 # Dirt shoulders and discontinuous upright pale slabs alongside the existing silver approach.
 for i,(a,b) in enumerate(zip(route,route[1:])):
  d=b-a;L=np.linalg.norm(d);u=d/L;n=np.array([u[1],-u[0]])
  for side in [-1,1]:
   c=(a+b)/2+n*side*3.4;add('approach earth shoulder',[c[0],.055,c[1]],[1.25,.05,L],'droneSoil',rot=math.atan2(*u))
   if L>35:
    for j,t in enumerate(np.arange(10,L-8,11)):
     p=a+u*t+n*side*3.55
     if np.linalg.norm(p-gate)<8:continue
     add('pale roadside panel section',[p[0],.65,p[1]],[.14,1.18,2.1+(j%2)*.5],'droneSlab',rot=math.atan2(*u))
  if L>35:
   for t in [L*.28,L*.65]:
    p=a+u*t+n*5.2;add('small stacked roadside slabs',[p[0],.32,p[1]],[1.25,.5,1.7],'droneSlab',rot=math.atan2(*u))
 # Flared road mouth remains entirely on the field side; centreline is unchanged.
 end=route[-1];u=(end-route[-2]);u/=np.linalg.norm(u);n=np.array([u[1],-u[0]]);edge=np.array(h['mainRoadJoinEdge']);poly('junction flared shoulder',[end-u*9-n*3.4,edge[0]-n*1.3,edge[1]+n*1.3,end-u*9+n*3.4],.065,.03,'droneSoil')
 # Roadside electrical poles and a framed electrical structure, positions visually estimated.
 main=np.array(geo['roads'][0]['points']);join=np.array(h['campusRoadCentre']);ix=min(range(len(main)-1),key=lambda i:np.linalg.norm((main[i]+main[i+1])/2-join));t=main[ix+1]-main[ix];t/=np.linalg.norm(t);n=np.array([t[1],-t[0]])
 if np.dot(np.array(h['centre'])-join,n)<0:n=-n
 poles=[]
 for distance in [-86,-58,-30,-2,26,54,82]:
  p=join+t*distance+n*6.6;poles.append(p)
  add('concrete utility pole',[p[0],4.15,p[1]],[.18,8.3,.18],'droneConcrete')
  add('utility pole crossarm',[p[0],7.75,p[1]],[2.0,.12,.12],'droneMetal',rot=math.atan2(-n[1],n[0]))
  for k in [-.7,0,.7]:
   q=p+n*k;add('pole ceramic insulator',[q[0],7.96,q[1]],[.065,.22,.065],'stone','cylinder')
 for a,b in zip(poles,poles[1:]):
  for k in [-.7,0,.7]:
   for j in range(8):
    f0=j/8;f1=(j+1)/8;p0=a+(b-a)*f0+n*k;p1=a+(b-a)*f1+n*k
    line('sagging overhead cable',[p0[0],7.98-.55*4*f0*(1-f0),p0[1]],[p1[0],7.98-.55*4*f1*(1-f1),p1[1]],.022,'droneCable')
 frame=join+t*(-38)-n*7.0
 for side in [-1,1]:
  p=frame+t*side*2.2;add('electrical frame upright',[p[0],4,p[1]],[.22,8,.22],'droneMetal')
 for y in [2.8,5.2,7.8]:line('electrical frame beam',[frame[0]-t[0]*2.2,y,frame[1]-t[1]*2.2],[frame[0]+t[0]*2.2,y,frame[1]+t[1]*2.2],.14,'droneMetal')
 for shift in [-1.1,0,1.1]:
  p=frame+t*shift;add('electrical equipment housing',[p[0],3.55,p[1]],[.60,1.3,.70],'droneConcrete')
 # Main auditorium: gabled corrugated roof with long ridge and repeated ribs.
 roof=next(o for o in objects if o['name'].startswith('Hall roof'))
 MESHES['droneHallGable']={'vertices':[[-.5,-.5,-.5],[.5,-.5,-.5],[0,.5,-.5],[-.5,-.5,.5],[.5,-.5,.5],[0,.5,.5]],'faces':[[0,1,2],[3,5,4],[0,3,4],[0,4,1],[0,2,5],[0,5,3],[2,1,4],[2,4,5]]}
 roof.update(shape='droneHallGable',mat='droneRoof');roof['p'][1]=10.35;roof['s'][1]=1.45
 cx,_,cz=roof['p'];w,_,depth=roof['s'];r=roof['rot'];co,si=math.cos(r),math.sin(r)
 def roofpoint(x,z,y):return [cx+co*x+si*z,y,cz-si*x+co*z]
 for x in np.arange(-w/2+.25,w/2,.65):
  y=9.625+1.45*(1-abs(x)/(w/2))+.035
  line('auditorium roof corrugation',roofpoint(x,-depth/2,y),roofpoint(x,depth/2,y),.035,'droneMetal','roof')
 line('auditorium ridge cap',roofpoint(0,-depth/2,11.12),roofpoint(0,depth/2,11.12),.16,'droneRoof','roof')
 for x in [-w/2,w/2]:line('auditorium eave gutter',roofpoint(x,-depth/2,9.62),roofpoint(x,depth/2,9.62),.14,'droneMetal','roof')
 # Frontage finish: thin pink coping, sill bands and downpipes; retain existing arches and doors.
 hm=np.array(geo['hallPlanTransform'])
 def hall(x,z):return np.array([x,z,1])@hm
 for z in np.arange(-39,23,8):
  p=hall(-18.15,z);add('auditorium facade pink sill',[p[0],4.35,p[1]],[.10,.14,6.1],'dronePink',group='shell',rot=r)
  if not 4<z<13:
   p=hall(-18.0,z);add('auditorium frontage drainpipe',[p[0],3.7,p[1]],[.065,6.2,.065],'droneMetal',group='shell')
 # Residential roof furniture and pink piers, within its existing registered footprint.
 q=np.array(next(f['points'] for f in geo['footprints'] if f['id']=='south'));U=q[1]-q[0];V=q[3]-q[0];angle=math.atan2(-U[1],U[0]);front=q[0];length=np.linalg.norm(U)
 for u in np.linspace(.04,.96,21):
  p=front+U*u;add('residential pink facade pier',[p[0],5.15,p[1]],[.62,7.7,.13],'dronePink',group='campus',rot=angle)
 for u in [.12,.41,.70,.91]:
  p=q[0]+U*u+V*.55;add('residential rooftop stair room',[p[0],10.15,p[1]],[6.0,2.0,4.2],'white',group='roof',rot=angle)
  add('residential rooftop room coping',[p[0],11.21,p[1]],[6.25,.15,4.45],'droneSlab',group='roof',rot=angle)
 for u in np.linspace(.03,.97,30):
  p=q[0]+U*u+V*.08;add('residential roof parapet upright',[p[0],9.9,p[1]],[.12,.8,.12],'droneMetal',group='roof')
 for y in [9.55,9.94,10.27]:line('residential parapet horizontal',[*(q[0]+V*.08)[:1],y,(q[0]+V*.08)[1]],[*(q[1]+V*.08)[:1],y,(q[1]+V*.08)[1]],.055,'droneMetal','roof')
 # Left compound: extra low annexes and visible unfinished columns, approximate video placement.
 ref=json.loads((ROOT/'work/helipad-layout-reference.json').read_text(encoding='utf-8'));M=np.array(ref['imageToRegisteredPixel']);fit=np.array(geo['pixelToLonLat'])
 def imagepoint(x,y):
  uv=np.array([x,y,1])@M;lon,lat=np.array([*uv,1])@fit;return np.array([(lon-geo['originLongitude'])*geo['eastMetresPerDegree'],(geo['originLatitude']-lat)*geo['northMetresPerDegree']])
 for x,y,ww,dd in [(94,188,13,10),(73,247,17,12),(122,264,12,9)]:
  p=imagepoint(x,y);add('left compound low brick annex',[p[0],1.8,p[1]],[ww,3.6,dd],'droneBrick')
  add('left compound annex roof',[p[0],3.65,p[1]],[ww+.25,.16,dd+.25],'droneConcrete')
  for dx in [-ww*.38,0,ww*.38]:add('left annex unfinished upper column',[p[0]+dx,4.35,p[1]],[.25,1.35,.25],'droneConcrete')
 for y in np.arange(174,320,22):
  for x in [55,90]:
   p=imagepoint(x,y);add('left compound avenue tree trunk',[p[0],1.5,p[1]],[.14,3,.14],'bark','cylinder')
   add('left compound avenue tree crown',[p[0],4.0,p[1]],[1.8,2.1,1.7],'droneLeaf','sphereSmooth')
 # Garden edge planting and pavilion ring paths; keep the existing lawn/cross-path footprint.
 garden=np.array(next(f['points'] for f in geo['footprints'] if f['id']=='garden'))
 for a,b in [(garden[0],garden[1]),(garden[2],garden[3])]:
  for u in [.08,.25,.43,.62,.81,.95]:
   p=a*(1-u)+b*u;add('garden clipped tree',[p[0],1.9,p[1]],[1.0,1.35,1.0],'droneLeaf','sphereSmooth','campus')
 pc=np.array(geo['pavilionCentre'])
 for a in np.linspace(0,math.tau,80,endpoint=False):
  p=pc+np.array([math.cos(a),math.sin(a)])*12.55
  add('lotus outer garden path edging',[p[0],.31,p[1]],[.16,.12,1.05],'stone',group='campus',rot=math.pi/2-a)
 # Gazebo posts and plinth refine the already-present red-roof garden hut.
 hut=next((o for o in objects if o['name'].startswith('Red garden hut pitched')),None)
 if hut:
  x,y,z=hut['p'];w,_,d=hut['s']
  for dx in [-w*.38,w*.38]:
   for dz in [-d*.38,d*.38]:add('red gazebo veranda post',[x+dx,1.65,z+dz],[.13,2.7,.13],'droneMetal',group='campus')
 # User-marked brown frontage strip: dense trees between road and lotus-side wall.
 # Road, gate apron and utility pole bases retain clear space.
 frontage_objects=[o for o in objects if o['name'].startswith('Frontage boundary wall')]
 for x in np.arange(5.0,62.0,2.8):
  candidates=[]
  for a,b in zip(main,main[1:]):
   if min(a[0],b[0])-1<=x<=max(a[0],b[0])+1:
    f=(x-a[0])/(b[0]-a[0]);q=a+f*(b-a);direction=(b-a)/np.linalg.norm(b-a);normal=np.array([-direction[1],direction[0]])
    if normal[1]<0:normal=-normal
    candidates.append((q,normal))
  if not candidates:continue
  q,normal=candidates[0]
  for row,offset in enumerate([6.4,9.0]):
   pt=q+normal*offset
   if np.linalg.norm(pt-np.array(h['gate']))<11:continue
   # Keep trunks away from utility poles and boundary corner.
   if any(np.linalg.norm(pt-p)<1.7 for p in poles):continue
   if pt[0]>62:continue
   crown=1.05 if row==0 else 1.20;height=3.4+(int(x)%3)*.18
   add('marked brown strip tree trunk',[pt[0],1.35,pt[1]],[.095,2.7,.095],'bark','cylinder','campus')
   add('marked brown strip dense foliage',[pt[0],height,pt[1]],[crown,1.65,crown],'droneLeaf','sphereSmooth','campus')
 geo['droneExteriorReview']={'source':'Four user drone videos supplied 24 October 2026','scope':'Exterior visual details only; deployment and simulation logic unchanged','accuracy':'Existing registered footprint retained; new small-object positions and heights visually estimated'}
 return objects,colors,geo
