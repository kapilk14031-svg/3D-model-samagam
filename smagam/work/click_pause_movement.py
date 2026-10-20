from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
s=s.replace('const depRouteEpoch=new Map();', 'const depRouteEpoch=new Map(),depPausedRoutes=new Map();',1)
s=s.replace('Math.max(0,depTime-(depRouteEpoch.get(u.id)||0))*u.speed', 'Math.max(0,(depPausedRoutes.get(u.id)??depTime)-(depRouteEpoch.get(u.id)||0))*u.speed',1)
s=s.replace('depRouteEpoch.set(u.id,depTime);depMode=null;', 'depRouteEpoch.set(u.id,depTime);depPausedRoutes.delete(u.id);depMode=null;',1)
s=s.replace('depRouteEpoch.set(drag.id,depDragPause.epoch+depTime-depDragPause.started);', 'if(!depPausedRoutes.has(drag.id))depRouteEpoch.set(drag.id,depDragPause.epoch+depTime-depDragPause.started);',1)
start=s.index('function depShowDutyCard(u,index=null)')
toggle="function depToggleMotion(u){if(!u.route||u.route.length<2||!['rider','qrt','patrol','footpatrol','ambulance','fire'].includes(u.type))return null;if(depPausedRoutes.has(u.id)){depRouteEpoch.set(u.id,(depRouteEpoch.get(u.id)||0)+depTime-depPausedRoutes.get(u.id));depPausedRoutes.delete(u.id)}else depPausedRoutes.set(u.id,depTime);dirty=true;return depPausedRoutes.has(u.id)}\n"
s=s[:start]+toggle+s[start:]
s=s.replace('function depShowDutyCard(u,index=null){depExtraCardKey', 'function depShowDutyCard(u,index=null){const paused=depToggleMotion(u);depExtraCardKey',1)
s=s.replace("+'</h3><div class=\"dep-location\">'+", "+'</h3><div class=\"dep-location\">'+") if False else s
needle="+'</h3><div class=\"dep-location\">Duty location: '"
assert needle in s
s=s.replace(needle,"+'</h3>'+(paused===null?'':'<p id=\"depMotionStatus\" style=\"padding:9px;background:#e6eee3;border-radius:6px\">Movement: '+(paused?'Paused':'Moving')+' · click model / icon again to '+(paused?'resume':'pause')+'</p><button id=\"depMotionToggle\" class=\"dep-card-action\">'+(paused?'Resume movement':'Pause movement')+'</button>')+'<div class=\"dep-location\">Duty location: '",1)
s=s.replace("depDutyCard.hidden=false;depEl('depCardClose').onclick=()=>{depCardUnit=null;", "depDutyCard.hidden=false;if(depEl('depMotionToggle'))depEl('depMotionToggle').onclick=()=>depShowDutyCard(u,index);depEl('depCardClose').onclick=()=>{depCardUnit=null;",1)
p.write_text(s,encoding='utf-8')
# Existing route tests now include the pause state used by depPose.
p=Path('work/test_deployment.py');s=p.read_text(encoding='utf-8').replace('const depRouteEpoch=new Map();','const depRouteEpoch=new Map(),depPausedRoutes=new Map();');p.write_text(s,encoding='utf-8')
