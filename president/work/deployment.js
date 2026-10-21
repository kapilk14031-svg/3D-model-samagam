// User-authored draft deployment, independent of the registered venue geometry.
const depUI=id=>root.querySelector('#dep-'+id),depGroup=new THREE.Group();scene.add(depGroup);
const dutyNames=['Outer perimeter duty','Binocular duty — rooftop','Lotus duty','Inner cordon duty','Outer cordon duty','Main gate — DFMD / HHMD','Naka & barricade duty','Auditorium main stage duty','Auditorium seating duty','VIP parking duty','VIP toilet duty','VIP lounge duty','Hall gate duty'];
for(const text of dutyNames){const o=document.createElement('option');o.value=text;depUI('duties').appendChild(o);}
const depSymbols={officer:'👮',barricade:'🚧',binocular:'🔭',dfmd:'🚪',hhmd:'🔍',radio:'📻',cone:'⚠️',cctv:'📹',light:'💡'};
// Visibility against the same opaque venue solids rendered by this viewer.
const depOccluders=[],depOccBox=new THREE.Box3(new THREE.Vector3(-.5,-.5,-.5),new THREE.Vector3(.5,.5,.5));
const depOccTransform=new THREE.Object3D();
for(const o of data.objects){if(o.mat==='glass'||o.mat==='lotusGlass'||!['shell','roof','ceiling','context','campus'].includes(o.group))continue;
 const solidName=/wall|roof|ceiling|slab|column|pier|beam|parapet|spandrel|building|enclosure|boundary|dome|drum/i.test(o.name);
 if(!solidName||!geos[o.shape])continue;
 depOccTransform.position.fromArray(o.p);depOccTransform.scale.fromArray(o.s);depOccTransform.rotation.set(o.tilt||0,o.rot,o.rz||0);depOccTransform.updateMatrix();const matrix=depOccTransform.matrix.clone(),inverse=matrix.clone().invert();
 const bounds=(o.shape==='box'?depOccBox:((geos[o.shape].boundingBox||geos[o.shape].computeBoundingBox()),geos[o.shape].boundingBox)).clone().applyMatrix4(matrix);
 const mesh=o.shape==='box'?null:new THREE.Mesh(geos[o.shape],new THREE.MeshBasicMaterial({side:THREE.DoubleSide}));if(mesh){mesh.matrixAutoUpdate=false;mesh.matrix.copy(matrix);mesh.matrixWorld.copy(matrix);}
 depOccluders.push({group:o.group,matrix,inverse,bounds,mesh});
}
const depOccRay=new THREE.Ray(),depOccLocal=new THREE.Ray(),depOccPoint=new THREE.Vector3(),depOccHit=new THREE.Vector3(),depOccCaster=new THREE.Raycaster();
let depOccStamp=0,depOccCache=new Map(),depOccCamera=new THREE.Matrix4(),depOccSignature='',depOccTimer=null;
function depOccluded(item){const target=new THREE.Vector3(item.x,item.y+(item.kind==='officer'?1.62:item.kind==='dfmd'?1.8:1),item.z),distance=camera.position.distanceTo(target);if(distance<.2)return false;
 depOccRay.set(camera.position,target.clone().sub(camera.position).normalize());depOccCaster.ray.copy(depOccRay);depOccCaster.near=.08;depOccCaster.far=distance-.15;
 for(const o of depOccluders){if(!groups[o.group]?.visible||!depOccRay.intersectBox(o.bounds,depOccHit)||depOccHit.distanceTo(camera.position)>distance-.15)continue;
  if(o.mesh){if(depOccCaster.intersectObject(o.mesh,false).length)return true;continue;}
  depOccLocal.copy(depOccRay).applyMatrix4(o.inverse);const hit=depOccLocal.intersectBox(depOccBox,depOccPoint);if(!hit)continue;const world=hit.clone().applyMatrix4(o.matrix);if(world.distanceTo(camera.position)>.08&&world.distanceTo(camera.position)<distance-.15)return true;
 }return false;
}
function depRefreshOcclusion(){
  const signature=current+'|'+depItems.map(o=>[o.id,o.x,o.y,o.z].join(',')).join(';')+'|'+Object.entries(groups).map(([k,g])=>k+g.visible).join(',');
  if(signature===depOccSignature&&camera.matrixWorld.equals(depOccCamera))return;
  depOccSignature=signature;
  depOccCamera.copy(camera.matrixWorld);
  depOccCache=new Map(depItems.map(o=>[o.id,depOccluded(o)]));
}

// Minimalist Hover Tooltip element (Only displays on cursor hover)
const depTooltip=root.querySelector('#dep-hover-tooltip');
let depHover=null,depHoverTimer=null;

const depPanelToggle = root.querySelector('#gms-dep-panel-toggle');
const depPanelEl = root.querySelector('#gms-deployment');
const depPanelClose = root.querySelector('#dep-panel-close-btn');

function isAnyTabOpen(){
  const radialOpen = depRadial && depRadial.style.display === 'block';
  const panelOpen = depPanelEl && depPanelEl.classList.contains('show');
  return !!(radialOpen || panelOpen);
}
window.__DEP_IS_TAB_OPEN = isAnyTabOpen;

function updateTabLock(){
  const locked = isAnyTabOpen();
  if (typeof controls !== 'undefined' && controls) {
    controls.enabled = !locked;
  }
  if (labelRoot) {
    labelRoot.style.pointerEvents = locked ? 'none' : '';
  }
}

function updateOfficerHud(officer) {
  const tc = root.querySelector('#dep-touch-controls');
  if (tc) {
    const isTouchDevice = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0) || window.innerWidth <= 900;
    tc.style.display = (officer && isTouchDevice) ? 'flex' : 'none';
  }
}

function initTouchControls() {
  const tc = root.querySelector('#dep-touch-controls');
  if (!tc) return;
  tc.querySelectorAll('.touch-btn').forEach(btn => {
    const key = btn.dataset.key;
    const action = btn.dataset.action;
    const press = (e) => {
      e.preventDefault();
      e.stopPropagation();
      btn.classList.add('active');
      if (action === 'jump') {
        const o = depItems.find(x => x.id === depSelected);
        if (o) triggerOfficerJump(o);
      } else if (key) {
        depKeysDown[key] = true;
      }
    };
    const release = (e) => {
      e.preventDefault();
      e.stopPropagation();
      btn.classList.remove('active');
      if (key) {
        depKeysDown[key] = false;
      }
    };
    btn.addEventListener('pointerdown', press);
    btn.addEventListener('pointerup', release);
    btn.addEventListener('pointercancel', release);
    btn.addEventListener('pointerleave', release);
  });
}
initTouchControls();

function depSyncDropdownLabels(item) {
  if (!item) return;
  const label = (depSymbols[item.kind] || '') + ' ' + (item.name || 'Item') + ' · ' + (item.duty || 'Post');
  const topOpt = root.querySelector(`#dep-top-list option[value="${item.id}"]`);
  if (topOpt) topOpt.textContent = label;
  const sideOpt = root.querySelector(`#dep-list option[value="${item.id}"]`);
  if (sideOpt) sideOpt.textContent = label;
  const btnObj = depButtons.find(b => b.item.id === item.id);
  if (btnObj && btnObj.e) btnObj.e.setAttribute('aria-label', (item.name || '') + ' · ' + (item.duty || ''));
  const titleEl = depPeekHead.querySelector('#dep-peek-title');
  if (titleEl) titleEl.textContent = (depSymbols[item.kind] || '') + ' ' + item.name;
}

function isOfficerSelected() {
  if (!depSelected || typeof depItems === 'undefined') return false;
  return depItems.some(x => x.id === depSelected);
}
window.__DEP_IS_OFFICER_SELECTED = isOfficerSelected;

if (depPanelToggle && depPanelEl) {
  depPanelToggle.addEventListener('click', e => {
    e.stopPropagation();
    const isShowing = depPanelEl.classList.contains('show');
    if (isShowing) {
      depPanelEl.classList.remove('show');
      depPanelToggle.classList.remove('active');
    } else {
      depPanelEl.classList.add('show');
      depPanelToggle.classList.add('active');
      const layersMenu = root.querySelector('#gms-layers-menu');
      if (layersMenu) layersMenu.classList.remove('show');
      if (depRadial) depRadial.style.display = 'none';
    }
    updateTabLock();
  });
}

if (depPanelClose && depPanelEl) {
  depPanelClose.addEventListener('click', e => {
    e.stopPropagation();
    depPanelEl.classList.remove('show');
    if (depPanelToggle) depPanelToggle.classList.remove('active');
    updateTabLock();
  });
}

if (depPanelEl) {
  for (const evt of ['pointerdown', 'pointerup', 'pointermove', 'mousedown', 'mouseup', 'mousemove', 'click', 'dblclick', 'contextmenu']) {
    depPanelEl.addEventListener(evt, e => e.stopPropagation());
  }
  depPanelEl.addEventListener('wheel', e => e.stopPropagation(), { passive: true });
}

document.addEventListener('click', e => {
  if (depPanelEl && depPanelEl.classList.contains('show')) {
    if (!depPanelEl.contains(e.target) && (!depPanelToggle || !depPanelToggle.contains(e.target))) {
      depPanelEl.classList.remove('show');
      if (depPanelToggle) depPanelToggle.classList.remove('active');
      updateTabLock();
    }
  }
});

function depShowHover(id){
  if(isAnyTabOpen()) return;
  clearTimeout(depHoverTimer);
  depHover=id;
  const item=depItems.find(o=>o.id===id);
  if(item&&depTooltip){
    depTooltip.textContent=(depSymbols[item.kind]||'')+ ' ' + item.name + ' · ' + (item.duty||'Post');
    depTooltip.style.display='block';
    const btn=depButtons.find(b=>b.item.id===id)?.e;
    if(btn){
      depTooltip.style.left=btn.style.left;
      depTooltip.style.top=(parseFloat(btn.style.top)-30)+'px';
    }
  }
}

function depLeaveHover(){
  clearTimeout(depHoverTimer);
  depHoverTimer=setTimeout(()=>{
    depHover=null;
    if(depTooltip) depTooltip.style.display='none';
  },100);
}

// Full Information Tab / Card (Opened on CLICK, Minimized by Default)
const depPeek=document.createElement('div');
depPeek.className='dep-peek minimized';
depPeek.hidden=true;
let depPeekIsMinimized=true;

const depPeekHead=document.createElement('div');
depPeekHead.className='dep-peek-head';
depPeekHead.innerHTML='<div class="dep-peek-title-row"><span id="dep-peek-title" class="dep-peek-title">👮 Post Information</span><span id="dep-peek-duty-badge" class="dep-peek-duty-badge"></span></div><div class="dep-peek-controls"><button type="button" id="dep-peek-del" class="dep-peek-btn-icon btn-danger-soft" title="Delete post">🗑️</button><button type="button" id="dep-peek-min" class="dep-peek-btn-icon" title="Maximize full details">+</button><button type="button" id="dep-peek-close" class="dep-peek-btn-icon" title="Close">✕</button></div>';

const depPeekBody=document.createElement('div');
depPeekBody.className='dep-peek-body';
depPeekBody.style.display='none';

const depPeekText=document.createElement('div'),depPeekActions=document.createElement('div');
depPeekActions.className='viz-controls';

depPeekBody.append(depPeekText,depPeekActions);
depPeek.append(depPeekHead,depPeekBody);
host.appendChild(depPeek);

// Stop event bubbling to canvas/stage so clicking card does not orbit or click canvas behind it
['pointerdown','pointerup','pointermove','mousedown','mouseup','mousemove','click','dblclick'].forEach(evt => {
  depPeek.addEventListener(evt, e => e.stopPropagation());
});
depPeek.addEventListener('wheel', e => e.stopPropagation(), { passive: true });

function setDepPeekMinimized(minimized){
  depPeekIsMinimized=!!minimized;
  const minBtn=depPeekHead.querySelector('#dep-peek-min');
  if(depPeekIsMinimized){
    depPeek.classList.add('minimized');
    if(minBtn){minBtn.textContent='+';minBtn.title='Maximize full details';}
    depPeekBody.style.display='none';
  }else{
    depPeek.classList.remove('minimized');
    if(minBtn){minBtn.textContent='−';minBtn.title='Minimize';}
    depPeekBody.style.display='block';
  }
  depUpdate();
}

const depPeekDelBtn = depPeekHead.querySelector('#dep-peek-del');
const depPeekMinBtn = depPeekHead.querySelector('#dep-peek-min');
const depPeekCloseBtn = depPeekHead.querySelector('#dep-peek-close');

