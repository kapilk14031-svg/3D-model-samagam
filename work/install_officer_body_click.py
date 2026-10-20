from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
s=s.replace("const r=canvas.getBoundingClientRect(),hit=e.button===0&&!e.shiftKey?deploymentModelHit", "const r=canvas.getBoundingClientRect(),officerHit=e.button===0&&!e.shiftKey?depOfficerModelHit((e.clientX-r.left)*W/r.width,(e.clientY-r.top)*H/r.height):null,hit=!officerHit&&e.button===0&&!e.shiftKey?deploymentModelHit",1)
s=s.replace("pointer={x:e.clientX,y:e.clientY,sx:", "pointer={officerHit,x:e.clientX,y:e.clientY,sx:",1)
s=s.replace("if(pointer.depDrag){depEndObjectDrag(pointer.depDrag);", "if(pointer.officerHit&&small){depOpenOfficerHit(pointer.officerHit);pointer=null;return}if(pointer.depDrag){depEndObjectDrag(pointer.depDrag);",1)
pos=s.index('// Point-first deployment wizard.')
s=s[:pos]+Path('work/officer_body_click.js').read_text(encoding='utf-8')+'\n'+s[pos:]
p.write_text(s,encoding='utf-8')
