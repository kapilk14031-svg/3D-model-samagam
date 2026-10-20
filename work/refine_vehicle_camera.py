from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
s=s.replace("function depEnterVehicleView(id,mode='third'){const u=", "function depEnterVehicleView(id,mode='third'){const wasFollowing=!!depFollowState;const u=",1)
s=s.replace("if(depPausedRoutes.has(u.id))depToggleMotion(u);depFollowTick(1)", "if(!wasFollowing&&depPausedRoutes.has(u.id))depToggleMotion(u);sceneEl.classList.add('vehicle-follow');resize();depFollowTick(1)",1)
s=s.replace("depFollowState=null;depVehicleCamera=null;depFollowHud.hidden=true;", "depFollowState=null;depVehicleCamera=null;depFollowHud.hidden=true;sceneEl.classList.remove('vehicle-follow');resize();",1)
s=s.replace("(7.5+pitch*10)","(8.5+pitch*10)",1)
s=s.replace("pose.angle)*4*scale", "pose.angle)*2*scale")
insert="const depVehicleStyle=document.createElement('style');depVehicleStyle.textContent='.scene.vehicle-follow{height:calc(100svh - 12px)!important;min-height:320px}#depVehicleViewHud{width:245px;padding:9px;gap:5px;font-size:11px}#depVehicleViewTitle{flex-basis:100%;font-weight:600;line-height:1.4}#depVehicleViewHud button{padding:6px 8px;font-size:11px}#depVehicleViewHud small{font-size:10px}';document.head.append(depVehicleStyle);\n"
pos=s.index('// Point-first deployment wizard.');s=s[:pos]+insert+s[pos:]
p.write_text(s,encoding='utf-8')
