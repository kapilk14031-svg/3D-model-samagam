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
function depRefreshOcclusion(){const stamp=performance.now(),signature=current+'|'+depItems.map(o=>[o.id,o.x,o.y,o.z].join(',')).join(';')+'|'+Object.entries(groups).map(([k,g])=>k+g.visible).join(',');
 if(signature===depOccSignature&&camera.matrixWorld.equals(depOccCamera))return;
 if(signature===depOccSignature&&stamp-depOccStamp<100){if(!depOccTimer)depOccTimer=setTimeout(()=>{depOccTimer=null;depOccStamp=0;depUpdate();draw();},105);return;}
 depOccSignature=signature;depOccCamera.copy(camera.matrixWorld);depOccStamp=stamp;depOccCache=new Map(depItems.map(o=>[o.id,depOccluded(o)]));
}

// Minimalist Hover Tooltip element (Only displays on cursor hover)
const depTooltip=root.querySelector('#dep-hover-tooltip');
let depHover=null,depHoverTimer=null;

const depPanelToggle = root.querySelector('#gms-dep-panel-toggle');
const depPanelEl = root.querySelector('#gms-deployment');
const depPanelClose = root.querySelector('#dep-panel-close-btn');

function isAnyTabOpen(){
  const radialOpen = depRadial && depRadial.style.display === 'block';
  const peekOpen = !!depSelected && !depPeek.hidden;
  const panelOpen = depPanelEl && depPanelEl.classList.contains('show');
  return !!(radialOpen || peekOpen || panelOpen);
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
depPeekHead.innerHTML='<div class="dep-peek-title-row"><span id="dep-peek-title" class="dep-peek-title">👮 Post Information</span><span id="dep-peek-duty-badge" class="dep-peek-duty-badge"></span></div><div class="dep-peek-controls"><button type="button" id="dep-peek-min" class="dep-peek-btn-icon" title="Maximize full details">+</button><button type="button" id="dep-peek-close" class="dep-peek-btn-icon" title="Close">✕</button></div>';

// Minimized Quick Action Bar
const depPeekMinBar=document.createElement('div');
depPeekMinBar.className='dep-peek-min-bar';
depPeekMinBar.innerHTML='<div class="dep-peek-quick-actions"><button type="button" id="dep-peek-min-left" class="btn-xs" title="Rotate left 30° (Q)">↺ -30°</button><button type="button" id="dep-peek-min-right" class="btn-xs" title="Rotate right 30° (E)">↻ +30°</button><button type="button" id="dep-peek-min-del" class="btn-xs btn-danger-soft" title="Delete post">🗑️</button></div><div class="dep-peek-keys-hint">⌨️ W/S/A/D move</div>';

const depPeekBody=document.createElement('div');
depPeekBody.className='dep-peek-body';
depPeekBody.style.display='none';

const depPeekText=document.createElement('div'),depPeekActions=document.createElement('div'),depPeekHint=document.createElement('div');
depPeekActions.className='viz-controls';
depPeekHint.className='dep-peek-hint';
depPeekHint.innerHTML='<span style="display:block;font-size:11px;color:#0284c7;font-weight:600;margin-top:6px;padding-top:4px;border-top:1px dashed #bae6fd;">⌨️ Keys: <b>W/S/A/D</b> to move · <b>Q/E</b> to rotate</span>';

depPeekBody.append(depPeekText,depPeekActions,depPeekHint);
depPeek.append(depPeekHead,depPeekMinBar,depPeekBody);
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
    depPeekMinBar.style.display='flex';
    depPeekBody.style.display='none';
  }else{
    depPeek.classList.remove('minimized');
    if(minBtn){minBtn.textContent='−';minBtn.title='Minimize';}
    depPeekMinBar.style.display='none';
    depPeekBody.style.display='block';
  }
  depUpdate();
}

const depPeekMinBtn = depPeekHead.querySelector('#dep-peek-min');
const depPeekCloseBtn = depPeekHead.querySelector('#dep-peek-close');

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

const depPeekMinLeft = depPeekMinBar.querySelector('#dep-peek-min-left');
const depPeekMinRight = depPeekMinBar.querySelector('#dep-peek-min-right');
const depPeekMinDel = depPeekMinBar.querySelector('#dep-peek-min-del');

