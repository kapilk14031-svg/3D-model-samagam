from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
s=s.replace("const local=item.category==='pandal'?[0,7,48]:[0,5,48]", "const local=item.category==='pandal'?[0,7,-75]:[0,5,-25]")
s=s.replace("elevation=.15;distance=item.category==='pandal'?48:38", "elevation=item.category==='pandal'?.025:.1;distance=item.category==='pandal'?175:100*Math.min(detail.sx,detail.sz)")
s=s.replace("function go(view){if(view==='interior')", "function go(view){activeDetailItem=null;if(view==='interior')",1)
s=s.replace("document.getElementById('street').onclick=()=>{if(pandalInterior)", "document.getElementById('street').onclick=()=>{if(!streetMode&&activeDetailItem){enterWorldFeature(activeDetailItem,true);return}if(pandalInterior)",1)
s=s.replace("if(!show||hidden.has(l.layer))continue;", "if(!show||hidden.has(l.layer))continue;if(streetMode&&Math.hypot(l.p[0]-walker[0],l.p[2]-walker[2])>85)continue;",1)
p.write_text(s,encoding='utf-8')
