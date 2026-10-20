# Additional illustrative details for the local venue. None is a surveyed count.
def detail_box(name,x,z,w,d,h,color,y=0,layer='services',ground=''):
    box(name,x,z,w,d,h,color,y=y,layer=layer,ground=ground)
def detail_shape(name,kind,x,y,z,w,h,d,color,layer,ground=''):
    add(name,kind,x,y,z,w,h,d,color,layer,ground)
# Preserve the individual tent footprints, improve fabric finishes and hardware.
tent_roofs=[o for o in objects if o['kind']=='roof' and o['layer']=='tents']
zone_trim={'A':'#839baa','B':'#b28e77','C':'#7e9b86','D':'#9e8794'}
for roof in tent_roofs:
    x,y,z=roof['p'];w,h,d=roof['s'];g=roof['ground'];name=roof['name'];trim=zone_trim[g]
    detail_shape(name+' scalloped front valance','valance',x,4.3,z+d/2+.25,w,1.5,.1,trim,'tents',g)
    detail_shape(name+' valance hem','valancehem',x,4.3,z+d/2+.3,w,1.5,.1,'#d3bc8a','tents',g)
    for side in [-1,1]:
        for dz in [-d*.24,d*.24]:
            detail_box(name+' side window',x+side*(w/2+.12),z+dz,.22,8,1.4,'#789798',y=2.6,layer='tents',ground=g)
        for dz in [-d/2,d/2]:
            a=[x+side*w/2,5.3,z+dz];b=[x+side*(w/2+4),.6,z+dz+(-3 if dz<0 else 3)]
            beam(name+' guy rope',a,b,.08,'#b4ae94');objects[-1].update(layer='tents',ground=g,name=name+' guy rope')
    detail_box(name+' lower fabric skirting',x,z+d/2+.2,w,.3,.4,trim,y=.25,layer='tents',ground=g)
# Replace geometric tree wedges with soft faceted crowns.
trees=[o for o in objects if o['name']=='Tree canopy']
objects[:]=[o for o in objects if o['name']!='Tree canopy']
for i,t in enumerate(trees):
    x,y,z=t['p']
    detail_shape('Tree crown','ellipsoid',x,5,z,13,17,13,'#5e8667' if i%2 else '#75936a','landscape')
    detail_shape('Tree secondary crown','ellipsoid',x+3.5,9,z+2,10,10,10,'#6c9271','landscape')
# Cylindrical water tanks with lids instead of simple cuboids.
tanks=[o for o in objects if 'water supply placeholder' in o['name']]
for tank in tanks:
    tank['p'][1]-=tank['s'][1]/2;tank['kind']='cylinder';x,y,z=tank['p'];w,h,d=tank['s']
    detail_shape(tank['name']+' lid','cylinder',x,y+h,z,w+.7,.4,d+.7,'#a9c8d4','utilities',tank['ground'])
    detail_box(tank['name']+' supply pipe',x+w*.55,z,1,1,h*.75,'#8eabae',layer='utilities',ground=tank['ground'])
# Roof caps, ventilation strips and accessible approach slabs at toilet banks.
for wc in [o for o in objects if 'toilet bank placeholder' in o['name']]:
    x,y,z=wc['p'];w,h,d=wc['s'];g=wc['ground'];name=wc['name']
    detail_box(name+' roof cap',x,z,w+1.8,d+1.8,.35,'#b9d0c4',y=h,layer='toilets',ground=g)
    detail_box(name+' ventilation band',x,z+d/2+.35,w-2,.3,.55,'#588781',y=h-1,layer='toilets',ground=g)
    detail_box(name+' entry apron',x,z+d/2+3,w+1,6,.25,'#d4d6c4',layer='toilets',ground=g)
# Dining/service structures receive eave bands and regular wall openings.
for roof in [o for o in objects if o['kind']=='roof' and o['layer']=='services']:
    x,y,z=roof['p'];w,h,d=roof['s'];g=roof['ground']
    for side in [-1,1]:
        detail_box(roof['name']+' eave band',x+side*w/2,z,.5,d,1,'#b5bd9f',y=4.4,layer='services',ground=g)
    for j in range(5):
        detail_box(roof['name']+' serving opening',x-w*.37+j*w*.185,z+d/2+.2,w*.11,.4,2.3,'#647e7a',y=1.7,layer='services',ground=g)
# Medical blocks and small ambulance models; placements remain illustrative.
for med in [o for o in objects if 'medical placeholder' in o['name']]:
    x,y,z=med['p'];g=med['ground']
    detail_box(g+' medical entrance',x,z+15.2,8,.4,5.5,'#5b8992',layer='services',ground=g)
    xx=x+23;zz=z+9
    detail_box(g+' ambulance body',xx,zz,2.7,6.1,2.2,'#e8e8dc',y=.45,layer='services',ground=g)
    detail_box(g+' ambulance cab',xx,zz+2.7,2.6,1.5,1.6,'#b1c8ca',y=.5,layer='services',ground=g)
    for side in [-1,1]:
        detail_box(g+' ambulance red cross vertical',xx+side*1.39,zz,.1,.35,1.1,'#b46151',y=1.2,layer='services',ground=g)
        detail_box(g+' ambulance red cross horizontal',xx+side*1.39,zz,.1,1.1,.35,'#b46151',y=1.55,layer='services',ground=g)
        for dz in [-1.8,1.8]:detail_shape(g+' ambulance wheel','ellipsoid',xx+side*1.35,.2,zz+dz,.35,.8,.8,'#3b4d4c','services',g)
# Bus doors, wheels, roof equipment and a simple waiting shelter.
for bus in [o for o in objects if o['name']=='Bus placeholder']:
    x,y,z=bus['p'];w,h,d=bus['s']
    for side in [-1,1]:
        for dz in [-d*.3,d*.3]:detail_shape('Bus wheel','ellipsoid',x+side*w/2,.3,z+dz,1.5,6.5,6.5,'#3e4b49','parking')
        detail_box('Bus side door',x+side*(w/2+.2),z+d*.25,.4,7,8,'#6c8f99',y=2,layer='parking')
    detail_box('Bus roof air conditioning',x,z,8,16,1.8,'#d8d9c4',y=h,layer='parking')
detail_box('Bus waiting shelter roof',485,1070,85,18,1,'#a5b6ab',y=8,layer='parking')
for x in [445,485,525]:detail_box('Bus shelter support',x,1070,.7,.7,8,'#8b9d94',layer='parking')
# Restrained internal lane markings, with lanes already marked as schematic.
for x in [-500,105,550]:
    for z in range(-990,1000,38):
        if any(abs(z-j)<28 for j in [-450,300,970]):continue
        detail_box('Internal road centre dash',x,z,.35,13,.04,'#e9e6d1',y=1.05,layer='site')
# Roadside context gains roof details, without claiming exact facades.
for b in [o for o in objects if 'map-observed, approximate mass' in o['name']]:
    x,y,z=b['p'];w,h,d=b['s']
    detail_box(b['name']+' glazing band',x,z+d/2+.15,w*.78,.3,1.5,'#829f9e',y=h*.55,layer='east')
