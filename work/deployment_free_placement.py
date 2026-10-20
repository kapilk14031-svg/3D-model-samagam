from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
s=s.replace("if(u.offset){u.position[0]+=u.offset[0];u.position[2]+=u.offset[2]}}}return u})}","if(u.offset){u.position[0]+=u.offset[0];u.position[2]+=u.offset[2]}u.position=depVacantSeedPosition(u.position,u.type)}}return u})}",1)
pos=s.index('function depValidate(data)')
s=s[:pos]+'''function depVacantSeedPosition(p,type){ensureWalkPhysics();const radius=({machan:3.4,morcha:4.7,qrt:5,patrol:5,ambulance:5,fire:6,naka:8})[type]||1.3;function clear(x,z){const reach=Math.ceil(radius/WALK_CELL)+1,ix=Math.floor(x/WALK_CELL),iz=Math.floor(z/WALK_CELL),seen=new Set();for(let a=-reach;a<=reach;a++)for(let b=-reach;b<=reach;b++)for(const wall of walkGrid.get((ix+a)+','+(iz+b))||[]){if(seen.has(wall))continue;seen.add(wall);if(wall.bottom<4&&wall.top>.55&&circleHitsBox(wall,x,z,radius))return false}return true}if(clear(p[0],p[2]))return p;for(let r=4;r<=48;r+=4)for(let i=0;i<16;i++){const x=p[0]+Math.cos(i*Math.PI/8)*r,z=p[2]+Math.sin(i*Math.PI/8)*r;if(clear(x,z))return[x,.3,z]}return p}
'''+s[pos:]
# Quick strength preview stays visible without expanding all shift forms.
s=s.replace('<label>Name / title<input id="depName"', '<div class="dep-plan-note">${Object.entries(u.shifts).map(([k,v])=>depEsc(DEP_SHIFT[k])+\': main \'+(v.force??\'?\')+\' + incharge \'+(v.incharge??\'?\')+\' + extra \'+(v.extra??\'?\')).join(\'<br>\')}</div><label>Name / title<input id="depName"',1)
p.write_text(s,encoding='utf-8')