if(depPeekMinLeft){
  depPeekMinLeft.addEventListener('pointerdown', e => e.stopPropagation());
  depPeekMinLeft.addEventListener('click', e => { e.stopPropagation(); depRotate(-30); });
}
if(depPeekMinRight){
  depPeekMinRight.addEventListener('pointerdown', e => e.stopPropagation());
  depPeekMinRight.addEventListener('click', e => { e.stopPropagation(); depRotate(30); });
}
if(depPeekMinDel){
  depPeekMinDel.addEventListener('pointerdown', e => e.stopPropagation());
  depPeekMinDel.addEventListener('click', e => {
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
  ['Close',()=>{depSelected=null;depPeek.hidden=true;if(depUI('editor'))depUI('editor').hidden=true;depUpdate();}]
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

const depMaterials={khaki:new THREE.MeshStandardMaterial({color:0x17365e}),dark:new THREE.MeshStandardMaterial({color:0x26323b}),yellow:new THREE.MeshStandardMaterial({color:0xf1bd26}),skin:new THREE.MeshStandardMaterial({color:0xc8956f}),red:new THREE.MeshStandardMaterial({color:0xd65524}),blue:new THREE.MeshStandardMaterial({color:0x245b89}),white:new THREE.MeshStandardMaterial({color:0xe9ede6})};
function depPart(g,shape,p,s,mat){const mesh=new THREE.Mesh(geos[shape],depMaterials[mat]);mesh.position.fromArray(p);mesh.scale.fromArray(s);mesh.castShadow=true;mesh.receiveShadow=true;g.add(mesh);return mesh;}
const depSignCanvas=document.createElement('canvas');depSignCanvas.width=512;depSignCanvas.height=128;const depSignCtx=depSignCanvas.getContext('2d');depSignCtx.fillStyle='#edbd2b';depSignCtx.fillRect(0,0,512,128);depSignCtx.fillStyle='#172837';depSignCtx.font='bold 82px sans-serif';depSignCtx.textAlign='center';depSignCtx.fillText('POLICE',256,93);const depPoliceSign=new THREE.MeshStandardMaterial({map:new THREE.CanvasTexture(depSignCanvas),side:THREE.FrontSide});
const depConeGeometry=new THREE.ConeGeometry(.22,.7,12),depBoardGeometry=new THREE.PlaneGeometry(1.4,.38);

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
    if(item.kind==='officer'){
      g.scale.setScalar(1);depPart(g,'rounded',[0,1.05,0],[.46,.6,.28],'khaki');depPart(g,'sphereSmooth',[0,1.58,0],[.16,.19,.16],'skin');depPart(g,'cylinder',[0,1.77,0],[.19,.09,.19],'dark');depPart(g,'sphereSmooth',[0,1.72,-.11],[.21,.025,.22],'dark');
      for(const x of [-.14,.14]){depPart(g,'cylinder',[x,.43,0],[.085,.62,.09],'khaki');depPart(g,'rounded',[x,.1,-.07],[.19,.18,.32],'dark');depPart(g,'cylinder',[x*2,1.04,0],[.065,.5,.065],'khaki');depPart(g,'sphereSmooth',[x*2,.76,0],[.065,.08,.065],'skin');depPart(g,'box',[x*2,1.32,0],[.12,.025,.14],'yellow');}
      depPart(g,'box',[0,.82,0],[.48,.07,.28],'dark');depPart(g,'box',[0,1.28,-.15],[.12,.07,.025],'yellow');
      for(const x of [-.06,.06])depPart(g,'sphereSmooth',[x,1.62,-.145],[.018,.018,.018],'dark');
      depPart(g,'box',[.3,.66,.03],[.035,.55,.035],'dark');
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
    else if(item.kind==='binocular'){
      depPart(g,'cylinder',[0,.65,0],[.04,1.3,.04],'dark');
      for(const x of [-.16,.16]){const b=depPart(g,'cylinder',[x,1.4,-.1],[.12,.44,.12],'dark');b.rotation.x=Math.PI/2;}
      depPart(g,'box',[0,1.4,0],[.35,.1,.2],'dark');
    }
    else if(item.kind==='cone'){
      const cone=new THREE.Mesh(depConeGeometry,depMaterials.red);cone.position.y=.4;g.add(cone);depPart(g,'box',[0,.05,0],[.55,.1,.55],'dark');
    }
    else if(item.kind==='hhmd'){
      depPart(g,'box',[0,.9,0],[.13,.35,.12],'dark');depPart(g,'box',[0,1.26,0],[.22,.42,.08],'blue');
    }
    else if(item.kind==='radio'){
      depPart(g,'box',[0,.65,0],[.22,.45,.14],'dark');depPart(g,'cylinder',[.08,1,0],[.018,.3,.018],'dark');
    }
    else{
      depPart(g,'cylinder',[0,1.3,0],[.045,2.6,.045],'dark');depPart(g,'box',[0,2.6,-.15],[.45,.25,.45],item.kind==='light'?'yellow':'white');
    }
    depNodes.push({item,g});
    const b=document.createElement('button');b.type='button';b.className='btn dep-marker';b.textContent=depSymbols[item.kind];
    b.setAttribute('aria-label',item.name+' · '+item.duty);
    b.addEventListener('pointerdown',e=>{e.stopPropagation();e.stopImmediatePropagation();});
    b.addEventListener('click',e=>{e.stopPropagation();e.stopImmediatePropagation();if(typeof suppressClick!=='undefined')suppressClick=true;depChoose(item.id, true);});
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
    if(badgeEl){
      badgeEl.textContent=peekItem.duty||(peekItem.kind==='officer'?'Security post':'Access control');
      badgeEl.title=peekItem.duty||'';
    }
    for(const [k,field] of Object.entries(depPeekFields)){
      if(document.activeElement!==field)field.value=peekItem[k];
      field.disabled=(k==='belt'||k==='mobile')&&peekItem.kind!=='officer';
      field.parentElement.hidden=field.disabled;
    }
    for(const b of depPeekActions.querySelectorAll('button'))if(b.textContent.includes('person')){b.disabled=peekItem.kind!=='officer';b.hidden=b.disabled;}
  }

  const r=host.getBoundingClientRect();
  depGroup.visible=current!=='alignment';
  for(const {item,g} of depNodes)g.visible=!(depCamera==='first'&&item.id===depSelected);
  
  const occupied=[];
  for(const {e,item} of [...depButtons].sort((a,b)=>(a.item.id===depSelected?-1:b.item.id===depSelected?1:0))){
    const v=new THREE.Vector3(item.x,item.y+(item.kind==='officer'?2.35:2.5),item.z),distance=camera.position.distanceTo(v),p=v.project(camera);
    e.style.display=(!depGroup.visible||depOccCache.get(item.id)||p.z< -1||p.z>1||Math.abs(p.x)>.96||Math.abs(p.y)>.95||(depCamera==='first'&&item.id===depSelected))?'none':'block';
    e.style.pointerEvents=depPlace?'none':'auto';
    
    // Keep icon compact: max scale 1.0 (at close zoom), scales gently down to 0.7 on zoom out
    const distScale=THREE.MathUtils.clamp(30/Math.max(22,distance),0.7,1.0);
    const isHigh=(item.id===depSelected);
    const finalScale=Math.round((distScale*(isHigh?1.25:1.0))*100)/100;
    e.style.transform=`translate(-50%, -50%) scale(${finalScale})`;
    
    const bw=Math.round(20*finalScale),bh=Math.round(18*finalScale);
    const baseX=(p.x+1)*r.width/2,baseY=(1-p.y)*r.height/2;let px=baseX,py=baseY;
    for(let attempt=0;attempt<(item.id===depSelected?0:35);attempt++){
      const box={x:px-bw/2,y:py-bh/2,w:bw,h:bh};
      if(!occupied.some(a=>box.x<a.x+a.w+2&&box.x+box.w+2>a.x&&box.y<a.y+a.h+2&&box.y+box.h+2>a.y)){
        if(e.style.display!=='none')occupied.push(box);break;
      }
      const ring=Math.floor(attempt/8)+1,theta=attempt*Math.PI/4;
      px=THREE.MathUtils.clamp(baseX+Math.cos(theta)*ring*16,bw/2,r.width-bw/2);
      py=THREE.MathUtils.clamp(baseY+Math.sin(theta)*ring*14,14,r.height-14);
    }
    if(item.id===depSelected)occupied.push({x:px-bw/2,y:py-bh/2,w:bw,h:bh});
    e.style.left=px+'px';e.style.top=py+'px';e.textContent=depSymbols[item.kind];e.setAttribute('aria-pressed',String(item.id===depSelected));
  }
  
  // Position Info Tab above clicked marker
  if(peekItem){
    const icon=depButtons.find(o=>o.item.id===peekItem.id)?.e;
    if(!icon||icon.style.display==='none')depPeek.hidden=true;
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
  if(!o)return;
  depUI('editkind').value=o.kind;
  for(const k of ['name','duty','belt','mobile','x','y','z','angle'])depUI(k).value=typeof o[k]==='number'?Math.round(o[k]*100)/100:o[k];
  for(const k of ['belt','mobile','first','third'])depUI(k).disabled=o.kind!=='officer';
  depUI('status').textContent=o.name+' · '+o.duty+(o.kind==='officer'?' · Belt: '+(o.belt||'—')+' · Mobile: '+(o.mobile||'—'):'')+' (W/S/A/D to move, Q/E to rotate)';

  if(zoom && depCamera!=='first'){
    const target=new THREE.Vector3(o.x,o.y+0.6,o.z);
    let offset=camera.position.clone().sub(controls.target);
    if(offset.lengthSq()<0.1) offset.set(10,8,10);
    offset.normalize().multiplyScalar(13);
    offset.y=Math.max(offset.y,4.5);
    moveTo(target.clone().add(offset), target);
  }
  depUpdate();draw();
}

depUI('list').addEventListener('change',()=>depChoose(depUI('list').value, true));

// TOP bar dropdown sync
const depTopSelect=root.querySelector('#dep-top-list');
if(depTopSelect){
  depTopSelect.addEventListener('change',()=>{
    const id=depTopSelect.value;
    if(!id)return;
    depChoose(id, true);
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
  depItems.push({id,kind,name:kind==='officer'?'New officer':kind.toUpperCase(),duty:'',belt:'',mobile:'',x:controls.target.x,y:.3,z:controls.target.z,angle:0});
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

function depView(mode){
  const o=depItems.find(o=>o.id===depSelected);if(!o||o.kind!=='officer')return;
  if(!depReturn)depReturn={p:camera.position.clone(),t:controls.target.clone(),view:select.value};
  const hq=geo.footprints.find(f=>f.id==='hall').points;let inside=false;
  for(let i=0,j=hq.length-1;i<hq.length;j=i++){const a=hq[i],b=hq[j];if(((a[1]>o.z)!==(b[1]>o.z))&&(o.x<(b[0]-a[0])*(o.z-a[1])/(b[1]-a[1])+a[0]))inside=!inside;}
  if(inside&&o.y<8){select.value='hall';applyView();}else if(current==='alignment'){select.value='campus';applyView();}
  depCamera=mode;motion=null;const angle=o.angle*Math.PI/180,dir=new THREE.Vector3(Math.sin(angle),0,-Math.cos(angle)),eye=new THREE.Vector3(o.x,o.y+1.65,o.z);
  camera.position.copy(mode==='first'?eye:eye.clone().addScaledVector(dir,-5).add(new THREE.Vector3(0,1.7,0)));
  controls.target.copy(eye.clone().addScaledVector(dir,mode==='first'?10:2));
  controls.update();depUpdate();draw();
  depUI('status').textContent=o.name+' · '+mode+' person view (Esc to return)';
}

function depReturnView(){
  if(depReturn){select.value=depReturn.view;applyView();camera.position.copy(depReturn.p);controls.target.copy(depReturn.t);controls.update();depReturn=null;}
  depCamera=null;depUpdate();draw();
}
depUI('first').onclick=()=>depView('first');depUI('third').onclick=()=>depView('third');depUI('return').onclick=depReturnView;

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
    const name=kind==='officer'?`Officer ${count}`:`${kind.toUpperCase()} #${count}`;
    const duty=kind==='officer'?'Security post':'Access control';
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
      if(o){o.x=depCandidate.point.x;o.y=Math.max(0,depCandidate.point.y+.03);o.z=depCandidate.point.z;depPlace=false;depNew=null;depStore();depBuild();depChoose(o.id);}
    }
    depCandidate=null;depConfirm.hidden=true;
  };
  depConfirm.appendChild(b);
}

// Keyboard controls:
// When an item IS selected: W,A,S,D move item, Q,E rotate item
// When NO item is selected: W,A,S,D drag/pan model, Q,E horizontal rotate model, Z,X vertical rotate model
window.addEventListener('keydown', e => {
  if (e.ctrlKey || e.metaKey || e.altKey || e.target.closest?.('input,textarea,select,[contenteditable="true"]')) return;
  const key = e.key.toLowerCase();

  // Escape: Close selection, radial menu, or panel
  if (key === 'escape') {
    if (depRadial) depRadial.style.display = 'none';
    if (depPanelEl && depPanelEl.classList.contains('show')) {
      depPanelEl.classList.remove('show');
      if (depPanelToggle) depPanelToggle.classList.remove('active');
    }
    depSelected = null;
    depPeek.hidden = true;
    if (depUI('editor')) depUI('editor').hidden = true;
    depUpdate();
    draw();
    return;
  }

  // 1. If an item IS selected -> WASD moves item, QE rotates item
  if (depSelected) {
    const o = depItems.find(o => o.id === depSelected);
    if (!o) return;
    const step = e.shiftKey ? 1.0 : 0.25;
    let moved = false;
    if (key === 'w') { o.z -= step; moved = true; }
    else if (key === 's') { o.z += step; moved = true; }
    else if (key === 'a') { o.x -= step; moved = true; }
    else if (key === 'd') { o.x += step; moved = true; }
    else if (key === 'q') { o.angle = (o.angle - 30 + 360) % 360; moved = true; }
    else if (key === 'e') { o.angle = (o.angle + 30 + 360) % 360; moved = true; }

    if (moved) {
      e.preventDefault();
      depStore();
      depBuild();
      depChoose(o.id, false); // Don't reset zoom while nudging
      if (depCamera) depView(depCamera);
    }
    return;
  }

  // 2. If NO item is selected -> W,A,S,D drag model, Q,E horizontal rotate, Z,X vertical rotate
  let modelChanged = false;
  const dist = camera.position.distanceTo(controls.target);
  const panStep = (e.shiftKey ? 4.5 : 1.8) * Math.max(0.6, dist * 0.025);

  if (['w', 's', 'a', 'd'].includes(key)) {
    // Camera-relative forward & right vectors on horizontal XZ plane
    const forward = new THREE.Vector3();
    camera.getWorldDirection(forward);
    forward.y = 0;
    forward.normalize();

    const right = new THREE.Vector3();
    right.crossVectors(forward, new THREE.Vector3(0, 1, 0)).normalize();

    const moveVec = new THREE.Vector3();
    if (key === 'w') moveVec.addScaledVector(forward, panStep);
    else if (key === 's') moveVec.addScaledVector(forward, -panStep);
    else if (key === 'a') moveVec.addScaledVector(right, -panStep);
    else if (key === 'd') moveVec.addScaledVector(right, panStep);

    camera.position.add(moveVec);
    controls.target.add(moveVec);
    modelChanged = true;
  } else if (key === 'q' || key === 'e') {
    // Q, E: Horizontal rotate around target (Azimuth / Yaw)
    const rotAngle = (key === 'q' ? 0.05 : -0.05) * (e.shiftKey ? 2.0 : 1.0);
    const offset = camera.position.clone().sub(controls.target);
    offset.applyAxisAngle(new THREE.Vector3(0, 1, 0), rotAngle);
    camera.position.copy(controls.target).add(offset);
    camera.lookAt(controls.target);
    modelChanged = true;
  } else if (key === 'z' || key === 'x') {
    // Z, X: Vertical rotate around target (Elevation / Pitch)
    const offset = camera.position.clone().sub(controls.target);
    const spherical = new THREE.Spherical();
    spherical.setFromVector3(offset);

    // Z: Vertical rotate up (tilt up / elevation higher)
    // X: Vertical rotate down (tilt down / horizon lower)
    const pitchDelta = (key === 'z' ? -0.045 : 0.045) * (e.shiftKey ? 2.0 : 1.0);
    spherical.phi = THREE.MathUtils.clamp(spherical.phi + pitchDelta, 0.08, Math.PI / 2 - 0.02);

    offset.setFromSpherical(spherical);
    camera.position.copy(controls.target).add(offset);
    camera.lookAt(controls.target);
    modelChanged = true;
  }

  if (modelChanged) {
    e.preventDefault();
    controls.update();
    draw();
    depUpdate();
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
      depSelected=null;
      depPeek.hidden=true;
      if(depUI('editor')) depUI('editor').hidden=true;
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
  return {
    version:1,
    origin:[geo.originLongitude,geo.originLatitude],
    coordinateFrame:'WGS84 local metres: east X, up Y, south Z',
    status:'Draft — user editable duty order',
    items:JSON.parse(JSON.stringify(depItems))
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
