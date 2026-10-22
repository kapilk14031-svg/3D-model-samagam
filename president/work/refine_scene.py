"""Video-informed visual refinements. Leaves satellite plan positions unchanged."""
import math
def refine(objects, colors):
    colors.update({'metal':'#8a8c87','curtain':'#b7ad96','skirt':'#276444','trim':'#bba14f','vent':'#70756f','tile':'#b5afa1','plaster':'#e4dfd4','soil':'#544c3b'})
    def add(name,p,s,mat='stone',shape='box',group='interior',rot=0,tilt=0):
        objects.append(dict(name=name,p=p,s=s,mat=mat,shape=shape,group=group,rot=rot,tilt=tilt))
    def box(name,x,y,z,w,h,d,mat='stone',group='interior',rot=0):add(name,[x,y,z],[w,h,d],mat,group=group,rot=rot)
    def cyl(name,x,y,z,r,h,mat='metal',group='interior'):add(name,[x,y,z],[r,h,r],mat,'cylinder',group)
    # Rebuild details rather than stacking incompatible old furniture over them.
    discard=('Illustrative audience seat','Illustrative chair back','Chair armrest','Stage sofa','Stage front flowers','Acoustic panel grid','Acoustic wall panels','Curtain below acoustic','Hall glazing','Stair handrail','Scalloped facade arch')
    objects[:]=[o for o in objects if not o['name'].startswith(discard)]
    for o in objects:
        if o['name']=='Hall roof • assumed height':o['group']='roof'
        if o['name']=='Stage backdrop • photo inspired':o['mat']='plaster'
        if o['name']=='Hall east wall':
            # The doorway itself is represented below with an actual gap.
            o['p'][2]=-.5;o['s'][2]=47
        if o['name']=='Hall west wall':o['group']='shell'
    # Side entry near the stage is directly visible in videos 8 and 9.
    box('Hall side wall forward of entry',-19,5,-38,.5,9,10,'white','shell')
    box('Hall side entrance lintel',-19,7.3,-28,.5,4.4,10,'white','shell')
    for z in [-32.4,-23.6]:box('Side entrance metal jamb',-18.7,3,z,.2,4,.18,'metal','shell')
    for z in [-31.4,-24.6]:box('Open glazed door leaf • side entry',-17.5,3,z,2.2,3.7,.09,'glass','shell',math.pi/5)
    for i in range(5):box('External black entry step • video 9',-16.8+i*.55,.95-i*.14,-28,.6,.22,7,'dark','campus')
    for z in [-31.8,-24.2]:
        for x in [-18,-16.5,-15]:cyl('Entrance stainless rail post',x,1.35,z,.04,1.2,'metal','campus')
        box('Entrance handrail',-16.5,2,z,4,.06,.06,'metal','campus')
    # Upholstered linked armchairs: cushions, rounded backs, frames and legs.
    for r in range(28):
        z=-20+r*1.4
        for c in range(30):
            x=-56.8+c*1.05+(3.1 if c>=15 else 0)
            add('Cream upholstered chair seat',[x,1.43,z],[.7,.76,.16],'seat','rounded','seating',tilt=math.pi/2)
            add('Rounded upholstered chair back',[x,1.89,z+.35],[.7,.78,.15],'seat','rounded','seating',tilt=-.09)
            for dx in [-.37,.37]:
                box('Chair metal armrest',x+dx,1.68,z,.065,.065,.75,'metal','seating')
                for dz in [-.26,.28]:box('Chair metal leg',x+dx,1.22,z+dz,.045,.44,.045,'metal','seating')
                box('Chair frame under seat',x+dx,1.37,z,.045,.04,.8,'metal','seating')
            box('Chair rear crossbar',x,1.17,z+.29,.75,.035,.035,'metal','seating')
    # Cream front sofas and ceremonial chairs, visible in stage-facing views.
    for x in [-52,-45,-38,-31]:
        add('Stage sofa upholstered seat',[x,2.48,-35],[4.5,.32,1.65],'white','rounded')
        add('Stage sofa padded back',[x,3.04,-35.7],[4.5,1,.3],'white','rounded')
        for dx in [-2.1,2.1]:add('Stage sofa arm',[x+dx,2.85,-35],[.35,.65,1.65],'white','rounded')
        for dx in [-1.8,1.8]:box('Stage sofa foot',x+dx,2.22,-35,.13,.3,1.1,'metal')
    for x in [-55,-25]:
        add('Gold ceremonial chair back',[x,3.1,-36.5],[1.2,1.8,.2],'trim','rounded')
        add('Ceremonial chair cushion',[x,2.7,-36],[1.1,.85,.16],'seat','rounded',tilt=math.pi/2)
    box('Stage green fascia • video reference',-40,1.55,-29.92,34,.95,.12,'skirt')
    for x in range(-56,-23,2):
        box('Gold fascia trim',x,1.55,-29.82,.05,.9,.035,'trim')
        add('Fascia garland loop',[x+.7,1.57,-29.78],[.55,.37,.03],'trim','arch',rot=math.pi)
    for x in [-51,-39,-27]:
        box('Low stage table',x,2.5,-32.8,3,.1,1.2,'white')
        for dx in [-1.2,1.2]:box('Table leg',x+dx,2.25,-32.8,.06,.5,.7,'metal')
    # Backdrop frame and side display boards. Event wording is not invented.
    for x in [-51,-48,-32,-29]:box('Backdrop vertical decorative band',x,4.7,-39.3,.18,5,.08,'pink')
    box('Central backdrop panel',-40,4.4,-39.2,10,3.3,.1,'pink')
    box('Central emblem backing',-40,5.2,-39.08,3.4,.95,.04,'white')
    for x in [-57,-23]:
        box('Side exhibition display frame',x,4,-38,3.8,4,.18,'metal')
        box('Side exhibition display face',x,4,-37.88,3.6,3.8,.04,'white')
    for x in [-55,-25]:
        cyl('Stage flower planter',x,2.4,-30.3,.3,.6,'white')
        for dx in [-.3,0,.3]:add('Stage floral arrangement',[x+dx,3,-30.3],[.25,.35,.25],'flower','sphere')
    # Angled railing follows the stair rise.
    for x in [-43.7,-36.3]:add('Sloping stainless stair handrail',[x,2.65,-28.9],[.065,.065,3.9],'metal',tilt=.3)
    # Actual acoustic motif is a grid of small squares, curtains below.
    for x in [-60.6,-19.4]:
        for z in range(-40,22,2):
            for y in [4.4,5.55,6.7,7.85]:box('Square acoustic wall tile',x,y,z,.1,.93,1.7,'acoustic','shell')
        for z in range(-35,23,8):
            if x>-20 and z==-27:continue
            for j in range(15):
                cyl('Vertical curtain pleat',x+(j%2)*.08,2.85,z-2.6+j*.37,.16,2.5,'curtain','shell')
    for x in range(-59,-19,2):
        for y in [4.4,5.55,6.7,7.85]:box('Rear wall acoustic tile',x,y,22.65,1.65,.93,.1,'acoustic','shell')
    # Ceiling grid, dark ventilation grilles and stage lighting battens.
    box('White suspended ceiling • video reference',-40,9.45,-10,42,.08,66,'white','ceiling')
    for x in range(-60,-18,2):box('Ceiling tile joint',x,9.36,-10,.018,.012,65,'vent','ceiling')
    for z in range(-42,24,2):box('Ceiling tile joint',-40,9.36,z,42,.012,.018,'vent','ceiling')
    for z in range(-35,22,6):
        for x in [-54,-42,-30]:box('Ceiling ventilation grille',x,9.31,z,1.1,.04,.8,'vent','ceiling')
    for z in [-32,-36]:
        box('Stage lighting crossbar',-40,8.8,z,34,.12,.12,'dark','ceiling')
        for x in range(-55,-23,2):
            cyl('Stage spotlight body',x,8.55,z,.19,.4,'dark','ceiling')
            cyl('Stage spotlight lens',x,8.32,z,.15,.02,'light','ceiling')
    # Porched arcade. Model bay positions stay approximate; shape is video-led.
    for z in range(-38,24,8):
        for offset,scale in [(-2,.65),(0,1),(2,.65)]:
            add('Scalloped frontage arch lobe',[-18.1,5.2,z+4+offset],[1.6,1.1*scale,.3],'stone','arch','shell',math.pi/2)
        for zz in [z+1.2,z+6.8]:
            box('Dark window frame',-18.65,3.15,zz,.12,2.35,1.5,'dark','shell')
            box('Window illuminated glass',-18.55,3.15,zz,.08,2.12,1.3,'glass','shell')
            box('Facade gold uplight niche',-18.25,1.55,zz,.22,.8,1.2,'trim','shell')
    # White gate vertical bars are clear in V3 3–13 sec.
    for centre in [-16.3,-9.7]:
        box('Entrance white gate bottom rail',centre,1,-61,5.7,.12,.1,'white','campus')
        for i in range(18):box('Entrance white gate vertical bar',centre-2.7+i*.3,2.6,-61,.055,3.2+.3*math.sin(i/17*math.pi),.06,'white','campus')
    # Tiled paths, red/yellow peripheral walkway, clipped hedges and planters.
    for z in range(-24,18,3):
        box('Garden large paving slab',23,.53,z,1.8,.06,2.65,'stone','campus')
    for x in [0,52]:
        for z in range(-27,23,3):
            box('Garden red border paver',x-.9,.49,z,.7,.05,2.8,'pink','campus')
            box('Garden yellow border paver',x+.3,.49,z,1.6,.05,2.8,'gold','campus')
    for x in [3,49]:
        for z in range(-22,18,3):
            add('Clipped garden hedge',[x,1.02,z],[.7,.65,1.4],'tree','rounded','campus')
    for x,z in [(1,-12),(51,-12),(1,12),(51,12)]:
        box('Garden bench seat',x,.9,z,2.7,.12,.65,'white','campus')
        box('Garden bench back',x,1.3,z+.3,2.7,.65,.12,'white','campus')
    # Slightly denser realistic foliage; placement remains inferred.
    for o in objects:
        if o['name'].startswith(('Landscape tree canopy','Pavilion dome','Lotus petal','Palm frond')):o['shape']='sphereSmooth'
        if o['name'].startswith('Lotus petal'):
            a=math.atan2(o['p'][2]+45,o['p'][0]-28);o['shape']='petal';o['s']=[2,2.4,.35];o['rot']=math.pi/2-a
    for a in range(15,360,30):
        t=math.radians(a);add('Lotus pointed petal • video/photo reference',[28+7.5*math.cos(t),2.5,-45+7.5*math.sin(t)],[2,2.4,.35],'pink','petal','campus',math.pi/2-t)
    return objects,colors
