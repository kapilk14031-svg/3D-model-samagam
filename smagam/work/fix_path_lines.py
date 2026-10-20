from pathlib import Path
p=Path('work/build_pdf_model.py');s=p.read_text(encoding='utf-8');a=s.index('for route in plan_routes:');b=s.index('# User-requested dark-brown',a);s=s[:a]+'''exec((ROOT/'work/aligned_routes.py').read_text(encoding='utf-8'))
for route_index,route in enumerate(plan_routes):
    current=route['id'];p=road_aligned_route(route,route_index)
    ribbon(route['id']+' road-aligned path',p,.55,.035,route['color'],'traffic')
    routes.append(dict(name=route['id'],points=p,color=route['color'],layer='traffic',width=.55,status='Visual route family snapped to schematic road axes; not turn-by-turn guidance'))
'''+s[b:];p.write_text(s,encoding='utf-8')
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8');a=s.index('// Direction arrows are real geometry;');b=s.index('const buffers=[]',a)
s=s[:a]+'''// Thin direction markers follow each route surface, including raised highway sections.
for(const route of DATA.routes){const key=route.layer+'|body',a=groups.get(key)||[];groups.set(key,a);const color=[1,3,5].map(i=>parseInt(route.color.slice(i,i+2),16)/255);let passed=0,next=35;for(let j=1;j<route.points.length;j++){const start=route.points[j-1],end=route.points[j],vx=end[0]-start[0],vz=end[2]-start[2],len=Math.hypot(vx,vz);if(len<.01)continue;const ux=vx/len,uz=vz/len;while(next<=passed+len){const k=next-passed,t=k/len,x=start[0]+ux*k,z=start[2]+uz*k,y=start[1]+(end[1]-start[1])*t+.08;pushTri(a,[[x+ux*2,y,z+uz*2],[x-ux-uz*.95,y,z-uz+ux*.95],[x-ux+uz*.95,y,z-uz-ux*.95]],[0,1,0],color);next+=70}passed+=len}}
'''+s[b:]
s=s.replace('[[16,.032],[10,.055],[6,.095],[3.2,.15]]','[[2,.035],[1.25,.065],[.7,.12]]',1)
s=s.replace("const nx=-dz/length*width/2,nz=dx/length*width/2,y=4.12;", "const nx=-dz/length*width/2,nz=dx/length*width/2,ya=a[1]+.09,yb=b[1]+.09;",1)
s=s.replace("const v=[[a[0]+nx,y,a[2]+nz],[b[0]+nx,y,b[2]+nz],[b[0]-nx,y,b[2]-nz],[a[0]-nx,y,a[2]-nz]];", "const v=[[a[0]+nx,ya,a[2]+nz],[b[0]+nx,yb,b[2]+nz],[b[0]-nx,yb,b[2]-nz],[a[0]-nx,ya,a[2]-nz]];",1)
s=s.replace("DATA.objects.filter(o=>o.name==='Pandal curved fabric roof')", "DATA.objects.filter(()=>false)",1)
p.write_text(s,encoding='utf-8')