if(depPeekDelBtn){
  depPeekDelBtn.addEventListener('pointerdown', e => e.stopPropagation());
  depPeekDelBtn.addEventListener('click', e => {
    e.stopPropagation();
    if(!depSelected) return;
    depItems = depItems.filter(x => x.id !== depSelected);
    depSelected = null;
    depStore();
    depBuild();
    depPeek.hidden = true;
    if(depUI('editor')) depUI('editor').hidden = true;
    depUI('status').textContent = '🗑️ Deployment removed (Auto-saved).';
    updateTabLock();
    depUpdate();
    draw();
  });
}

if(depPeekMinBtn){
  depPeekMinBtn.addEventListener('pointerdown', e => e.stopPropagation());
  depPeekMinBtn.addEventListener('click', e => {
    e.preventDefault();
    e.stopPropagation();
    setDepPeekMinimized(!depPeekIsMinimized);
  });
}

if(depPeekCloseBtn){
  depPeekCloseBtn.addEventListener('pointerdown', e => e.stopPropagation());
  depPeekCloseBtn.addEventListener('click', e => {
    e.preventDefault();
    e.stopPropagation();
    depSelected = null;
    depPeek.hidden = true;
    if(depUI('editor')) depUI('editor').hidden = true;
    updateTabLock();
    depUpdate();
    draw();
  });
}

const depPeekFields={};
for(const [key,label] of [['name','Name'],['belt','Belt no.'],['duty','Duty'],['mobile','Mobile']]){
  const wrap=document.createElement('label');wrap.className='form-label';wrap.textContent=label;
  const field=document.createElement('input');field.className='form-control';field.maxLength=key==='mobile'?30:100;
  field.setAttribute('aria-label','Edit '+label);
  wrap.appendChild(field);depPeekText.appendChild(wrap);depPeekFields[key]=field;
  function commitField(){
    const o=depItems.find(o=>o.id===depSelected);if(!o)return;
    const value=field.value.trim();if(o[key]===value)return;
    o[key]=value;depStore();depBuild();depChoose(o.id);
  }
  field.addEventListener('input',()=>{
    const o=depItems.find(o=>o.id===depSelected);
    if(o){ o[key]=field.value; depStore(); }
  });
  field.addEventListener('change',commitField);
  field.addEventListener('blur',commitField);
  field.addEventListener('keydown',e=>{e.stopPropagation();if(e.key==='Enter'){e.preventDefault();field.blur();}});
}

for(const [text,fn] of [
  ['First person',()=>depView('first')],
  ['Third person',()=>depView('third')],
  ['↺ −30°',()=>depRotate(-30)],
  ['↻ +30°',()=>depRotate(30)],
  ['Move',()=>depUI('move').click()],
  ['Minimize',()=>setDepPeekMinimized(true)],
  ['Close',()=>depDeselect(true)]
]){
  const b=document.createElement('button');b.type='button';b.className='btn';b.textContent=text;
  b.addEventListener('click',e=>{e.stopPropagation();fn();});
  depPeekActions.appendChild(b);
}

const depTypes=Object.keys(depSymbols),depStorage='gyan-mansarovar-duty-v1';
depUI('editkind').innerHTML=depUI('kind').innerHTML;
let depItems=[],depSelected=null,depPlace=false,depCamera=null,depReturn=null,depNodes=[],depButtons=[],depReady=false,depNew=null,depClickPoint=null;

function depSeed(){const positions=[[-14,.3,-58],[-30,10,-24],[28,.3,-35],[-10,.3,8],[54,.3,-2],[-13,.3,-59],[-13,.3,-69],[-53,1.2,11],[-42,.5,-8],[-8,.3,21],[20,.3,38],[0,.3,39],[-16,.9,8.5]];
const items=dutyNames.map((d,i)=>{const p=mapPreset(positions[i],i===1||i===7||i===8||i===12?'hall':'campus');if(i===0||i===5||i===6){p[0]+=geo.gateDelta[0];p[2]+=geo.gateDelta[1];}return {id:'post-'+(i+1),kind:'officer',name:'Officer '+(i+1),duty:d,belt:'',mobile:'',x:p[0],y:p[1],z:p[2],angle:0};});
const gate=mapPreset([-13,.3,-61],'gate');for(const [kind,dx,dz] of [['dfmd',-3,0],['hhmd',-2,2],['barricade',-4,-8],['barricade',4,-8],['binocular',0,0]]){const roof=kind==='binocular'?items[1]:null;items.push({id:'equipment-'+items.length,kind,name:kind.toUpperCase(),duty:kind==='binocular'?dutyNames[1]:dutyNames[5],belt:'',mobile:'',x:roof?roof.x+1:gate[0]+dx,y:roof?roof.y:.3,z:roof?roof.z:gate[2]+dz,angle:0});if(kind==='barricade')Object.assign(items[items.length-1],[{"x":-58.43806872039645,"y":0.36,"z":-71.52475246652457,"angle":80.22,"name":"West boundary road corner","duty":"Road barricade — boundary corner"},{"x":63.20502773270095,"y":0.36,"z":-92.49764470660074,"angle":80.22,"name":"East boundary road corner","duty":"Road barricade — boundary corner"}][dx<0?0:1]);}return items;}

function depValid(items){return Array.isArray(items)&&items.length<=500&&items.every(o=>o&&typeof o.id==='string'&&depTypes.includes(o.kind)&&['x','y','z','angle'].every(k=>typeof o[k]==='number'&&Number.isFinite(o[k]))&&Math.abs(o.x)<5000&&Math.abs(o.z)<5000&&o.y>=0&&o.y<=100&&['name','duty','belt','mobile'].every(k=>typeof o[k]==='string'&&o[k].length<=200))&&new Set(items.map(o=>o.id)).size===items.length;}

function depLoadLocal(){
  try{
    const raw=localStorage.getItem(depStorage);if(!raw)return null;
    const parsed=JSON.parse(raw);
    const items=Array.isArray(parsed)?parsed:(parsed&&Array.isArray(parsed.items)?parsed.items:null);
    if(depValid(items))return {items,savedAt:(parsed&&parsed.savedAt)||0};
  }catch(e){console.warn('depLoadLocal error:',e);}
  return null;
}

const initialLocal=depLoadLocal();
depItems=initialLocal?initialLocal.items:depSeed();

function depStore(){
  try{
    const record={version:1,savedAt:Date.now(),origin:[geo.originLongitude,geo.originLatitude],items:depItems};
    localStorage.setItem(depStorage,JSON.stringify(record));
    depUI('status').textContent='✅ Auto-saved · '+depItems.filter(o=>o.kind==='officer').length+' officers · '+depItems.filter(o=>o.kind!=='officer').length+' equipment';
  }catch(e){console.warn('localStorage save warning:',e);}
  depQueue();
}

const depMaterials={
  khaki:new THREE.MeshStandardMaterial({color:0xb58e5c,roughness:0.82}), // Real Indian Police Khaki uniform shirt
  trousers:new THREE.MeshStandardMaterial({color:0x9f7947,roughness:0.85}), // Khaki trousers
  dark:new THREE.MeshStandardMaterial({color:0x16181b,roughness:0.35,metalness:0.2}), // Polished black leather boots, holster, belt, visor
  yellow:new THREE.MeshStandardMaterial({color:0xe5b839,roughness:0.3,metalness:0.65}), // Brass stars, insignia, buckle
  skin:new THREE.MeshStandardMaterial({color:0xc48c66,roughness:0.75}), // Realistic Indian skin tone
  red:new THREE.MeshStandardMaterial({color:0xb91c1c,roughness:0.5}), // Officer cap red ribbon band
  blue:new THREE.MeshStandardMaterial({color:0x1d3557,roughness:0.6}), // Navy blue cap crown / DFMD / equipment
  white:new THREE.MeshStandardMaterial({color:0xf3f4f6,roughness:0.7}), // Whistle cord / name text
  hair:new THREE.MeshStandardMaterial({color:0x1c1917,roughness:0.9}), // Neat hair
  lathi:new THREE.MeshStandardMaterial({color:0x6e3c1b,roughness:0.4}), // Polished wood baton
  hhmdBody:new THREE.MeshStandardMaterial({color:0x1b1f24,roughness:0.42,metalness:0.12}), // Tactical matte polycarbonate scanner casing
  hhmdGrip:new THREE.MeshStandardMaterial({color:0x0c0e11,roughness:0.88,metalness:0.04}), // Non-slip textured rubber handle grip
  hhmdSwitch:new THREE.MeshStandardMaterial({color:0xd92d20,roughness:0.35,metalness:0.15}), // Red power/sensitivity toggle slider
  hhmdSpeaker:new THREE.MeshStandardMaterial({color:0x333b47,roughness:0.45,metalness:0.4}), // Audio buzzer sound emitter grille
  hhmdLedGreen:new THREE.MeshStandardMaterial({color:0x22c55e,emissive:0x15803d,emissiveIntensity:1.5,roughness:0.2}), // Power ON green LED
  hhmdLedAmber:new THREE.MeshStandardMaterial({color:0xf59e0b,emissive:0xb45309,emissiveIntensity:1.2,roughness:0.2}), // Ready/Standby amber LED
  hhmdLedRed:new THREE.MeshStandardMaterial({color:0xef4444,emissive:0xb91c1c,emissiveIntensity:1.5,roughness:0.2}), // Alarm metal-detect red LED
  hhmdStripe:new THREE.MeshStandardMaterial({color:0xfacc15,roughness:0.35,metalness:0.1}) // High-visibility hazard yellow band
};
function depPart(g,shape,p,s,mat){
  const m = (typeof mat === 'string' ? depMaterials[mat] : mat) || depMaterials.dark;
  const mesh = new THREE.Mesh(geos[shape], m);
  mesh.position.fromArray(p);
  mesh.scale.fromArray(s);
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  g.add(mesh);
  return mesh;
}
const depHhmdCanvas=document.createElement('canvas');depHhmdCanvas.width=128;depHhmdCanvas.height=512;
const dhc=depHhmdCanvas.getContext('2d');
dhc.fillStyle='#181b20';dhc.fillRect(0,0,128,512);
dhc.strokeStyle='#374151';dhc.lineWidth=4;dhc.strokeRect(6,6,116,500);
dhc.fillStyle='#eab308';dhc.fillRect(10,16,108,64);
dhc.fillStyle='#0f172a';dhc.font='900 18px sans-serif';dhc.textAlign='center';dhc.fillText('SECURITY',64,42);
dhc.font='800 13px sans-serif';dhc.fillText('SCANNER',64,62);
dhc.fillStyle='#1e293b';
for(let i=0;i<4;i++){dhc.beginPath();dhc.moveTo(12+i*28,72);dhc.lineTo(24+i*28,72);dhc.lineTo(16+i*28,80);dhc.lineTo(4+i*28,80);dhc.fill();}
dhc.fillStyle='#111827';dhc.fillRect(16,92,96,276);
dhc.strokeStyle='#64748b';dhc.lineWidth=2.5;dhc.strokeRect(22,100,84,260);
dhc.strokeStyle='#eab308';dhc.lineWidth=1.5;dhc.strokeRect(28,110,72,240);
dhc.strokeStyle='#38bdf8';dhc.lineWidth=2.5;
dhc.beginPath();dhc.arc(64,185,26,0,Math.PI*2);dhc.stroke();
dhc.beginPath();dhc.arc(64,185,16,0,Math.PI*2);dhc.stroke();
dhc.fillStyle='#38bdf8';dhc.beginPath();dhc.arc(64,185,6,0,Math.PI*2);dhc.fill();
dhc.fillStyle='#f8fafc';dhc.font='bold 11px sans-serif';dhc.fillText('360° SENSING',64,235);
dhc.font='9px sans-serif';dhc.fillStyle='#94a3b8';dhc.fillText('HIGH SENSITIVITY',64,252);dhc.fillText('ALL METALS',64,268);
for(let y=290;y<=340;y+=8){dhc.fillStyle=y%16===0?'#eab308':'#64748b';dhc.fillRect(36,y,56,3);}
dhc.fillStyle='#dc2626';dhc.fillRect(16,382,96,28);
dhc.fillStyle='#ffffff';dhc.font='bold 12px sans-serif';dhc.fillText('METAL DETECTOR',64,401);
dhc.fillStyle='#94a3b8';dhc.font='bold 9px sans-serif';dhc.fillText('PWR ● BATT ● ALARM',64,435);
const depHhmdDecalFront=new THREE.MeshStandardMaterial({map:new THREE.CanvasTexture(depHhmdCanvas),roughness:0.35,metalness:0.1});
const depSignCanvas=document.createElement('canvas');depSignCanvas.width=512;depSignCanvas.height=128;const depSignCtx=depSignCanvas.getContext('2d');depSignCtx.fillStyle='#edbd2b';depSignCtx.fillRect(0,0,512,128);depSignCtx.fillStyle='#172837';depSignCtx.font='bold 82px sans-serif';depSignCtx.textAlign='center';depSignCtx.fillText('POLICE',256,93);const depPoliceSign=new THREE.MeshStandardMaterial({map:new THREE.CanvasTexture(depSignCanvas),side:THREE.FrontSide});
const depConeGeometry=new THREE.ConeGeometry(.22,.7,12),depBoardGeometry=new THREE.PlaneGeometry(1.4,.38);

