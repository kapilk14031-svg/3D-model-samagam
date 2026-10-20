# An illustrative architectural upgrade; no approved stage/structural plan was supplied.
extra_shapes={}
# Curved fabric canopy: arched cross-section, slight sag between longitudinal bays.
v=[];f=[];nx=12;nz=20
for iz in range(nz+1):
    z=iz/nz-.5
    for ix in range(nx+1):
        x=ix/nx-.5
        y=.035+.965*math.sqrt(max(0,1-(2*x)**2))-.035*math.sin(iz/nz*math.pi*8)**2
        v.append([x,max(.015,y),z])
for iz in range(nz):
    for ix in range(nx):
        a=iz*(nx+1)+ix;f.append([a,a+nx+1,a+nx+2,a+1])
extra_shapes['canopy']=[v,f]
# Hanging scalloped fabric and a separate narrow gold hem.
for name,hem in [('valance',False),('valancehem',True)]:
    v=[];f=[]
    for i in range(17):
        x=i/16-.5;bottom=.7*math.sin(math.pi*x)**2
        v.extend([[x,bottom,0],[x,bottom+.075 if hem else 1,0]])
    for i in range(16):a=i*2;f.append([a,a+2,a+3,a+1])
    extra_shapes[name]=[v,f]
# Semicircular arch band, with depth, used for the stage and entrance.
v=[];f=[]
for z in [-.5,.5]:
    for i in range(33):
        a=math.pi*i/32
        v.extend([[.5*math.cos(a),.57+.43*math.sin(a),z],[.435*math.cos(a),.57+.35*math.sin(a),z]])
for i in range(32):
    a=2*i;b=a+2;c=a+66;d=b+66
    f.extend([[a,b,b+1,a+1],[c+1,d+1,d,c],[a,c,d,b],[a+1,b+1,d+1,c+1]])
f.extend([[0,1,67,66],[64,130,131,65]])
extra_shapes['arch']=[v,f]
# Faceted ellipsoids and cylinders for floral arrangements, posts and luminaires.
v=[];f=[];rings=6;sides=12
for r in range(rings+1):
    a=math.pi*r/rings
    for j in range(sides):
        t=2*math.pi*j/sides;v.append([.5*math.sin(a)*math.cos(t),.5+.5*math.cos(a),.5*math.sin(a)*math.sin(t)])
for r in range(rings):
    for j in range(sides):
        a=r*sides+j;b=r*sides+(j+1)%sides;c=a+sides;d=b+sides
        if r==0:f.append([a,c,d])
        elif r==rings-1:f.append([a,c,b])
        else:f.append([a,c,d,b])
extra_shapes['ellipsoid']=[v,f]
v=[];f=[]
for y in [0,1]:
    for j in range(12):a=2*math.pi*j/12;v.append([.5*math.cos(a),y,.5*math.sin(a)])
for j in range(12):k=(j+1)%12;f.append([j,j+12,k+12,k])
f.extend([list(range(12)),list(range(23,11,-1))]);extra_shapes['cylinder']=[v,f]
def pb(name,x,z,w,d,h=1,color='#d5c7a7',y=0):box('Pandal / '+name,x,z,w,d,h,color,y=y,layer='pandal',ground='A')
def ps(name,kind,x,y,z,w,h,d,color,roof=False):
    add('Pandal / '+name,kind,x,y,z,w,h,d,color,'pandal','A')
    if roof:objects[-1]['part']='roof'
def beam(name,a,b,width=.4,color='#b9b8a5'):
    delta=[b[i]-a[i] for i in range(3)];length=math.sqrt(sum(t*t for t in delta));unit=[t/length for t in delta]
    q=[unit[2],0,-unit[0],1+unit[1]];ln=math.sqrt(sum(t*t for t in q));q=[t/ln for t in q]
    center=[(a[i]+b[i])/2 for i in range(3)]
    add('Pandal / '+name,'box',*center,width,length,width,color,'pandal','A');objects[-1]['quaternion']=q
pb('raised platform',325,100,334,344,1.7,'#c8b697')
pb('platform edge front',325,272,334,2.3,1.8,'#a18b69')
for i in range(10):
    x=176.5+i*33
    ps('curved fabric canopy '+str(i+1),'canopy',x,20,100,32.8,7.4,344,'#f0e6cf' if i%2 else '#e4cf9e',True)
    for z in [-72,272]:
        ps('scalloped fabric valance','valance',x,16.5,z,32.9,3.5,.1,'#925366',True)
        ps('gold scalloped hem','valancehem',x,16.5,z-.05,32.9,3.5,.1,'#d5b267',True)
    for z in [-67,18,103,188,268]:
        pb('support post',x-16.5,z,.8,.8,18.5,'#b4ae98',y=1.7)
        pb('column decorative sleeve',x-16.5,z,1.4,1.4,3,'#f1dfb7',y=1.7)
        # Open truss chords remain visible when the fabric roof is removed.
        beam('roof truss tie',[x-16,20,z],[x+16,20,z],.3)
        for k in range(4):
            xx=x-16+k*8;yy=20+6*math.sqrt(max(0,1-((xx-x)/16)**2))
            xx2=xx+8;yy2=20+6*math.sqrt(max(0,1-((xx2-x)/16)**2))
            beam('arched roof truss',[xx,yy,z],[xx2,yy2,z],.32)
            beam('roof truss web',[xx,20,z],[xx2,yy2,z],.18,'#c4bda8')
    for z in [30,115,205]:
        ps('warm ceiling light','ellipsoid',x,18.7,z,1.5,.7,1.5,'#ffe6ac')
