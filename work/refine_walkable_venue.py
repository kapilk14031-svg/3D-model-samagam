from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
s=s.replace("if(o.layer==='tents'&&o.name.endsWith('entrance flap'))continue;", "if(o.featureId==='H05'&&o.name.endsWith('/ dark brown facade')){const[x,y,z]=o.p,[w,h,d]=o.s;for(const[xx,zz,ww,dd]of[[x-w/2,z,.6,d],[x,z-d/2,w,.6],[x,z+d/2,w,.6],[x+w/2,z-(d+7)/4,.6,(d-7)/2],[x+w/2,z+(d+7)/4,.6,(d-7)/2]])openedAccommodation.push({...o,name:o.name+' / station open wall',p:[xx,y,zz],s:[ww,h,dd]});continue}if(o.layer==='tents'&&o.name.endsWith('entrance flap'))continue;",1)
s=s.replace("if(['B01','B09','B10','B12','B17','W29'].includes(o.featureId))continue;", "if(['B01','B09','B10','B12','B17','W29'].includes(o.featureId))continue;if(o.layer==='context'&&/tree|palm/i.test(o.name)&&Math.abs(o.p[0]-137.322)<153&&Math.abs(o.p[2]-314.3)<71)continue;",1)
# Keep integrated pandal fabric in the user's chosen warm golden-brown palette.
s=s.replace("verts.set(point(raw.subarray(i,i+3)),i);const n=", "verts.set(point(raw.subarray(i,i+3)),i);if(item.category==='pandal'&&raw[i+9]===2)verts.set([srgbToLinear(.72),srgbToLinear(.57),srgbToLinear(.36)],i+6);const n=",1)
p.write_text(s,encoding='utf-8')