function depBuildOfficer(g, mode='officer'){
  g.scale.setScalar(1);

  // 1. Pelvis / Hips & Torso Group (Pivoting at y = 0.88)
  const torsoGroup = new THREE.Group();
  torsoGroup.position.set(0, 0.88, 0);
  g.add(torsoGroup);

  // Main Torso / Chest (Khaki shirt, tailored fit)
  depPart(torsoGroup, 'rounded', [0, 0.24, 0], [.44, .54, .27], 'khaki');
  
  // Shirt button placket (vertical center stripe)
  depPart(torsoGroup, 'box', [0, 0.24, -.14], [.04, .52, .01], 'khaki');
  for (let by = 0.08; by <= 0.42; by += 0.08) {
    depPart(torsoGroup, 'sphereSmooth', [0, by, -.146], [.01, .01, .01], 'yellow');
  }

  // Dual pleated chest pockets with flaps
  for (const px of [-.12, .12]) {
    depPart(torsoGroup, 'box', [px, 0.28, -.14], [.11, .14, .02], 'khaki');
    depPart(torsoGroup, 'box', [px, 0.36, -.144], [.12, .035, .025], 'khaki');
    depPart(torsoGroup, 'sphereSmooth', [px, 0.35, -.158], [.008, .008, .008], 'yellow');
  }

  // Police Ribbon Bar (Medal ribbons) above left pocket
  depPart(torsoGroup, 'box', [-.12, 0.41, -.144], [.09, .022, .012], 'red');
  depPart(torsoGroup, 'box', [-.145, 0.41, -.146], [.03, .022, .012], 'blue');
  depPart(torsoGroup, 'box', [-.095, 0.41, -.146], [.03, .022, .012], 'yellow');

  // Brass Name Plate above right pocket
  depPart(torsoGroup, 'box', [.12, 0.41, -.144], [.08, .02, .01], 'yellow');

  // Shoulder Epaulettes (Straps with 3 Brass Rank Stars)
  for (const sx of [-.23, .23]) {
    depPart(torsoGroup, 'box', [sx, 0.49, 0], [.11, .025, .15], 'khaki');
    depPart(torsoGroup, 'box', [sx, 0.505, 0], [.09, .015, .13], 'yellow');
    for (const sz of [-.04, 0, .04]) {
      depPart(torsoGroup, 'sphereSmooth', [sx, 0.52, sz], [.014, .012, .014], 'yellow');
    }
  }

  // Whistle lanyard cord looping from left shoulder
  depPart(torsoGroup, 'torus', [-.18, 0.42, -.10], [.08, .012, 1], 'yellow');

  // Sam Browne Leather Duty Belt around waist
  depPart(torsoGroup, 'box', [0, -0.01, 0], [.46, .085, .29], 'dark');
  depPart(torsoGroup, 'box', [0, -0.01, -.15], [.085, .095, .02], 'yellow');
  depPart(torsoGroup, 'box', [0, -0.01, -.155], [.05, .06, .02], 'dark');
  const strap = depPart(torsoGroup, 'box', [.02, 0.23, -.142], [.045, .54, .015], 'dark');
  strap.rotation.z = -0.42;

  // Leather service holster with revolver/pistol on right hip
  depPart(torsoGroup, 'box', [.24, -0.07, 0], [.07, .18, .12], 'dark');
  depPart(torsoGroup, 'box', [.24, .03, -.04], [.035, .06, .08], 'dark');
  // Utility pouch on left hip
  depPart(torsoGroup, 'box', [-.24, -0.01, 0], [.06, .10, .10], 'dark');

  // Neck & Shirt collar
  depPart(torsoGroup, 'cylinder', [0, 0.53, 0], [.08, .14, .08], 'skin');
  depPart(torsoGroup, 'box', [-.08, 0.49, -.08], [.08, .06, .03], 'khaki');
  depPart(torsoGroup, 'box', [.08, 0.49, -.08], [.08, .06, .03], 'khaki');

  // 2. Head Group (At top of neck)
  const headGroup = new THREE.Group();
  headGroup.position.set(0, 0.62, 0);
  torsoGroup.add(headGroup);

  // Realistic Head & Facial Proportions
  depPart(headGroup, 'sphereSmooth', [0, 0.10, 0], [.145, .17, .15], 'skin');
  depPart(headGroup, 'rounded', [0, 0.03, -.03], [.16, .11, .16], 'skin');
  depPart(headGroup, 'sphereSmooth', [-.15, 0.10, -.01], [.025, .045, .025], 'skin');
  depPart(headGroup, 'sphereSmooth', [.15, 0.10, -.01], [.025, .045, .025], 'skin');
  depPart(headGroup, 'box', [0, 0.10, -.15], [.028, .055, .04], 'skin');
  for (const ex of [-.055, .055]) {
    depPart(headGroup, 'box', [ex, 0.145, -.145], [.036, .012, .012], 'hair');
    depPart(headGroup, 'sphereSmooth', [ex, 0.115, -.142], [.016, .016, .014], 'white');
    depPart(headGroup, 'sphereSmooth', [ex, 0.115, -.150], [.010, .010, .010], 'dark');
  }
  depPart(headGroup, 'box', [0, 0.055, -.145], [.065, .016, .018], 'hair');
  depPart(headGroup, 'sphereSmooth', [0, 0.12, .05], [.15, .15, .14], 'hair');

  // INDIAN POLICE PEAKED SERVICE CAP
  depPart(headGroup, 'cylinder', [0, 0.19, 0], [.165, .06, .175], 'blue');
  depPart(headGroup, 'cylinder', [0, 0.185, 0], [.17, .035, .18], 'red');
  depPart(headGroup, 'cylinder', [0, 0.24, -.01], [.195, .06, .21], 'blue');
  depPart(headGroup, 'cylinder', [0, 0.27, -.02], [.21, .02, .225], 'blue');
  depPart(headGroup, 'box', [0, 0.21, -.18], [.045, .06, .012], 'yellow'); // Ashoka Lion Emblem Crest
  depPart(headGroup, 'sphereSmooth', [0, 0.24, -.18], [.02, .02, .01], 'yellow');
  const peak = depPart(headGroup, 'rounded', [0, 0.165, -.17], [.22, .02, .14], 'dark');
  peak.rotation.x = 0.26;
  depPart(headGroup, 'box', [0, 0.168, -.168], [.20, .012, .015], 'yellow');
  depPart(headGroup, 'sphereSmooth', [-.11, 0.17, -.14], [.014, .014, .014], 'yellow');
  depPart(headGroup, 'sphereSmooth', [.11, 0.17, -.14], [.014, .014, .014], 'yellow');

  // 3. Legs & Boots (Pivoting at hips: y = 0.82)
  const leftLeg = new THREE.Group();
  leftLeg.position.set(-.13, 0.82, 0);
  g.add(leftLeg);

  depPart(leftLeg, 'cylinder', [0, -.20, 0], [.095, .40, .10], 'trousers');
  depPart(leftLeg, 'cylinder', [0, -.48, 0], [.085, .36, .09], 'trousers');
  depPart(leftLeg, 'box', [0, -.48, -.092], [.015, .36, .01], 'trousers');
  depPart(leftLeg, 'box', [0, -.62, 0], [.105, .16, .13], 'dark');
  depPart(leftLeg, 'box', [0, -.60, -.068], [.06, .12, .02], 'dark');
  depPart(leftLeg, 'rounded', [0, -.71, -.06], [.115, .11, .26], 'dark');
  depPart(leftLeg, 'box', [0, -.76, -.04], [.12, .03, .28], 'dark');

  const rightLeg = new THREE.Group();
  rightLeg.position.set(.13, 0.82, 0);
  g.add(rightLeg);

  depPart(rightLeg, 'cylinder', [0, -.20, 0], [.095, .40, .10], 'trousers');
  depPart(rightLeg, 'cylinder', [0, -.48, 0], [.085, .36, .09], 'trousers');
  depPart(rightLeg, 'box', [0, -.48, -.092], [.015, .36, .01], 'trousers');
  depPart(rightLeg, 'box', [0, -.62, 0], [.105, .16, .13], 'dark');
  depPart(rightLeg, 'box', [0, -.60, -.068], [.06, .12, .02], 'dark');
  depPart(rightLeg, 'rounded', [0, -.71, -.06], [.115, .11, .26], 'dark');
  depPart(rightLeg, 'box', [0, -.76, -.04], [.12, .03, .28], 'dark');

  // 4. Arms & Hands (Pivoting at shoulders: y = 1.34)
  const leftArm = new THREE.Group();
  leftArm.position.set(-.26, 1.34, 0);
  g.add(leftArm);

  depPart(leftArm, 'cylinder', [0, -.16, 0], [.08, .32, .08], 'khaki');
  depPart(leftArm, 'cylinder', [0, -.30, 0], [.088, .04, .088], 'khaki');
  depPart(leftArm, 'cylinder', [0, -.46, 0], [.065, .30, .065], 'skin');
  depPart(leftArm, 'sphereSmooth', [0, -.63, 0], [.065, .08, .065], 'skin');
  depPart(leftArm, 'box', [0, -.63, -.04], [.05, .07, .03], 'skin');

  const rightArm = new THREE.Group();
  rightArm.position.set(.26, 1.34, 0);
  g.add(rightArm);

  depPart(rightArm, 'cylinder', [0, -.16, 0], [.08, .32, .08], 'khaki');
  depPart(rightArm, 'cylinder', [0, -.30, 0], [.088, .04, .088], 'khaki');
  depPart(rightArm, 'cylinder', [0, -.46, 0], [.065, .30, .065], 'skin');
  depPart(rightArm, 'sphereSmooth', [0, -.63, 0], [.065, .08, .065], 'skin');

  let baseRightArmRotX = 0;

  // Equipment & Post Specific Gear
  if(mode === 'binocular'){
    leftArm.rotation.set(Math.PI/3.2, 0, Math.PI/6);
    rightArm.rotation.set(Math.PI/3.2, 0, -Math.PI/6);
    baseRightArmRotX = Math.PI/3.2;

    depPart(g,'cylinder',[0,.68,-.45],[.04,1.36,.04],'dark');
    for(const rot of [0, 2.094, 4.188]){
      const leg = depPart(g,'cylinder',[Math.sin(rot)*.18, .35, -.45 + Math.cos(rot)*.18],[.03,.72,.03],'dark');
      leg.rotation.set(Math.cos(rot)*.35, 0, -Math.sin(rot)*.35);
    }
    depPart(g,'box',[0,1.44,-.42],[.3,.09,.18],'dark');
    for(const x of [-.09, .09]){
      const barrel = depPart(g,'cylinder',[x, 1.44, -.5],[.09,.36,.09],'dark');
      barrel.rotation.x = Math.PI/2;
      const lens = depPart(g,'cylinder',[x, 1.44, -.68],[.092,.02,.092],'blue');
      lens.rotation.x = Math.PI/2;
      const eyeP = depPart(g,'cylinder',[x, 1.44, -.32],[.06,.06,.06],'dark');
      eyeP.rotation.x = Math.PI/2;
    }
  }
  else if(mode === 'hhmd'){
    rightArm.rotation.set(Math.PI/3.6, 0, -Math.PI/12);
    baseRightArmRotX = Math.PI/3.6;

    // Realistic Handheld Metal Detector (Garrett SuperScanner style high-fidelity wand)
    const hhmd = new THREE.Group();
    hhmd.position.set(0, -.63, -.04);
    hhmd.rotation.set(Math.PI/4.2, 0, 0);
    rightArm.add(hhmd);

    // 1. Bottom Tail Cap & Brass Lanyard Loop Ring
    depPart(hhmd, 'cylinder', [0, -.16, 0], [.019, .024, .019], 'dark');
    depPart(hhmd, 'torus', [0, -.176, 0], [.011, .003, 1], 'yellow');
    const cord = depPart(hhmd, 'cylinder', [0, -.23, -.01], [.003, .10, .003], 'dark');
    cord.rotation.z = 0.15;

    // 2. Rubber Handle Grip (Ergonomic cylindrical core with 6 anti-slip knurled ribs)
    depPart(hhmd, 'cylinder', [0, -.07, 0], [.017, .15, .017], 'hhmdGrip');
    for(const ry of [-.135, -.115, -.095, -.075, -.055, -.035]){
      depPart(hhmd, 'cylinder', [0, ry, 0], [.019, .005, .019], 'dark');
    }

    // 3. Ergonomic Hand Stopper / Collar (Prevents hand slippage toward detector paddle)
    depPart(hhmd, 'cylinder', [0, .01, 0], [.024, .014, .024], 'dark');

    // 4. Officer's Hand Gripping the HHMD (Curled fingers & resting thumb)
    depPart(hhmd, 'rounded', [.016, -.025, .016], [.034, .08, .022], 'skin');
    depPart(hhmd, 'rounded', [-.020, .015, .018], [.020, .04, .020], 'skin');

    // 5. Control Module / Transition Housing
    depPart(hhmd, 'box', [0, .07, 0], [.066, .10, .036], 'hhmdBody');
    depPart(hhmd, 'rounded', [0, .03, 0], [.054, .035, .032], 'hhmdBody');

    // 6. Slide Power / Sensitivity Control Switch (Front thumb face)
    depPart(hhmd, 'box', [0, .045, .020], [.020, .042, .006], 'dark');
    depPart(hhmd, 'box', [0, .052, .024], [.014, .016, .006], 'hhmdSwitch');
    depPart(hhmd, 'box', [0, .032, .021], [.010, .003, .002], 'white');

    // 7. Perforated Audio Buzzer / Sound Emitter Grille
    const speaker = depPart(hhmd, 'cylinder', [0, .085, .019], [.015, .004, .015], 'hhmdSpeaker');
    speaker.rotation.x = Math.PI/2;
    const speakerCore = depPart(hhmd, 'cylinder', [0, .085, .021], [.007, .003, .007], 'dark');
    speakerCore.rotation.x = Math.PI/2;

    // 8. Tri-Color Status LED Cluster (Power Green, Batt Amber, Alarm Red)
    depPart(hhmd, 'box', [0, .112, .019], [.054, .014, .005], 'dark');
    depPart(hhmd, 'sphereSmooth', [-.018, .112, .022], [.006, .006, .006], 'hhmdLedGreen');
    depPart(hhmd, 'sphereSmooth', [0, .112, .022], [.0055, .0055, .0055], 'hhmdLedAmber');
    depPart(hhmd, 'sphereSmooth', [.018, .112, .022], [.006, .006, .006], 'hhmdLedRed');

    // 9. Scanning Paddle / Detection Blade with Decals & Safety Trims
    depPart(hhmd, 'box', [0, .26, 0], [.076, .26, .022], 'hhmdBody');
    depPart(hhmd, 'cylinder', [-.038, .26, 0], [.007, .26, .007], 'dark');
    depPart(hhmd, 'cylinder', [.038, .26, 0], [.007, .26, .007], 'dark');
    const tip = depPart(hhmd, 'cylinder', [0, .39, 0], [.038, .022, .011], 'dark');
    tip.rotation.z = Math.PI/2;

    // High-visibility yellow safety band across paddle top
    depPart(hhmd, 'box', [0, .365, 0], [.078, .024, .024], 'hhmdStripe');

    // High-contrast security scanner decals (Front & Back)
    depPart(hhmd, 'sign', [0, .255, .0115], [.068, .22, 1], depHhmdDecalFront);
    const decalBack = depPart(hhmd, 'sign', [0, .255, -.0115], [.068, .22, 1], depHhmdDecalFront);
    decalBack.rotation.y = Math.PI;
  }
  else if(mode === 'radio'){
    rightArm.rotation.set(-Math.PI/2.8, 0, -Math.PI/4.5);
    baseRightArmRotX = -Math.PI/2.8;

    const radioBody = depPart(rightArm,'box',[0,-.68,-.08],[.09,.17,.06],'dark');
    radioBody.rotation.set(-Math.PI/6, 0, 0);
    const ant = depPart(rightArm,'cylinder',[-.02,-.52,-.10],[.012,.22,.012],'dark');
    ant.rotation.set(-Math.PI/6, 0, 0);
    depPart(rightArm,'cylinder',[.02,-.58,-.09],[.018,.04,.018],'yellow');
    const screen = depPart(rightArm,'box',[0,-.66,-.05],[.06,.06,.01],'yellow');
    screen.rotation.set(-Math.PI/6, 0, 0);
    depPart(rightArm,'box',[-.045,-.68,-.08],[.015,.04,.03],'red');
  }
  else {
    const lathi = depPart(rightArm,'cylinder',[0,-.72,.06],[.028,.85,.028],'lathi');
    lathi.rotation.set(0.18, 0, 0);
    depPart(rightArm,'cylinder',[0,-.30,.14],[.032,.05,.032],'yellow');
    depPart(rightArm,'cylinder',[0,-1.14,-.02],[.032,.06,.032],'dark');
    depPart(rightArm,'torus',[0,-.62,.06],[.04,.008,1],'dark');
  }

  g.userData.rig = {
    leftLeg,
    rightLeg,
    leftArm,
    rightArm,
    torsoGroup,
    headGroup,
    baseRightArmRotX,
    walkPhase: 0,
    isMoving: false,
    jumpVy: 0,
    isJumping: false
  };
}

