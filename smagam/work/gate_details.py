"""Decorative gate treatment at source gate positions; architectural styling illustrative."""
exec((ROOT/'work/photo_gate_geometry.py').read_text(encoding='utf-8'))
exec((ROOT/'work/gate3_photo_geometry.py').read_text(encoding='utf-8'))
def premium_gate(f,x,z,w,d):
    if f['id']=='G03':return gate3_photo(f,x,z,w,d)
    if f['id'] in ['G01','G02']:return photo_gate(f,x,z,w,d)
    layer='gates';name=f['name'];span=max(20,min(32,d));angle={'G01':-math.pi/2,'G02':-math.pi/2,'G03':-1.45,'G04':-.89,'G05':-math.pi/2,'G06':.98}.get(f['id'],0)
    start=len(objects)
    def gb(part,xx,zz,ww,dd,hh,color,y=0):box(name+' / '+part,xx,zz,ww,dd,hh,color,y,layer)
    def gs(part,kind,xx,yy,zz,ww,hh,dd,color):add(name+' / '+part,kind,xx,yy,zz,ww,hh,dd,color,layer)
    for side in [-1,1]:
        px=side*(span/2+1.7)
        gb('stone plinth',px,0,5.4,5.2,1.2,'#b6ad93')
        gb('tiered base',px,0,4.4,4.3,.8,'#e5d9bc',1.2)
        gb('ivory pillar',px,0,3.5,3.8,13.6,'#e9e0c9',2)
        for sx in [-1,1]:
            gb('gold pillar inset',px+sx*1.35,-2,.18,.15,11.7,'#c2a368',2.6)
            gb('wine side drape',px+sx*.97,2.01,.42,.16,10.4,'#87515b',3)
        gb('pillar front panel',px,-1.98,1.65,.15,9.2,'#31565a',3.7)
        gb('panel golden motif',px,-2.09,.22,.12,6,'#d6bd7d',5.2)
        for yy in [2.2,14.8,15.6]:gb('golden collar',px,0,4,4.2,.23,'#c4a15c',yy)
        gb('capital cornice',px,0,5.4,5,1,'#e9dfc5',15.9)
        gb('capital gold edge',px,0,5.6,5.2,.25,'#c8aa6c',16.8)
        gs('lantern pedestal','cylinder',px,17.1,0,1.5,.55,1.5,'#b99b60')
        gs('warm lantern','ellipsoid',px,17.6,0,2.3,2.3,2.3,'#f1d4a0')
        gs('lantern cap','roof',px,19.8,0,3,.9,3,'#bc9c61')
        # Paired flower urns flank the opening, with a clear passage between pillars.
        for zz in [-3.7,3.7]:
            gs('flower urn','cylinder',px,0,zz,2.4,2.2,2.4,'#b5a07c')
            gs('foliage','ellipsoid',px,2.1,zz,3.8,2.4,3.8,'#5b7c5e')
            for j in range(5):
                a=j*math.tau/5;gs('floral arrangement','ellipsoid',px+math.cos(a)*1.25,3.6,zz+math.sin(a)*1.2,.9,.85,.9,'#dba48a' if j%2 else '#efe0bd')
    gs('ivory ceremonial arch','arch',0,10.3,0,span+3.2,11,2.5,'#e8dcc0')
    gs('gold arch lining','arch',0,10.42,-1.38,span+2.25,10.5,.2,'#bf9b55')
    gs('wine scalloped pelmet','valance',0,15.4,.8,span+1.5,2.1,.15,'#85515c')
    gs('gold scalloped hem','valancehem',0,15.37,.63,span+1.5,2.1,.15,'#d1b16d')
    gb('name board frame',0,0,span*.8,1.7,3.7,'#c4a15f',21.4)
    gb('name board face',0,-.92,span*.8-.65,.15,3.05,'#20494f',21.72)
    for side in [-1,1]:gs('crown finial','ellipsoid',side*span*.46,21.2,0,1.1,2.5,1.1,'#d5bc7e')
    # Small lamps follow the curve; no lighting-equipment inventory is asserted.
    for j in range(13):
        t=math.pi*j/12;xx=span*.48*math.cos(t);yy=16.5+4.3*math.sin(t)
        gs('arch jewel light','ellipsoid',xx,yy,-1.6,.32,.4,.32,'#f6dfab')
    ca=math.cos(angle);sa=math.sin(angle)
    for o in objects[start:]:
        ox,oy,oz=o['p'];width_scale=1.5*(.28 if f['id']=='G03' else 1);ox*=width_scale;oy*=1.5;o['s'][0]*=width_scale;o['s'][1]*=1.5;o['p']=[x+ox*ca+oz*sa,oy,z-ox*sa+oz*ca];o['rotY']=angle
        if o['color'] in ['#e9e0c9','#e8dcc0','#e5d9bc','#e9dfc5']:o['color']='#f5eee2' # Regal ivory marble
        elif o['color'] in ['#c2a368','#c4a15c','#c8aa6c','#bf9b55','#c4a15f','#d5bc7e','#bc9c61','#b99b60']:o['color']='#d8b668' # Rich lustrous gold
        elif o['color'] in ['#31565a','#20494f','#87515b','#85515c']:o['color']='#782836' # Deep ceremonial wine velvet
        elif o['color'] in ['#b6ad93','#b5a07c']:o['color']='#b8ab96' # Carved stone plinth
        elif o['color'] in ['#f1d4a0','#f6dfab']:o['color']='#fff2cb' # Warm lantern glow
        o['status']='Gate position follows PDF; ceremonial decoration, orientation, height and materials are illustrative'
    for l in labels:
        if l.get('featureId')==f['id']:l['p']=[x,40.5,z];l['text']=f['name'];l['layer']='gates'
