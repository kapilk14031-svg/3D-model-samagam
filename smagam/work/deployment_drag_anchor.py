from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
s=s.replace("drag={sx:e.clientX,sy:e.clientY,undo:false}};el.onpointermove", "const rect=canvas.getBoundingClientRect(),current=depUnits.find(v=>v.id===el.dataset.id);drag={sx:e.clientX,sy:e.clientY,undo:false,initial:[...current.position],ground:groundAt((e.clientX-rect.left)*W/rect.width,(e.clientY-rect.top)*H/rect.height)}};el.onpointermove",1)
s=s.replace("if(current)depMoveUnit(current,depRoadPoint(p,false))", "if(current){const point=drag.ground?[drag.initial[0]+p[0]-drag.ground[0],drag.initial[1],drag.initial[2]+p[2]-drag.ground[2]]:p;point[1]=drag.initial[1];depMoveUnit(current,point)}",1)
p.write_text(s,encoding='utf-8')