function depBuild(){
  depGroup.clear();depButtons.forEach(o=>o.e.remove());depButtons=[];depNodes=[];
  const list=depUI('list');
  if(list){
    list.replaceChildren();
    const blank=document.createElement('option');blank.value='';blank.textContent='Select officer / equipment';list.appendChild(blank);
  }

  // Sort items according to Duty Place (duty name / location), then by item name
  const sortedByDuty = [...depItems].sort((a, b) => {
    const da = (a.duty || '').trim() || 'General / Unassigned Duty';
    const db = (b.duty || '').trim() || 'General / Unassigned Duty';
    if (da.startsWith('General') && !db.startsWith('General')) return 1;
    if (!da.startsWith('General') && db.startsWith('General')) return -1;
    const cmp = da.localeCompare(db, undefined, { sensitivity: 'base', numeric: true });
    if (cmp !== 0) return cmp;
    return (a.name || '').localeCompare(b.name || '', undefined, { numeric: true });
  });

  // Populate TOP bar dropdown next to camera perspectives (Grouped & Sorted by Duty Place)
  const topList=root.querySelector('#dep-top-list');
  if(topList){
    topList.replaceChildren();
    const topBlank=document.createElement('option');
    topBlank.value='';
    topBlank.textContent=`👮 All Deployed Posts (${depItems.length})`;
    topList.appendChild(topBlank);

    const byDuty={};
    for(const item of depItems){
      const d = (item.duty || '').trim() || 'General / Unassigned Duty';
      (byDuty[d] = byDuty[d] || []).push(item);
    }

    const sortedDuties = Object.keys(byDuty).sort((a, b) => {
      if (a.startsWith('General')) return 1;
      if (b.startsWith('General')) return -1;
      return a.localeCompare(b, undefined, { sensitivity: 'base', numeric: true });
    });

    for(const d of sortedDuties){
      const items = byDuty[d];
      items.sort((a, b) => (a.name || '').localeCompare(b.name || '', undefined, { numeric: true }));
      const group=document.createElement('optgroup');
      group.label=`📍 ${d} (${items.length})`;
      for(const item of items){
        const opt=document.createElement('option');
        opt.value=item.id;
        opt.textContent=`📍 ${d} — ${depSymbols[item.kind]||'👮'} ${item.name}${item.belt ? ' ('+item.belt+')' : ''}`;
        group.appendChild(opt);
      }
      topList.appendChild(group);
    }
    topList.value=depSelected||'';
    const badge=root.querySelector('#dep-count-badge');
    if(badge)badge.textContent=depItems.length;
  }

  if(list){
    for(const item of sortedByDuty){
      const o=document.createElement('option');
      o.value=item.id;
      o.textContent=(depSymbols[item.kind]+' '+(item.duty ? item.duty+' — ' : '')+item.name).slice(0,100);
      list.appendChild(o);
    }
  }

  for(const item of depItems){
    const g=new THREE.Group();g.position.set(item.x,item.y,item.z);g.rotation.y=-item.angle*Math.PI/180;g.userData.depId=item.id;depGroup.add(g);
    if(item.kind==='officer' || item.kind==='hhmd' || item.kind==='binocular' || item.kind==='radio'){
      depBuildOfficer(g, item.kind);
    }
    else if(item.kind==='barricade'){
      for(const x of [-1.25,1.25]){depPart(g,'box',[x,.6,0],[.12,1.2,.15],'dark');depPart(g,'box',[x,.06,0],[.2,.12,.9],'dark');}
      depPart(g,'box',[0,.88,0],[3,.66,.12],'yellow');
      for(let x=-1.3;x<1.4;x+=.4){const stripe=depPart(g,'box',[x,.88,-.071],[.15,.62,.018],'dark');stripe.rotation.z=-.3;}
      const board=new THREE.Mesh(depBoardGeometry,depPoliceSign);board.position.set(0,.88,-.09);board.rotation.y=Math.PI;g.add(board);
      const back=board.clone();back.rotation.y=0;back.position.z=.09;g.add(back);
    }
    else if(item.kind==='dfmd'){
      for(const x of [-.6,.6])depPart(g,'box',[x,1.12,0],[.18,2.24,.45],'blue');
      depPart(g,'box',[0,2.22,0],[1.38,.18,.45],'blue');depPart(g,'box',[.6,1.7,-.24],[.1,.2,.03],'yellow');
    }
    else if(item.kind==='cone'){
      const cone=new THREE.Mesh(depConeGeometry,depMaterials.red);cone.position.y=.4;g.add(cone);depPart(g,'box',[0,.05,0],[.55,.1,.55],'dark');
    }
    else{
      depPart(g,'cylinder',[0,1.3,0],[.045,2.6,.045],'dark');depPart(g,'box',[0,2.6,-.15],[.45,.25,.45],item.kind==='light'?'yellow':'white');
    }
    depNodes.push({item,g});
    const b=document.createElement('button');b.type='button';b.className='btn dep-marker';b.textContent=depSymbols[item.kind];
    b.setAttribute('aria-label',item.name+' · '+item.duty);
    b.addEventListener('pointerdown',e=>{e.stopPropagation();e.stopImmediatePropagation();});
    b.addEventListener('click',e=>{
      e.stopPropagation();
      e.stopImmediatePropagation();
      if(typeof suppressClick!=='undefined')suppressClick=true;
      b.blur();
      if(document.activeElement && document.activeElement.blur) document.activeElement.blur();
      if(canvas && canvas.focus) canvas.focus();
      depChoose(item.id, true);
    });
    labelRoot.appendChild(b);depButtons.push({e:b,item});
  }
  if(list)list.value=depSelected||'';
  if(topList)topList.value=depSelected||'';
  depUI('editor').hidden=!depSelected;
  depUpdate();draw();
}

