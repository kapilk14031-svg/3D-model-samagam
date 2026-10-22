
const assert=require('node:assert/strict');
const listeners={},docListeners={};
class HTMLInputElement{};class HTMLTextAreaElement{};class HTMLSelectElement{};
const window={addEventListener:(n,f)=>listeners[n]=f};
const document={hidden:false,addEventListener:(n,f)=>docListeners[n]=f,getElementById:()=>({classList:{remove(){}}})};
const canvas={dataset:{}};const heldKeys=new Set();
let conceptMode=false,filmRecording=false,streetMode=false,depFollowState=null,target=[0,0,0],yaw=0,elevation=.5,distance=1000,anim=null,orbit=false,topView=false,dirty=false,desiredPitch=.23,followDistance=9;
function zoomBy(k){if(depFollowState){depFollowState.zoom=(depFollowState.zoom||1)*k;return}if(streetMode){followDistance=Math.max(5,Math.min(22,followDistance*k));return}distance=Math.max(35,Math.min(5500,distance*k))}
function leaveStreet(){streetMode=false;resetNavigationKeys()};function exitNavigation(){resetNavigationKeys()};function depExitVehicleView(){depFollowState=null}
function reset(){resetNavigationKeys();conceptMode=filmRecording=streetMode=false;depFollowState=null;target=[0,0,0];yaw=0;elevation=.5;distance=1000;desiredPitch=.23;followDistance=9}
function run(keys,seconds=1,fps=60){heldKeys.clear();for(const k of keys)heldKeys.add(k);for(let i=0;i<seconds*fps;i++)updateKeyboardCamera(1/fps,10000+i*1000/fps)}
// Smooth keyboard camera: movement is integrated in seconds, independent of key repeat.
const cameraKeys=new Set(['w','s','a','d','q','e','k','l','z','x','arrowup','arrowdown','arrowleft','arrowright','shift']);
const cameraVelocity={forward:0,side:0,turn:0,zoom:0,tilt:0},cameraPulses=new Map();
function resetNavigationKeys(){heldKeys.clear();cameraPulses.clear();for(const k in cameraVelocity)cameraVelocity[k]=0}
function isNavigationField(el){return el instanceof HTMLInputElement||el instanceof HTMLTextAreaElement||el instanceof HTMLSelectElement||el?.isContentEditable}
function updateKeyboardCamera(dt,now=performance.now()){
 if(conceptMode||filmRecording){resetNavigationKeys();return}
 const down=k=>heldKeys.has(k)||(cameraPulses.get(k)||0)>now;
 for(const [k,until] of cameraPulses)if(until<=now)cameraPulses.delete(k);
 const following=!!depFollowState,manual=!!depFollowState?.manual,free=!streetMode&&!following;
 const command={forward:(free||manual)?Number(down('w'))-Number(down('s')):0,side:(free||manual)?Number(down('d'))-Number(down('a')):0,turn:streetMode?0:Number(down('e')||down('arrowright'))-Number(down('q')||down('arrowleft')),zoom:Number(down('l'))-Number(down('k')),tilt:Number(down('z')||(!streetMode&&down('arrowup')))-Number(down('x')||(!streetMode&&down('arrowdown')))};
 const length=Math.max(1,Math.hypot(command.forward,command.side));command.forward/=length;command.side/=length;
 const ease=1-Math.exp(-12*dt);
 for(const k in cameraVelocity){cameraVelocity[k]+=(command[k]-cameraVelocity[k])*ease;if(Math.abs(cameraVelocity[k])<.0001)cameraVelocity[k]=0}
 const v=cameraVelocity;if(manual)depManualTick(dt,v);if(!Object.values(v).some(Boolean))return;
 anim=null;orbit=false;document.getElementById('tour').classList.remove('active');
 if(free){
  yaw+=v.turn*1.15*dt;
  const speed=Math.max(12,Math.min(1100,distance*.65))*(down('shift')?2:1);
  target[0]+=(Math.cos(yaw)*v.side-Math.sin(yaw)*v.forward)*speed*dt;
  target[2]+=(-Math.sin(yaw)*v.side-Math.cos(yaw)*v.forward)*speed*dt;
  // Preserve near-horizontal gate views; keyboard tilt must not snap to a new minimum.
  if(v.tilt)elevation=Math.max(-.12,Math.min(1.565,elevation+v.tilt*.65*dt));
 }else if(streetMode){
  desiredPitch=Math.max(-.08,Math.min(1.05,desiredPitch+v.tilt*.65*dt));
 }else if(following){
  if(!manual)depFollowState.offset+=v.turn*1.15*dt;
  depFollowState.pitch=Math.max(depFollowState.mode==='fpv'?-.65:-.4,Math.min(.65,depFollowState.pitch+v.tilt*.65*dt));
 }
 if(v.zoom)zoomBy(Math.exp(v.zoom*.95*dt));
 if(free)topView=false;
 dirty=true;
 canvas.dataset.keyboardCamera=JSON.stringify({target:target.map(n=>+n.toFixed(4)),yaw:+yaw.toFixed(5),elevation:+elevation.toFixed(5),distance:+distance.toFixed(4)});
}
window.addEventListener('keydown',e=>{
 if(isNavigationField(e.target)||e.ctrlKey||e.altKey||e.metaKey)return;
 const k=e.key.toLowerCase();
 if(k===' '&&depFollowState?.manual){e.preventDefault();if(!e.repeat)depManualJump();return}
 if(k==='capslock'&&depFollowState){e.preventDefault();resetNavigationKeys();depExitVehicleView();return}
 if(k==='escape'){if(depFollowState){resetNavigationKeys();depExitVehicleView();return}if(streetMode)leaveStreet();else exitNavigation();return}
 if(conceptMode||filmRecording)return;
 if(cameraKeys.has(k)){
  e.preventDefault();heldKeys.add(k);
  // A brief tap remains visible even if keydown and keyup land between animation frames.
  if(!e.repeat&&!streetMode)cameraPulses.set(k,performance.now()+90);
  return;
 }
 if(e.target===canvas&&['+','=','-'].includes(k)){e.preventDefault();zoomBy(k==='-'?1.1:.9)}
});
window.addEventListener('keyup',e=>heldKeys.delete(e.key.toLowerCase()));
window.addEventListener('blur',resetNavigationKeys);
document.addEventListener('focusin',e=>{if(isNavigationField(e.target))resetNavigationKeys()});
document.addEventListener('visibilitychange',()=>{if(document.hidden)resetNavigationKeys()});
reset();run(['w']);assert(target[2]<-500&&Math.abs(target[0])<.001);
reset();run(['s']);assert(target[2]>500);
reset();run(['a']);assert(target[0]<-500);
reset();run(['d']);const straight=Math.hypot(target[0],target[2]);assert(target[0]>500);
reset();run(['w','d']);assert(Math.abs(Math.hypot(target[0],target[2])-straight)<.01,'diagonal speed');
reset();yaw=Math.PI/2;run(['w']);assert(target[0]<-500&&Math.abs(target[2])<.001,'camera-relative forward');
reset();run(['w','s','a','d','q','e','k','l','z','x']);assert.deepEqual(target,[0,0,0]);assert.equal(distance,1000);assert.equal(yaw,0);assert.equal(elevation,.5);
reset();run(['e']);assert(yaw>1);reset();run(['q']);assert(yaw<-1);
reset();run(['k']);assert(distance<500);run(['l'],8);assert.equal(distance,5500);run(['k'],12);assert.equal(distance,35);
reset();run(['z'],8);assert.equal(elevation,1.565);run(['x'],8);assert.equal(elevation,-.12);
reset();elevation=.035;run(['w'],.1);assert.equal(elevation,.035,'gate view must not snap tilt');
reset();run(['w'],1,30);const low=target[2];reset();run(['w'],1,120);assert(Math.abs(target[2]-low)/Math.abs(low)<.015,'frame-rate independent speed');
reset();run(['w'],.5);const before=target[2],speed=cameraVelocity.forward;run([],1);assert(target[2]<before,'smooth deceleration');assert(cameraVelocity.forward<speed/100);
reset();streetMode=true;run(['w','e','k','z'],.5);assert.deepEqual(target,[0,0,0]);assert.equal(yaw,0);assert(followDistance<9&&desiredPitch>.23);assert(heldKeys.has('w'),'AK keeps walking keys');
reset();depFollowState={mode:'fpv',offset:0,pitch:0};run(['w','e','k','z'],.5);assert.deepEqual(target,[0,0,0]);assert(depFollowState.offset>0&&depFollowState.pitch>0&&depFollowState.zoom<1);
reset();conceptMode=true;run(['w']);assert.deepEqual(target,[0,0,0]);assert.equal(heldKeys.size,0);
reset();filmRecording=true;run(['w']);assert.deepEqual(target,[0,0,0]);
function event(key,extra={}){return {key,target:canvas,preventDefault(){this.prevented=true},...extra}}
reset();let e=event('w',{target:new HTMLInputElement()});listeners.keydown(e);assert.equal(heldKeys.size,0);assert(!e.prevented);
e=event('s',{ctrlKey:true});listeners.keydown(e);assert.equal(heldKeys.size,0);assert(!e.prevented);
e=event('W');listeners.keydown(e);assert(heldKeys.has('w')&&e.prevented);listeners.keyup(event('w'));assert.equal(heldKeys.size,0);updateKeyboardCamera(1/60,performance.now());assert(target[2]<0,'short tap between frames');
run(['w']);docListeners.focusin({target:new HTMLInputElement()});assert.equal(heldKeys.size,0);assert(Object.values(cameraVelocity).every(x=>x===0));assert.equal(cameraPulses.size,0);
run(['e']);listeners.blur();assert.equal(heldKeys.size,0);assert.equal(cameraVelocity.turn,0);
run(['d']);document.hidden=true;docListeners.visibilitychange();assert.equal(heldKeys.size,0);assert.equal(cameraVelocity.side,0);
console.log('PASS: all ten keys, camera-relative movement, diagonal normalization, smooth stop, 30/120fps, zoom/tilt limits, gate view, AK/follow modes, tap, form/modifier guard, blur/hidden reset');
