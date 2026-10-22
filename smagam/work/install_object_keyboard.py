from pathlib import Path
p=Path(__file__).with_name('viewer-pdf.html');s=p.read_text(encoding='utf-8')
assert 'function depEnterObjectControl' not in s
# Use the same damped input for free-camera navigation and selected-object movement.
s=s.replace("const following=!!depFollowState,free=!streetMode&&!following;", "const following=!!depFollowState,manual=!!depFollowState?.manual,free=!streetMode&&!following;")
s=s.replace("forward:free?Number", "forward:(free||manual)?Number").replace("side:free?Number", "side:(free||manual)?Number")
s=s.replace("const v=cameraVelocity;if(!Object.values(v).some(Boolean))return;", "const v=cameraVelocity;if(manual)depManualTick(dt,v);if(!Object.values(v).some(Boolean))return;")
s=s.replace("depFollowState.offset+=v.turn*1.15*dt;", "if(!manual)depFollowState.offset+=v.turn*1.15*dt;")
s=s.replace("if(k==='escape'){if(depFollowState)", "if(k==='capslock'&&depFollowState){e.preventDefault();resetNavigationKeys();depExitVehicleView();return}\n if(k==='escape'){if(depFollowState)")
# The manual pose keeps route animation from fighting keyboard adjustments.
s=s.replace("function depPose(u){if(!u.position)return null;", "function depPose(u){if(!u.position)return null;if(depFollowState?.id===u.id&&depFollowState.manual)return{p:[...depFollowState.manual.p],angle:depFollowState.manual.angle};")
# All deployment clicks use the same detail card; entering control here covers icons,
# solid-model clicks and the officers belonging to a deployment without duplicate markers.
s=s.replace("function depShowDutyCard(u,index=null){const paused=depToggleMotion(u);", "function depShowDutyCard(u,index=null,enterControl=true){const paused=enterControl?null:depToggleMotion(u);if(enterControl)depEnterObjectControl(u.id);")
s=s.replace("onclick=()=>depShowDutyCard(u,index);", "onclick=()=>depShowDutyCard(u,index,false);")
s=s.replace("depEl('depCardEdit').onclick=()=>{depDutyCard.hidden=true;depOpen(u.id)}", "depEl('depCardEdit').onclick=()=>{depExitVehicleView(false);depDutyCard.hidden=true;depOpen(u.id)}")
s=s.replace("const u=hit.unit,ray=depScreenRay", "const u=hit.unit,ray=depScreenRay")
# Selecting another object in third person also opens its control view.
old="if(hit?.unit.id===u?.id)depToggleMotion(u)"
new="if(hit?.unit.id===u?.id){depFinishManualControl();depToggleMotion(u)}else if(hit)depShowDutyCard(hit.unit)"
assert old in s;s=s.replace(old,new)
# Camera entry and exit support static deployments as well as moving vehicles.
s=s.replace("if(!u||!u.position||!['rider','qrt','patrol'].includes(u.type))return;const previous=", "if(!u||!u.position||mode==='fpv'&&!['rider','qrt','patrol','ambulance','fire'].includes(u.type))return;depFinishManualControl();resetNavigationKeys();const previous=")
s=s.replace("function depExitVehicleView(restore=true){if(!depFollowState)return;const old=", "function depExitVehicleView(restore=true){if(!depFollowState)return;depFinishManualControl();resetNavigationKeys();depDutyCard.hidden=true;const old=")
s=s.replace("p[1]+(8.5+pitch*10)*scale", "p[1]+((type==='machan'?16.5:8.5)+pitch*10)*scale")
s=s.replace("p[1]+2.4*scale,p[2]+Math.cos(pose.angle)*2*scale", "p[1]+(type==='machan'?6:2.4)*scale,p[2]+Math.cos(pose.angle)*2*scale")
s=s.replace("+(!moving?'No route':paused?'Paused':'Moving')", "+(state.manual?'Keyboard control':!moving?'No route':paused?'Paused':'Moving')")
s=s.replace("depEl('depViewMotion').disabled=!moving;", "depEl('depViewMotion').disabled=!moving;depEl('depViewFPV').hidden=!['rider','qrt','patrol','ambulance','fire'].includes(u.type);depEl('depViewSave').hidden=!state.manual;")
s=s.replace("if(u)depToggleMotion(u);depFollowTick(.05)", "if(u){depFinishManualControl();depToggleMotion(u)}depFollowTick(.05)")
s=s.replace("<button id=\"depViewExit\">Exit vehicle view</button>", "<button id=\"depViewSave\">Save position</button><button id=\"depViewExit\">Exit third person</button>")
s=s.replace("Drag to look around · Scroll to zoom · Esc to exit", "W/S move · A/D left/right · Q/E rotate · K/L zoom · Z/X tilt · Caps Lock exits · Drag to look around")
insert=r'''
// Manual deployment placement shares the existing third-person camera and roster.
function depEnterObjectControl(id){
 const u=depUnits.find(v=>v.id===id);if(!u?.position)return;
 const pose=depPose(u);
 depEnterVehicleView(id,'third');
 if(!depFollowState)return;
 if(u.route.length>1&&!depPausedRoutes.has(id))depPausedRoutes.set(id,depTime);
 depFollowState.manual={p:[...pose.p],angle:pose.angle,changed:false,undo:false,idle:0};
 depFollowState.heading=pose.angle;depFollowState.chase=u.type==='machan'?27:18;
 depVehicleCamera=null;depFollowTick(1);dirty=true;
}
function depManualTick(dt,v){
 const state=depFollowState,m=state?.manual,u=depUnits.find(v=>v.id===state?.id);if(!m||!u)return;
 const moving=Math.abs(v.forward)+Math.abs(v.side)+Math.abs(v.turn)>.001;
 if(!moving){if(m.changed){m.idle+=dt;if(m.idle>.35){depPersist();m.changed=false;depEl('depVehicleViewTitle').textContent=u.title+' · Third person · Position saved'}}return}
 if(!m.undo){depUndoPush();m.undo=true}
 const angleDelta=-v.turn*1.15*dt;
 if(angleDelta){
  const c=Math.cos(angleDelta),s=Math.sin(angleDelta),pivot=m.p;
  const rotate=p=>{const x=p[0]-pivot[0],z=p[2]-pivot[2];return[pivot[0]+x*c+z*s,p[1],pivot[2]-x*s+z*c]};
  u.position=rotate(u.position);u.route=u.route.map(rotate);u.rotation+=angleDelta;m.angle+=angleDelta;
 }
 const speed=(u.type==='rider'||u.type==='patrol'||u.type==='qrt'?10:5)*(heldKeys.has('shift')?2:1);
 const dx=(Math.sin(m.angle)*v.forward-Math.cos(m.angle)*v.side)*speed*dt;
 const dz=(Math.cos(m.angle)*v.forward+Math.sin(m.angle)*v.side)*speed*dt;
 depMoveUnit(u,[u.position[0]+dx,u.position[1],u.position[2]+dz]);m.p[0]+=dx;m.p[2]+=dz;
 m.changed=true;m.idle=0;dirty=true;
 canvas.dataset.controlledObject=JSON.stringify({id:u.id,position:m.p.map(n=>+n.toFixed(4)),rotation:+m.angle.toFixed(5)});
}
function depFinishManualControl(){
 const state=depFollowState,m=state?.manual;if(!m)return;
 if(m.changed)depPersist();
 state.manual=null;
}
depEl('depViewSave').onclick=()=>{if(depFollowState?.manual){depPersist();depFollowState.manual.changed=false;depToast('Object position and rotation saved')}};
'''
s=s.replace("const depVehicleStyle=document.createElement('style');",insert+"\nconst depVehicleStyle=document.createElement('style');")
s=s.replace('Vehicle FPV / follow: Q/E look, K/L zoom, Z/X tilt; the vehicle stays on its route.', 'Click a deployed object: third person + W/A/S/D move the object, Q/E rotate. Caps Lock exits. Position saves after movement stops; Save position also saves it.')
p.write_text(s,encoding='utf-8');print('Installed deployment object keyboard control / third person / Caps Lock exit')
