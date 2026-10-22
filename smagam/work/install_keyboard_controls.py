from pathlib import Path

p=Path(__file__).with_name('viewer-pdf.html')
s=p.read_text(encoding='utf-8')
assert 'function updateKeyboardCamera' not in s
s=s.replace('heldKeys.clear()', 'resetNavigationKeys()')
start=s.index("window.addEventListener('keydown',e=>{if(e.target instanceof HTMLInputElement")
end=s.index('\n',start)
code=r'''// Smooth keyboard camera: movement is integrated in seconds, independent of key repeat.
const cameraKeys=new Set(['w','s','a','d','q','e','k','l','z','x','arrowup','arrowdown','arrowleft','arrowright','shift']);
const cameraVelocity={forward:0,side:0,turn:0,zoom:0,tilt:0},cameraPulses=new Map();
function resetNavigationKeys(){heldKeys.clear();cameraPulses.clear();for(const k in cameraVelocity)cameraVelocity[k]=0}
function isNavigationField(el){return el instanceof HTMLInputElement||el instanceof HTMLTextAreaElement||el instanceof HTMLSelectElement||el?.isContentEditable}
function updateKeyboardCamera(dt,now=performance.now()){
 if(conceptMode||filmRecording){resetNavigationKeys();return}
 const down=k=>heldKeys.has(k)||(cameraPulses.get(k)||0)>now;
 for(const [k,until] of cameraPulses)if(until<=now)cameraPulses.delete(k);
 const following=!!depFollowState,free=!streetMode&&!following;
 const command={forward:free?Number(down('w'))-Number(down('s')):0,side:free?Number(down('d'))-Number(down('a')):0,turn:streetMode?0:Number(down('e')||down('arrowright'))-Number(down('q')||down('arrowleft')),zoom:Number(down('l'))-Number(down('k')),tilt:Number(down('z')||(!streetMode&&down('arrowup')))-Number(down('x')||(!streetMode&&down('arrowdown')))};
 const length=Math.max(1,Math.hypot(command.forward,command.side));command.forward/=length;command.side/=length;
 const ease=1-Math.exp(-12*dt);
 for(const k in cameraVelocity){cameraVelocity[k]+=(command[k]-cameraVelocity[k])*ease;if(Math.abs(cameraVelocity[k])<.0001)cameraVelocity[k]=0}
 const v=cameraVelocity;if(!Object.values(v).some(Boolean))return;
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
  depFollowState.offset+=v.turn*1.15*dt;
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
document.addEventListener('visibilitychange',()=>{if(document.hidden)resetNavigationKeys()});'''
s=s[:start]+code+s[end:]
s=s.replace('updateAK(dt);deploymentTick(dt);depFollowTick(dt);','updateKeyboardCamera(dt);updateAK(dt);deploymentTick(dt);depFollowTick(dt);')
s=s.replace('W/S move · A/D strafe · Q/E or ↶ ↷ turn · Hold buttons to walk','W/S move · A/D strafe · Q/E turn · K/L zoom · Z/X tilt')
s=s.replace('DRAG: PAN · SHIFT + DRAG: ROTATE · SCROLL: CURSOR ZOOM','W/S: MOVE · A/D: STRAFE · Q/E: ROTATE · K/L: ZOOM · Z/X: TILT')
s=s.replace('<div class="legend">PDF positions traced.', '''<details id="keyboardGuide" class="legend"><summary>Keyboard controls</summary><div><b>W / S</b> — forward / backward<br><b>A / D</b> — left / right<br><b>Q / E</b> — rotate left / right<br><b>K / L</b> — zoom in / out<br><b>Z / X</b> — tilt camera up / down<br>Hold a key for smooth movement.<br>Shift + W/A/S/D — faster movement.<br>Street view: W/A/S/D controls AK.<br>Vehicle FPV / follow: Q/E look, K/L zoom, Z/X tilt; the vehicle stays on its route.</div></details><div class="legend">PDF positions traced.''')
s=s.replace('aria-label="Interactive PDF based Samagam 3D model"','aria-label="Interactive PDF based Samagam 3D model" aria-describedby="keyboardGuide" aria-keyshortcuts="W S A D Q E K L Z X"')
p.write_text(s,encoding='utf-8')
print('Installed smooth keyboard navigation and visible guide')
