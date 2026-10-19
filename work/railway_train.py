"""Illustrative passenger train placed on the traced railway axis."""
current='TRAIN01';start=len(objects)
rail=next(f for f in features if f['id']=='H06')['path']
def rail_position(u):
    for a,b in zip(rail,rail[1:]):
        if a[0]<=u<=b[0]:
            t=(u-a[0])/(b[0]-a[0]);p=planpoint(u,a[1]+t*(b[1]-a[1]))
            aa=planpoint(*a);bb=planpoint(*b)
            angle=math.atan2(bb[0]-aa[0],bb[2]-aa[2]);return p,angle
for car in range(7):
    origin,angle=rail_position(1084-car*19.5);ca=math.cos(angle);sa=math.sin(angle);engine=car==0
    length=21 if engine else 25;body='#bd592c' if engine else '#245c84';name='TRAIN / '+('LOCOMOTIVE' if engine else f'COACH {car:02}')
    def tb(part,x,z,w,d,h,color,y=0,kind='box'):
        px=origin[0]+x*ca+z*sa;pz=origin[2]-x*sa+z*ca
        if kind=='box':box(name+' / '+part,px,pz,w,d,h,color,y,'context')
        else:add(name+' / '+part,kind,px,y,pz,w,h,d,color,'context')
        objects[-1]['rotY']=angle
    tb('underframe',0,0,4.4,length,.7,'#232a2c',2)
    tb('painted coach body',0,0,5.2,length,3.4,body,2.7)
    tb('rounded metal roof',0,0,5.35,length+.2,.7,'#b6b9b5',6.1,'ellipsoid')
    for side in [-1,1]:
        tb('cream window band',side*2.62,0,.07,length-.5,1.25,'#e6dfca',4.45)
        tb('lower trim',side*2.64,0,.07,length-.3,.18,'#c8c6b8',3.25)
        for z in ([-5,5] if engine else [-8,-4,0,4,8]):
            tb('passenger window' if not engine else 'cab side window',side*2.68,z,.09,2.5,.95,'#25424e',4.62)
        for z in [-length*.39,length*.39]:
            tb('door',side*2.68,z,.1,1.5,2.6,'#bcc6c6' if not engine else '#774530',3)
            tb('door glazing',side*2.75,z,.06,.85,.8,'#253d48',4.6)
        for z in [-length*.31,length*.31]:
            tb('bogie',0,z,4.8,4.2,.65,'#24292a',1.7)
            for off in [-1.2,1.2]:tb('steel wheel',side*2.15,z+off,.65,1.5,1.5,'#252b2e',1.15,'ellipsoid')
    for end in [-1,1]:
        tb('coupling',0,end*(length/2+.5),.75,1.1,.5,'#22282a',2.25)
        if engine:
            tb('cab windscreen',0,end*(length/2+.06),4.1,.08,1.3,'#253c46',4.5)
            for side in [-1,1]:tb('headlamp',side*1.65,end*(length/2+.13),.55,.1,.45,'#f3e1ac',3.5)
    if engine:
        tb('roof equipment',0,0,3.4,8,.65,'#596167',6.65)
        for off in [-3,3]:tb('roof insulator',0,off,.6,.6,.5,'#615648',7.2)
        tb('pantograph top',0,0,3.5,5,.16,'#252b2e',8.3)
for o in objects[start:]:
    o['userAdded']=True;o['status']='Illustrative stationary train on source railway alignment; no actual service, livery or timetable asserted'
train_anchor,_=rail_position(1025)
labels.append(dict(text='PASSENGER TRAIN · BHODWAL MAJRI',p=[train_anchor[0],12,train_anchor[2]],layer='context',userAdded=True))
train_info=dict(coaches=6,locomotives=1,anchor=train_anchor,status='Illustrative stationary train, not a real service depiction')
