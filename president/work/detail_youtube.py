import math

def improve(objects,colors):
    """Visible tour details only; geographic registration remains downstream."""
    additions=[]
    def add(n,p,s,mat='metal',shape='box',group='interior',rot=0,tilt=0):
        additions.append(dict(name=n,p=p,s=s,mat=mat,shape=shape,group=group,rot=rot,tilt=tilt))
    for o in objects:
        x,y,z=o['p'];w,h,d=o['s']
        if o['name'].startswith('Garden bollard lamp'):o['mat']='carpet'
        if o['name']=='Ceiling ventilation grille':
            for k in range(6):add('Ceiling diffuser parallel louvre',[x,y-.035,z-d*.4+k*d*.16],[w*.9,.028,.035],'dark',group='ceiling')
            for xx in [-w*.5,w*.5]:add('Ceiling diffuser white rim',[x+xx,y-.04,z],[.04,.035,d+.08],'white',group='ceiling')
        if o['name'].startswith('Ceiling light panel'):
            for xx in [-w*.51,w*.51]:add('Recessed ceiling light slim bezel',[x+xx,y-.015,z],[.035,.04,d+.06],'metal',group='ceiling')
        if o['name'].startswith('Hanging speaker'):
            add('Hanging speaker lower grille',[x,y-.2,z+.26],[w*.8,h*.65,.015],'vent',group='ceiling')
            add('Speaker upper mounting yoke',[x,y+h*.5+.07,z],[w+.1,.07,d*.6],'metal',group='ceiling')
        if o['name'].startswith('Open glazed door leaf'):
            add('Hall glazed entrance metal pull',[x+.15,y,z+.1],[.035,.65,.04],'metal',group='shell',rot=o['rot'])
    # Ground-level front-row sofas are visible separately from stage furniture.
    colors['lampBrown']='#72564a'
    for x in [-28,-8,12,32]:
        add('Decorative compound lantern pole • Short ~10s',[x,1.8,24],[.09,3.3,.09],'lampBrown',group='campus')
        add('Compound lantern glass housing',[x,3.6,24],[.38,.55,.38],'light',group='campus')
        add('Compound lantern pointed cap',[x,3.9,24],[.52,.3,.52],'lampBrown','hutRoof','campus')
        add('Compound lantern planter cross arm',[x,2.2,24],[1.25,.05,.05],'lampBrown',group='campus')
        for dx in [-.55,.55]:
            add('Lantern white hanging bowl',[x+dx,2.1,24],[.23,.18,.23],'white','sphereSmooth','campus')
            add('Lantern bowl planting',[x+dx,2.3,24],[.21,.25,.21],'tree','sphereSmooth','campus')
    for x in [-51,-44,-34,-27]:
        add('Hall front-row sofa seat',[x,1.35,4.5],[4.5,.3,1.5],'white','rounded')
        add('Hall front-row sofa back',[x,1.98,3.88],[4.5,1.1,.25],'white','rounded')
        for dx in [-2.1,2.1]:add('Hall front-row sofa arm',[x+dx,1.7,4.5],[.3,.65,1.5],'white','rounded')
    # Tapasya Dham: curtains, grey floor, white sheet, perimeter chairs, display
    # frame, vases and hanging ornament are visible at 10:40–11:20.
    def lotus(n,p,s,mat='white',shape='box',rot=0,tilt=0):
        add('Pavilion interior '+n,[28+p[0],p[1],-45+p[2]],s,mat,shape,'lotusInterior',rot,tilt)
    lotus('grey circular floor',[0,3.78,0],[5.72,.10,5.72],'vent','cylinder')
    lotus('continuous cream curtain backing',[0,3.85,0],[.95,2.9,.95],'curtain','lotusDrum')
    lotus('white meditation sheet',[0,3.86,0],[4,.035,4.5])
    for i in range(44):
        a=math.tau*i/44
        if min(a,math.tau-a)<.22:continue
        lotus('cream curtain fold',[5.58*math.sin(a),5.38,5.58*math.cos(a)],[.11,2.9,.11],'curtain','cylinder')
    for x in [-4.15,4.15]:
        for z in [-1.3,1.3]:
            lotus('cream perimeter chair cushion',[x,4.2,z],[1,.2,1],'seat','rounded')
            lotus('cream perimeter chair back',[x,4.65,z-.4],[1,.85,.18],'seat','rounded')
    lotus('wooden display frame',[0,5.2,-4.95],[2.9,3,.18],'wood')
    lotus('display artwork area • portrait not replicated',[0,5.2,-4.82],[2.5,2.65,.025],'lotusGlass')
    for x in [-1.8,1.8]:
        lotus('tall floral vase',[x,4.45,-4.7],[.22,1.2,.22],'white','cylinder')
        lotus('white floral arrangement',[x,5.15,-4.7],[.34,.38,.34],'white','sphereSmooth')
    lotus('hanging gold ornament bowl',[0,6.55,0],[.65,.3,.65],'gold','sphereSmooth')
    lotus('hanging ornament suspension',[0,7.7,0],[.025,2,.025],'gold','cylinder')
    for i in range(12):
        a=math.tau*i/12;lotus('hanging ornament strand',[.5*math.sin(a),6.08,.5*math.cos(a)],[.012,.8,.012],'gold','cylinder')
    objects.extend(additions)
    return objects,colors
