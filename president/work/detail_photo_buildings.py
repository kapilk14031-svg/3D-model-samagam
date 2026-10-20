def improve(objects):
    # Continuous metal gallery rails are visible in screenshots 110153/110303.
    # Preserve the newer 2026 portico colours and lettering.
    for o in objects:
        if o['name'].startswith('Upper gallery side parapet'):
            o['s'][1]=.22;o['p'][1]=4.95
    def box(n,p,s,mat='metal',group='campus'):
        objects.append(dict(name=n,p=p,s=s,mat=mat,shape='box',group=group,rot=0))
    for x in [-31,31]:
        for y in [5.15,5.5,5.85]:box('Residential continuous balcony horizontal rail',[x,y,29.6],[49,.045,.055])
        for xx in range(int(x-24),int(x+25),4):box('Residential gallery railing upright',[xx,5.42,29.6],[.055,1,.06])
    for x in [-31,31]:
        for y in [9.7,10.05,10.4]:box('Residential terrace horizontal guardrail',[x,y,30.2],[49,.05,.06],group='roof')
    for x in [-32,32]:
        box('Residential terrace service block • roof study',[x,10.25,42],[10,2,5],'white','roof')
    return objects