for x in [160,490]:
    pb('side drape upper band',x,100,.5,344,2.3,'#dfc896',y=17.5)
    for z in range(-64,270,28):
        pb('side tied curtain',x,z,1.5,4.5,12,'#a4737e',y=2)
        pb('curtain tie',x,z,1.8,4.7,.7,'#d6b467',y=7)
# Seating carpets separated into blocks and cross aisles, without asserting capacity.
for row,z in enumerate([22,68,114,160,206,248]):
    for x in [205,278,372,445]:
        pb('seating carpet block',x,z,62,34,.16,'#9f6470' if row%2 else '#b87d70',y=1.75)
        for dx in [-30.3,30.3]:pb('carpet border',x+dx,z,.65,34,.03,'#dabd88',y=1.92)
        for zz in [z-16.5,z+16.5]:pb('carpet border',x,zz,62,.65,.03,'#dabd88',y=1.92)
pb('central processional aisle',325,139,16,280,.22,'#eadab8',y=1.75)
for x in [316,334]:pb('central aisle border',x,140,.75,278,.08,'#c6a458',y=1.98)
# Layered stage: no claim to reproduce the approved 2026 stage design.
pb('stage lower deck',325,-42,142,49,3.1,'#b39576',y=1.7)
pb('stage upper deck',325,-44,134,43,1,'#f0dfba',y=4.8)
pb('stage front fabric',325,-18.1,142,.5,2.6,'#a07176',y=1.9)
pb('stage back panel',325,-64,148,1.4,23,'#507c83',y=5.8)
for x in [254,396]:
    pb('backdrop side gold frame',x,-62.9,1.6,1,24,'#d3b271',y=5.8)
pb('backdrop top frame',325,-62.9,144,1,1.3,'#d3b271',y=29)
ps('central decorative medallion','ellipsoid',325,19,-62,10,10,.9,'#dfc486')
pb('podium',302,-34,3.5,3.5,4,'#4a6d72',y=5.8)
pb('podium gold facing',302,-32.2,3,.15,3.4,'#ccb379',y=6)
for x,w,h in [(325,76,26),(269,34,19),(381,34,19)]:
    ps('decorative stage arch','arch',x,5.8,-61.8,w,h,1.1,'#e2c88d')
    for xx in [x-w*.47,x+w*.47]:pb('stage arch pier',xx,-61.8,w*.065,1.1,h*.58,'#e2c88d',y=5.8)
for x in [237,413]:
    pb('LED screen frame',x,-57,30,2,18,'#2f4c58',y=5)
    pb('LED display',x,-55.8,27,.3,15.4,'#8bc0c6',y=6.3)
    pb('LED screen base',x,-57,34,5,1.6,'#c9b488',y=3.8)
for x in [218,432]:
    for k in range(4):pb('speaker array module',x,-20,3.5,3.5,2,'#34484d',y=7+k*2.3)
for k in range(6):pb('wide stage stair',325,-12+k*2.2,48,2.2,(6-k)*.65,'#d9c39b',y=1.7)
for x in [286,364]:
    pb('stage planter',x,-19,20,3.6,1,'#ab946e',y=5.7)
    for k in range(10):
        xx=x-9+k*2
        ps('floral foliage','ellipsoid',xx,6.4,-19,2.6,1.8,3,'#688b65')
        ps('marigold flowers','ellipsoid',xx,7.4,-18.7,1.7,1.5,1.7,'#e6b75a' if k%2 else '#e7d4ae')
for x in [255,395]:
    pb('stage floral pedestal',x,-31,3.5,3.5,5,'#d3b678',y=5.8)
    ps('pedestal flower bouquet','ellipsoid',x,10.5,-31,7,4.5,7,'#c6a26e')
# Entrance portal, queue railings and plant pots.
ps('entrance arch','arch',325,1.7,281,50,19,2.7,'#d8bc7b')
for x in [301.5,348.5]:
    pb('entrance arch column',x,281,3.2,3,11.3,'#d8bc7b',y=1.7)
for x in [313,337]:
    for z in range(278,309,6):
        ps('queue stanchion','cylinder',x,1.7,z,.45,1.3,.45,'#b89b68')
    pb('queue guide rail',x,293,.17,31,.15,'#c8ae7b',y=2.7)
for x in [171,200,450,479]:
    ps('entry plant pot','cylinder',x,1.7,274,3.4,3.5,3.4,'#b79878')
    ps('entry topiary','ellipsoid',x,4.7,274,5.5,6,5.5,'#658668')
label('MAIN SATSANG PANDAL',325,175,42);labels[-1]['layer']='pandal'
label('STAGE • ILLUSTRATIVE DESIGN',325,-60,36);labels[-1]['layer']='pandal'
label('CENTRAL AISLE',325,120,4);labels[-1]['layer']='pandal'
label('PANDAL ENTRANCE',325,282,23);labels[-1]['layer']='pandal'
label('79th Nirankari Sant Samagam',325,-60.3,17);labels[-1].update(layer='pandal',stageOnly=True,banner=True)
