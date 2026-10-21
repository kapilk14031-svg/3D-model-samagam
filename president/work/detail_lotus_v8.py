import math
from detail_lotus import DOME

def swept(profile,start,end,n=40):
    vertices=[];faces=[];m=len(profile)
    for i in range(n+1):
        a=start+(end-start)*i/n
        vertices.extend([[r*math.sin(a),y,r*math.cos(a)] for r,y in profile])
    for i in range(n):
        for j in range(m-1):
            a=i*m+j;b=a+m;faces.extend([[a,b,a+1],[a+1,b,b+1]])
    for off,reverse in [(0,False),(n*m,True)]:
        for j in range(1,m-2):faces.append([off,off+j+1,off+j] if reverse else [off,off+j,off+j+1])
    return dict(vertices=vertices,faces=[q[::-1] for q in faces])

def petal(inverted=False):
    vertices=[];faces=[];nu=8;nv=8
    for side in [-1,1]:
        for j in range(nv+1):
            t=j/nv
            for i in range(nu+1):
                u=2*i/nu-1
                if inverted:
                    x=.5*u*(.96-.18*math.sin(math.pi*t));y=t+.08*(1-abs(u))*(1-t)**5;z=.45*(1-t)**2+.12*math.cos(u*math.pi/2)
                else:
                    width=max(.005,(1-t)**.5)*(1+.2*math.sin(math.pi*t));x=.5*u*width;y=t;z=.19*(1-u*u)*math.sin(math.pi*t)+.5*t*t
                vertices.append([x,y,z+side*.018])
    count=(nu+1)*(nv+1)
    for side in range(2):
        for j in range(nv):
            for i in range(nu):
                a=side*count+j*(nu+1)+i;b=a+nu+1;tri=[[a,b,a+1],[a+1,b,b+1]]
                faces.extend([q[::-1] if side else q for q in tri])
    return dict(vertices=vertices,faces=faces)

MESHES={
 'hutRoof':dict(vertices=[[-.5,0,-.5],[.5,0,-.5],[.5,0,.5],[-.5,0,.5],[0,1,0]],faces=[[0,4,1],[1,4,2],[2,4,3],[3,4,0],[0,1,2],[0,2,3]]),
 'lotusCup':swept([(6.1,0),(6.1,1),(8,1),(8.2,.9),(7.1,.4),(7.5,0),(6.1,0)],math.radians(18),math.tau-math.radians(18)),
 'lotusDrum':swept([(5.74,0),(5.74,1),(5.92,1),(5.92,0),(5.74,0)],math.radians(10),math.tau-math.radians(10)),
 'lotusStair':swept([(0,0),(0,1),(1,1),(1,0),(0,0)],-math.radians(28),math.radians(28),32),
 'lotusNosing':swept([(.986,0),(.986,1),(1,1),(1,0),(.986,0)],-math.radians(28),math.radians(28),32),
 'lotusPetalSculpt':petal(), 'lotusSkirtPetal':petal(True)}

