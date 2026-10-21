from copy import deepcopy

def correct(objects):
    """Human site correction: two side stairs; no central stage staircase."""
    selected=[];replacement=[]
    for o in objects:
        n=o['name']
        if n.startswith('Green carpet stage stair'):
            selected.append(o)
            for x,side in [(-54,'left'),(-26,'right')]:
                c=deepcopy(o);c['name']='Stage '+side+' side green stair';c['p'][0]=x;c['s'][0]=4.6;replacement.append(c)
        elif n.startswith(('Stair railing post','Sloping stainless stair handrail')):
            selected.append(o)
            edge=-2.45 if o['p'][0]<-40 else 2.45
            for x,side in [(-54,'left'),(-26,'right')]:
                c=deepcopy(o);c['name']='Stage '+side+' side '+('railing post' if n.startswith('Stair railing') else 'sloping handrail');c['p'][0]=x+edge;replacement.append(c)
    objects[:]=[o for o in objects if o not in selected]
    objects.extend(replacement)
    return objects
