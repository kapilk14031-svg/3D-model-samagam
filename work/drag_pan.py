from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8');s=s.replace('<button id="street"', '<button id="dragMode" class="active" aria-pressed="true">Drag / Pan</button><button id="street"',1)
s=s.replace("let streetMode=false,boxMode=false", "let panDrag=true;let streetMode=false,boxMode=false",1)
s=s.replace("pan:e.shiftKey||e.button===2", "pan:panDrag?!e.shiftKey&&e.button!==2:e.shiftKey||e.button===2",1)
s=s.replace("'DRAG: ORBIT · SHIFT + DRAG: PAN · SCROLL: ZOOM'", "(panDrag?'DRAG: PAN · SHIFT + DRAG: ROTATE · SCROLL: CURSOR ZOOM':'DRAG: ROTATE · SHIFT + DRAG: PAN · SCROLL: CURSOR ZOOM')",1)
pos=s.index("canvas.addEventListener('pointerdown'")
s=s[:pos]+"document.getElementById('dragMode').onclick=e=>{panDrag=!panDrag;e.currentTarget.textContent=panDrag?'Drag / Pan':'Rotate model';e.currentTarget.classList.toggle('active',panDrag);e.currentTarget.setAttribute('aria-pressed',String(panDrag));navUI()};\n"+s[pos:]
# Pan in the screen plane so grabbing the model feels direct at every orbit angle.
s=s.replace("let s=distance/H*.65;target[0]-=(dx*Math.cos(yaw)+dy*Math.sin(yaw))*s;target[2]+=(dx*Math.sin(yaw)-dy*Math.cos(yaw))*s", "const scale=distance/H*(topView?.88:2*Math.tan(.72/2)),forward=[-Math.sin(yaw)*Math.cos(elevation),-Math.sin(elevation),-Math.cos(yaw)*Math.cos(elevation)],right=norm(cross(forward,[0,1,0])),up=cross(right,forward);target=target.map((v,i)=>v-right[i]*dx*scale+up[i]*dy*scale)")
p.write_text(s,encoding='utf-8')
