"""User-added amusement area in a vacant parcel behind source road R18."""
current='';park_x,park_z=-576.8,-203.;park_start=len(objects);ride_layout=[]
def ab(part,x,z,w,d,h,color,y=0):box('USER ADDED JHULA ZONE / '+part,park_x+x,park_z+z,w,d,h,color,y,'amusement')
def ash(part,kind,x,y,z,w,h,d,color):add('USER ADDED JHULA ZONE / '+part,kind,park_x+x,y,park_z+z,w,h,d,color,'amusement')
def ap(x,y,z):return [park_x+x,y,park_z+z]
def arm(part,a,b,width=.35,color='#758c86'):beam3('USER ADDED JHULA ZONE / '+part,ap(*a),ap(*b),width,color,'amusement')
def ride(name,x,z):ride_layout.append(dict(name=name,p=[park_x+x,0,park_z+z],userAdded=True))
for side in [-1,1]:
    ab('perimeter walkway',side*45,0,4,94,.1,'#c6b592',.02)
    ab('perimeter walkway',0,side*45,94,4,.1,'#c6b592',.02)
ab('central promenade',0,0,5,88,.11,'#c9b997',.03)
ab('cross promenade',0,0,88,5,.11,'#c9b997',.03)
# 1. Ferris wheel: two steel rings, spokes, suspended cabins and braced A frames.
wx,wz=-24,-23;radius=12;cy=15
ash('Ferris wheel circular pad','cylinder',wx,0,wz,32,.18,28,'#b8a07b')
for side in [-1,1]:
    arm('Ferris wheel A frame',(wx-9,0,wz+side*5),(wx,cy,wz+side*1.5),.9,'#456d79')
    arm('Ferris wheel A frame',(wx+9,0,wz+side*5),(wx,cy,wz+side*1.5),.9,'#456d79')
    for j in range(24):
        a=j*math.tau/24;b=(j+1)*math.tau/24
        arm('Ferris wheel outer rim',(wx+radius*math.cos(a),cy+radius*math.sin(a),wz+side*1.2),(wx+radius*math.cos(b),cy+radius*math.sin(b),wz+side*1.2),.4,'#dbba6c')
    for j in range(12):
        a=j*math.tau/12;arm('Ferris wheel spoke',(wx,cy,wz+side*1.2),(wx+radius*math.cos(a),cy+radius*math.sin(a),wz+side*1.2),.2,'#9dada3')
for j in range(12):
    a=j*math.tau/12;xx=wx+radius*math.cos(a);yy=cy+radius*math.sin(a)
    color=['#b85c43','#d1a446','#487f8e','#698b61'][j%4]
    ab('Ferris wheel suspended cabin',xx,wz,2.7,2.7,2.2,color,yy-2.1)
    ab('Ferris cabin window',xx,wz+1.38,2.1,.1,.9,'#8bafb2',yy-.9)
    arm('Ferris cabin suspension',(xx,yy,wz),(xx,yy+1.1,wz),.12,'#687d77')
ride('Ferris wheel',wx,wz)
# 2. Carousel with a striped conical canopy and six small mounted seats.
cx,cz=23,-23
ash('carousel circular platform','cylinder',cx,.05,cz,22,.5,22,'#9b8370')
ash('carousel centre mast','cylinder',cx,.5,cz,1.5,7,1.5,'#c3a365')
vv=[[0,1,0]]+[[.5*math.cos(j*math.tau/24),0,.5*math.sin(j*math.tau/24)] for j in range(24)];ff=[[0,j+1,(j+1)%24+1] for j in range(24)]
extra_shapes['carouselcone']=[vv,ff];ash('carousel golden canopy','carouselcone',cx,6.4,cz,24,4,24,'#ca9b51')
for j in range(8):
    a=j*math.tau/8;xx=cx+7*math.cos(a);zz=cz+7*math.sin(a)
    ash('carousel seat pole','cylinder',xx,.6,zz,.16,5.9,.16,'#cbb77d')
    ab('carousel ride seat',xx,zz,2.6,1.5,.6,['#8c4d4e','#4f8290'][j%2],1.5)
    ab('carousel seat back',xx,zz+.7,2.6,.22,1,'#bcb593',1.9)
