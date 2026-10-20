from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
s=s.replace("let interiorWorldVertices=null;", "let interiorWorldVertices=null;const interiorCollisionParts=[];",1)
s=s.replace("function part(kind,p,size,color,mat=3){const[v,f]", "function part(kind,p,size,color,mat=3){interiorCollisionParts.push({kind,p:[...p],s:[...size]});const[v,f]",1)
s=s.replace("function beam(a,b,width,color='#171c20'){", "function beam(a,b,width,color='#171c20'){if(Math.abs(a[0]-b[0])<.01&&Math.abs(a[2]-b[2])<.01)interiorCollisionParts.push({kind:'box',p:a.map((v,i)=>(v+b[i])/2),s:[width,Math.abs(b[1]-a[1]),width]});",1)
s=s.replace("const out=[],boards=[];", "const out=[],boards=[],collisionParts=[];",1)
s=s.replace("function part(kind,x,y,z,w,h,d,color,mat=3){const[v,f]", "function part(kind,x,y,z,w,h,d,color,mat=3){collisionParts.push({kind,p:[x,y,z],s:[w,h,d]});const[v,f]",1)
s=s.replace("camera,vertices:new Float32Array(out)", "camera,parts:collisionParts,vertices:new Float32Array(out)",1)
s=s.replace("return{buffer,count:verts.length/10,boards,item,point,sx,sy,sz,turn}", "return{buffer,count:verts.length/10,boards,item,point,sx,sy,sz,turn,parts:src.parts||interiorCollisionParts}",1)
s=s.replace("walker=[p[0],.3,p[2]]", "walker=safeWalkSpawn(p)",1)
s=s.replace("walker[0]=Math.max(-1400,Math.min(1400,walker[0]+dx));walker[2]=Math.max(-1000,Math.min(1400,walker[2]+dz));", "moveWalker(dx,dz,dt);",1)
s=s.replace("(moving?(speed>7?'Running':'Walking'):'Ready')", "(akBlocked?'Obstacle · move around':moving?(speed>7?'Running':'Walking'):'Ready')",1)
pos=s.index('function focusFeature(f)');s=s[:pos]+Path('work/walk_physics.js').read_text(encoding='utf-8')+'\n'+s[pos:]
# Bridge and underpass destinations remain real model positions.
s=s.replace("for(const item of conceptItems.filter(i=>", "for(const item of conceptItems.filter(i=>",1)
needle="document.getElementById('walkControls').append(exploreSelect);"
s=s.replace(needle,needle+"\nfor(const side of[-1,1]){const opt=document.createElement('option');opt.value='BRIDGE-'+side;opt.textContent='Foot-overbridge · '+(side<0?'Venue-side stairs':'Parking-side stairs');exploreSelect.append(opt)}const previousDestination=exploreSelect.onchange;exploreSelect.onchange=()=>{if(!exploreSelect.value.startsWith('BRIDGE-')){previousDestination();return}const side=+exploreSelect.value.slice(7),b=DATA.meta.s04_footbridge,a=b.angle||.264,c=Math.cos(a),s=Math.sin(a),x=side*b.span/2,z=side*((b.stair_run||24)+1);pandalInterior=false;setConcept(false);enterStreet([b.anchor[0]+x*c+z*s,.3,b.anchor[2]-x*s+z*c]);heading=desiredHeading=side>0?a:Math.PI+a;desiredPitch=pitch=.24;followDistance=6;dirty=true};",1)
p.write_text(s,encoding='utf-8')
p=Path('work/foot_overbridge.py');s=p.read_text(encoding='utf-8');s=s.replace("fb('steel support pier',x,z", "fb('steel support pier',x-math.copysign(3,x),z").replace("fb('pier foundation',x,z", "fb('pier foundation',x-math.copysign(3,x),z").replace('deck+3.8','deck+5.2');p.write_text(s,encoding='utf-8')
