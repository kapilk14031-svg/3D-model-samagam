"""User-proposed water supply cluster in a vacant service parcel."""
current='WATER01';u,v=1260,610;x,_,z=planpoint(u,v);start=len(objects)
# Placement checks against source routes/walls/facilities and residential modules.
for du,dv in [(0,0),(-9,-11),(9,-11),(9,11),(-9,11)]:
    assert vacant(u+du,v+dv),'Supply pad intersects a reserved source feature'
assert all(abs(x-t['p'][0])>22 or abs(z-t['p'][2])>20 for t in sleeping_tent_centres)
def wb(part,dx,dz,w,d,h,color,y=0):box('WATER SUPPLY / '+part,x+dx,z+dz,w,d,h,color,y,'services')
def wc(part,dx,dz,diam,h,color,y=0):add('WATER SUPPLY / '+part,'cylinder',x+dx,y,z+dz,diam,h,diam,color,'services')
def pipe(part,a,b,r=.2,color='#315e80'):beam3('WATER SUPPLY / '+part,[x+a[0],a[1],z+a[2]],[x+b[0],b[1],z+b[2]],r,color,'services')
wb('concrete service pad',0,0,28,24,.35,'#b3aa96')
for dx in [-4,4]:
    for dz in [-4,4]:
        wb('steel tower leg',dx,dz,.45,.45,13,'#26363c',.35)
        wb('foundation pedestal',dx,dz,1.8,1.8,.8,'#97958a',.35)
for h in [1,5,9]:
    for dz in [-4,4]:
        pipe('tower cross brace',[-4,h,dz],[4,h+4,dz],.2,'#34474d')
        pipe('tower cross brace',[4,h,dz],[-4,h+4,dz],.2,'#34474d')
    for dx in [-4,4]:pipe('side brace',[dx,h,-4],[dx,h+4,4],.2,'#34474d')
wb('maintenance platform',0,0,12,12,.3,'#59696d',13)
wc('elevated blue supply tank',0,0,10.5,7,'#245b85',13.3)
for h in [13.7,15.5,17.3,19.1,20.2]:wc('tank reinforcing band',0,0,10.65,.12,'#7c9fae',h)
add('WATER SUPPLY / domed tank cover','ellipsoid',x,20.3,z,10.6,1.1,10.6,'#b4c6cc','services')
wc('inspection hatch',0,0,1.4,.35,'#465a62',21.1)
for off in [-.65,.65]:pipe('access ladder rail',[5.8+off,.4,0],[5.8+off,21.5,0],.1,'#a5b4b7')
for h in range(1,22):pipe('ladder rung',[5.15,h,0],[6.45,h,0],.09,'#a5b4b7')
for off in [-1,1]:
    wc('ground buffer tank',off*9,6,5,4,'#244f74',.35)
    add('WATER SUPPLY / buffer tank dome','ellipsoid',x+off*9,4.35,z+6,5,1,5,'#4b7290','services')
    pipe('buffer feed manifold',[off*9,.9,3.5],[off*9,.9,-6],.25)
pipe('vertical outlet riser',[-5.6,17,0],[-5.6,.8,0],.32)
pipe('outlet header',[-9,.8,-6],[9,.8,-6],.3)
pipe('distribution pipe',[-5.6,.8,0],[-5.6,.8,-6],.3)
wc('valve wheel',-5.6,-6,.8,.12,'#ae5540',1)
labels.append(dict(text='WATER SUPPLY TANKS · PROPOSED',p=[x,26,z],layer='services',userAdded=True))
for o in objects[start:]:o['userAdded']=True;o['status']='User-proposed water supply tanks in vacant parcel; illustrative geometry; capacity and pipe network not engineered'
water_info=dict(anchor=[x,0,z],elevated_tanks=1,buffer_tanks=2,source_uv=[u,v],status='User-proposed supply cluster, not an original PDF facility')