ride('Carousel',cx,cz)
# 3. Paired swing frames and hanging seats.
for base in [-28,-15]:
    for side in [-1,1]:
        arm('swing A frame',(base+side*5,0,15),(base+side*5,5.2,19),.35,'#497b82')
        arm('swing A frame',(base+side*5,0,23),(base+side*5,5.2,19),.35,'#497b82')
    arm('swing crossbeam',(base-5,5.2,19),(base+5,5.2,19),.45,'#c19353')
    for xx in [base-2.3,base+2.3]:
        for off in [-.9,.9]:arm('swing chain',(xx+off,5,19),(xx+off,1.6,19),.06,'#7a8780')
        ab('swing seat',xx,19,2.2,.8,.18,'#b76b4b',1.45)
ride('Swings',-22,19)
# 4. Slide tower, ladder and sloped chute.
sx,sz=23,19
for dx in [-2,2]:
    for dz in [-2,2]:ab('slide tower post',sx+dx,sz+dz,.35,.35,4.8,'#759060')
ab('slide tower platform',sx,sz,4.8,4.8,.3,'#b9965c',4)
ash('slide tower canopy','roof',sx,5.4,sz,5.7,2.2,5.7,'#a85c48')
for j in range(9):
    y=.3+j*.44;ab('slide ladder rung',sx,sz+3+j*.35,3,.22,.18,'#819587',y)
arm('slide chute',(sx,4.1,sz-2.5),(sx,.4,sz-13),2.5,'#77a2a5')
for side in [-1,1]:arm('slide side rail',(sx+side*1.35,4.5,sz-2.5),(sx+side*1.35,.8,sz-13),.22,'#d1a656')
ride('Slide tower',sx,sz)
# 5. Roundabout and two seesaws.
ash('roundabout base','cylinder',9,.1,33,9,.35,9,'#a98053')
ash('roundabout centre post','cylinder',9,.45,33,.5,1.5,.5,'#d3bb78')
for j in range(4):
    a=j*math.tau/4;arm('roundabout handrail',(9,1.7,33),(9+3.4*math.cos(a),1.7,33+3.4*math.sin(a)),.15,'#597e89')
ride('Roundabout',9,33)
for zz in [31,39]:
    ash('seesaw pivot','cylinder',-25,.1,zz,1.5,1.3,1.5,'#d0a255')
    arm('seesaw beam',(-30,1,zz),(-20,2.3,zz),.45,'#6f8c8b')
    ab('seesaw seat',-30,zz,1.5,1.2,.18,'#ad6148',1)
    ab('seesaw seat',-20,zz,1.5,1.2,.18,'#ad6148',2.3)
ride('Seesaws',-25,35)
# Low perimeter railings, benches and planted corners.
for side in [-1,1]:
    for q in range(-42,43,7):
        ab('playground fence post',side*48,q,.16,.16,1.5,'#557b74')
        ab('playground fence post',q,side*48,.16,.16,1.5,'#557b74')
    for yy in [.5,1.1]:
        ab('playground side fence rail',side*48,0,.12,96,.12,'#76938a',yy)
        for off in [-27,27]:ab('playground entrance-side fence',off,side*48,42,.12,.12,'#76938a',yy)
    for zz in [-35,0,35]:
        ab('park bench',side*39,zz,1.5,5,.3,'#938065',.8)
        ab('park bench back',side*40,zz,.2,5,1,'#938065',.8)
for xx,zz in [(-39,-39),(39,-39),(-39,39),(39,39)]:
    ash('park planter','cylinder',xx,0,zz,3,1.2,3,'#a18d6a')
    ash('park shrub','ellipsoid',xx,1.2,zz,4,2.2,4,'#60805d')
for o in objects[park_start:]:
    o['userAdded']=True;o['status']='User-requested jhula/amusement-zone proposal behind R18; not a facility shown in the source PDF; layout and dimensions illustrative'
labels.append(dict(text='R18 REAR / JHULA ZONE / USER ADDED',p=[park_x,32,park_z],layer='amusement',userAdded=True))
(OUT/'amusement-layout.json').write_text(json.dumps(ride_layout,indent=2),encoding='utf-8')
amusement_info=dict(centre=[park_x,0,park_z],user_added=True,rides=[r['name'] for r in ride_layout],area_source='Vacant parcel behind R18; user requested recreation zone')