function depUpdate(){
  if(!depReady)return;
  updateTabLock();
  depRefreshOcclusion();
  // NO CIRCLE on ground
  if(depLocation) depLocation.visible=false;
  
  // Information Tab (depPeek) is only visible when an item is selected (CLICKED)
  const peekItem=depItems.find(o=>o.id===depSelected);
  depPeek.hidden=!peekItem;
  if(peekItem){
    const titleEl=depPeekHead.querySelector('#dep-peek-title');
    const badgeEl=depPeekHead.querySelector('#dep-peek-duty-badge');
    if(titleEl) titleEl.textContent=(depSymbols[peekItem.kind]||'')+' '+peekItem.name;
    const isOfficerLike = ['officer','hhmd','binocular','radio'].includes(peekItem.kind);
    if(badgeEl){
      badgeEl.textContent=peekItem.duty||(isOfficerLike?'Security post':'Access control');
      badgeEl.title=peekItem.duty||'';
    }
    for(const [k,field] of Object.entries(depPeekFields)){
      if(document.activeElement!==field)field.value=peekItem[k];
      field.disabled=(k==='belt'||k==='mobile')&&!isOfficerLike;
      field.parentElement.hidden=field.disabled;
    }
    for(const b of depPeekActions.querySelectorAll('button')){
      if(b.textContent.includes('First')){ b.disabled=!isOfficerLike; b.hidden=b.disabled; }
      else if(b.textContent.includes('Third')){ b.disabled=false; b.hidden=false; }
    }
  }

  const r=host.getBoundingClientRect();
  depGroup.visible=current!=='alignment';
  for(const {item,g} of depNodes)g.visible=!(depCamera==='first'&&item.id===depSelected);
  
  for(const {e,item} of depButtons){
    const isOfficerLike = ['officer','hhmd','binocular','radio'].includes(item.kind);
    const headHeight = isOfficerLike ? 2.15 : (item.kind==='dfmd'?2.3:1.6);
    const v = new THREE.Vector3(item.x, item.y + headHeight, item.z);
    const distance = camera.position.distanceTo(v);
    const p = v.project(camera);
    
    const isVisible = depGroup.visible && !depOccCache.get(item.id) && p.z >= -1 && p.z <= 1 && Math.abs(p.x) <= 0.98 && Math.abs(p.y) <= 0.98 && !(depCamera && item.id===depSelected);
    e.style.display = isVisible ? 'block' : 'none';
    if (!isVisible) continue;
    
    e.style.pointerEvents = depPlace ? 'none' : 'auto';
    
    // Scale smoothly based on distance, compact size (0.7 to 1.0)
    const distScale = THREE.MathUtils.clamp(30 / Math.max(22, distance), 0.7, 1.0);
    const isHigh = (item.id === depSelected);
    const finalScale = Math.round((distScale * (isHigh ? 1.25 : 1.0)) * 100) / 100;
    
    // Exact screen anchor positioned directly above the 3D model
    const px = (p.x + 1) * r.width / 2;
    const py = (1 - p.y) * r.height / 2;
    
    e.style.left = px + 'px';
    e.style.top = py + 'px';
    e.style.transform = `translate(-50%, -100%) scale(${finalScale})`;
    e.textContent = depSymbols[item.kind];
    e.setAttribute('aria-pressed', String(item.id === depSelected));
  }
  
  // Position Info Tab above clicked marker (or docked when in third/first person view)
  if(peekItem){
    const icon=depButtons.find(o=>o.item.id===peekItem.id)?.e;
    if(depCamera){
      const r=host.getBoundingClientRect();
      const w=depPeek.offsetWidth||260;
      depPeek.style.left=Math.max(8, r.width - w - 16)+'px';
      depPeek.style.top='56px';
    }
    else if(!icon||icon.style.display==='none')depPeek.hidden=true;
    else{
      const px=parseFloat(icon.style.left),py=parseFloat(icon.style.top);
      const w=depPeek.offsetWidth||260,h=depPeek.offsetHeight||(depPeekIsMinimized?42:260);
      depPeek.style.left=THREE.MathUtils.clamp(px-w/2,8,Math.max(8,r.width-w-8))+'px';
      let topPos=py-h-14;
      if(topPos<8) topPos=py+30;
      depPeek.style.top=THREE.MathUtils.clamp(topPos,8,Math.max(8,r.height-h-8))+'px';
    }
  }
}

function depChoose(id, zoom = true){
  depSelected=depItems.some(o=>o.id===id)?id:null;depHover=null;depPlace=false;
  if(depTooltip) depTooltip.style.display='none';
  const list=depUI('list'), topList=root.querySelector('#dep-top-list');
  if(list)list.value=depSelected||'';
  if(topList)topList.value=depSelected||'';
  depUI('editor').hidden=!depSelected;
  setDepPeekMinimized(true); // By default open in minimized state!
  updateTabLock();
  const o=depItems.find(o=>o.id===depSelected);
  if(!o){
    updateOfficerHud(null);
    return;
  }
  if (!depIsCycling) {
    depTabChain = [o.id];
    depTabChainIndex = 0;
  }
  depUI('editkind').value=o.kind;
  for(const k of ['name','duty','belt','mobile','x','y','z','angle'])depUI(k).value=typeof o[k]==='number'?Math.round(o[k]*100)/100:o[k];
  const isOfficerLike = ['officer','hhmd','binocular','radio'].includes(o.kind);
  for(const k of ['belt','mobile','first']) depUI(k).disabled=!isOfficerLike;
  depUI('third').disabled = false;

  updateOfficerHud(o);
  depUI('status').textContent='🎮 Controlling ' + (depSymbols[o.kind] || '') + ' ' + o.name + ' · Move: W/S/↑/↓ · Rotate: A/D/←/→/Q/E · Jump: SPACE · Next: TAB · Deselect: CAPSLOCK';

  if(zoom){
    depView('third', true);
  }
  depUpdate();draw();
}

depUI('list').addEventListener('change',()=>{
  const val = depUI('list').value;
  if (!val) {
    depDeselect(true);
  } else {
    depChoose(val, true);
  }
  depUI('list').blur();
  if(canvas && canvas.focus) canvas.focus();
});

// TOP bar dropdown sync
const depTopSelect=root.querySelector('#dep-top-list');
if(depTopSelect){
  depTopSelect.addEventListener('change',()=>{
    const id=depTopSelect.value;
    if(!id) {
      depDeselect(true);
      return;
    }
    depChoose(id, true);
    depTopSelect.blur();
    if(canvas && canvas.focus) canvas.focus();
  });
}

depUI('form').addEventListener('submit',e=>{
  e.preventDefault();const o=depItems.find(o=>o.id===depSelected);if(!o)return;
  const next={...o,kind:depUI('editkind').value};
  for(const k of ['name','duty','belt','mobile'])next[k]=depUI(k).value.trim();
  for(const k of ['x','y','z','angle'])next[k]=Number(depUI(k).value);
  if(!depValid([next])){depUI('status').textContent='Check coordinates and height (0–100 m).';return;}
  Object.assign(o,next);depStore();depBuild();depChoose(o.id);
  if(depCamera)depView(depCamera);
});
depUI('form').addEventListener('change',()=>{if(depUI('form').checkValidity())depUI('form').requestSubmit();});
if(depUI('name')) depUI('name').addEventListener('input', () => {
  const o = depItems.find(x => x.id === depSelected);
  if (o) { o.name = depUI('name').value; depSyncDropdownLabels(o); }
});
if(depUI('duty')) depUI('duty').addEventListener('input', () => {
  const o = depItems.find(x => x.id === depSelected);
  if (o) { o.duty = depUI('duty').value; depSyncDropdownLabels(o); }
});

function depRotate(delta){
  const o=depItems.find(o=>o.id===depSelected);if(!o)return;
  o.angle=(o.angle+delta+360)%360;
  depStore();depBuild();depChoose(o.id);
  if(depCamera)depView(depCamera);
}
depUI('left').onclick=()=>depRotate(-30);depUI('right').onclick=()=>depRotate(30);

depUI('add').onclick=()=>{
  if(depItems.length>=500){depUI('status').textContent='Maximum 500 items per plan.';return;}
  depReturnView();const kind=depUI('kind').value,id='item-'+Date.now()+'-'+Math.random().toString(36).slice(2,6);
  const count=depItems.filter(o=>o.kind===kind).length+1;
  const name = kind === 'officer' ? `Officer ${count}`
    : kind === 'hhmd' ? `HHMD Officer ${count}`
    : kind === 'binocular' ? `Spotter Officer ${count}`
    : kind === 'radio' ? `Radio Officer ${count}`
    : `${kind.toUpperCase()} #${count}`;
  const duty = kind === 'officer' ? 'Security post'
    : kind === 'hhmd' ? 'Main gate — DFMD / HHMD'
    : kind === 'binocular' ? 'Binocular duty — rooftop'
    : kind === 'radio' ? 'Control & wireless duty'
    : '';
  depItems.push({id,kind,name,duty,belt:'',mobile:'',x:controls.target.x,y:.3,z:controls.target.z,angle:0});
  depSelected=id;depNew=id;depBuild();depChoose(id);depPlace=true;depUpdate();
  depUI('status').textContent='Click the model surface to place the new '+kind+'. Esc cancels.';
};
depUI('move').onclick=()=>{
  if(!depSelected){depUI('status').textContent='Select an item first.';return;}
  depReturnView();depPlace=true;depUpdate();
  depUI('status').textContent='Click a ground / roof surface to move this item (or use W/A/S/D keys).';
};
depUI('delete').onclick=()=>{
  if(!depSelected)return;
  depReturnView();depItems=depItems.filter(o=>o.id!==depSelected);
  depSelected=null;depPlace=false;depStore();depBuild();
};

function depView(mode, smooth = true){
  const o=depItems.find(o=>o.id===depSelected);if(!o)return;
  if(!depReturn)depReturn={p:camera.position.clone(),t:controls.target.clone(),view:select.value};
  const hq=geo.footprints.find(f=>f.id==='hall').points;let inside=false;
  for(let i=0,j=hq.length-1;i<hq.length;j=i++){const a=hq[i],b=hq[j];if(((a[1]>o.z)!==(b[1]>o.z))&&(o.x<(b[0]-a[0])*(o.z-a[1])/(b[1]-a[1])+a[0]))inside=!inside;}
  if(inside&&o.y<8){select.value='hall';applyView();}else if(current==='alignment'){select.value='campus';applyView();}
  depCamera=mode;
  const isOfficerLike = ['officer','hhmd','binocular','radio'].includes(o.kind);
  const itemHeight = isOfficerLike ? 1.65
    : o.kind === 'dfmd' ? 1.8
    : o.kind === 'cctv' || o.kind === 'light' ? 2.2
    : o.kind === 'barricade' ? 0.9
    : 0.6;
  const distBehind = isOfficerLike ? 3.8
    : ['barricade','dfmd'].includes(o.kind) ? 4.5
    : 3.2;
  const heightAbove = isOfficerLike ? 1.2 : 1.5;

  const angle=o.angle*Math.PI/180,dir=new THREE.Vector3(Math.sin(angle),0,-Math.cos(angle)),eye=new THREE.Vector3(o.x,o.y+itemHeight,o.z);
  const idealCam = mode==='first' ? eye : eye.clone().addScaledVector(dir,-distBehind).add(new THREE.Vector3(0,heightAbove,0));
  const targetLook = eye.clone().addScaledVector(dir,mode==='first'?10:2.0);

  let targetCam = idealCam;
  if (mode !== 'first') {
    const camRayVec = idealCam.clone().sub(eye);
    const maxDist = camRayVec.length();
    const camRayDir = camRayVec.clone().normalize();
    const springRay = new THREE.Raycaster(eye, camRayDir, 0.1, maxDist);
    const occluderMeshes = (typeof clickable !== 'undefined' ? clickable : []).filter(m => m.visible && m.parent.visible && m !== depGroup);
    const hits = springRay.intersectObjects(occluderMeshes, false);
    if (hits.length > 0) {
      targetCam = eye.clone().addScaledVector(camRayDir, Math.max(0.65, hits[0].distance - 0.28));
    }
  }
  if(smooth && typeof moveTo === 'function'){
    moveTo(targetCam, targetLook);
  } else {
    motion=null;
    camera.position.copy(targetCam);
    controls.target.copy(targetLook);
    controls.update();
  }
  depUpdate();draw();
  depUI('status').textContent=(depSymbols[o.kind]||'')+' '+o.name+' · '+(mode==='first'?'First':'Third')+' person follow (Press ESC to return)';
}

function depReturnView(smooth = true){
  depCamera = null;
  updateOfficerHud(null);

  let destPos, destTarget, destView = 'campus';
  if (depReturn) {
    destPos = depReturn.p.clone();
    destTarget = depReturn.t.clone();
    destView = depReturn.view || 'campus';
    depReturn = null;
  } else {
    destPos = new THREE.Vector3(135, 135, 157);
    destTarget = new THREE.Vector3(-20, 0, 0);
  }

  if (typeof select !== 'undefined') select.value = destView;
  if (typeof root !== 'undefined') root.dataset.view = destView;
  if (typeof groups !== 'undefined') {
    const internal = ['hall', 'stage'].includes(destView);
    const cut = ['cutaway', 'plan', 'lounge', 'stageplan'].includes(destView);
    for (const g of Object.values(groups)) g.visible = destView !== 'alignment';
    if (groups.roof) groups.roof.visible = !cut;
    if (groups.ceiling) groups.ceiling.visible = internal;
    if (groups.shell) groups.shell.visible = !cut;
    if (groups.event) groups.event.visible = typeof eventInput !== 'undefined' ? eventInput.checked : true;
    if (groups.context) groups.context.visible = typeof contextInput !== 'undefined' ? contextInput.checked : false;
    if (groups.lotusInterior) groups.lotusInterior.visible = destView === 'lotusinside';
    if (groups.snapshot) groups.snapshot.visible = typeof snapshotInput !== 'undefined' ? snapshotInput.checked : false;
  }
  if (typeof setLighting === 'function') setLighting();

  if (smooth && typeof moveTo === 'function') {
    moveTo(destPos, destTarget);
  } else {
    motion = null;
    camera.position.copy(destPos);
    controls.target.copy(destTarget);
    controls.update();
  }

  depUpdate();
  draw();
  depUI('status').textContent = 'Returned to overview.';
}

