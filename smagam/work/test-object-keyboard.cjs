
const assert=require('node:assert/strict');
let depFollowState=null,depVehicleCamera=null,depTime=10,depUnits=[],dirty=false,saved=0,undo=0;
const heldKeys=new Set(),depPausedRoutes=new Map(),depRouteEpoch=new Map(),canvas={dataset:{}};let depDragPause=null;
function depEl(){return {textContent:''}};function depPersist(){saved++};function depUndoPush(){undo++};function depFollowTick(){};
function depEnterVehicleView(id,mode){depFinishManualControl();depFollowState={id,mode}}
function unit(type,route=[]){return {id:type,type,position:[0,1,0],rotation:0,scale:1,speed:2,route,routeMode:'pingpong'}}
function tick(f=0,side=0,turn=0,n=60){for(let i=0;i<n;i++)depManualTick(1/60,{forward:f,side,turn})}
function depPose(u){if(!u.position)return null;if(depFollowState?.id===u.id&&depFollowState.manual)return{p:depFollowState.manual.p.map((v,i)=>v+(i===1?(depFollowState.manual.jump?.height||0):0)),angle:depFollowState.manual.angle};if(depDragPause?.id===u.id)return{p:[...depDragPause.p],angle:depDragPause.angle};let p=[...u.position],angle=u.rotation;if(u.route?.length>1&&['rider','qrt','patrol','footpatrol','ambulance','fire'].includes(u.type)){const points=u.routeMode==='loop'?[...u.route,u.route[0]]:u.route,lengths=points.slice(1).map((v,i)=>Math.hypot(v[0]-points[i][0],v[2]-points[i][2])),total=lengths.reduce((a,b)=>a+b,0);if(total>.01){let d=Math.max(0,(depPausedRoutes.get(u.id)??depTime)-(depRouteEpoch.get(u.id)||0))*u.speed,reverse=false;if(u.routeMode==='loop')d%=total;else{d%=total*2;if(d>total){d=total*2-d;reverse=true}}for(let i=0;i<lengths.length;i++){if(d<=lengths[i]||i===lengths.length-1){const a=points[i],b=points[i+1],t=lengths[i]?d/lengths[i]:0;p=a.map((v,k)=>v+(b[k]-v)*t);angle=Math.atan2(b[0]-a[0],b[2]-a[2])+(reverse?Math.PI:0);break}d-=lengths[i]}}}return{p,angle}}
function depMoveUnit(u,p,moveRoute=true){if(u.position&&moveRoute&&u.route.length){const delta=p.map((v,i)=>v-u.position[i]);u.route=u.route.map(q=>q.map((v,i)=>v+delta[i]))}u.position=[...p]}
function depVehicleShot(pose,type,mode,offset=0,pitch=0,chase=18,scale=1){const a=pose.angle+offset,fx=Math.sin(a),fz=Math.cos(a),p=pose.p;let eye,at;if(mode==='fpv'){eye=[p[0]+Math.sin(pose.angle)*1.2*scale,p[1]+(type==='rider'?3.45:3.35)*scale,p[2]+Math.cos(pose.angle)*1.2*scale];at=[eye[0]+fx*Math.cos(pitch)*24,eye[1]+Math.sin(pitch)*24,eye[2]+fz*Math.cos(pitch)*24]}else{eye=[p[0]-fx*chase*scale,p[1]+((type==='machan'?16.5:8.5)+pitch*10)*scale,p[2]-fz*chase*scale];at=[p[0]+Math.sin(pose.angle)*2*scale,p[1]+(type==='machan'?6:2.4)*scale,p[2]+Math.cos(pose.angle)*2*scale]}return{eye,at}}
function depEnterObjectControl(id){
 const u=depUnits.find(v=>v.id===id);if(!u?.position)return;
 const pose=depPose(u);
 depEnterVehicleView(id,'third');
 if(!depFollowState)return;
 if(u.route.length>1&&!depPausedRoutes.has(id))depPausedRoutes.set(id,depTime);
 depFollowState.manual={p:[...pose.p],angle:pose.angle,changed:false,undo:false,idle:0,jump:{height:0,velocity:0}};
 depFollowState.heading=pose.angle;depFollowState.chase=u.type==='machan'?27:18;
 depVehicleCamera=null;depFollowTick(1);dirty=true;
}
function depManualJump(){const m=depFollowState?.manual;if(!m)return;if(!m.jump)m.jump={height:0,velocity:0};if(m.jump.height<.001&&m.jump.velocity===0){m.jump.velocity=11;dirty=true}}
function depManualTick(dt,v){
 const state=depFollowState,m=state?.manual,u=depUnits.find(v=>v.id===state?.id);if(!m||!u)return;
 if(m.jump&&(m.jump.velocity||m.jump.height)){const j=m.jump;j.height+=j.velocity*dt-10*dt*dt;j.velocity-=20*dt;if(j.height<=0){j.height=0;j.velocity=0}dirty=true;canvas.dataset.objectJump=String(j.height)}
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

for(const type of ['machan','morcha','barricade','naka','officer','rider','qrt','patrol','ambulance','fire','parking']){
 depFollowState=null;depUnits=[unit(type)];const u=depUnits[0];depEnterObjectControl(u.id);assert.equal(depFollowState.mode,'third');
 tick(1);assert(Math.abs(u.position[2]-(type==='rider'||type==='patrol'||type==='qrt'?10:5))<1e-7);
 const old=[...u.position];tick(0,1);assert(u.position[0]<old[0]&&Math.abs(u.position[2]-old[2])<1e-7,'screen-relative right');
 tick(0,0,1);assert(Math.abs(u.rotation+1.15)<1e-7);const pose=depPose(u);assert.deepEqual(pose.p,u.position);assert.equal(pose.angle,u.rotation);
 const ground=u.position[1];depManualJump();tick(0,0,0,15);assert(depPose(u).p[1]>ground+1);const airborneVelocity=depFollowState.manual.jump.velocity;depManualJump();assert.equal(depFollowState.manual.jump.velocity,airborneVelocity,'no repeated airborne jump');tick(0,0,0,90);assert.equal(depPose(u).p[1],ground);assert.equal(u.position[1],ground,'jump never saves elevated Y');
 tick(1);const before=saved;tick();assert(saved>before,'idle autosave');tick(1);depFinishManualControl();assert.equal(depFollowState.manual,null);assert.deepEqual(depPose(u).p,u.position);
}
// Route must stay paused, move/rotate as a complete plan, then continue at the
// adjusted location without losing its points or jumping when control exits.
depFollowState=null;depUnits=[unit('patrol',[[0,1,0],[0,1,100]])];let u=depUnits[0],pose=depPose(u);assert.equal(pose.p[2],20);
depEnterObjectControl(u.id);assert(depPausedRoutes.has(u.id));tick(1);depTime+=5;assert(Math.abs(depPose(u).p[2]-30)<1e-7);tick(0,0,1);pose=depPose(u);const lengths=Math.hypot(u.route[1][0]-u.route[0][0],u.route[1][2]-u.route[0][2]);assert(Math.abs(lengths-100)<1e-7);depFinishManualControl();const after=depPose(u);assert(Math.hypot(after.p[0]-pose.p[0],after.p[2]-pose.p[2])<1e-7);assert(Math.abs(after.angle-pose.angle)<1e-7);assert.equal(u.route.length,2);
console.log('PASS: 11 deployment types, object-relative keyboard placement, rotation, idle save, manual pose, whole-route translation/rotation, paused route and no exit jump');
