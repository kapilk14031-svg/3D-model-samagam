"""Thin presentation routes snapped to road axes; source route sketches remain in PDF."""
def road_aligned_route(route,index):
    road_segments=[]
    for f in features:
        if f['kind'] not in ['road','internal_road','flyover'] or not f.get('path'):continue
        pp=[planpoint(*q) for q in f['path']]
        for a,b in zip(pp,pp[1:]):road_segments.append((f,a,b))
    raw=[planpoint(*q) for q in route['points']];samples=[]
    for a,b in zip(raw,raw[1:]):
        n=max(1,math.ceil(math.dist(a,b)/6))
        samples.extend([[a[k]+(b[k]-a[k])*i/n for k in range(3)] for i in range(n)])
    samples.append(raw[-1]);result=[]
    for p in samples:
        best=None
        for f,a,b in road_segments:
            dx=b[0]-a[0];dz=b[2]-a[2];ll=dx*dx+dz*dz
            if ll<.01:continue
            t=max(0,min(1,((p[0]-a[0])*dx+(p[2]-a[2])*dz)/ll));x=a[0]+t*dx;z=a[2]+t*dz;dist=math.hypot(x-p[0],z-p[2])
            if best is None or dist<best[0]:best=(dist,f,x,z,dx,dz,math.sqrt(ll))
        _,f,x,z,dx,dz,ll=best;offset=((index%5)-2)*.65
        x-=dz/ll*offset;z+=dx/ll*offset;y=1.32
        if f['kind'] in ['road','flyover']:
            for u in underpass_nav:
                along=(x-u['anchor'][0])*math.sin(u['angle'])+(z-u['anchor'][2])*math.cos(u['angle'])
                y=max(y,1.32+9.9*max(0,min(1,(90-abs(along))/75)))
        if f['kind']=='flyover':y=max(y,11.22)
        if not result or math.dist(result[-1],[x,y,z])>.1:result.append([x,y,z])
    return result