function depDeselect(smooth = true){
  depSelected = null;
  depHover = null;
  depPlace = false;
  if (depNew) {
    depItems = depItems.filter(x => x.id !== depNew);
    depNew = null;
    depStore();
    depBuild();
  }
  if (depCandidate) {
    depCandidate = null;
    if (depConfirm) depConfirm.hidden = true;
  }
  if (depRadial) depRadial.style.display = 'none';
  if (depPeek) depPeek.hidden = true;
  const editor = depUI('editor');
  if (editor) editor.hidden = true;
  const list = depUI('list');
  if (list) list.value = '';
  const topList = root.querySelector('#dep-top-list');
  if (topList) topList.value = '';
  if (depTooltip) depTooltip.style.display = 'none';

  updateOfficerHud(null);
  updateTabLock();

  depTabChain = [];
  depTabChainIndex = -1;

  for (const k in depKeysDown) {
    depKeysDown[k] = false;
  }

  depReturnView(smooth);
}
window.__DEP_DESELECT = depDeselect;

let depTabChain = [];
let depTabChainIndex = -1;
let depIsCycling = false;

function depCycleNearestItem(reverse = false) {
  if (!depItems || depItems.length === 0) {
    depUI('status').textContent = 'No deployed items to cycle. Deploy items from panel.';
    return;
  }

  const validItems = depItems.filter(o => o && typeof o.x === 'number' && typeof o.z === 'number');
  if (validItems.length === 0) return;

  if (validItems.length === 1) {
    depIsCycling = true;
    depChoose(validItems[0].id, true);
    depIsCycling = false;
    depTabChain = [validItems[0].id];
    depTabChainIndex = 0;
    return;
  }

  if (!depSelected) {
    const target = (typeof controls !== 'undefined' && controls && controls.target) 
      ? controls.target 
      : new THREE.Vector3(0, 0, 0);
    let best = validItems[0], bestDist = Infinity;
    for (const it of validItems) {
      const d = Math.hypot(it.x - target.x, (it.y || 0) - target.y, it.z - target.z);
      if (d < bestDist) {
        bestDist = d;
        best = it;
      }
    }
    depTabChain = [best.id];
    depTabChainIndex = 0;
    depIsCycling = true;
    depChoose(best.id, true);
    depIsCycling = false;
    return;
  }

  const currentItem = validItems.find(x => x.id === depSelected);
  if (!currentItem) {
    depTabChain = [validItems[0].id];
    depTabChainIndex = 0;
    depIsCycling = true;
    depChoose(validItems[0].id, true);
    depIsCycling = false;
    return;
  }

  const validIds = new Set(validItems.map(o => o.id));
  depTabChain = depTabChain.filter(id => validIds.has(id));

  const matchesChain = depTabChain.length > 0 && 
    depTabChainIndex >= 0 && 
    depTabChainIndex < depTabChain.length && 
    depTabChain[depTabChainIndex] === currentItem.id;

  if (!matchesChain) {
    depTabChain = [currentItem.id];
    depTabChainIndex = 0;
  }

  if (reverse) {
    if (depTabChain.length > 1) {
      depTabChainIndex = (depTabChainIndex - 1 + depTabChain.length) % depTabChain.length;
      depIsCycling = true;
      depChoose(depTabChain[depTabChainIndex], true);
      depIsCycling = false;
      return;
    }
  }

  const visitedSet = new Set(depTabChain);
  const unvisited = validItems.filter(it => !visitedSet.has(it.id));

  if (unvisited.length > 0) {
    let nearest = unvisited[0], minDist = Infinity;
    for (const it of unvisited) {
      const d = Math.hypot(it.x - currentItem.x, (it.y || 0) - (currentItem.y || 0), it.z - currentItem.z);
      if (d < minDist) {
        minDist = d;
        nearest = it;
      }
    }
    depTabChain.push(nearest.id);
    depTabChainIndex = depTabChain.length - 1;
    depIsCycling = true;
    depChoose(nearest.id, true);
    depIsCycling = false;
  } else {
    depTabChainIndex = (depTabChainIndex + 1) % depTabChain.length;
    depIsCycling = true;
    depChoose(depTabChain[depTabChainIndex], true);
    depIsCycling = false;
  }
}
window.__DEP_CYCLE_NEAREST = depCycleNearestItem;
depUI('first').onclick=()=>depView('first', true);depUI('third').onclick=()=>depView('third', true);depUI('return').onclick=()=>depReturnView(true);

// Contextual Click-to-Deploy Menu
const depRadial=root.querySelector('#dep-radial-deploy'), depRadialClose=root.querySelector('#dep-radial-close');
if(depRadial){
  for(const evt of ['pointerdown','pointerup','pointermove','mousedown','mouseup','mousemove','click','dblclick','contextmenu']){
    depRadial.addEventListener(evt, e => e.stopPropagation());
  }
  depRadial.addEventListener('wheel', e => e.stopPropagation(), { passive: true });
}
if(depRadialClose){
  depRadialClose.addEventListener('pointerdown', e => e.stopPropagation());
  depRadialClose.addEventListener('click', e => {
    e.preventDefault();
    e.stopPropagation();
    if(depRadial) depRadial.style.display = 'none';
    updateTabLock();
  });
}

root.querySelectorAll('.deploy-item-btn').forEach(btn=>{
  btn.addEventListener('pointerdown', e => e.stopPropagation());
  btn.addEventListener('click',e=>{
    e.preventDefault();
    e.stopPropagation();
    if(!depClickPoint)return;
    const kind=btn.dataset.kind;
    const count=depItems.filter(o=>o.kind===kind).length+1;
    const id='post-'+Date.now().toString(36)+'-'+Math.random().toString(36).slice(2,5);
    const name = kind === 'officer' ? `Officer ${count}`
      : kind === 'hhmd' ? `HHMD Officer ${count}`
      : kind === 'binocular' ? `Spotter Officer ${count}`
      : kind === 'radio' ? `Radio Officer ${count}`
      : `${kind.toUpperCase()} #${count}`;
    const duty = kind === 'officer' ? 'Security post'
      : kind === 'hhmd' ? 'Main gate — DFMD / HHMD'
      : kind === 'binocular' ? 'Binocular duty — rooftop'
      : kind === 'radio' ? 'Control & wireless duty'
      : 'Access control';
    const newItem={
      id,
      kind,
      name,
      duty,
      belt:'',
      mobile:'',
      x:Math.round(depClickPoint.x*100)/100,
      y:Math.max(0.3,Math.round((depClickPoint.y+0.03)*100)/100),
      z:Math.round(depClickPoint.z*100)/100,
      angle:0
    };
    depItems.push(newItem);
    if(depRadial)depRadial.style.display='none';
    depStore();
    depBuild();
    setDepPeekMinimized(true);
    depChoose(id, true);
    depUI('status').textContent=`✅ Deployed ${name}! (Position: ${newItem.x}, ${newItem.z}) — Keys: W/S/A/D to move, Q/E to rotate.`;
  });
});

// Top bar quick deploy button
const depTopQuickDeploy=root.querySelector('#dep-top-quick-deploy');
if(depTopQuickDeploy){
  depTopQuickDeploy.addEventListener('click',e=>{
    e.stopPropagation();
    if(depRadial){
      if(depRadial.style.display==='block'){
        depRadial.style.display='none';
      }else{
        const r=canvas.getBoundingClientRect();
        depClickPoint=controls.target.clone();
        depClickPoint.y=0.3;
        depRadial.style.display='block';
        depRadial.style.left=Math.round((r.width-260)/2)+'px';
        depRadial.style.top='54px';
        depUI('status').textContent='Click item below to deploy, or click anywhere on the 3D map:';
      }
    }
  });
}

function getSurfaceHeight(x, z, currentY = 0) {
  const startY = Math.max(currentY + 3.0, 15);
  const rayOrigin = new THREE.Vector3(x, startY, z);
  const ray = new THREE.Raycaster(rayOrigin, new THREE.Vector3(0, -1, 0), 0.05, 50);
  const targets = (typeof clickable !== 'undefined' ? clickable : []).filter(m => m.visible && m.parent.visible && m !== depGroup);
  const hits = ray.intersectObjects(targets, false);
  for (const h of hits) {
    if (h.face && h.face.normal && h.face.normal.y > 0.25) {
      return h.point.y;
    }
  }
  return 0.3; // Default ground plane level
}

const depKeysDown = {};
let depOfficerJump = {
  vy: 0,
  isJumping: false,
  gravity: 16.0,
  jumpStrength: 5.6
};

function triggerOfficerJump(o) {
  const groundUnder = getSurfaceHeight(o.x, o.z, o.y);
  // Only jump when on or close to ground (prevents mid-air multi-jump while falling from heights)
  if (!depOfficerJump.isJumping && (Math.abs(o.y - groundUnder) <= 0.22 || o.y <= groundUnder)) {
    depOfficerJump.vy = depOfficerJump.jumpStrength;
    depOfficerJump.isJumping = true;
    o.y += 0.08;
    depUI('status').textContent = '🦘 ' + (depSymbols[o.kind] || '') + ' ' + o.name + ' jumped!';
    if (typeof draw === 'function') draw();
  }
}

let lastDepStoreTime = 0;

