from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
s=s.replace("ground:{label:'Grounds',color:'#8b9954',short:'GR'}","ground:{label:'Grounds',color:'#8b9954',short:'GR'},traffic:{label:'Traffic points',color:'#a44d76',short:'TP'}")
pos=s.index("const cstyle=ce('style')")
s=s[:pos]+'''for(const f of DATA.features.filter(f=>f.kind==='alighting'||f.kind==='underpass'||f.id==='S04')){const b=f.bbox;if(!b)continue;conceptItems.push({id:f.id,name:f.id+' · '+f.name,category:'traffic',poly:[[b[0],b[1]],[b[2],b[1]],[b[2],b[3]],[b[0],b[3]]],bbox:b,world:f.world,layer:f.layer,source:f,description:(f.detail||f.name)+'. Select Open 3D view for an illustrative local traffic-control scene, or Explore with AK for the actual position in the venue model.'})}
'''+s[pos:]
s=s.replace("if(item.category==='gate'){ctext", "if(item.category==='traffic'){ctext(item.id,cx,cy,14,g,{class:'c-label','font-weight':700});continue}if(item.category==='gate'){ctext")
s=s.replace("if(item.category==='road'){box(0,.05", "if(item.category==='road'||item.category==='traffic'){if(item.category==='traffic'){for(const x of[-20,20]){box(x,1.5,-44,12,3,.8,'#cfaa3f');person(x,-36,false,true)}car(-7,-70,true);box(25,3,-70,13,6,9,'#c6c8b6')}box(0,.05")
p.write_text(s,encoding='utf-8')
