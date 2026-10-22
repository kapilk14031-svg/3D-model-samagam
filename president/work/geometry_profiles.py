import numpy as np
import trimesh

# Normalised profile of the solid scalloped spandrel seen above the arcade.
_PROFILE=[[-.5,-.5],[-.47,-.36],[-.42,-.15],[-.36,-.11],[-.32,-.12],[-.27,.04],[-.20,.11],[-.10,.12],[-.04,.24],[0,.30],[.04,.24],[.10,.12],[.20,.11],[.27,.04],[.32,-.12],[.36,-.11],[.42,-.15],[.47,-.36],[.5,-.5]]
SCALLOP=[]
for i in range(len(_PROFILE)-1):
    p0=np.array(_PROFILE[max(0,i-1)]);p1=np.array(_PROFILE[i]);p2=np.array(_PROFILE[i+1]);p3=np.array(_PROFILE[min(len(_PROFILE)-1,i+2)])
    for t in [0,.25,.5,.75]:SCALLOP.append((.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t)).tolist())
SCALLOP.extend([_PROFILE[-1],[.5,.5],[-.5,.5]])
def extruded_polygon(points):
    p=np.array(points,float)
    area=sum(p[i,0]*p[(i+1)%len(p),1]-p[(i+1)%len(p),0]*p[i,1] for i in range(len(p)))
    if area<0:p=p[::-1]
    ids=list(range(len(p)));tri=[]
    def cross(a,b,c):
        u=b-a;v=c-a;return u[0]*v[1]-u[1]*v[0]
    def inside(q,a,b,c):return min(cross(a,b,q),cross(b,c,q),cross(c,a,q))>=-1e-9
    while len(ids)>3:
        found=False
        for k,i in enumerate(ids):
            a=ids[k-1];c=ids[(k+1)%len(ids)]
            if cross(p[a],p[i],p[c])<=1e-9:continue
            if any(inside(p[j],p[a],p[i],p[c]) for j in ids if j not in [a,i,c]):continue
            tri.append([a,i,c]);ids.pop(k);found=True;break
        if not found:raise ValueError('Could not triangulate profile')
    tri.append(ids);n=len(p);verts=[[x,y,z] for z in [-.5,.5] for x,y in p];faces=[]
    for a,b,c in tri:faces.extend([[c,b,a],[a+n,b+n,c+n]])
    for j in range(n):
        k=(j+1)%n;faces.extend([[j,k,k+n],[j,k+n,j+n]])
    return trimesh.Trimesh(vertices=verts,faces=faces,process=False)

def paint_and_architecture(objects,colors):
    objects[:]=[o for o in objects if not o['name'].startswith(('Scalloped frontage arch lobe','Hall facade pilaster','Hall pink parapet cap'))]
    colors.update(plaster='#ece5db',pinkColumn='#c598a2',nicheGreen='#536443')
    def add(name,p,s,mat,shape='box',rot=0):objects.append(dict(name=name,p=p,s=s,mat=mat,shape=shape,group='shell',rot=rot))
    # All eight panels share exact springing stations over the hall envelope.
    stations=np.linspace(-43,23,9)
    for a,b in zip(stations,stations[1:]):
        add('Hall solid scalloped arcade spandrel • photo design',[-18.15,6.45,(a+b)/2],[b-a,2.6,.35],'plaster','spandrel',np.pi/2)
    for z in stations:
        add('Hall pink circular arcade column',[-18.25,2.65,float(z)],[.21,5.3,.21],'pinkColumn','cylinder')
        add('Hall arcade white springing collar',[-18.25,5.24,float(z)],[.26,.18,.26],'plaster','cylinder')
    add('Hall continuous pink parapet coping',[-18.4,8.5,-10],[1.1,.12,66],'pink')
    for o in objects:
        if o['name'].startswith('Facade gold uplight niche'):
            o['mat']='nicheGreen';x,y,z=o['p']
            for dz in [-.7,.7]:add('Niche white tiled side border',[x+.04,y,z+dz],[.26,1,.15],'white')
            for yy in [y-.45,y+.45]:add('Niche white tiled top and base',[x+.04,yy,z],[.26,.13,1.4],'white')
            add('Facade niche warm centre lamp',[x+.2,y,z],[.1,.12,.16],'light')
    return objects,colors