window.__DEP_TICK = function(dt) {
  let needsDraw = false;

  // Handle item walking/moving, turning, climbing stairs, jumping & obstacle collision
  if (depSelected) {
    const o = depItems.find(x => x.id === depSelected);
    if (o) {
      const node = depNodes.find(n => n.item.id === o.id);
      const rig = node?.g?.userData?.rig;
      
      // ROTATION:
      // Turn left: A, ArrowLeft, or Q
      // Turn right: D, ArrowRight, or E
      const turnLeft = !!(depKeysDown['a'] || depKeysDown['arrowleft'] || depKeysDown['q']);
      const turnRight = !!(depKeysDown['d'] || depKeysDown['arrowright'] || depKeysDown['e']);
      const turnSpeed = 95; // degrees per second
      if (turnLeft && !turnRight) {
        o.angle = (o.angle - turnSpeed * dt + 360) % 360;
        needsDraw = true;
      } else if (turnRight && !turnLeft) {
        o.angle = (o.angle + turnSpeed * dt) % 360;
        needsDraw = true;
      }

      // MOVEMENT:
      // Forward: W or ArrowUp
      // Backward: S or ArrowDown
      const moveFwd = !!(depKeysDown['w'] || depKeysDown['arrowup']);
      const moveBack = !!(depKeysDown['s'] || depKeysDown['arrowdown']);
      const rad = o.angle * Math.PI / 180;
      const fwd = new THREE.Vector3(Math.sin(rad), 0, -Math.cos(rad));
      let moveSpeed = 0;
      const isShift = !!depKeysDown['shift'];
      if (moveFwd && !moveBack) moveSpeed += (isShift ? 6.2 : 3.8);
      if (moveBack && !moveFwd) moveSpeed -= (isShift ? 3.8 : 2.4);

      const isMoving = Math.abs(moveSpeed) > 0.01;

      // Natural Gravity Falling Physics & Ground Snapping
      const groundUnder = getSurfaceHeight(o.x, o.z, o.y);
      const isFallingFree = !depOfficerJump.isJumping && o.y > groundUnder + 0.12;

      // If item walked off a high terrace/roof/stage, start free fall under gravity:
      if (isFallingFree) {
        depOfficerJump.isJumping = true;
        depOfficerJump.vy = 0;
      }

      if (depOfficerJump.isJumping) {
        o.y += depOfficerJump.vy * dt;
        depOfficerJump.vy -= depOfficerJump.gravity * dt;
        // Landing check: only land when moving downward (vy <= 0) and reaching ground
        if (depOfficerJump.vy <= 0 && o.y <= groundUnder) {
          o.y = groundUnder;
          depOfficerJump.vy = 0;
          depOfficerJump.isJumping = false;
        }
        needsDraw = true;
      } else {
        const groundDecay = 1 - Math.exp(-18 * dt);
        o.y = THREE.MathUtils.lerp(o.y, groundUnder, groundDecay);
      }

      if (isMoving) {
        const nextX = o.x + fwd.x * moveSpeed * dt;
        const nextZ = o.z + fwd.z * moveSpeed * dt;
        const surfaceNext = getSurfaceHeight(nextX, nextZ, o.y);
        const heightDiff = surfaceNext - o.y;

        // Forward chest-height raycast to prevent tunneling through thin walls / partitions:
        const chestY = o.y + 0.8;
        const fwdDir = fwd.clone().normalize();
        const fwdCaster = new THREE.Raycaster(new THREE.Vector3(o.x, chestY, o.z), fwdDir, 0.05, 0.5);
        const occluderMeshes = (typeof clickable !== 'undefined' ? clickable : []).filter(m => m.visible && m.parent.visible && m !== depGroup);
        const wallHits = fwdCaster.intersectObjects(occluderMeshes, false);
        const wallBlocked = wallHits.length > 0 && Math.abs(wallHits[0].face.normal.y) < 0.4;

        if (wallBlocked && (!depOfficerJump.isJumping || o.y < surfaceNext - 0.2)) {
          depUI('status').textContent = '⚠️ Blocked by obstacle / wall! Press SPACE to jump over.';
        } else if (heightDiff <= 0.45) {
          // Normal stair step, curb or ground ramp: climb on top smoothly!
          o.x = nextX;
          o.z = nextZ;
          if (!depOfficerJump.isJumping) {
            const stepDecay = 1 - Math.exp(-22 * dt);
            o.y = THREE.MathUtils.lerp(o.y, surfaceNext, stepDecay);
          }
          needsDraw = true;
        } else {
          // High obstacle or wall in front: can only pass if jumping high enough!
          if (depOfficerJump.isJumping && o.y >= surfaceNext - 0.2) {
            o.x = nextX;
            o.z = nextZ;
            needsDraw = true;
          } else {
            depUI('status').textContent = '⚠️ Obstacle ahead! Press SPACE to jump over.';
          }
        }

        // Throttle auto-save position when walking
        const now = Date.now();
        if (now - lastDepStoreTime > 1500) {
          lastDepStoreTime = now;
          depStore();
        }
      }

      // Update 3D node position & rotation
      if (node && node.g) {
        node.g.position.set(o.x, o.y, o.z);
        node.g.rotation.y = -o.angle * Math.PI / 180;
      }

      // Animate officer limbs (Legs & Arms walking cycle)
      if (rig) {
        if (isMoving) {
          rig.walkPhase += dt * (Math.abs(moveSpeed) * 3.0);
          const swing = Math.sin(rig.walkPhase);
          rig.leftLeg.rotation.x = swing * 0.55;
          rig.rightLeg.rotation.x = -swing * 0.55;
          rig.leftArm.rotation.x = -swing * 0.45;
          if (o.kind === 'officer') {
            rig.rightArm.rotation.x = swing * 0.45;
          } else {
            rig.rightArm.rotation.x = rig.baseRightArmRotX + Math.sin(rig.walkPhase * 2) * 0.05;
          }
          rig.torsoGroup.position.y = 0.88 + Math.abs(Math.sin(rig.walkPhase * 2)) * 0.035;
          rig.torsoGroup.rotation.z = Math.sin(rig.walkPhase) * 0.025;
          needsDraw = true;
        } else if (depOfficerJump.isJumping) {
          const jumpPoseDecay = 1 - Math.exp(-14 * dt);
          rig.leftLeg.rotation.x = THREE.MathUtils.lerp(rig.leftLeg.rotation.x, 0.4, jumpPoseDecay);
          rig.rightLeg.rotation.x = THREE.MathUtils.lerp(rig.rightLeg.rotation.x, 0.3, jumpPoseDecay);
          rig.leftArm.rotation.x = THREE.MathUtils.lerp(rig.leftArm.rotation.x, -0.4, jumpPoseDecay);
          needsDraw = true;
        } else {
          // Idle rest pose with smooth exponential decay
          const idleDecay = 1 - Math.exp(-14 * dt);
          rig.leftLeg.rotation.x = THREE.MathUtils.lerp(rig.leftLeg.rotation.x, 0, idleDecay);
          rig.rightLeg.rotation.x = THREE.MathUtils.lerp(rig.rightLeg.rotation.x, 0, idleDecay);
          rig.leftArm.rotation.x = THREE.MathUtils.lerp(rig.leftArm.rotation.x, 0, idleDecay);
          if (o.kind === 'officer') rig.rightArm.rotation.x = THREE.MathUtils.lerp(rig.rightArm.rotation.x, 0, idleDecay);
          rig.torsoGroup.position.y = THREE.MathUtils.lerp(rig.torsoGroup.position.y, 0.88, idleDecay);
          rig.torsoGroup.rotation.z = THREE.MathUtils.lerp(rig.torsoGroup.rotation.z, 0, idleDecay);
        }
      }

      // Smooth Third-Person Camera Follow behind the moving item with Spring-Arm
      if (depCamera === 'third') {
        if (typeof motion !== 'undefined' && motion && (isMoving || turnLeft || turnRight || depOfficerJump.isJumping)) {
          motion = null; // instantly cancel any lingering moveTo lerp when user operates controls!
        }
        const angle = o.angle * Math.PI / 180;
        const dir = new THREE.Vector3(Math.sin(angle), 0, -Math.cos(angle));
        const isOfficerLike = ['officer','hhmd','binocular','radio'].includes(o.kind);
        const itemHeight = isOfficerLike ? 1.65
          : o.kind === 'dfmd' ? 1.8
          : o.kind === 'cctv' || o.kind === 'light' ? 2.2
          : o.kind === 'barricade' ? 0.9
          : 0.6;
        const distBehind = isOfficerLike ? 3.8
          : ['barricade','dfmd'].includes(o.kind) ? 4.5
          : 3.2;
        const heightAbove = isOfficerLike ? 1.2 : 1.5;

        const eye = new THREE.Vector3(o.x, o.y + itemHeight, o.z);
        const idealCam = eye.clone().addScaledVector(dir, -distBehind).add(new THREE.Vector3(0, heightAbove, 0));
        const targetLook = eye.clone().addScaledVector(dir, 2.0);

        // Spring-arm camera obstacle avoidance
        const camRayVec = idealCam.clone().sub(eye);
        const maxDist = camRayVec.length();
        const camRayDir = camRayVec.clone().normalize();
        const springRay = new THREE.Raycaster(eye, camRayDir, 0.1, maxDist);
        const occluderMeshes = (typeof clickable !== 'undefined' ? clickable : []).filter(m => m.visible && m.parent.visible && m !== depGroup);
        const hits = springRay.intersectObjects(occluderMeshes, false);
        let targetCam = idealCam;
        if (hits.length > 0) {
          targetCam = eye.clone().addScaledVector(camRayDir, Math.max(0.65, hits[0].distance - 0.28));
        }

        const camDecay = 1 - Math.exp(-14 * dt);
        camera.position.lerp(targetCam, camDecay);
        controls.target.lerp(targetLook, camDecay);
        needsDraw = true;
      }
    }
  }

  return needsDraw;
};

let depCandidate=null;
const depLocation=new THREE.Mesh(new THREE.RingGeometry(.3,.55,32),new THREE.MeshBasicMaterial({color:0x0284c7,side:THREE.DoubleSide,depthTest:true,depthWrite:false}));
depLocation.rotation.x=-Math.PI/2;depLocation.renderOrder=999;
depLocation.visible=false; // Keep circle hidden
scene.add(depLocation);

const depConfirm=document.createElement('div');depConfirm.className='dep-confirm';depConfirm.hidden=true;host.appendChild(depConfirm);
for(const [text,accept] of [['Place here',true],['Cancel',false]]){
  const b=document.createElement('button');b.type='button';b.className='btn btn-sm '+(accept?'btn-primary':'btn-secondary');b.textContent=text;
  b.onclick=()=>{
    if(accept&&depCandidate){
      const o=depItems.find(o=>o.id===depCandidate.id);
      if(o){
        o.x=depCandidate.point.x;
        o.y=getSurfaceHeight(depCandidate.point.x, depCandidate.point.z, depCandidate.point.y);
        o.z=depCandidate.point.z;
        depPlace=false;depNew=null;depStore();depBuild();depChoose(o.id);
      }
    }
    depCandidate=null;depConfirm.hidden=true;
  };
  depConfirm.appendChild(b);
}

// Keyboard controls:
window.addEventListener('keydown', e => {
  if (e.ctrlKey || e.metaKey || e.altKey) return;
  if (e.target.closest?.('input,textarea,select,[contenteditable="true"]')) return;
  const key = e.key.toLowerCase();
  depKeysDown[key] = true;

  // Spacebar: Jump active officer / equipment!
  if (key === ' ' || key === 'spacebar' || e.code === 'Space') {
    if (depSelected) {
      const o = depItems.find(o => o.id === depSelected);
      if (o) {
        e.preventDefault();
        e.stopPropagation();
        triggerOfficerJump(o);
        return;
      }
    }
  }

  // CapsLock: Deselect currently selected item and return camera from 3rd-person to overview
  if (key === 'capslock' || e.code === 'CapsLock') {
    e.preventDefault();
    depDeselect(true);
    return;
  }

  // Tab / Shift+Tab: Cycle to next nearest deployed item
  if (key === 'tab' || e.code === 'Tab') {
    e.preventDefault();
    e.stopPropagation();
    if (e.target && typeof e.target.blur === 'function' && !e.target.matches('input,textarea')) {
      e.target.blur();
    }
    depCycleNearestItem(e.shiftKey);
    return;
  }

  // Escape: Exit first/third person view, cancel placement, close radial menu, or deselect
  if (key === 'escape' || e.code === 'Escape') {
    e.preventDefault();
    if (depRadial && depRadial.style.display === 'block') {
      depRadial.style.display = 'none';
      updateTabLock();
      return;
    }
    if (depPanelEl && depPanelEl.classList.contains('show')) {
      depPanelEl.classList.remove('show');
      if (depPanelToggle) depPanelToggle.classList.remove('active');
    }
    depDeselect(true);
    return;
  }

  // Check if an item is currently selected
  const activeItem = depSelected ? depItems.find(o => o.id === depSelected) : null;

  // If item is selected, prevent arrow keys and WASD/QE from triggering page scroll or camera pan
  if (activeItem) {
    if (['arrowup', 'arrowdown', 'arrowleft', 'arrowright', 'w', 'a', 's', 'd', 'q', 'e'].includes(key)) {
      e.preventDefault();
      return;
    }
  }

  // Camera Controls (Only when NO item is selected and NOT in third-person view)
  if (!activeItem && depCamera !== 'third') {
    const v = window.__CAM_VELOCITY;
    if (v) {
      const mult = e.shiftKey ? 1.8 : 1.0;
      const dist = camera.position.distanceTo(controls.target);
      const panSpeed = (e.shiftKey ? 1.8 : 0.9) * Math.max(0.4, dist * 0.018);
      let handled = false;

      if (key === 'a') { v.panRight -= panSpeed; handled = true; }
      else if (key === 'd') { v.panRight += panSpeed; handled = true; }
      else if (key === 'w') { v.panForward += panSpeed; handled = true; }
      else if (key === 's') { v.panForward -= panSpeed; handled = true; }

      // Q, E: Horizontal turntable rotate
      if (key === 'q') { v.theta -= 0.045 * mult; handled = true; }
      else if (key === 'e') { v.theta += 0.045 * mult; handled = true; }

      // Z, X: Camera elevation angle (tilt up/down)
      else if (key === 'z') { v.phi -= 0.035 * mult; handled = true; }
      else if (key === 'x') { v.phi += 0.035 * mult; handled = true; }

      // K: Zoom in, L: Zoom out
      else if (key === 'k') { v.zoom -= 0.045 * mult; handled = true; }
      else if (key === 'l') { v.zoom += 0.045 * mult; handled = true; }

      if (handled) {
        e.preventDefault();
        return;
      }
    }
  }
});

