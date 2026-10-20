"""Presentation detailing on PDF-traced axes; no surveyed road dimensions inferred."""
def offset_path(points,offset):
    result=[]
    for i,p in enumerate(points):
        a=points[max(0,i-1)];b=points[min(len(points)-1,i+1)]
        if i==0 or i==len(points)-1:
            dx=b[0]-a[0];dz=b[2]-a[2];ll=math.hypot(dx,dz);nx=-dz/ll;nz=dx/ll;factor=1
        else:
            d1=[p[0]-a[0],p[2]-a[2]];d2=[b[0]-p[0],b[2]-p[2]]
            l1=math.hypot(*d1);l2=math.hypot(*d2);n1=[-d1[1]/l1,d1[0]/l1];n2=[-d2[1]/l2,d2[0]/l2]
            nx=n1[0]+n2[0];nz=n1[1]+n2[1];ll=math.hypot(nx,nz)
            if ll<.01:nx,nz=n1;factor=1
            else:nx/=ll;nz/=ll;factor=min(1.75,1/max(.57,nx*n1[0]+nz*n1[1]))
        result.append([p[0]+nx*offset*factor,p[1],p[2]+nz*offset*factor])
    return result

def ribbon(name,pts,width,height,color,layer,y=0,offset=0):
    p=offset_path(pts,offset);left=offset_path(p,-width/2);right=offset_path(p,width/2)
    vv=[];ff=[]
    for a,b in zip(left,right):vv.extend([[a[0],a[1]+y,a[2]],[b[0],b[1]+y,b[2]],[a[0],a[1]+y+height,a[2]],[b[0],b[1]+y+height,b[2]]])
    for i in range(len(pts)-1):
        k=i*4;n=k+4;ff.extend([[k+3,n+3,n+2,k+2],[k,k+1,n+1,n],[k,n,n+2,k+2],[k+1,k+3,n+3,n+1]])
    ff.extend([[0,2,3,1],[len(vv)-4,len(vv)-3,len(vv)-1,len(vv)-2]])
    key='roadmesh'+str(len(extra_shapes));extra_shapes[key]=[vv,ff];add(name,key,0,0,0,1,1,1,color,layer)

def dashed(name,pts,offset,width,color,layer,y=1.16,dash=5,gap=9):
    p=offset_path(pts,offset);phase=0
    for a,b in zip(p,p[1:]):
        dx=b[0]-a[0];dz=b[2]-a[2];ll=math.hypot(dx,dz);t=phase
        while t<ll:
            end=min(ll,t+dash)
            if end-t>.1:
                aa=[a[j]+(b[j]-a[j])*t/ll for j in range(3)];bb=[a[j]+(b[j]-a[j])*end/ll for j in range(3)]
                ribbon(name,[aa,bb],width,.045,color,layer,y)
            t+=dash+gap
        phase=t-ll

def detailed_road(f,p,width):
    name=f['name'];highway=f['kind']=='road';layer='context'
    if highway:
        dense=[]
        for a,b in zip(p,p[1:]):
            n=max(1,math.ceil(math.dist(a,b)/6))
            dense.extend([[a[j]+(b[j]-a[j])*i/n for j in range(3)] for i in range(n)])
        p=dense+[p[-1]]
    ribbon(name+' compacted shoulder',p,width+5,.35,'#b9b7a0',layer,-.1)
    ribbon(name+' continuous road surface',p,width,1.1,'#283639' if highway else '#3d4847',layer)
    for off in [-width/2+.65,width/2-.65]:
        ribbon(name+' edge line',p,.22,.04,'#e8e5d2',layer,1.13,off)
        if highway:ribbon('NH44 shoulder edge',p,.8,.28,'#c9c7b1',layer,.4,off+(.95 if off>0 else -.95))
    if highway:
        ribbon('NH44 raised median',p,2.4,1,'#acb18c',layer,1.1)
        for off in [-1.35,1.35]:ribbon('NH44 median curb',p,.3,.48,'#ddd7bc',layer,1.1,off)
        for off in [-11.7,-6.7,6.7,11.7]:dashed('NH44 dashed lane separator',p,off,.28,'#f1edda',layer,dash=6,gap=11)
        # Sparse roadside luminaires; aesthetic equipment, not source inventory.
        for a,b in zip(p,p[1:]):
            length=math.dist(a,b)
            for t in range(48,int(length),110):
                ratio=t/length;v=[a[j]+(b[j]-a[j])*ratio for j in range(3)];dx=b[0]-a[0];dz=b[2]-a[2];ll=math.hypot(dx,dz)
                for side in [-1,1]:
                    xx=v[0]-dz/ll*side*(width/2+3);zz=v[2]+dx/ll*side*(width/2+3)
                    box('Illustrative NH44 light pole',xx,zz,.35,.35,11,'#8b9a94',0,layer)
                    box('Road light luminaire',xx,zz,1.5,2,.25,'#e5d4a6',11,layer)
    else:dashed(name+' centre guide',p,0,.22,'#dfd9bf',layer,dash=3,gap=8)

def detailed_flyover(p):
    def extended(a,b):
        dx=a[0]-b[0];dz=a[2]-b[2];ll=math.hypot(dx,dz)
        return [a[0]+dx/ll*90,-.9,a[2]+dz/ll*90]
    deck=[[v[0],9,v[2]] for v in p];deck=[extended(p[0],p[1])]+deck+[extended(p[-1],p[-2])]
    ribbon('NH44 flyover continuous deck and sloped ramps',deck,28,2,'#2d3b3e','bridges')
    for off in [-14,14]:
        ribbon('Flyover concrete parapet',deck,.8,1.25,'#d9d3bb','bridges',2,off)
        ribbon('Flyover edge reflector line',deck,.22,.04,'#f0e5bf','bridges',2.04,off*.93)
    ribbon('Flyover centre median',deck,1,1,'#b5b497','bridges',2)
    for off in [-7,7]:dashed('Flyover lane markings',deck,off,.25,'#f1ecda','bridges',2.07,5,9)
    for a,b in zip(p,p[1:]):
        dx=b[0]-a[0];dz=b[2]-a[2];ll=math.hypot(dx,dz)
        for t in range(15,int(ll),38):
            xx=a[0]+dx*t/ll;zz=a[2]+dz*t/ll
            box('Flyover concrete pier',xx,zz,4,6,8,'#b5b8aa',0,'bridges')
            box('Flyover pier crosshead',xx,zz,22,4,1,'#c8c9b6',8,'bridges');objects[-1]['rotY']=-math.atan2(dz,dx)+math.pi/2

