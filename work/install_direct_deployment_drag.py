from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8');pos=s.index('// Screen-space minimum width');s=s[:pos]+Path('work/deployment_direct_drag.js').read_text(encoding='utf-8')+'\n'+s[pos:]
s=s.replace("function depPose(u){if(!u.position)return null;", "function depPose(u){if(!u.position)return null;if(depDragPause?.id===u.id)return{p:[...depDragPause.p],angle:depDragPause.angle};",1)
s=s.replace("function deploymentCollision(x,z,y){if(!depVisible)return false;", "function deploymentCollision(x,z,y){if(!depVisible||!depModelsOn)return false;",1)
s=s.replace("const r=canvas.getBoundingClientRect();pointer={", "const r=canvas.getBoundingClientRect(),hit=e.button===0&&!e.shiftKey?deploymentModelHit((e.clientX-r.left)*W/r.width,(e.clientY-r.top)*H/r.height):null;pointer={",1)
s=s.replace("pan:panDrag?!e.shiftKey&&e.button!==2:e.shiftKey||e.button===2};canvas.setPointerCapture", "pan:panDrag?!e.shiftKey&&e.button!==2:e.shiftKey||e.button===2,depDrag:hit?depStartObjectDrag(hit,(e.clientX-r.left)*W/r.width,(e.clientY-r.top)*H/r.height):null};canvas.setPointerCapture",1)
s=s.replace("if(!pointer)return;let dx=e.clientX-pointer.x,dy=e.clientY-pointer.y;if(boxMode)", "if(!pointer)return;let dx=e.clientX-pointer.x,dy=e.clientY-pointer.y;if(pointer.depDrag){if(Math.hypot(e.clientX-pointer.sx,e.clientY-pointer.sy)>4){const r=canvas.getBoundingClientRect();depDragObject(pointer.depDrag,(e.clientX-r.left)*W/r.width,(e.clientY-r.top)*H/r.height)}pointer.x=e.clientX;pointer.y=e.clientY;return}if(boxMode)",1)
s=s.replace("small=Math.hypot(e.clientX-pointer.sx,e.clientY-pointer.sy)<5;if(small&&deploymentPick", "small=Math.hypot(e.clientX-pointer.sx,e.clientY-pointer.sy)<5;if(pointer.depDrag){depEndObjectDrag(pointer.depDrag);pointer=null;return}if(small&&deploymentPick",1)
s=s.replace("canvas.addEventListener('pointercancel',()=>{pointer=null;", "canvas.addEventListener('pointercancel',()=>{if(pointer?.depDrag)depEndObjectDrag(pointer.depDrag);pointer=null;",1)
s=s.replace("placeLabels();placeDeploymentIcons()", "placeLabels();placeDeploymentIcons();placeDutyCard()",1)
s=s.replace("function depOpen(id){if(conceptMode)", "function depOpen(id){if(typeof depDutyCard!=='undefined')depDutyCard.hidden=true;if(conceptMode)",1)
p.write_text(s,encoding='utf-8')