window.addEventListener('keyup', e => {
  const key = e.key.toLowerCase();
  depKeysDown[key] = false;
  if (key === ' ' || key === 'spacebar' || e.code === 'Space') {
    depKeysDown[' '] = false;
    depKeysDown['spacebar'] = false;
  }
});

window.addEventListener('blur', () => {
  for (const k in depKeysDown) {
    depKeysDown[k] = false;
  }
});

function depHit(e){
  const r=canvas.getBoundingClientRect(),raycaster=new THREE.Raycaster();
  raycaster.setFromCamera(new THREE.Vector2((e.clientX-r.left)/r.width*2-1,1-(e.clientY-r.top)/r.height*2),camera);
  let hit=raycaster.intersectObject(depGroup,true).find(h=>h.object.visible&&h.object.parent.visible);
  if(!hit)return null;
  let object=hit.object;while(object&&!object.userData.depId)object=object.parent;
  const id=object?.userData.depId;
  return depOccCache.get(id)?null:id;
}

let depRightDown = null;
canvas.addEventListener('pointerdown', e => {
  if (isAnyTabOpen()) {
    e.stopPropagation();
    return;
  }
  if (e.button === 2) {
    depRightDown = [e.clientX, e.clientY];
  }
});

// Canvas Click handler: Left-click selects existing item or dismisses popups
canvas.addEventListener('pointerup',e=>{
  if(e.button !== 0) return;

  // If ANY tab is open and user clicks on canvas, close all open tabs cleanly without reacting:
  if(isAnyTabOpen()){
    e.stopImmediatePropagation();
    if(typeof suppressClick!=='undefined')suppressClick=true;
    if(depPanelEl && depPanelEl.classList.contains('show')){
      depPanelEl.classList.remove('show');
      if(depPanelToggle) depPanelToggle.classList.remove('active');
    }
    if(depRadial) depRadial.style.display='none';
    if(depSelected){
      depDeselect(true);
      return;
    }
    updateTabLock();
    depUpdate();
    draw();
    return;
  }

  if(selection||!down||Math.hypot(e.clientX-down[0],e.clientY-down[1])>5)return;
  
  // 1. Did the user click an existing item?
  const id=depHit(e);
  if(id){
    e.stopImmediatePropagation();
    if(typeof suppressClick!=='undefined')suppressClick=true;
    if(depRadial)depRadial.style.display='none';
    depChoose(id, true);
    return;
  }
  
  // 2. If user is in manual reposition/move mode:
  if(depPlace){
    const o=depItems.find(o=>o.id===depSelected);if(!o)return;
    const r=canvas.getBoundingClientRect(),rcast=new THREE.Raycaster();
    rcast.setFromCamera(new THREE.Vector2((e.clientX-r.left)/r.width*2-1,1-(e.clientY-r.top)/r.height*2),camera);
    scene.updateMatrixWorld(true);
    const hit=rcast.intersectObjects(clickable.filter(m=>m.visible&&m.parent.visible),false)[0];
    if(hit&&hit.face.normal.y>.4){
      e.stopImmediatePropagation();
      depCandidate={id:o.id,point:hit.point.clone()};
      depConfirm.hidden=false;
      depConfirm.style.left=THREE.MathUtils.clamp(e.clientX-r.left,8,r.width-180)+'px';
      depConfirm.style.top=THREE.MathUtils.clamp(e.clientY-r.top,8,r.height-90)+'px';
      depUI('status').textContent='Confirm Place here (or use W/A/S/D)';
      depUpdate();draw();
      return;
    }
  }

  // Left click on empty space: close deploy popup if open (NEVER open deploy on left-click)
  if(depRadial) depRadial.style.display='none';
},{capture:true});

// RIGHT-CLICK: Open "Choose Item to Deploy" popup on 3D Model / Ground
canvas.addEventListener('contextmenu', e => {
  e.preventDefault();
  e.stopPropagation();

  // If user was right-click dragging/panning the camera (> 5px), ignore
  if (depRightDown && Math.hypot(e.clientX - depRightDown[0], e.clientY - depRightDown[1]) > 5) {
    return;
  }

  const r = canvas.getBoundingClientRect();
  const rcast = new THREE.Raycaster();
  rcast.setFromCamera(new THREE.Vector2((e.clientX - r.left) / r.width * 2 - 1, 1 - (e.clientY - r.top) / r.height * 2), camera);
  scene.updateMatrixWorld(true);

  let targetPoint = null;
  const hits = rcast.intersectObjects(clickable.filter(m => m.visible && m.parent && m.parent.visible), false);
  if (hits.length > 0) {
    targetPoint = hits[0].point.clone();
  } else {
    const groundPlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
    const gPoint = new THREE.Vector3();
    if (rcast.ray.intersectPlane(groundPlane, gPoint)) {
      if (Math.abs(gPoint.x) < 400 && Math.abs(gPoint.z) < 400) {
        targetPoint = gPoint.clone();
      }
    }
  }

  if (targetPoint) {
    depClickPoint = targetPoint;
    if (depRadial) {
      depRadial.style.display = 'block';
      const menuW = 260, menuH = 210;
      const left = THREE.MathUtils.clamp(e.clientX - r.left - menuW / 2, 10, Math.max(10, r.width - menuW - 10));
      let top = e.clientY - r.top - menuH - 12;
      if (top < 10) top = Math.min(Math.max(10, r.height - menuH - 10), e.clientY - r.top + 14);
      depRadial.style.left = left + 'px';
      depRadial.style.top = top + 'px';
      updateTabLock();
    }
    depUI('status').textContent = `📍 Target: (${Math.round(targetPoint.x * 10) / 10}, ${Math.round(targetPoint.z * 10) / 10}). Choose item to deploy:`;
    draw();
  }
});

depUI('export').onclick=()=>{
  const payload={version:1,coordinateFrame:'WGS84 local metres: east X, up Y, south Z',origin:[geo.originLongitude,geo.originLatitude],status:'Draft — user editable, not approved duty order',items:depItems},url=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{type:'application/json'})),a=document.createElement('a');
  a.href=url;a.download='gyan-mansarovar-deployment.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
};
depUI('import').onchange=async e=>{
  const file=e.target.files[0];if(!file)return;
  try{
    if(file.size>1000000)throw Error('File exceeds 1 MB');
    const plan=JSON.parse(await file.text());
    if(plan.version!==1||!depValid(plan.items)||!Array.isArray(plan.origin)||Math.abs(plan.origin[0]-geo.originLongitude)>1e-6||Math.abs(plan.origin[1]-geo.originLatitude)>1e-6)throw Error('Invalid plan or different map origin');
    depReturnView();depItems=plan.items;depSelected=null;depStore();depBuild();
  }catch(err){depUI('status').textContent='Import failed: '+err.message;}
  e.target.value='';
};

depReady=true;depBuild();

let depRevision=0,depBackendReady=false,depPending=null,depSaving=false,depSaveTimer=null;
const depPanel=root.querySelector('#gms-deployment'),
depBackendURL=location.protocol.startsWith('http')&&['127.0.0.1','localhost'].includes(location.hostname)?'/api/deployment':null;

function depPayload(){
  const sanitized = JSON.parse(JSON.stringify(depItems));
  for (const item of sanitized) {
    item.x = Math.max(-4900, Math.min(4900, Math.round((Number(item.x) || 0) * 100) / 100));
    item.z = Math.max(-4900, Math.min(4900, Math.round((Number(item.z) || 0) * 100) / 100));
    item.y = Math.max(0, Math.min(99, Math.round((Number(item.y) || 0) * 100) / 100));
    item.angle = Math.round(((((Number(item.angle) || 0) % 360) + 360) % 360) * 100) / 100;
  }
  return {
    version:1,
    origin:[geo.originLongitude,geo.originLatitude],
    coordinateFrame:'WGS84 local metres: east X, up Y, south Z',
    status:'Draft — user editable duty order',
    items:sanitized
  };
}

function depQueue(){
  if(!depBackendURL)return;
  depPending=depPayload();
  if(depUI('sync'))depUI('sync').textContent='Backend: auto-saving…';
  clearTimeout(depSaveTimer);
  depSaveTimer=setTimeout(depFlush,50);
}

async function depFlush(){
  if(depSaving||!depPending||!depBackendURL)return;
  depSaving=true;
  const snapshot=depPending;
  depPending=null;
  try{
    const r=await fetch(depBackendURL,{
      method:'PUT',
      headers:{'Content-Type':'application/json','X-GMS-Plan':'1'},
      body:JSON.stringify({revision:depRevision,plan:snapshot})
    });
    if(r.status===409){
      const conf=await r.json();
      if(typeof conf.revision==='number'){
        depRevision=conf.revision;
        depPending=snapshot;
        depSaving=false;
        depFlush();
        return;
      }
    }
    const result=await r.json();
    if(!r.ok)throw Error(result.error||'Save failed');
    depRevision=result.revision;
    depBackendReady=true;
    if(depUI('retry'))depUI('retry').hidden=true;
    if(depUI('sync')){
      const timeStr=new Date(result.updated||Date.now()).toLocaleTimeString();
      depUI('sync').textContent=`✅ Auto-saved to Database · rev ${depRevision} · ${timeStr}`;
    }
  }catch(e){
    depPending=depPending||snapshot;
    if(depUI('sync'))depUI('sync').textContent='Auto-saved locally (Backend offline: '+e.message+')';
    if(depUI('retry'))depUI('retry').hidden=false;
  }finally{
    depSaving=false;
    if(depPending)depFlush();
  }
}

async function depLoadBackend(){
  const local=depLoadLocal();
  if(!depBackendURL){
    if(local&&depValid(local.items)){
      depItems=local.items;
      depBuild();
    }
    if(depUI('sync')){
      depUI('sync').textContent='✅ Auto-saved in browser storage ('+depItems.length+' items)';
      depUI('retry').hidden=true;
    }
    return;
  }

  depPanel.inert=true;
  try{
    const r=await fetch(depBackendURL,{cache:'no-store'});
    if(!r.ok)throw Error('Backend HTTP '+r.status);
    const result=await r.json();
    depRevision=result.revision||0;
    depBackendReady=true;

    const backendPlan=result.plan;
    const backendItems=backendPlan&&Array.isArray(backendPlan.items)&&depValid(backendPlan.items)?backendPlan.items:null;
    const backendTime=result.updated?new Date(result.updated).getTime():0;
    const localTime=local?(local.savedAt||0):0;

    // Smart sync: determine whether local storage or backend is newer
    if(local&&local.items&&localTime>backendTime+2000){
      depItems=local.items;
      depBuild();
      depStore();
      if(depUI('sync'))depUI('sync').textContent=`✅ Auto-saved · restored ${depItems.length} items & synced to DB`;
    }else if(backendItems){
      depItems=backendItems;
      depBuild();
      try{localStorage.setItem(depStorage,JSON.stringify({version:1,savedAt:Date.now(),origin:[geo.originLongitude,geo.originLatitude],items:depItems}));}catch(e){}
      if(depUI('sync'))depUI('sync').textContent=`✅ Auto-saved · loaded ${depItems.length} items from DB (rev ${depRevision})`;
    }else if(local&&local.items){
      depItems=local.items;
      depBuild();
      depStore();
    }else{
      depItems=depSeed();
      depBuild();
      depStore();
    }
    if(depUI('retry'))depUI('retry').hidden=true;
  }catch(e){
    console.warn('Backend load failed, using local storage:',e);
    if(local&&depValid(local.items)){
      depItems=local.items;
      depBuild();
    }
    if(depUI('sync')){
      depUI('sync').textContent='✅ Auto-saved in browser ('+depItems.length+' items, backend offline)';
      depUI('retry').hidden=false;
    }
  }finally{
    depPanel.inert=false;
  }
}

function depSaveBeforeLeave(){
  try{
    localStorage.setItem(depStorage,JSON.stringify({version:1,savedAt:Date.now(),origin:[geo.originLongitude,geo.originLatitude],items:depItems}));
  }catch(e){}
  if(depBackendURL&&(depPending||depItems.length>0)){
    const payload=depPayload();
    const body=JSON.stringify({revision:depRevision,plan:payload});
    try{
      fetch(depBackendURL,{
        method:'POST',
        headers:{'Content-Type':'application/json','X-GMS-Plan':'1'},
        body:body,
        keepalive:true
      });
    }catch(e){}
  }
}
window.addEventListener('beforeunload',depSaveBeforeLeave);
window.addEventListener('pagehide',depSaveBeforeLeave);

depUI('retry').onclick=()=>depBackendReady?depFlush():depLoadBackend();
depLoadBackend();
