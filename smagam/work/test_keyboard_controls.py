from pathlib import Path
import subprocess

root=Path(__file__).resolve().parents[1]
s=(root/'work/viewer-pdf.html').read_text(encoding='utf-8')
code=s[s.index('// Smooth keyboard camera:'):s.index('\n',s.index("document.addEventListener('visibilitychange',()=>{if(document.hidden)resetNavigationKeys()});"))]
preamble=r'''
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
'''
tests=r'''
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
'''
p=root/'work/test-keyboard-controls.cjs';p.write_text(preamble+code+tests,encoding='utf-8')
subprocess.run(['C:/Program Files/nodejs/node.exe',str(p)],check=True)