def refine_lotus(objects,colors,signs):
    objects[:]=[o for o in objects if not o['name'].startswith(('Lotus ','Meditation pavilion','Pavilion '))]
    colors.update(lotusIvory='#eeeae2',lotusPink='#dfabbc',lotusGlass='#718185',lotusFinial='#f8ad36',lotusStone='#626a6a',lotusPot='#e7e9dd')
    def add(name,p,s,mat='lotusIvory',shape='box',rot=0):
        objects.append(dict(name='Pavilion '+name,p=[28+p[0],p[1],-45+p[2]],s=s,mat=mat,shape=shape,group='campus',rot=rot))
    def cyl(name,r,y,h,mat='lotusIvory',x=0,z=0):add(name,[x,y,z],[r,h,r],mat,'cylinder')
    cyl('circular paved apron • satellite outline',11.4,.25,.15,'stone')
    add('pink circular lotus base with entrance opening',[0,.4,0],[1,3.4,1],'lotusPink','lotusCup')
    for i in range(52):
        a=math.tau*i/52
        if min(a,math.tau-a)<math.radians(19):continue
        add('curved upper pink petal • count inferred',[7.98*math.sin(a),3.55,7.98*math.cos(a)],[.99,1.65,1.12],'lotusPink','lotusPetalSculpt',a)
        add('fluted lower inverted petal',[7.6*math.sin(a),.43,7.6*math.cos(a)],[.98,3.12,1.0],'lotusPink','lotusSkirtPetal',a)
    add('white drum with entrance void',[0,3.75,0],[1,3.4,1],'lotusIvory','lotusDrum')
    for i in range(12):
        a=math.tau*i/12
        if i==0:continue
        x=5.95*math.sin(a);z=5.95*math.cos(a)
        add('narrow two-part drum window',[x,5.45,z],[.58,2.65,.10],'lotusGlass',rot=a)
        for dx in [-.34,.34]:add('white window side frame',[x+math.cos(a)*dx,5.45,z-math.sin(a)*dx],[.055,2.75,.13],rot=a)
        for y in [4.1,5.77,6.8]:add('window horizontal transom',[x,y,z],[.7,.065,.14],rot=a)
        for dx in [-.17,0,.17]:add('fine window grille',[x+math.cos(a)*dx,5.5,z-math.sin(a)*dx],[.014,2.5,.13],'metal',rot=a)
    for i in range(12):
        r=12.6-i*.54;top=.4+(i+1)*.28
        add('curved entrance stair riser',[0,.31,0],[r,top-.31,r],'lotusStone','lotusStair')
        add('dark stone stair tread',[0,top,0],[r-.07,.045,r-.07],'lotusStone','lotusStair')
        add('light stair nosing',[0,top+.05,0],[r,.035,r],'lotusIvory','lotusNosing')
        if i%2==0:
            for side in [-1,1]:
                a=side*math.radians(27);x=(r-.2)*math.sin(a);z=(r-.2)*math.cos(a)
                cyl('stair-side flower pot',.20,top+.18,.32,'lotusPot',x,z)
                add('stair pot planting',[x,top+.43,z],[.22,.22,.22],'tree','sphereSmooth')
    add('entrance landing',[0,3.75,6.08],[3.5,.14,1.65],'lotusStone')
    add('double glass entrance door',[0,5.37,5.94],[2,3.2,.08],'lotusGlass')
    for x in [-1.04,0,1.04]:add('entrance tall white jamb',[x,5.4,6],[.07,3.3,.12])
    for y in [3.8,4.25,6.3,7.02]:add('entrance white horizontal rail',[0,y,6],[2.14,.07,.12])
    for x in [-.14,.14]:add('door handle',[x,5.25,6.1],[.025,.35,.035],'metal')
    cyl('projecting white eave fascia',6.65,7.2,.27)
    cyl('eave lower shadow reveal',6.42,7.01,.08,'stone')
    add('curved white dome',[0,7.32,0],[6.35,5,6.35],'lotusIvory','lotusDome')
    for i in range(240):
        a=math.tau*i/240;phase=(i%20)/20;h=.18+.52*(1-abs(2*phase-1))
        add('pink fluted dome springing band',[6.32*math.sin(a),7.35+h/2,6.32*math.cos(a)],[.07,h,.055],'lotusPink',rot=a)
    for r,y,h in [(.65,12.34,.17),(.49,12.55,.22),(.37,12.76,.17)]:cyl('pink finial pedestal collar',r,y,h,'lotusPink')
    for i in range(10):
        a=math.tau*i/10
        add('finial lotus crown petal',[.41*math.sin(a),12.78,.41*math.cos(a)],[.31,.49,.35],'lotusPink','lotusPetalSculpt',a)
    add('orange finial emblem disk',[0,13.7,0],[.34,.44,.075],'lotusFinial','sphereSmooth')
    key='sign-lotus';colors[key]='#ffffff';p=[28,7.22,-38.31]
    signs.append(dict(key=key,lines=['तपस्या धाम'],p=p,size=[2.5,.25],rot=0,source='Screenshot 110314: visible red doorway-frieze text; Dec 2022 imagery. Current presence not independently verified.',bg='#eeeae2',fg='#9c4e59',placement='Above entrance as photographed; dimensions estimated'))
    objects.append(dict(name='Pavilion observed entrance name: तपस्या धाम',p=p,s=[2.5,.25,1],mat=key,shape='sign',group='campus',rot=0))
    add('raised front flower bed',[0,.58,15.2],[4.2,.6,2.2],'lotusStone')
    add('flower-bed soil',[0,.91,15.2],[3.8,.08,1.8],'soil')
    for i in range(7):
        x=-1.8+i*.6;cyl('front ledge flower pot',.22,1.15,.42,'lotusPot',x,14.2)
        add('front pot plant',[x,1.56,14.2],[.28,.43,.28],'tree','sphereSmooth')
    for i in range(18):
        x=-1.7+(i%6)*.67;z=14.8+(i//6)*.43
        add('flower-bed foliage',[x,1.08,z],[.35,.25,.3],'tree','sphereSmooth')
        add('flower blossom',[x+.1,1.31,z],[.09,.065,.09],'flower','sphereSmooth')
    for a in [45,85,125,165,205,245,285,315]:
        t=math.radians(a);x=10.9*math.sin(t);z=10.9*math.cos(t)
        cyl('slender globe lamp post',.045,1.02,1.45,'metal',x,z)
        add('white spherical garden lamp',[x,1.8,z],[.19,.19,.19],'light','sphereSmooth')
    add('wide straight front walkway • Retreat-centre photo',[0,.38,20],[6,.13,15],'stone')
    for z in [17,20,23,26]:
        for x in [-3.2,3.2]:
            cyl('front walkway globe post',.045,1.03,1.3,'metal',x,z)
            add('front walkway globe',[x,1.76,z],[.19,.19,.19],'light','sphereSmooth')
    for x in [-5.2,5.2]:
        cyl('walkway fan palm trunk',.32,1.9,3.3,'bark',x,24)
        for i in range(10):
            a=math.tau*i/10
            add('walkway fan palm leaf',[x+1.1*math.sin(a),3.7,24+1.1*math.cos(a)],[1.3,2.2,.08],'tree','petal',a)
            objects[-1]['tilt']=math.pi/2-.2
    return objects,colors,signs
