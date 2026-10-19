# Executed by build_model.py with its local mesh helpers. All dimensions and
# reconstruction details are illustrative, not a surveyed engineering design.
fly_x=round(325+(77.0117753-77.0261412)*111320*math.cos(math.radians(29.21)))
fly_z=round(100-(29.2405197-29.179636)*111320)
fly_angle=math.radians(23.26)
def flypos(x,z):
    return [fly_x+x*math.cos(fly_angle)+z*math.sin(fly_angle),fly_z-x*math.sin(fly_angle)+z*math.cos(fly_angle)]
def fbox(name,x,z,w,d,h=1,color='#a9b1a3',y=0,angle=0):
    xx,zz=flypos(x,z);box('Samalkha flyover / '+name,xx,zz,w,d,h,color,y=y,layer='flyover')
    objects[-1]['rotY']=fly_angle+angle
def flabel(text,x,z,y=14):
    xx,zz=flypos(x,z);label(text,xx,zz,y);labels[-1]['layer']='flyover'
fbox('separate northern context base',0,0,760,1770,2,'#b7bea5',y=-3)
for side in [-1,1]:
    fbox('ground-level service road',side*39,0,14,1680,.45,'#a9aca2')
    fbox('sidewalk',side*50,0,4,1680,.55,'#d4cdb6')
for z in [-600,600]:
    fbox('NH-44 approach pavement',0,z,40,570,.6,'#657379')
for x in [-10,10]:
    fbox('elevated deck slab',x,0,18.8,180,1.3,'#bfc3b7',y=8.8)
    fbox('elevated road wearing surface',x,0,18.5,180,.16,'#5e6c73',y=10.1)
# Concrete deck girders and pier caps, leaving the transverse road unobstructed.
for x in [-16,-10,-4,4,10,16]:
    fbox('longitudinal underside girder',x,0,1.4,176,1,'#9ba8a3',y=7.8)
for z in [-62,62]:
    for x in [-10,10]:
        fbox('pier base',x,z,6,8,.6,'#c3c2af')
        fbox('support pier',x,z,2.7,3.8,6.6,'#b5c0b8',y=.6)
        fbox('pier cap',x,z,17.5,4,1.2,'#a9b7b1',y=7.2)
fbox('transverse road below span',0,0,720,17,.42,'#8c9591')
for side in [-1,1]:
    # Wedge geometry makes the approaches visibly slope down to ground.
    xx,zz=flypos(0,side*200)
    add('Samalkha flyover / approach ramp — assumed length','ramp',xx,.55,zz,40,9.7,220,'#657379','flyover')
    objects[-1]['rotY']=fly_angle+(math.pi if side<0 else 0)
    for k in range(22):
        z=side*(95+k*10);height=10.25-(abs(z)-90)/220*9.7
        for x in [-19.7,19.7]:
            fbox('ramp side retaining wall',x,z,.6,10,max(.4,height),'#babfae')
            fbox('ramp barrier',x,z,.65,10,1,'#dedac8' if k%2 else '#43504f',y=height)
        fbox('ramp centre divider',0,z,1.1,10,.8,'#b9bba4',y=height)
        if k%2==0:
            for x in [-13,-7,7,13]:fbox('ramp lane dash',x,z,.16,5,.06,'#eee7cf',y=height+.12)
# Side barriers alternate black and white, as seen in the Street View reference.
for z in range(-85,90,5):
    for x in [-19.5,19.5]:
        fbox('black and white concrete edge barrier',x,z,.8,5,1.1,'#ebe9db' if z%10 else '#3f5051',y=10.25)
    fbox('central safety barrier',0,z,1.1,5,.9,'#b9c0af',y=10.25)
for z in range(-850,860,20):
    if 90<abs(z)<310:continue
    yy=10.35 if abs(z)<=90 else .72
    for x in [-13,-7,7,13]:fbox('NH-44 lane marking',x,z,.16,8,.06,'#ede7d3',y=yy)
for z in [-115,-45,35,115]:
    yy=10.25 if abs(z)<=90 else 9.15
    fbox('median lighting mast',0,z,.2,.2,10,'#647878',y=yy)
    fbox('lighting cross-arm',0,z,7,.25,.2,'#647878',y=yy+9.5)
    for x in [-3,3]:fbox('lamp head',x,z,.8,1.4,.25,'#dcd6ae',y=yy+9.3)
for side in [-1,1]:
    for r in range(8):
        for c in range(3):
            x=side*(85+c*64);z=-640+r*175+(c%2)*25
            h=5+(r+c)%4*2
            fbox('illustrative roadside urban building',x,z,35+(r%3)*8,65,h,'#c1baa6')
            fbox('building roof coping',x,z,37+(r%3)*8,67,.3,'#dfd8bf',y=h)
            for dz in [-15,10]:
                fbox('roadside shop frontage',x-side*(18+(r%3)*4),z+dz,.3,13,2.5,'#8fa49f',y=1)
def fcar(name,x,z,yy,color='#d6d8cd',truck=False):
    w=2.5 if not truck else 3;length=5 if not truck else 12
    fbox(name+' body',x,z,w,length,1.2 if not truck else 3.1,color,y=yy+.35)
    fbox(name+' windscreen',x,z-1,w*.86,1.9,.75,'#6c8f9b',y=yy+1.5 if not truck else yy+2.6)
    for dx in [-w/2,w/2]:
        for dz in [-length*.32,length*.32]:fbox(name+' wheel',x+dx,z+dz,.24,.7,.65,'#384442',y=yy)
for i,(x,z) in enumerate([(-5,-68),(-12,-20),(5,12),(12,65),(-12,45),(5,-48)]):
    fcar('vehicle '+str(i+1),x,z,10.3,['#dedfce','#8ba5b0','#c49f6b'][i%3],i==1)
for i,(x,z) in enumerate([(-39,-25),(39,80),(-39,200)]):fcar('service-road vehicle '+str(i),x,z,.5,'#c6d1c5')
flabel('SAMALKHA • NH-44 VEHICLE FLYOVER',0,-55,37)
flabel('ELEVATED CARRIAGEWAYS',0,30,27)
flabel('ROAD UNDER THE FLYOVER',110,0,8)
flabel('APPROACH RAMP • APPROXIMATE',0,245,18)
flabel('GROUND-LEVEL SERVICE ROAD',-65,140,12)
flabel('TOWARD SAMAGAM • SOUTH',0,680,14)
flyover_info=dict(name='Samalkha Flyover',maps_pin=[29.2405197,77.0117753],local_anchor=[fly_x,0,fly_z],straight_line_km=6.91,imagery_capture='August 2023',geometry='Illustrative deck, ramps, piers and urban masses. No surveyed dimensions.',placement='Approximate northern offset from venue listing pin; not a georeferenced survey.',street_view='https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=29.2405716,77.0117377&heading=156.74')
