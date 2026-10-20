"""User-proposed pedestrian bridge at the S04/P5 annotation; dimensions illustrative."""
current='S04';start=len(objects)
uv=source_at(855);cx,_,cz=planpoint(*uv)
# Across NH44; same local axis as the P5 parking approach.
segment=next((a,b) for a,b in zip(highway,highway[1:]) if a[0]<=uv[0]<=b[0])
aa,bb=segment
angle=math.atan2(aa[1]-bb[1],bb[0]-aa[0]);ca=math.cos(angle);sa=math.sin(angle)
def fp(x,y,z):return [cx+x*ca+z*sa,y,cz-x*sa+z*ca]
def fb(part,x,z,w,d,h,color,y=0):
    px,py,pz=fp(x,y,z);box('S04 FOOT OVER BRIDGE / '+part,px,pz,w,d,h,color,py,'bridges');objects[-1]['rotY']=angle
def fbeam(part,a,b,width=.16,color='#181e22'):
    beam3('S04 FOOT OVER BRIDGE / '+part,fp(*a),fp(*b),width,color,'bridges')
deck=24.;half=21.25;width=5.
fb('pedestrian deck',0,0,half*2,width,.55,'#b8b3a3',deck)
for x in [-half,half]:
    for z in [-2,2]:
        fb('steel support pier',x-math.copysign(1.6,x),z,.8,.8,deck,'#181e22')
        fb('pier foundation',x-math.copysign(1.6,x),z,2.3,2.3,.7,'#99988b')
for z in [-width/2,width/2]:
    for y in [deck+.75,deck+1.7,deck+5.2]:fbeam('walkway steel rail',[-half,y,z],[half,y,z],.18)
    for x in sorted(set(list(range(-int(half),int(half)+1,8))+[-int(half),int(half)])):
        fbeam('walkway vertical frame',[x,deck+.55,z],[x,deck+5.2,z],.16)
        if x+8<=half:fbeam('lattice brace',[x,deck+.75,z],[x+8,deck+1.7,z],.09)
fb('covered roof',0,0,half*2+1,width+1,.25,'#ded6bc',deck+5.2)
for side in [-1,1]:
    x=side*half;direction=side
    for i in range(48):
        z=direction*(48-i-.5)*.5
        fb('non-slip stair tread',x,z,5.3,.52,.5,'#b9b8ac',i*.5)
    for off in [-2.8,2.8]:
        fbeam('stair stringer',[x+off,0,direction*24],[x+off,deck,0],.3)
        fbeam('stair handrail',[x+off,1.6,direction*24],[x+off,deck+1.6,0],.16)
        for i in range(0,49,6):fbeam('stair guard post',[x+off,i*.5,direction*(48-i)*.5],[x+off,i*.5+1.6,direction*(48-i)*.5],.12)
    fb('stair entry landing',x,direction*26,6,5,.2,'#b7a990',.1)
labels.append(dict(text='S04 · FOOT OVER BRIDGE / P5',p=fp(0,31,0),layer='bridges',featureId='S04',userAdded=True))
for o in objects[start:]:
    o['userAdded']=True;o['status']='User-proposed S04/P5 pedestrian bridge across NH44; approximate position and illustrative dimensions; not a surveyed/approved design'
footbridge_info=dict(anchor=fp(0,0,0),deck_height=deck,span=half*2,angle=angle,stair_run=24.,stair_half_width=2.65,stair_x=half,deck_width=width,source='S04 near foot-overbridge / local bus stop annotation',status='User-requested schematic crossing; geometry is illustrative')
