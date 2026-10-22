var vvipSavedView = null;
var vvipHiddenHelicopterMatrices = [];
// User-authored draft deployment, independent of the registered venue geometry.







const depUI=id=>root.querySelector('#dep-'+id),depGroup=new THREE.Group();scene.add(depGroup);







const depDefaultDuties = [
  'Main gate — DFMD / HHMD',
  'Naka & barricade duty',
  'Helipad security & landing cordon',
  'Helipad approach road security',
  'Auditorium main stage duty',
  'Hall gate duty',
  'Auditorium seating duty',
  'VIP lounge duty',
  'VIP toilet duty',
  'VIP parking duty',
  'Binocular duty — rooftop',
  'Lotus duty',
  'Central lawn duty',
  'Inner cordon duty',
  'Outer perimeter duty',
  'Outer cordon duty',
  'Control & wireless duty',
  'Emergency Medical Response',
  'Fire & Safety Standby',
  'Queue & Crowd Management'
];
const dutyNames = depDefaultDuties;

let depCustomDuties = [];
try {
  const _savedCustom = localStorage.getItem('gyan-mansarovar-custom-duties');
  if (_savedCustom) depCustomDuties = JSON.parse(_savedCustom) || [];
} catch (e) { depCustomDuties = []; }

function depGetAllDuties() {
  const set = new Set(depDefaultDuties);
  if (Array.isArray(depCustomDuties)) {
    depCustomDuties.forEach(d => { if (d && typeof d === 'string' && d.trim()) set.add(d.trim()); });
  }
  if (typeof depItems !== 'undefined' && Array.isArray(depItems)) {
    depItems.forEach(item => {
      if (item && item.duty && typeof item.duty === 'string' && item.duty.trim()) {
        set.add(item.duty.trim());
      }
    });
  }
  return Array.from(set).sort((a, b) => a.localeCompare(b, undefined, { sensitivity: 'base', numeric: true }));
}
window.depGetAllDuties = depGetAllDuties;

function depRegisterCustomDuty(duty) {
  if (!duty || typeof duty !== 'string') return;
  const trimmed = duty.trim();
  if (!trimmed) return;
  if (!depCustomDuties.includes(trimmed)) {
    depCustomDuties.push(trimmed);
    try {
      localStorage.setItem('gyan-mansarovar-custom-duties', JSON.stringify(depCustomDuties));
    } catch (e) {}
  }
  depSyncDutyLists();
}
window.depRegisterCustomDuty = depRegisterCustomDuty;

function depSyncDutyLists() {
  const allDuties = depGetAllDuties();
  const datalist1 = typeof depUI === 'function' ? depUI('duties') : null;
  if (datalist1) {
    datalist1.replaceChildren();
    allDuties.forEach(text => {
      const opt = document.createElement('option');
      opt.value = text;
      datalist1.appendChild(opt);
    });
  }
  const datalist2 = document.getElementById('dep-dlg-duty-list');
  if (datalist2) {
    datalist2.replaceChildren();
    allDuties.forEach(text => {
      const opt = document.createElement('option');
      opt.value = text;
      datalist2.appendChild(opt);
    });
  }
}
window.depSyncDutyLists = depSyncDutyLists;

// Initial sync
setTimeout(depSyncDutyLists, 60);







const depSymbols={officer:'👮',_dummy:'👮',barricade:'🚧',binocular:'🔭',dfmd:'🚪',hhmd:'🔍',radio:'📻',cone:'⚠️',cctv:'📹',light:'💡',square_box:'📦',ambulance:'🚑',firebrigade:'🚒',qbelt:'🎗️',parking:'🅿️'};







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















function depGetAutoDuty(x, y, z, kind='officer'){
  if(kind==='ambulance') return 'Emergency Medical Response';
  if(kind==='firebrigade') return 'Fire & Safety Standby';
  if(kind==='qbelt') return 'Queue & Crowd Management';
  if(kind==='dfmd') return 'Main gate — DFMD / HHMD';
  if(kind==='parking') return 'Vehicle parking & police bus depot';
  if(kind==='square_box') return 'Security Sentry Booth';
  if(kind==='barricade'){
    if(z <= -64) return 'Road barricade — highway naka';
    return 'Campus security barricade';
  }

  // 1. Elevated observation posts / Rooftops
  if(y >= 6.5) return 'Binocular duty — rooftop';

  // 2. Helipad & Flight Corridor
  const distHelipad = Math.hypot(x - 6.39, z - (-308.2));
  if(distHelipad <= 42) return 'Helipad security & landing cordon';
  if(z <= -135) return 'Helipad approach road security';

  // 3. Vehicle Parking & Bus Fleet Depot
  if((x >= 55 && z <= -85 && z >= -145) || (x >= 80 && z <= -70 && z >= -145)) return 'VIP parking duty';

  // 4. Highway Naka & Outer Barricades
  if(z <= -66) return 'Naka & barricade duty';

  // 5. Main Gate & Entry Checkpoint
  if(z > -66 && z <= -54 && x >= -32 && x <= 5) return 'Main gate — DFMD / HHMD';

  // 6. Auditorium Complex
  if(x >= -58 && x <= -17 && z >= -58 && z <= 15){
    if(z >= 0 && z <= 15 && x >= -55 && x <= -20) return 'Auditorium main stage duty';
    if(x >= -24 && x <= -17 && z >= -8 && z <= 5) return 'Hall gate duty';
    if(x <= -48 && z >= 5) return 'VIP lounge duty';
    if(x <= -42 && z >= -14 && z <= -4) return 'VIP toilet duty';
    return 'Auditorium seating duty';
  }

  // 7. Lotus Meditation Temple
  if(Math.hypot(x - 27.0, z - (-53.1)) <= 24) return 'Lotus duty';

  // 8. Central Lawn & Garden
  if(Math.hypot(x - 27.6, z - (-11.2)) <= 25) return 'Central lawn duty';

  // 9. Dadi Prakashmani Residential Complex
  if(x >= -25 && x <= 25 && z >= 20 && z <= 48){
    if(x >= 12) return 'VIP toilet duty';
    return 'VIP lounge duty';
  }

  // 10. Outer Campus Boundary / Perimeter Walls
  if(x <= -55 || x >= 52 || z <= -68 || z >= 45) return 'Outer perimeter duty';

  // 11. Campus Corridors
  if(x >= -24 && x <= 5 && z >= -54 && z <= 15) return 'Inner cordon duty';

  return 'Outer cordon duty';
}

function depDeleteItemById(id) {
  if (!id) return;
  const item = depItems.find(x => x.id === id);
  const name = item ? item.name : 'Post';
  depItems = depItems.filter(x => x.id !== id);
  if (depSelected === id) {
    depSelected = null;
    depPeek.hidden = true;
    if (depUI('editor')) depUI('editor').hidden = true;
  }
  depStore();
  depBuild();
  draw();
  if (typeof depShowToast === 'function') {
    depShowToast(`🗑️ ${name} removed`);
  }
}
window.depDeleteItemById = depDeleteItemById;

function depDuplicateItemById(id) {
  if (!id) return;
  const cur = depItems.find(x => x.id === id);
  if (!cur) return;
  depSelected = id;
  depDuplicateSelectedItem();
}
window.depDuplicateItemById = depDuplicateItemById;

function depRebuildTopList() {
  const topList = root.querySelector('#dep-top-list');
  const customBtn = root.querySelector('#dep-top-custom-btn');
  const btnLabel = root.querySelector('#dep-top-btn-label');
  const menu = root.querySelector('#dep-top-menu');
  const badge = root.querySelector('#dep-count-badge');

  if (badge) badge.textContent = depItems.length;

  const currentId = (typeof depSelected !== 'undefined' && depSelected) ? depSelected : (topList ? topList.value : '');
  const selItem = depItems.find(o => o.id === currentId);

  // Update button label
  if (btnLabel) {
    if (selItem) {
      btnLabel.textContent = `${depSymbols[selItem.kind] || '👮'} ${selItem.name} · ${selItem.duty || 'Post'}`;
    } else {
      btnLabel.textContent = `👮 All Deployed Posts (${depItems.length})`;
    }
  }

  // 1. Sync hidden native <select> for compatibility
  if (topList) {
    topList.replaceChildren();
    const topBlank = document.createElement('option');
    topBlank.value = '';
    topBlank.textContent = `👮 All Deployed Posts (${depItems.length})`;
    topList.appendChild(topBlank);
  }

  // 2. Build grouped custom menu with +, ✏️, 🗑️ on each item
  const byDuty = {};
  for (const item of depItems) {
    const d = (item.duty || '').trim() || 'General / Unassigned Duty';
    (byDuty[d] = byDuty[d] || []).push(item);
  }

  const sortedDuties = Object.keys(byDuty).sort((a, b) => {
    if (a.startsWith('General')) return 1;
    if (b.startsWith('General')) return -1;
    return a.localeCompare(b, undefined, { sensitivity: 'base', numeric: true });
  });

  if (menu) {
    menu.replaceChildren();

    // Top 'All Deployed Posts' header
    const allHdr = document.createElement('div');
    allHdr.className = 'dep-menu-all-header';
    allHdr.innerHTML = `<span>👮 All Deployed Posts (${depItems.length})</span><span style="font-size:11px;color:#0284c7;font-weight:600;">Overview View ↩</span>`;
    allHdr.addEventListener('click', (e) => {
      e.stopPropagation();
      menu.style.display = 'none';
      if (customBtn) customBtn.setAttribute('aria-expanded', 'false');
      if (typeof depFreeCamera === 'function') depFreeCamera();
    });
    menu.appendChild(allHdr);

    for (const d of sortedDuties) {
      const items = byDuty[d];
      items.sort((a, b) => (a.name || '').localeCompare(b.name || '', undefined, { numeric: true }));

      // Optgroup header in native select
      let nativeGroup = null;
      if (topList) {
        nativeGroup = document.createElement('optgroup');
        nativeGroup.label = `📍 ${d} (${items.length})`;
        topList.appendChild(nativeGroup);
      }

      // Group header in custom menu
      const grpHdr = document.createElement('div');
      grpHdr.className = 'dep-menu-group-header';
      grpHdr.innerHTML = `<span>📍 ${d} (${items.length})</span>`;
      menu.appendChild(grpHdr);

      for (const item of items) {
        // Native option
        if (nativeGroup) {
          const opt = document.createElement('option');
          opt.value = item.id;
          opt.textContent = `📍 ${d} — ${depSymbols[item.kind]||'👮'} ${item.name}${item.belt ? ' ('+item.belt+')' : ''}`;
          nativeGroup.appendChild(opt);
        }

        // Custom interactive row with +, ✏️, 🗑️
        const row = document.createElement('div');
        row.className = 'dep-menu-item-row' + (currentId === item.id ? ' selected' : '');
        row.dataset.id = item.id;

        row.innerHTML = `
          <div class="dep-menu-item-info" title="Click to view & select ${item.name} on 3D map">
            <span style="font-size:14px;line-height:1;">${depSymbols[item.kind] || '👮'}</span>
            <span class="dep-menu-item-name">${item.name || 'Post'}</span>
            ${item.belt ? `<span class="dep-menu-item-belt">(${item.belt})</span>` : ''}
          </div>
          <div class="dep-menu-actions">
            <button type="button" class="dep-row-action-btn btn-add" data-id="${item.id}" title="Add another / Duplicate (एक और जोड़ें)">+</button>
            <button type="button" class="dep-row-action-btn btn-edit" data-id="${item.id}" title="Edit officer details (अधिकारी विवरण बदलें)">✏️</button>
            <button type="button" class="dep-row-action-btn btn-del" data-id="${item.id}" title="Delete post (हटाएं)">🗑️</button>
          </div>
        `;

        // Select item on row info click
        row.querySelector('.dep-menu-item-info').addEventListener('click', (e) => {
          e.stopPropagation();
          menu.style.display = 'none';
          if (customBtn) customBtn.setAttribute('aria-expanded', 'false');
          depChoose(item.id, true);
        });

        // + Action: Duplicate item
        row.querySelector('.btn-add').addEventListener('click', (e) => {
          e.preventDefault();
          e.stopPropagation();
          depDuplicateItemById(item.id);
        });

        // ✏️ Action: Open Minimalist Edit Dialog
        row.querySelector('.btn-edit').addEventListener('click', (e) => {
          e.preventDefault();
          e.stopPropagation();
          menu.style.display = 'none';
          if (customBtn) customBtn.setAttribute('aria-expanded', 'false');
          openOfficerDialog(item.id);
        });

        // 🗑️ Action: Delete item
        row.querySelector('.btn-del').addEventListener('click', (e) => {
          e.preventDefault();
          e.stopPropagation();
          depDeleteItemById(item.id);
        });

        menu.appendChild(row);
      }
    }
  }

  if (topList) topList.value = currentId || '';
}
window.depRebuildTopList = depRebuildTopList;

// Bind Custom Dropdown Toggle & Outside Click
function initCustomTopDropdown() {
  const customBtn = root.querySelector('#dep-top-custom-btn');
  const menu = root.querySelector('#dep-top-menu');
  const container = root.querySelector('#dep-top-dropdown-container');

  if (customBtn && menu) {
    customBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const isClosed = menu.style.display === 'none' || !menu.style.display;
      if (isClosed) {
        depRebuildTopList();
        menu.style.display = 'flex';
        customBtn.setAttribute('aria-expanded', 'true');
      } else {
        menu.style.display = 'none';
        customBtn.setAttribute('aria-expanded', 'false');
      }
    });

    document.addEventListener('click', (e) => {
      if (container && !container.contains(e.target)) {
        menu.style.display = 'none';
        if (customBtn) customBtn.setAttribute('aria-expanded', 'false');
      }
    });
  }
}
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initCustomTopDropdown);
} else {
  setTimeout(initCustomTopDropdown, 80);
}

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
  const dutyEl = depPeekHead.querySelector('#dep-peek-duty');
  if (dutyEl) dutyEl.textContent = item.duty || 'Unassigned';
  if (depSelected === item.id && depUI('duty') && document.activeElement !== depUI('duty')) {
    depUI('duty').value = item.duty || '';
  }
  depRebuildTopList();
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







depPeekHead.innerHTML='<div class="dep-peek-title-row" id="dep-peek-title-row" title="Click to edit details" style="cursor:pointer;"><span id="dep-peek-title" class="dep-peek-title" title="Click to edit officer details" style="cursor:pointer;">👮 Post Information</span><span id="dep-peek-duty-badge" class="dep-peek-duty-badge" title="Click to edit duty & details" style="cursor:pointer;"></span></div><div class="dep-peek-controls"><button type="button" id="dep-peek-edit" class="dep-peek-btn-icon" title="Edit details" style="color:#0284c7;font-size:13px;">✏️</button><button type="button" id="dep-peek-del" class="dep-peek-btn-icon btn-danger-soft" title="Delete post">🗑️</button><button type="button" id="dep-peek-min" class="dep-peek-btn-icon" title="Duplicate post">+</button><button type="button" id="dep-peek-close" class="dep-peek-btn-icon" title="Close">✕</button></div>';















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







    depDuplicateSelectedItem();







  });







}















function depFreeCamera() {
  if (document.activeElement && typeof document.activeElement.blur === 'function') {
    document.activeElement.blur();
  }
  // Free camera right where it is without returning to campus overview
  depCamera = null;
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
  if (typeof controls !== 'undefined' && controls) {
    controls.enabled = true;
    controls.update();
  }
  if (typeof renderer !== 'undefined' && renderer && renderer.domElement) {
    renderer.domElement.tabIndex = 0;
    renderer.domElement.focus();
  }
  window.focus();
  depUpdate();
  draw();
  if (depUI('status')) {
    depUI('status').textContent = '🎮 Free camera mode: Use W/A/S/D or Arrow keys to fly · Press CAPSLOCK to reset view.';
  }
}
window.depFreeCamera = depFreeCamera;

if(depPeekCloseBtn){







  depPeekCloseBtn.addEventListener('pointerdown', e => e.stopPropagation());







  depPeekCloseBtn.addEventListener('click', e => {
    e.preventDefault();
    e.stopPropagation();
    depFreeCamera();
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







  ['Close',()=>depFreeCamera()]







]){







  const b=document.createElement('button');b.type='button';b.className='btn';b.textContent=text;







  b.addEventListener('click',e=>{e.stopPropagation();fn();});







  depPeekActions.appendChild(b);







}















const depInitialPlan = (typeof window !== 'undefined' && window.__DEP_INITIAL_PLAN__) ? window.__DEP_INITIAL_PLAN__ : null;
const depTypes=Object.keys(depSymbols),depStorage='gyan-mansarovar-duty-v1';







depUI('editkind').innerHTML=depUI('kind').innerHTML;







let depItems=[],depSelected=null,depPlace=false,depCamera=null,depReturn=null,depNodes=[],depButtons=[],depReady=false,depNew=null,depClickPoint=null;















function depSeed(){
  if (depInitialPlan && Array.isArray(depInitialPlan.items) && depValid(depInitialPlan.items)) {
    return JSON.parse(JSON.stringify(depInitialPlan.items));
  }
  const positions=[[-14,.3,-58],[-30,10,-24],[28,.3,-35],[-10,.3,8],[54,.3,-2],[-13,.3,-59],[-13,.3,-69],[-53,1.2,11],[-42,.5,-8],[-8,.3,21],[20,.3,38],[0,.3,39],[-16,.9,8.5]];







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







if (initialLocal && depValid(initialLocal.items) && (!depInitialPlan || !depInitialPlan.items || initialLocal.items.length >= depInitialPlan.items.length)) {
  depItems=initialLocal.items;
} else if (depInitialPlan && Array.isArray(depInitialPlan.items) && depValid(depInitialPlan.items)) {
  depItems=JSON.parse(JSON.stringify(depInitialPlan.items));
} else {
  depItems=depSeed();
}
depItems=(depItems||[]).filter(o=>o&&o.kind!=='helicopter');
depItems.forEach(o => {
  if (o) {
    if (!o.duty || o.duty === 'Security post' || o.duty === 'Post' || o.duty.trim() === '') {
      const match = typeof depInitialPlan !== 'undefined' && depInitialPlan && depInitialPlan.items && depInitialPlan.items.find(x => x.id === o.id || x.name === o.name);
      if (match && match.duty && match.duty !== 'Security post') {
        o.duty = match.duty;
      } else {
        o.duty = depGetAutoDuty(o.x, o.y, o.z, o.kind);
      }
    }
  }
});
try{
  const _raw=localStorage.getItem(depStorage);
  if(_raw){
    const _p=JSON.parse(_raw);
    const _arr=Array.isArray(_p)?_p:(_p&&_p.items);
    if(_arr&&_arr.some(x=>x.kind==='helicopter')){
      const _c=_arr.filter(x=>x.kind!=='helicopter');
      if(Array.isArray(_p))localStorage.setItem(depStorage,JSON.stringify(_c));
      else{_p.items=_c;localStorage.setItem(depStorage,JSON.stringify(_p));}
    }
  }
}catch(e){}















function depStore(){







  try{







    const record={version:1,savedAt:Date.now(),origin:[geo.originLongitude,geo.originLatitude],items:depItems};







    localStorage.setItem(depStorage,JSON.stringify(record));







    depUI('status').textContent='✅ Auto-saved · '+depItems.filter(o=>o.kind==='officer').length+' officers · '+depItems.filter(o=>o.kind!=='officer').length+' equipment';







  }catch(e){console.warn('localStorage save warning:',e);}







  depQueue();







}















const depMaterials={







  vipSaree:new THREE.MeshStandardMaterial({color:0xf1eadd,roughness:0.55}),







  vipGold:new THREE.MeshStandardMaterial({color:0xf59e0b,roughness:0.25,metalness:0.75}),







  vipPallu:new THREE.MeshStandardMaterial({color:0x8e293b,roughness:0.5}),







  vipCar:new THREE.MeshStandardMaterial({color:0x09090b,roughness:0.2,metalness:0.85}),







  vipGlass:new THREE.MeshStandardMaterial({color:0x1e293b,roughness:0.1,metalness:0.9,transparent:true,opacity:0.85}),







  vipChrome:new THREE.MeshStandardMaterial({color:0xe2e8f0,roughness:0.1,metalness:0.95}),







  vipBeaconRed:new THREE.MeshStandardMaterial({color:0xef4444,emissive:0xdc2626,emissiveIntensity:1.5}),







  vipBeaconBlue:new THREE.MeshStandardMaterial({color:0x3b82f6,emissive:0x2563eb,emissiveIntensity:1.5}),







  heliWhite:new THREE.MeshStandardMaterial({color:0xf8fafc,roughness:0.3}),







  heliNavy:new THREE.MeshStandardMaterial({color:0x0f172a,roughness:0.3,metalness:0.3}),







  heliRotor:new THREE.MeshStandardMaterial({color:0x27272a,roughness:0.5}),







  barricadeYellow:new THREE.MeshStandardMaterial({color:0xeab308,roughness:0.4}),







  barricadeDark:new THREE.MeshStandardMaterial({color:0x1e293b,roughness:0.5}),







  stageSofaRed:new THREE.MeshStandardMaterial({color:0x881337,roughness:0.6}),







  stageSofaGold:new THREE.MeshStandardMaterial({color:0xd97706,roughness:0.25,metalness:0.75}),















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







  hhmdStripe:new THREE.MeshStandardMaterial({color:0xfacc15,roughness:0.35,metalness:0.1}), // High-visibility hazard yellow band







  whiteBody:new THREE.MeshStandardMaterial({color:0xf8fafc,roughness:0.25,metalness:0.1}), // Gloss white vehicle body







  fireRed:new THREE.MeshStandardMaterial({color:0xc1121f,roughness:0.28,metalness:0.12}), // Tactical fire engine signal red







  chrome:new THREE.MeshStandardMaterial({color:0xd8dee9,roughness:0.15,metalness:0.85}), // Polished chrome & stainless steel







  glassTint:new THREE.MeshStandardMaterial({color:0x1e293b,roughness:0.12,metalness:0.6,transparent:true,opacity:0.75}), // Tinted glass







  tireRubber:new THREE.MeshStandardMaterial({color:0x111315,roughness:0.92,metalness:0.05}), // Black rubber tire tread







  shutterMetal:new THREE.MeshStandardMaterial({color:0x94a3b8,roughness:0.45,metalness:0.65}), // Ribbed equipment roller shutter







  stanchionChrome:new THREE.MeshStandardMaterial({color:0xe2e8f0,roughness:0.12,metalness:0.9}), // Polished queue stanchion







  qbeltRibbon:new THREE.MeshStandardMaterial({color:0xbe123c,roughness:0.55,metalness:0.05}), // High-tension red nylon webbing







  crateWood:new THREE.MeshStandardMaterial({color:0x8b5a2b,roughness:0.78,metalness:0.05}), // Heavy cargo crate wood







  crateTrim:new THREE.MeshStandardMaterial({color:0x272e39,roughness:0.38,metalness:0.7}) // Reinforced steel corner brackets







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















// Ambulance Emergency Livery Decal (Sides) - Clean White with Bold Red AMBULANCE







const depAmbCanvas=document.createElement('canvas');depAmbCanvas.width=512;depAmbCanvas.height=128;



const dac=depAmbCanvas.getContext('2d');



dac.clearRect(0,0,512,128);



dac.fillStyle='#dc2626';



dac.font='900 64px Arial, sans-serif';dac.textAlign='center';dac.textBaseline='middle';



dac.fillText('AMBULANCE',256,64);



const depAmbulanceDecal=new THREE.MeshStandardMaterial({



  map:new THREE.CanvasTexture(depAmbCanvas),



  transparent:true,opacity:1.0,roughness:0.25,metalness:0.1,side:THREE.FrontSide,



  polygonOffset:true,polygonOffsetFactor:-1,polygonOffsetUnits:-1



});







// Ambulance Hood Inverted/Mirrored Decal



const depAmbHoodCanvas=document.createElement('canvas');depAmbHoodCanvas.width=256;depAmbHoodCanvas.height=128;



const dahc=depAmbHoodCanvas.getContext('2d');



dahc.clearRect(0,0,256,128);



dahc.fillStyle='#dc2626';



dahc.fillRect(108,12,40,40);



dahc.clearRect(108,26,40,12);dahc.clearRect(122,12,12,40);



dahc.fillRect(110,28,36,8);dahc.fillRect(124,14,8,36);



dahc.font='900 36px Arial, sans-serif';dahc.textAlign='center';dahc.textBaseline='middle';



dahc.fillText('ECNALUBMA',128,96);



const depAmbulanceHoodDecal=new THREE.MeshStandardMaterial({



  map:new THREE.CanvasTexture(depAmbHoodCanvas),



  transparent:true,opacity:1.0,roughness:0.25,metalness:0.1,side:THREE.FrontSide,



  polygonOffset:true,polygonOffsetFactor:-1,polygonOffsetUnits:-1



});















// Fire Engine Rear Tailgate Chevrons Decal







const depFireChevCanvas=document.createElement('canvas');depFireChevCanvas.width=512;depFireChevCanvas.height=256;







const dfc=depFireChevCanvas.getContext('2d');







dfc.fillStyle='#eab308';dfc.fillRect(0,0,512,256);







dfc.fillStyle='#dc2626';







for(let x=-256;x<=512;x+=64){







  dfc.beginPath();







  dfc.moveTo(x,256);dfc.lineTo(x+64,0);dfc.lineTo(x+96,0);dfc.lineTo(x+32,256);







  dfc.fill();







}







// Central Caution Box







dfc.fillStyle='#1e293b';dfc.fillRect(64,88,384,80);







dfc.strokeStyle='#eab308';dfc.lineWidth=4;dfc.strokeRect(68,92,376,72);







dfc.fillStyle='#ffffff';dfc.font='bold 26px sans-serif';dfc.textAlign='center';







dfc.fillText('FIRE & RESCUE SERVICE',256,124);







dfc.fillStyle='#eab308';dfc.font='bold 18px sans-serif';







dfc.fillText('अग्नि शमन सेवा · EMERGENCY 101',256,150);







const depFireChevronDecal=new THREE.MeshStandardMaterial({map:new THREE.CanvasTexture(depFireChevCanvas),roughness:0.4,metalness:0.1});















// Industrial Cargo Crate Stencil Decal







const depCrateCanvas=document.createElement('canvas');depCrateCanvas.width=256;depCrateCanvas.height=256;







const dcc=depCrateCanvas.getContext('2d');







dcc.fillStyle='#78350f';dcc.fillRect(0,0,256,256);







// Corner Hazard Chevrons







dcc.fillStyle='#eab308';







for(const [cx,cy] of [[0,0],[208,0],[0,208],[208,208]]){







  dcc.fillRect(cx,cy,48,48);







}







dcc.fillStyle='#1e293b';







dcc.fillRect(16,32,224,192);







dcc.strokeStyle='#f59e0b';dcc.lineWidth=3;







dcc.strokeRect(22,38,212,180);







dcc.fillStyle='#f8fafc';dcc.font='900 18px sans-serif';dcc.textAlign='center';







dcc.fillText('DEPLOYMENT POINT',128,72);







dcc.font='bold 14px sans-serif';dcc.fillStyle='#f59e0b';







dcc.fillText('ITEM PLACEHOLDER',128,95);







// Crosshair target symbol







dcc.strokeStyle='#38bdf8';dcc.lineWidth=3;







dcc.beginPath();dcc.arc(128,142,26,0,Math.PI*2);dcc.stroke();







dcc.beginPath();dcc.moveTo(128,108);dcc.lineTo(128,176);dcc.moveTo(94,142);dcc.lineTo(162,142);dcc.stroke();







dcc.fillStyle='#ffffff';dcc.font='bold 12px sans-serif';







dcc.fillText('↑↑ THIS SIDE UP ↑↑',128,198);







const depCrateDecal=new THREE.MeshStandardMaterial({map:new THREE.CanvasTexture(depCrateCanvas),roughness:0.65,metalness:0.05});















// 1. High-Fidelity Emergency Ambulance Van Builder







function depBuildAmbulance(g){







  g.scale.setScalar(1);







  const wheels=[];







  const beacons=[];















  // Chassis Frame & Skid Plates







  depPart(g,'box',[0,.32,0],[1.75,.22,4.8],'dark');







  depPart(g,'box',[0,.44,-2.55],[2.08,.34,.32],'dark'); // Front bumper







  depPart(g,'box',[0,.40,2.45],[2.04,.22,.32],'dark'); // Rear step bumper















  // 4 Realistic Rubber Tires & Chrome Hubcaps







  const wCoords=[[-0.96,.38,-1.5],[0.96,.38,-1.5],[-0.96,.38,1.4],[0.96,.38,1.4]];







  for(const [wx,wy,wz] of wCoords){







    const wGroup=new THREE.Group();wGroup.position.set(wx,wy,wz);g.add(wGroup);







    const tire=depPart(wGroup,'cylinder',[0,0,0],[.38,.22,.38],'tireRubber');tire.rotation.z=Math.PI/2;







    const rim=depPart(wGroup,'cylinder',[0,0,0],[.25,.23,.25],'chrome');rim.rotation.z=Math.PI/2;







    const nut=depPart(wGroup,'cylinder',[wx>0?.12:-.12,0,0],[.08,.04,.08],'dark');nut.rotation.z=Math.PI/2;







    wheels.push(wGroup);







    depPart(g,'cylinder',[wx>0?1.02:-1.02,wy+.18,wz],[.44,.08,.44],'dark');







  }















  // Lower Front Cab, Grille & Headlights







  depPart(g,'box',[0,.72,-2.58],[1.2,.30,.08],'dark');







  depPart(g,'box',[0,.72,-2.54],[.9,.06,.09],'chrome');







  for(const hx of [-0.78,0.78]){







    depPart(g,'box',[hx,.72,-2.55],[.32,.20,.08],'white');







    depPart(g,'box',[hx>0?hx+.14:hx-.14,.72,-2.55],[.08,.20,.085],'yellow');







    depPart(g,'cylinder',[hx,.42,-2.62],[.08,.04,.08],'yellow');







  }















  // Sloping Hood & Windshield







  depPart(g,'box',[0,1.05,-2.12],[1.98,.44,.96],'whiteBody');







  const ws=depPart(g,'box',[0,1.56,-1.55],[1.88,.78,.08],'glassTint');ws.rotation.x=-0.48;







  for(const wx of [-0.4,0.35]){







    const wip=depPart(g,'cylinder',[wx,1.34,-1.72],[.012,.44,.012],'dark');wip.rotation.set(-0.48,0,0.25);







  }















  // Dual Side Mirrors







  for(const mx of [-1.15,1.15]){







    depPart(g,'cylinder',[mx>0?mx-.08:mx+.08,1.48,-1.48],[.018,.25,.018],'dark');







    depPart(g,'box',[mx,1.48,-1.50],[.10,.26,.08],'dark');







    depPart(g,'box',[mx,1.48,-1.46],[.08,.22,.01],'chrome');







  }















  // Main Van Body & High-Roof







  depPart(g,'box',[0,1.42,.25],[2.06,1.56,3.85],'whiteBody');







  depPart(g,'rounded',[0,2.26,.25],[2.00,.34,3.80],'whiteBody');















  // Tinted Cabin Windows







  for(const wx of [-1.04,1.04]){







    depPart(g,'box',[wx,1.58,-1.18],[.04,.54,.68],'glassTint');







    depPart(g,'box',[wx,1.58,.45],[.04,.54,1.95],'glassTint');







  }















  // Side Entry Step Plate & Door Handle







  depPart(g,'box',[1.04,.45,.20],[.12,.08,.75],'dark');







  depPart(g,'cylinder',[1.05,1.15,.55],[.015,.14,.015],'dark');















  // Rear Twin Loading Doors & Taillights







  for(const rx of [-0.48,0.48]){







    depPart(g,'box',[rx,1.40,2.18],[.94,1.48,.04],'whiteBody');







    depPart(g,'box',[rx,1.66,2.20],[.65,.48,.03],'glassTint');







  }







  depPart(g,'cylinder',[.08,1.15,2.22],[.015,.16,.015],'chrome');







  for(const tx of [-0.98,0.98]){







    depPart(g,'box',[tx,1.05,2.18],[.08,.45,.04],'red');







    depPart(g,'box',[tx,.72,2.18],[.08,.16,.04],'yellow');







  }















  // Emergency Livery Decals - Flush on both side walls (no protruding strips)



  const dL=depPart(g,'sign',[-1.036,1.08,0.42],[2.7,0.38,1],depAmbulanceDecal);



  dL.rotation.y=-Math.PI/2;







  const dR=depPart(g,'sign',[1.036,1.08,0.42],[2.7,0.38,1],depAmbulanceDecal);



  dR.rotation.y=Math.PI/2;







  const dH=depPart(g,'sign',[0,1.275,-2.12],[1.2,0.42,1],depAmbulanceHoodDecal);



  dH.rotation.x=-Math.PI/2;















  // Roof Emergency Lightbar & Sirens (Flashing!)







  depPart(g,'box',[0,2.47,-1.05],[1.45,.08,.28],'dark');







  const bL=depPart(g,'box',[-0.46,2.53,-1.05],[.46,.10,.24],'blue');







  const bLM=bL.material.clone();bLM.emissive=new THREE.Color(0x0284c7);bLM.emissiveIntensity=2.0;bL.material=bLM;







  beacons.push({mat:bLM,speed:2.8,phase:0,intensity:2.4});















  const bR=depPart(g,'box',[0.46,2.53,-1.05],[.46,.10,.24],'red');







  const bRM=bR.material.clone();bRM.emissive=new THREE.Color(0xdc2626);bRM.emissiveIntensity=2.0;bR.material=bRM;







  beacons.push({mat:bRM,speed:2.8,phase:Math.PI,intensity:2.4});















  const siren=depPart(g,'cylinder',[0,2.52,-1.05],[.11,.14,.11],'chrome');siren.rotation.x=Math.PI/2;







  for(const [px,phase] of [[-0.92,0.8],[0.92,2.4]]){







    const rPod=depPart(g,'box',[px,2.44,2.05],[.14,.10,.14],px>0?'red':'yellow');







    const rpm=rPod.material.clone();rpm.emissive=new THREE.Color(px>0?0xdc2626:0xd97706);rpm.emissiveIntensity=1.6;rPod.material=rpm;







    beacons.push({mat:rpm,speed:2.5,phase,intensity:1.8});







  }







  depPart(g,'rounded',[0,2.48,.85],[.95,.16,1.25],'whiteBody'); // AC Unit















  g.userData.wheels=wheels;







  g.userData.beacons=beacons;







}















// 2. High-Fidelity Tactical Fire Engine / Rescue Tender Builder







function depBuildFireBrigade(g){







  g.scale.setScalar(1);







  const wheels=[];







  const beacons=[];















  // Heavy Chassis Frame & Massive Push Bumper







  depPart(g,'box',[0,.42,0],[1.95,.28,7.2],'dark');







  depPart(g,'box',[0,.52,-3.75],[2.48,.42,.35],'dark');







  for(const hx of [-0.65,0.65]){







    depPart(g,'torus',[hx,.52,-3.95],[.08,.025,1],'chrome');







  }







  depPart(g,'box',[0,.45,3.35],[2.46,.24,.38],'dark');















  // 6 Heavy-Duty Wheels (3 Axles: Front + Dual Rear Drive Axles)







  const twCoords=[[-1.16,.52,-2.4],[1.16,.52,-2.4],[-1.16,.52,1.5],[1.16,.52,1.5],[-1.16,.52,2.7],[1.16,.52,2.7]];







  for(const [wx,wy,wz] of twCoords){







    const wGroup=new THREE.Group();wGroup.position.set(wx,wy,wz);g.add(wGroup);







    const tire=depPart(wGroup,'cylinder',[0,0,0],[.52,.32,.52],'tireRubber');tire.rotation.z=Math.PI/2;







    const rim=depPart(wGroup,'cylinder',[0,0,0],[.34,.33,.34],'chrome');rim.rotation.z=Math.PI/2;







    const hub=depPart(wGroup,'cylinder',[wx>0?.17:-.17,0,0],[.14,.06,.14],'dark');hub.rotation.z=Math.PI/2;







    wheels.push(wGroup);







    depPart(g,'cylinder',[wx>0?1.22:-1.22,wy+.26,wz],[.60,.10,.60],'dark');







  }















  // Crew Cabin & Chrome Grille







  depPart(g,'box',[0,1.65,-2.35],[2.45,1.85,2.45],'fireRed');







  depPart(g,'box',[0,2.62,-2.35],[2.46,.16,2.45],'whiteBody');







  depPart(g,'box',[0,1.18,-3.60],[1.65,.65,.08],'dark');







  for(const gy of [1.04,1.18,1.32]){







    depPart(g,'box',[0,gy,-3.55],[1.45,.08,.09],'chrome');







  }















  // Front Windshield & Wipers







  const fWind=depPart(g,'box',[0,1.96,-3.40],[2.26,.92,.08],'glassTint');fWind.rotation.x=-0.16;







  for(const wx of [-0.55,0.55]){







    const wip=depPart(g,'cylinder',[wx,1.58,-3.55],[.014,.55,.014],'dark');wip.rotation.set(-0.16,0,0.18);







  }















  // Headlights & Bumper Fog Lights







  for(const hx of [-1.02,1.02]){







    depPart(g,'box',[hx,1.08,-3.58],[.34,.24,.08],'white');







    depPart(g,'box',[hx>0?hx+.14:hx-.14,1.08,-3.58],[.08,.24,.085],'yellow');







    depPart(g,'cylinder',[hx,.52,-3.85],[.10,.05,.10],'yellow');







  }















  // Side Cab Windows, Entry Steps & Tubular Chrome Mirrors







  for(const sx of [-1.24,1.24]){







    depPart(g,'box',[sx,1.95,-2.35],[.05,.72,1.85],'glassTint');







    depPart(g,'box',[sx>0?sx+.06:sx-.06,.65,-2.35],[.14,.06,.85],'dark');







    depPart(g,'cylinder',[sx>0?sx+.15:sx-.15,1.95,-3.20],[.02,.55,.02],'chrome');







    depPart(g,'box',[sx>0?sx+.22:sx-.22,1.95,-3.20],[.08,.36,.14],'dark');







  }















  // Rear Equipment Body & 6 Metallic Roller Shutters







  depPart(g,'box',[0,1.72,0.98],[2.45,1.98,4.35],'fireRed');







  for(const sx of [-1.24,1.24]){







    for(const [sz,sw] of [[-0.55,1.15],[0.85,1.25],[2.25,1.15]]){







      depPart(g,'box',[sx,1.68,sz],[.04,1.48,sw],'shutterMetal');







      depPart(g,'cylinder',[sx>0?sx+.03:sx-.03,.98,sz],[.015,sw*.85,.015],'chrome');







    }







  }















  // Side External Suction Hoses & Delivery Valves







  for(const hx of [-1.25,1.25]){







    const hose=depPart(g,'cylinder',[hx,2.58,.95],[.06,4.1,.06],'dark');hose.rotation.x=Math.PI/2;







    for(const hz of [-1.05,2.95]){







      const coup=depPart(g,'cylinder',[hx,2.58,hz],[.075,.12,.075],'chrome');coup.rotation.x=Math.PI/2;







    }







    for(const vz of [0.75,0.95]){







      const vOut=depPart(g,'cylinder',[hx>0?hx+.06:hx-.06,.78,vz],[.045,.12,.045],'chrome');vOut.rotation.z=Math.PI/2;







    }







  }















  // Roof Water Monitor Cannon / Turret







  depPart(g,'cylinder',[0,2.82,-.65],[.22,.22,.22],'chrome');







  depPart(g,'sphereSmooth',[0,2.98,-.65],[.15,.15,.15],'dark');







  const nozzle=depPart(g,'cylinder',[0,3.08,-.98],[.065,.75,.065],'chrome');nozzle.rotation.x=-Math.PI/2.3;







  depPart(g,'torus',[.14,2.98,-.65],[.07,.015,1],'yellow');















  // Roof Rescue Extension Ladder (Dual Fly Aluminum)







  depPart(g,'box',[.38,2.85,.95],[.04,.10,4.4],'chrome');







  depPart(g,'box',[.82,2.85,.95],[.04,.10,4.4],'chrome');







  for(let rz=-1.1;rz<=3.0;rz+=.30){







    const rung=depPart(g,'cylinder',[.60,2.85,rz],[.015,.42,.015],'chrome');rung.rotation.z=Math.PI/2;







  }















  // Full-Width Rear Tailgate Hazard Chevron Decal & Access Ladder







  depPart(g,'sign',[0,1.68,3.18],[2.42,1.85,1],depFireChevronDecal);







  for(const rz of [-0.72,-0.98]) depPart(g,'box',[rz,1.75,3.22],[.03,2.1,.03],'chrome');







  for(let ry=0.85;ry<=2.65;ry+=.25) depPart(g,'cylinder',[-0.85,ry,3.22],[.014,.26,.014],'chrome');















  // Emergency Red Lightbar & Dual Chrome Air Horns (Flashing!)







  depPart(g,'box',[0,2.84,-2.35],[1.85,.16,.32],'dark');







  for(const [bx,phase] of [[-0.65,0],[0.65,Math.PI]]){







    const bec=depPart(g,'cylinder',[bx,2.95,-2.35],[.18,.16,.18],'fireRed');







    const bm=bec.material.clone();bm.emissive=new THREE.Color(0xef4444);bm.emissiveIntensity=2.4;bec.material=bm;







    beacons.push({mat:bm,speed:3.2,phase,intensity:2.6});







  }







  for(const hx of [-0.42,0.42]){







    const horn=depPart(g,'cylinder',[hx,2.82,-3.15],[.05,.65,.05],'chrome');horn.rotation.x=Math.PI/2;







    const flare=depPart(g,'cylinder',[hx,2.82,-3.45],[.09,.08,.09],'chrome');flare.rotation.x=Math.PI/2;







  }







  for(const [rx,phase] of [[-1.12,1.0],[1.12,2.6]]){







    const rFlash=depPart(g,'box',[rx,2.75,3.12],[.15,.12,.12],'yellow');







    const rfm=rFlash.material.clone();rfm.emissive=new THREE.Color(0xf59e0b);rfm.emissiveIntensity=1.8;rFlash.material=rfm;







    beacons.push({mat:rfm,speed:2.8,phase,intensity:2.0});







  }















  g.userData.wheels=wheels;







  g.userData.beacons=beacons;







}















// 3. Retractable Belt Barrier / Q-Belt Stanchion Builder







function depBuildQBelt(g){







  g.scale.setScalar(1);







  for(const px of [-1.0,1.0]){







    depPart(g,'cylinder',[px,.024,0],[.18,.048,.18],'stanchionChrome');







    depPart(g,'torus',[px,.008,0],[.182,.012,1],'dark');







    depPart(g,'cylinder',[px,.50,0],[.032,.92,.032],'stanchionChrome');







    depPart(g,'cylinder',[px,.94,0],[.052,.12,.052],'stanchionChrome');







    for(const rot of [0,Math.PI/2,Math.PI,-Math.PI/2]){







      const slot=depPart(g,'box',[px+Math.sin(rot)*.053,.94,Math.cos(rot)*.053],[.008,.08,.016],'dark');







      slot.rotation.y=rot;







    }







    depPart(g,'sphereSmooth',[px,1.02,0],[.044,.044,.044],'stanchionChrome');







  }







  depPart(g,'box',[0,.94,0],[1.92,.055,.006],'qbeltRibbon');







  depPart(g,'box',[.94,.94,0],[.025,.068,.016],'stanchionChrome');







  depPart(g,'box',[-.94,.94,0],[.025,.068,.016],'stanchionChrome');







}















// 4. Industrial Square Box / Deployment Point Placeholder Crate








function depBuildParking(g){
  g.scale.setScalar(1);
  // Double-sized parking lot: 28m wide x 20m deep (exact 2x footprint)
  depPart(g,'box',[0,0.02,0],[28,0.04,20],'dark');

  // White boundary demarcation border around the 28x20 parking lot
  depPart(g,'box',[0,0.045,-9.9],[27.8,0.02,0.16],'white');
  depPart(g,'box',[0,0.045,9.9],[27.8,0.02,0.16],'white');
  depPart(g,'box',[-13.9,0.045,0],[0.16,0.02,19.8],'white');
  depPart(g,'box',[13.9,0.045,0],[0.16,0.02,19.8],'white');

  // Yellow central driving lane demarcation (connecting rows)
  for(let x=-12.5; x<=12.5; x+=2.8){
    depPart(g,'box',[x,0.045,0],[1.6,0.02,0.16],'yellow');
  }

  // Row 1 (North bays: z = -5.8) stall divider lines and concrete wheel stops
  for(const x of [-11.4, -7.6, -3.8, 0, 3.8, 7.6, 11.4]){
    depPart(g,'box',[x,0.05,-5.8],[0.14,0.02,7.6],'white');
    if (x > -11.4) {
      depPart(g,'box',[x - 1.9, 0.08, -9.2],[2.4, 0.12, 0.22],'white');
    }
  }
  // Row 2 (South bays: z = 5.8) stall divider lines and concrete wheel stops
  for(const x of [-11.4, -7.6, -3.8, 0, 3.8, 7.6, 11.4]){
    depPart(g,'box',[x,0.05,5.8],[0.14,0.02,7.6],'white');
    if (x > -11.4) {
      depPart(g,'box',[x - 1.9, 0.08, 9.2],[2.4, 0.12, 0.22],'white');
    }
  }

  // Parking Entrance Signboard "P" at corner
  depPart(g,'cylinder',[13.0,1.4,-9.0],[0.08,2.8,0.08],'dark');
  depPart(g,'box',[13.0,2.6,-9.0],[1.1,1.1,0.08],'blue');
  depPart(g,'box',[13.0,2.6,-8.95],[0.22,0.72,0.02],'white'); // P stem
  depPart(g,'box',[13.16,2.78,-8.95],[0.38,0.36,0.02],'white'); // P loop
  depPart(g,'box',[13.14,2.78,-8.93],[0.18,0.18,0.03],'blue'); // P hole

  // Vehicles: Sizes remain EXACTLY the same (1:1 standard scale)
  // Perfectly centered inside their respective parking stalls!
  // 1. White VIP Staff Car (Exact original size: 2.1 x 0.55 x 4.2) in Stall 1 (center X = -9.5)
  const car1X=-9.5, car1Z=-5.8;
  depPart(g,'box',[car1X,0.42,car1Z],[2.1,0.55,4.2],'whiteBody');
  depPart(g,'box',[car1X,0.88,car1Z-0.2],[1.9,0.48,2.4],'glassTint');
  depPart(g,'cylinder',[car1X-0.95,0.28,car1Z+1.2],[0.35,0.25,0.35],'tireRubber');
  depPart(g,'cylinder',[car1X+0.95,0.28,car1Z+1.2],[0.35,0.25,0.35],'tireRubber');
  depPart(g,'cylinder',[car1X-0.95,0.28,car1Z-1.2],[0.35,0.25,0.35],'tireRubber');
  depPart(g,'cylinder',[car1X+0.95,0.28,car1Z-1.2],[0.35,0.25,0.35],'tireRubber');

  // 2. Dark VIP SUV (Exact original size: 2.2 x 0.65 x 4.4) in Stall 2 (center X = -5.7)
  const car2X=-5.7, car2Z=-5.8;
  depPart(g,'box',[car2X,0.5,car2Z],[2.2,0.65,4.4],'vipCar');
  depPart(g,'box',[car2X,1.02,car2Z-0.1],[2.0,0.55,2.8],'glassTint');
  depPart(g,'box',[car2X,1.34,car2Z-0.1],[0.3,0.1,0.8],'vipBeaconRed');
  depPart(g,'cylinder',[car2X-1.0,0.32,car2Z+1.3],[0.4,0.28,0.4],'tireRubber');
  depPart(g,'cylinder',[car2X+1.0,0.32,car2Z+1.3],[0.4,0.28,0.4],'tireRubber');
  depPart(g,'cylinder',[car2X-1.0,0.32,car2Z-1.3],[0.4,0.28,0.4],'tireRubber');
  depPart(g,'cylinder',[car2X+1.0,0.32,car2Z-1.3],[0.4,0.28,0.4],'tireRubber');

  // 3. Official VIP Sedan (Exact original size: 2.1 x 0.55 x 4.2) in Stall 3 (center X = -1.9)
  const car3X=-1.9, car3Z=-5.8;
  depPart(g,'box',[car3X,0.42,car3Z],[2.1,0.55,4.2],'whiteBody');
  depPart(g,'box',[car3X,0.88,car3Z-0.2],[1.9,0.48,2.4],'glassTint');
  depPart(g,'cylinder',[car3X-0.95,0.28,car3Z+1.2],[0.35,0.25,0.35],'tireRubber');
  depPart(g,'cylinder',[car3X+0.95,0.28,car3Z+1.2],[0.35,0.25,0.35],'tireRubber');
  depPart(g,'cylinder',[car3X-0.95,0.28,car3Z-1.2],[0.35,0.25,0.35],'tireRubber');
  depPart(g,'cylinder',[car3X+0.95,0.28,car3Z-1.2],[0.35,0.25,0.35],'tireRubber');

  // 4. Police Troop Bus (Exact original size: 2.3 x 1.1 x 5.0) in Stall 5 (center X = +5.7)
  const busX=5.7, busZ=-5.8;
  depPart(g,'box',[busX,0.75,busZ],[2.3,1.1,5.0],'dark');
  depPart(g,'box',[busX,1.45,busZ-0.2],[2.2,0.6,3.8],'glassTint');
  depPart(g,'box',[busX,0.85,busZ],[2.34,0.18,5.02],'yellow');
  depPart(g,'box',[busX,1.82,busZ-0.2],[0.3,0.12,1.2],'vipBeaconBlue');
  depPart(g,'cylinder',[busX-1.05,0.36,busZ+1.5],[0.42,0.3,0.42],'tireRubber');
  depPart(g,'cylinder',[busX+1.05,0.36,busZ+1.5],[0.42,0.3,0.42],'tireRubber');
  depPart(g,'cylinder',[busX-1.05,0.36,busZ-1.5],[0.42,0.3,0.42],'tireRubber');
  depPart(g,'cylinder',[busX+1.05,0.36,busZ-1.5],[0.42,0.3,0.42],'tireRubber');
}

function depBuildSquareBox(g){







  g.scale.setScalar(1);







  for(const sx of [-0.42,0,0.42]){







    depPart(g,'box',[sx,.05,0],[.10,.10,1.02],'dark');







  }







  depPart(g,'box',[0,.55,0],[.96,.90,.96],'crateWood');







  for(const cx of [-0.47,0.47]){







    for(const cy of [0.16,0.94]){







      for(const cz of [-0.47,0.47]){







        depPart(g,'box',[cx,cy,cz],[.10,.10,.10],'crateTrim');







      }







    }







  }







  depPart(g,'box',[0,.22,0],[.98,.04,.98],'crateTrim');







  depPart(g,'box',[0,.88,0],[.98,.04,.98],'crateTrim');







  for(const hx of [-0.49,0.49]){







    depPart(g,'box',[hx,.55,0],[.02,.10,.24],'crateTrim');







    const ring=depPart(g,'torus',[hx>0?hx+.02:hx-.02,.54,0],[.055,.012,1],'chrome');







    ring.rotation.y=Math.PI/2;







  }







  depPart(g,'box',[0,1.005,0],[.98,.03,.98],'crateTrim');







  depPart(g,'box',[0,.98,.49],[.08,.06,.02],'chrome');







  depPart(g,'box',[0,.98,-.49],[.08,.06,.02],'chrome');















  depPart(g,'sign',[0,.55,.485],[.72,.65,1],depCrateDecal);







  const dB=depPart(g,'sign',[0,.55,-.485],[.72,.65,1],depCrateDecal);dB.rotation.y=Math.PI;







  const dL=depPart(g,'sign',[-.485,.55,0],[.72,.65,1],depCrateDecal);dL.rotation.y=-Math.PI/2;







  const dR=depPart(g,'sign',[.485,.55,0],[.72,.65,1],depCrateDecal);dR.rotation.y=Math.PI/2;







}















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







    // Arm held prominently in FRONT of chest/shoulder holding wireless radio







    rightArm.rotation.set(Math.PI / 2.35, Math.PI / 11, -Math.PI / 6.0);







    baseRightArmRotX = Math.PI / 2.35;















    // Radio handset held prominently IN FRONT of the hand (completely clear of palm, 100% visible)







    const radioHand = new THREE.Group();







    radioHand.position.set(0, -0.62, -0.16);







    radioHand.rotation.set(Math.PI / 6.5, 0, Math.PI / 14);







    rightArm.add(radioHand);















    // Main tactical radio body (large, bold, clearly visible)







    depPart(radioHand, 'box', [0, 0.05, 0], [0.11, 0.22, 0.065], 'dark');















    // Yellow tactical safety collar around top of radio







    depPart(radioHand, 'box', [0, 0.15, 0], [0.114, 0.025, 0.068], 'yellow');















    // Tall flexible whip antenna pointing upwards







    const ant = depPart(radioHand, 'cylinder', [-0.035, 0.29, 0], [0.012, 0.28, 0.012], 'dark');







    ant.rotation.z = -0.06;







    depPart(radioHand, 'sphereSmooth', [-0.043, 0.43, 0], [0.018, 0.018, 0.018], 'yellow');















    // Top volume/channel selector knobs







    depPart(radioHand, 'cylinder', [0.032, 0.18, 0], [0.018, 0.04, 0.018], 'yellow');







    depPart(radioHand, 'cylinder', [-0.005, 0.175, 0], [0.015, 0.03, 0.015], 'dark');















    // High-contrast backlit LCD display screen (bright green/yellow)







    depPart(radioHand, 'box', [0, 0.09, 0.034], [0.075, 0.055, 0.008], 'yellow');















    // Speaker/microphone sound grille slots







    for (const sy of [0.035, 0.015, -0.005, -0.025]) {







      depPart(radioHand, 'box', [0, sy, 0.034], [0.065, 0.006, 0.006], 'dark');







    }















    // Red PTT (Push-To-Talk) button on side







    depPart(radioHand, 'box', [-0.058, 0.06, 0], [0.014, 0.055, 0.025], 'red');















    // Hand palm supporting behind and fingers on sides (NOT covering front screen/antenna)







    depPart(radioHand, 'rounded', [0, -0.01, 0.042], [0.075, 0.08, 0.025], 'skin');







    depPart(radioHand, 'rounded', [0.058, 0.02, 0.008], [0.024, 0.09, 0.026], 'skin');







    depPart(radioHand, 'rounded', [-0.052, -0.01, 0.008], [0.024, 0.05, 0.022], 'skin');







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
  if (typeof depSyncDutyLists === 'function') depSyncDutyLists();
  if (typeof restoreStaticHelicopter === 'function') {
    try { restoreStaticHelicopter(); } catch(e){}
  }







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
  depRebuildTopList();















  if(list){







    for(const item of sortedByDuty){







      const o=document.createElement('option');







      o.value=item.id;







      o.textContent=(depSymbols[item.kind]+' '+(item.duty ? item.duty+' — ' : '')+item.name).slice(0,100);







      list.appendChild(o);







    }







  }















function depCreateEquipmentMesh(kind) {







  const g = new THREE.Group();







  if (kind === 'officer' || kind === 'hhmd' || kind === 'binocular' || kind === 'radio') {







    depBuildOfficer(g, kind);







  } else if (kind === 'ambulance') {







    depBuildAmbulance(g);







  } else if (kind === 'firebrigade') {



    depBuildFireBrigade(g);



  } else if (kind === 'helicopter') {



    const heli = buildVvipHelicopter();



    g.add(heli);



    g.userData.heliGroup = heli;



    g.userData.mainRotor = heli.userData.mainRotor;



    g.userData.tailRotor = heli.userData.tailRotor;



    g.userData.rotorDisc = heli.userData.rotorDisc;







  } else if (kind === 'qbelt') {







    depBuildQBelt(g);







  } else if (kind === 'parking') {
    depBuildParking(g);
  } else if (kind === 'square_box') {







    depBuildSquareBox(g);







  } else if (kind === 'barricade') {







    for (const x of [-1.25, 1.25]) {







      depPart(g, 'box', [x, 0.6, 0], [0.12, 1.2, 0.15], 'dark');







      depPart(g, 'box', [x, 0.06, 0], [0.2, 0.12, 0.9], 'dark');







    }







    depPart(g, 'box', [0, 0.88, 0], [3, 0.66, 0.12], 'yellow');







    for (let x = -1.3; x < 1.4; x += 0.4) {







      const stripe = depPart(g, 'box', [x, 0.88, -0.071], [0.15, 0.62, 0.018], 'dark');







      stripe.rotation.z = -0.3;







    }







    if (typeof depBoardGeometry !== 'undefined' && typeof depPoliceSign !== 'undefined') {







      const board = new THREE.Mesh(depBoardGeometry, depPoliceSign);







      board.position.set(0, 0.88, -0.09);







      board.rotation.y = Math.PI;







      g.add(board);







      const back = board.clone();







      back.rotation.y = 0;







      back.position.z = 0.09;







      g.add(back);







    }







  } else if (kind === 'dfmd') {







    for (const x of [-0.6, 0.6]) depPart(g, 'box', [x, 1.12, 0], [0.18, 2.24, 0.45], 'blue');







    depPart(g, 'box', [0, 2.22, 0], [1.38, 0.18, 0.45], 'blue');







    depPart(g, 'box', [0.6, 1.7, -0.24], [0.1, 0.2, 0.03], 'yellow');







    depPart(g, 'box', [0, 2.15, -0.23], [0.85, 0.12, 0.04], 'dark');







    for (let y = 0.45; y <= 1.95; y += 0.35) {







      depPart(g, 'box', [-0.5, y, -0.23], [0.08, 0.08, 0.03], 'red');







      depPart(g, 'box', [0.5, y, -0.23], [0.08, 0.08, 0.03], 'red');







    }







  } else if (kind === 'cone') {







    const cone = new THREE.Mesh(depConeGeometry, depMaterials.red);







    cone.position.y = 0.4;







    g.add(cone);







    depPart(g, 'box', [0, 0.05, 0], [0.55, 0.1, 0.55], 'dark');







    depPart(g, 'cylinder', [0, 0.38, 0], [0.16, 0.08, 0.16], 'white');







    depPart(g, 'cylinder', [0, 0.52, 0], [0.11, 0.06, 0.11], 'white');







  } else if (kind === 'cctv') {







    depPart(g, 'cylinder', [0, 1.3, 0], [0.045, 2.6, 0.045], 'dark');







    depPart(g, 'cylinder', [0, 0.1, 0], [0.22, 0.2, 0.22], 'dark');







    depPart(g, 'box', [0, 2.6, -0.15], [0.45, 0.25, 0.45], 'white');







    depPart(g, 'sphereSmooth', [0, 2.45, -0.15], [0.14, 0.14, 0.14], 'dark');







    depPart(g, 'cylinder', [0, 2.48, -0.15], [0.16, 0.04, 0.16], 'yellow');







  } else if (kind === 'light') {







    depPart(g, 'cylinder', [0, 1.3, 0], [0.05, 2.6, 0.05], 'dark');







    depPart(g, 'cylinder', [0, 0.1, 0], [0.25, 0.2, 0.25], 'dark');







    depPart(g, 'box', [0, 2.6, -0.15], [0.55, 0.32, 0.45], 'yellow');







    depPart(g, 'box', [0, 2.6, -0.38], [0.48, 0.26, 0.02], 'white');







  } else {







    depPart(g, 'box', [0, 0.5, 0], [1, 1, 1], 'dark');







  }







  return g;







}







window.depCreateEquipmentMesh = depCreateEquipmentMesh;















  for(const item of depItems){

    const g = depCreateEquipmentMesh(item.kind);

    g.position.set(item.x, item.y, item.z);

    g.rotation.y = -item.angle * Math.PI / 180;

    g.userData.depId = item.id;

    g.traverse(child => {

      child.userData.depId = item.id;

    });



    // Invisible hitBox so clicking anywhere on or around helicopter registers immediately

    if (item.kind === 'helicopter') {

      const hitBox = new THREE.Mesh(new THREE.BoxGeometry(4.8, 4.2, 10.2), new THREE.MeshBasicMaterial({visible: false}));

      hitBox.position.set(0, 1.8, 0);

      hitBox.userData.depId = item.id;

      hitBox.userData.isHitBox = true;

      g.add(hitBox);

    }



    depGroup.add(g);

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







  const topList = (typeof root !== 'undefined' && root) ? root.querySelector('#dep-top-list') : document.getElementById('dep-top-list');
  if(topList)topList.value=depSelected||'';







  depUI('editor').hidden=!depSelected;







  depUpdate();draw();







}















let depLastSimulationUI=0;







function depUpdate(){







  if(!depReady)return;







  if(vvipActive){const now=performance.now();if(now-depLastSimulationUI<100)return;depLastSimulationUI=now;}







  if (typeof window !== "undefined" && typeof window.refreshDeployedCatalogCounts === "function") { window.refreshDeployedCatalogCounts(); }







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







    const canFirstPerson = isOfficerLike || peekItem.kind === 'ambulance' || peekItem.kind === 'firebrigade';







    if(badgeEl){







      badgeEl.textContent=peekItem.duty||(







        isOfficerLike?'Security post'







        :peekItem.kind==='ambulance'?'Emergency Medical Response'







        :peekItem.kind==='firebrigade'?'Fire & Safety Standby'







        :peekItem.kind==='qbelt'?'Queue & Crowd Management'







        :peekItem.kind==='square_box'?'Deployment Point / Placeholder'







        :'Access control'







      );







      badgeEl.title=peekItem.duty||'';







    }







    for(const [k,field] of Object.entries(depPeekFields)){







      if(document.activeElement!==field)field.value=peekItem[k];







      field.disabled=(k==='belt'||k==='mobile')&&!isOfficerLike;







      field.parentElement.hidden=field.disabled;







    }







    for(const b of depPeekActions.querySelectorAll('button')){







      if(b.textContent.includes('First')){ b.disabled=!canFirstPerson; b.hidden=!canFirstPerson; }







      else if(b.textContent.includes('Third')){ b.disabled=false; b.hidden=false; }







    }







  }















  const r=host.getBoundingClientRect();







  depGroup.visible=current!=='alignment';







  for(const {item,g} of depNodes)g.visible=!(depCamera==='first'&&item.id===depSelected);







  







  for(const {e,item} of depButtons){







    const isOfficerLike = ['officer','hhmd','binocular','radio'].includes(item.kind);







    const headHeight = isOfficerLike ? 2.15 : (item.kind==='firebrigade'?3.4:(item.kind==='ambulance'?2.7:(item.kind==='dfmd'?2.3:1.6)));







    const v = new THREE.Vector3(item.x, item.y + headHeight, item.z);







    const distance = camera.position.distanceTo(v);







    const p = v.project(camera);







    







    const isVisible = depGroup.visible && p.z >= -1 && p.z <= 1 && Math.abs(p.x) <= 0.98 && Math.abs(p.y) <= 0.98 && !(depCamera && item.id===depSelected);
    e.style.opacity = depOccCache.get(item.id) ? "0.45" : "1.0";







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







  const list=depUI('list');







  if(list)list.value=depSelected||'';







  const topList = (typeof root !== 'undefined' && root) ? root.querySelector('#dep-top-list') : document.getElementById('dep-top-list');
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







  const canFirstPerson = isOfficerLike || o.kind === 'ambulance' || o.kind === 'firebrigade';







  for(const k of ['belt','mobile']) depUI(k).disabled=!isOfficerLike;







  depUI('first').disabled = !canFirstPerson;







  depUI('third').disabled = false;















  updateOfficerHud(o);







  const isVehicle = o.kind === 'ambulance' || o.kind === 'firebrigade';







  if (o.kind === 'helicopter') {



    depUI('status').textContent = '🚁 Helicopter Selected — SPACE: Take Off / Ascend | RIGHT CTRL: Land / Descend | W/S: Fly | A/D: Steer | SHIFT: Turbo';



  } else depUI('status').textContent='🎮 Controlling ' + (depSymbols[o.kind] || '') + ' ' + o.name + (isVehicle ? ' · Drive: W/S/↑/↓ · Steer: A/D/←/→/Q/E · Turbo: SHIFT · Bump/Jump: SPACE · Next: TAB · Deselect: CAPSLOCK' : ' · Move: W/S/↑/↓ · Rotate: A/D/←/→/Q/E · Jump: SPACE · Next: TAB · Deselect: CAPSLOCK');















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







  Object.assign(o,next);
  if (next.duty && next.duty.trim()) {
    o.customDuty = true;
    if (typeof depRegisterCustomDuty === 'function') depRegisterCustomDuty(next.duty);
  }
  depStore();depBuild();depChoose(o.id);







  if(depCamera)depView(depCamera);







});







depUI('form').addEventListener('change',()=>{if(depUI('form').checkValidity())depUI('form').requestSubmit();});







if(depUI('name')) depUI('name').addEventListener('input', () => {







  const o = depItems.find(x => x.id === depSelected);







  if (o) { o.name = depUI('name').value; depSyncDropdownLabels(o); depStore(); }







});







if(depUI('duty')) depUI('duty').addEventListener('input', () => {
  const o = depItems.find(x => x.id === depSelected);
  if (o) {
    o.duty = depUI('duty').value;
    o.customDuty = true;
    if (typeof depRegisterCustomDuty === 'function' && o.duty.trim()) {
      depRegisterCustomDuty(o.duty);
    }
    depSyncDropdownLabels(o);
    depStore();
  }







});







if(depUI('belt')) depUI('belt').addEventListener('input', () => {







  const o = depItems.find(x => x.id === depSelected);







  if (o) { o.belt = depUI('belt').value; depStore(); }







});







if(depUI('mobile')) depUI('mobile').addEventListener('input', () => {







  const o = depItems.find(x => x.id === depSelected);







  if (o) { o.mobile = depUI('mobile').value; depStore(); }







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







    : kind === 'ambulance' ? `Ambulance ${count}`







    : kind === 'firebrigade' ? `Fire Tender ${count}`



    : kind === 'helicopter' ? `VIP Helicopter ${count}`







    : kind === 'qbelt' ? `Q-Belt Barrier ${count}`







    : kind === 'helicopter' ? `VIP Helicopter ${count}`
      : kind === 'parking' ? `Vehicle Parking #${count}`
      : kind === 'square_box' ? `Item Box ${count}`







    : `${kind.toUpperCase()} #${count}`;







  const duty = kind === 'officer' ? 'Security post'







    : kind === 'hhmd' ? 'Main gate — DFMD / HHMD'







    : kind === 'binocular' ? 'Binocular duty — rooftop'







    : kind === 'radio' ? 'Control & wireless duty'







    : kind === 'ambulance' ? 'Emergency Medical Response'







    : kind === 'firebrigade' ? 'Fire & Safety Standby'



    : kind === 'helicopter' ? 'VVIP Helipad Air Transit & Surveillance'







    : kind === 'qbelt' ? 'Queue & Crowd Management'







    : kind === 'helicopter' ? 'VIP Helipad Air Transit & Surveillance'
      : kind === 'parking' ? 'VIP Parking & Fleet Transit'
      : kind === 'square_box' ? 'Designated Deployment Point'







    : '';







  depItems.push({id,kind,name,duty,belt:'',mobile:'',x:controls.target.x,y:.3,z:controls.target.z,angle:0});







  depSelected=id;depNew=id;depStore();depBuild();depChoose(id);depPlace=true;depUpdate();







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







    : o.kind === 'firebrigade' ? 2.5







    : o.kind === 'ambulance' ? 1.85







    : o.kind === 'dfmd' ? 1.8







    : o.kind === 'cctv' || o.kind === 'light' ? 2.2







    : o.kind === 'barricade' ? 0.9







    : o.kind === 'square_box' ? 0.8







    : o.kind === 'qbelt' ? 0.8







    : 0.6;







  const distBehind = o.kind === 'parking' ? 18.0 : o.kind === 'firebrigade' ? 9.2







    : o.kind === 'ambulance' ? 6.8







    : isOfficerLike ? 3.8







    : ['barricade','dfmd'].includes(o.kind) ? 4.5







    : 3.2;







  const heightAbove = o.kind === 'firebrigade' ? 3.4







    : o.kind === 'ambulance' ? 2.4







    : isOfficerLike ? 1.2







    : 1.5;















  const angle=o.angle*Math.PI/180,dir=new THREE.Vector3(Math.sin(angle),0,-Math.cos(angle));







  let eyeY = o.y + itemHeight;







  if(mode === 'first'){







    if(o.kind === 'ambulance') eyeY = o.y + 1.62;







    if(o.kind === 'firebrigade') eyeY = o.y + 2.15;







  }







  const eye = new THREE.Vector3(o.x, eyeY, o.z);







  if(mode === 'first'){







    if(o.kind === 'ambulance') eye.addScaledVector(dir, 1.2);







    if(o.kind === 'firebrigade') eye.addScaledVector(dir, 2.1);







  }







  const idealCam = mode==='first' ? eye : eye.clone().addScaledVector(dir,-distBehind).add(new THREE.Vector3(0,heightAbove,0));







  const lookDistance = o.kind==='firebrigade' ? 4.8 : (o.kind==='ambulance' ? 3.8 : (mode==='first' ? 10 : 2.0));







  const targetLook = eye.clone().addScaledVector(dir, lookDistance);















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
  if (document.activeElement && typeof document.activeElement.blur === 'function') {
    document.activeElement.blur();
  }
  if (typeof renderer !== 'undefined' && renderer && renderer.domElement) {
    renderer.domElement.tabIndex = 0;
    renderer.domElement.focus();
  }
  window.focus();
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







      : kind === 'ambulance' ? `Ambulance ${count}`







      : kind === 'firebrigade' ? `Fire Tender ${count}`







      : kind === 'qbelt' ? `Q-Belt Barrier ${count}`







      : kind === 'helicopter' ? `VIP Helicopter ${count}`
      : kind === 'parking' ? `Vehicle Parking #${count}`
      : kind === 'square_box' ? `Item Box ${count}`







      : `${kind.toUpperCase()} #${count}`;







    const duty = depGetAutoDuty(Math.round(depClickPoint.x*100)/100, Math.round(depClickPoint.y*100)/100, Math.round(depClickPoint.z*100)/100, kind);
    const _ignoredDuty = kind === 'hhmd' ? 'Main gate — DFMD / HHMD'







      : kind === 'binocular' ? 'Binocular duty — rooftop'







      : kind === 'radio' ? 'Control & wireless duty'







      : kind === 'ambulance' ? 'Emergency Medical Response'







      : kind === 'firebrigade' ? 'Fire & Safety Standby'







      : kind === 'qbelt' ? 'Queue & Crowd Management'







      : kind === 'helicopter' ? 'VIP Helipad Air Transit & Surveillance'
      : kind === 'parking' ? 'VIP Parking & Fleet Transit'
      : kind === 'square_box' ? 'Designated Deployment Point'







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
  // If character is below roof level (< 7m), cast from head height (currentY + 1.8)
  // so we stay underneath ceilings/roofs inside buildings like the auditorium!
  const startY = currentY < 7.0 ? Math.min(currentY + 1.8, 6.5) : (currentY + 3.0);
  const rayOrigin = new THREE.Vector3(x, startY, z);
  const ray = new THREE.Raycaster(rayOrigin, new THREE.Vector3(0, -1, 0), 0.05, 50);
  const targets = (typeof clickable !== 'undefined' ? clickable : []).filter(m => m.visible && m.parent.visible && m !== depGroup);
  const hits = ray.intersectObjects(targets, false);
  for (const h of hits) {
    if (h.face && h.face.normal && h.face.normal.y > 0.25) {
      if (currentY < 7.0 && h.point.y > 6.8) continue; // Skip roof/ceiling surfaces when walking on ground/floor
      return h.point.y;
    }
  }
  return 0.36; // Default ground plane level
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







  if (typeof vvipActive !== 'undefined' && vvipActive) {







    if (tickVvipSimulation(dt)) needsDraw = true;







  }















  // Handle item walking/moving, turning, climbing stairs, jumping & obstacle collision



  if (depSelected) {



    const o = depItems.find(x => x.id === depSelected);



    if (o) {



      const node = depNodes.find(n => n.item.id === o.id);



      if (o.kind === 'helicopter' && node && node.g) {



        // ====================================================================



        // HELICOPTER KEYBOARD FLIGHT CONTROLS (WASD, SPACE Takeoff, RIGHT CTRL Land)



        // ====================================================================



        const groundUnder = getSurfaceHeight(o.x, o.z, o.y);



        const isGroundLevel = o.y <= groundUnder + 0.18;







        const keyAscend = !!(depKeysDown[' '] || depKeysDown['spacebar']);



        const keyDescend = !!(depKeysDown['controlright'] || depKeysDown['control']);



        const moveFwd = !!(depKeysDown['w'] || depKeysDown['arrowup']);



        const moveBack = !!(depKeysDown['s'] || depKeysDown['arrowdown']);



        const turnLeft = !!(depKeysDown['a'] || depKeysDown['arrowleft'] || depKeysDown['q']);



        const turnRight = !!(depKeysDown['d'] || depKeysDown['arrowright'] || depKeysDown['e']);



        const isShift = !!depKeysDown['shift'];







        // Steering / Heading (Yaw)



        const yawSpeed = isShift ? 75 : 50;



        if (turnLeft && !turnRight) {



          o.angle = (o.angle - yawSpeed * dt + 360) % 360;



          needsDraw = true;



        } else if (turnRight && !turnLeft) {



          o.angle = (o.angle + yawSpeed * dt) % 360;



          needsDraw = true;



        }







        // Rotor blade spin animation



        let targetRPM = (keyAscend || !isGroundLevel) ? 42 : 12;



        if (!node.g.userData._currentRPM) node.g.userData._currentRPM = 12;



        node.g.userData._currentRPM = THREE.MathUtils.lerp(node.g.userData._currentRPM, targetRPM, 1 - Math.exp(-6 * dt));



        const rotorDelta = node.g.userData._currentRPM * dt;







        if (node.g.userData.mainRotor) {



          node.g.userData.mainRotor.rotation.y += rotorDelta;



        }



        if (node.g.userData.tailRotor) {



          node.g.userData.tailRotor.rotation.x += rotorDelta * 2.2;



        }



        if (node.g.userData.rotorDisc) {



          const discOpacity = THREE.MathUtils.clamp((node.g.userData._currentRPM - 18) / 18, 0, 0.42);



          node.g.userData.rotorDisc.material.opacity = discOpacity;



          node.g.userData.rotorDisc.visible = discOpacity > 0.05;



        }







        // Take Off (SPACE) & Landing (RIGHT CONTROL)



        let climbSpeed = 0;



        const maxAscentSpeed = isShift ? 16.0 : 9.0;



        const maxDescentSpeed = isShift ? 12.0 : 7.0;







        if (keyAscend && !keyDescend) {



          climbSpeed = maxAscentSpeed;



          o.y = Math.min(260, o.y + climbSpeed * dt);



          needsDraw = true;



          depUI('status').textContent = `🚁 Helicopter Airborne! (Altitude: ${Math.round(o.y)}m) — W/S/A/D to Fly, RIGHT CTRL to Land`;



        } else if (keyDescend && !keyAscend) {



          if (o.y > groundUnder + 0.12) {



            climbSpeed = -maxDescentSpeed;



            o.y = Math.max(groundUnder + 0.05, o.y + climbSpeed * dt);



            needsDraw = true;



            depUI('status').textContent = `🚁 Helicopter Landing... (Altitude: ${Math.round(o.y)}m) — Approaching ground/helipad`;



          } else {



            o.y = groundUnder + 0.05;



            depUI('status').textContent = '🚁 Helicopter Touchdown & Landed safely on surface! Press SPACE to Take Off.';



          }



        } else if (!isGroundLevel) {



          const hoverFloat = Math.sin(Date.now() * 0.003) * 0.006;



          o.y = Math.max(groundUnder + 0.05, o.y + hoverFloat);



          needsDraw = true;



        }







        // Horizontal Forward / Backward Flight



        let flightSpeed = 0;



        const baseFlightSpeed = isShift ? 25.0 : 14.0;



        if (moveFwd && !moveBack) flightSpeed = baseFlightSpeed;



        else if (moveBack && !moveFwd) flightSpeed = -baseFlightSpeed * 0.6;







        if (Math.abs(flightSpeed) > 0.05) {



          const rad = o.angle * Math.PI / 180;



          const fwd = new THREE.Vector3(Math.sin(rad), 0, -Math.cos(rad));



          o.x += fwd.x * flightSpeed * dt;



          o.z += fwd.z * flightSpeed * dt;



          if (isGroundLevel && !keyAscend) {



            o.y = groundUnder + 0.05;



          }



          needsDraw = true;



        }







        // Realistic Aerodynamic Pitch & Roll Tilt



        let targetPitch = 0;



        if (moveFwd) targetPitch = -0.16;



        else if (moveBack) targetPitch = 0.12;







        let targetRoll = 0;



        if (turnLeft) targetRoll = -0.22;



        else if (turnRight) targetRoll = 0.22;







        if (!node.g.userData._currentPitch) node.g.userData._currentPitch = 0;



        if (!node.g.userData._currentRoll) node.g.userData._currentRoll = 0;



        node.g.userData._currentPitch = THREE.MathUtils.lerp(node.g.userData._currentPitch, targetPitch, 1 - Math.exp(-8 * dt));



        node.g.userData._currentRoll = THREE.MathUtils.lerp(node.g.userData._currentRoll, targetRoll, 1 - Math.exp(-8 * dt));







        node.g.position.set(o.x, o.y, o.z);



        node.g.rotation.set(0, 0, 0);



        node.g.rotation.y = -o.angle * Math.PI / 180;



        if (node.g.userData.heliGroup) {



          node.g.userData.heliGroup.rotation.x = node.g.userData._currentPitch;



          node.g.userData.heliGroup.rotation.z = -node.g.userData._currentRoll;



        }







        const now = Date.now();



        if (now - lastDepStoreTime > 1500) {



          lastDepStoreTime = now;



          depStore();



        }



        return;



      }







      // node already defined above







      const rig = node?.g?.userData?.rig;







      







      // ROTATION:







      // Turn left: A, ArrowLeft, or Q







      // Turn right: D, ArrowRight, or E







      const turnLeft = !!(depKeysDown['a'] || depKeysDown['arrowleft'] || depKeysDown['q']);







      const turnRight = !!(depKeysDown['d'] || depKeysDown['arrowright'] || depKeysDown['e']);







      let turnSpeed = 95; // degrees per second







      if (o.kind === 'ambulance') turnSpeed = 75;







      else if (o.kind === 'firebrigade') turnSpeed = 65;







      else if (o.kind === 'square_box' || o.kind === 'qbelt') turnSpeed = 90;















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















      let baseFwdSpeed = 3.8;







      let sprintFwdSpeed = 6.2;







      let baseBackSpeed = 2.4;















      if (o.kind === 'ambulance') {







        baseFwdSpeed = 6.8;







        sprintFwdSpeed = 11.8;







        baseBackSpeed = 3.4;







      } else if (o.kind === 'firebrigade') {







        baseFwdSpeed = 5.4;







        sprintFwdSpeed = 9.2;







        baseBackSpeed = 2.8;







      } else if (o.kind === 'square_box' || o.kind === 'qbelt' || o.kind === 'barricade') {







        baseFwdSpeed = 3.2;







        sprintFwdSpeed = 5.5;







        baseBackSpeed = 2.4;







      }















      if (moveFwd && !moveBack) moveSpeed += (isShift ? sprintFwdSpeed : baseFwdSpeed);







      if (moveBack && !moveFwd) moveSpeed -= (isShift ? (sprintFwdSpeed * 0.6) : baseBackSpeed);















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
        let wallBlocked = false;
        if (wallHits.length > 0 && Math.abs(wallHits[0].face.normal.y) < 0.4) {
          const hitObj = wallHits[0].object;
          const hitItem = hitObj?.userData?.items && hitObj.userData.items[wallHits[0].instanceId];
          const hitName = (hitItem?.name || '').toLowerCase();
          const isPassable = hitName.includes('door') || hitName.includes('glazed') || hitName.includes('entry') ||
                             hitName.includes('step') || hitName.includes('stair') || hitName.includes('rail') ||
                             hitName.includes('jamb') || hitName.includes('curtain') || hitName.includes('carpet') ||
                             hitName.includes('aisle') || hitName.includes('open') || hitName.includes('foyer') ||
                             hitName.includes('chair') || hitName.includes('seat');
          if (!isPassable) {
            wallBlocked = true;
          }
        }

        if (wallBlocked && (!depOfficerJump.isJumping || o.y < surfaceNext - 0.2)) {
          depUI('status').textContent = '⚠️ Blocked by obstacle / wall! Press SPACE to jump over.';
        } else if (heightDiff <= 0.65) {







          // Normal stair step, curb or ground ramp: climb on top smoothly!







          o.x = nextX;







          o.z = nextZ;







          if (!depOfficerJump.isJumping) {







            const stepDecay = 1 - Math.exp(-22 * dt);







            o.y = THREE.MathUtils.lerp(o.y, surfaceNext, stepDecay);
          }
          // Auto-cutaway roof when officer walks into or out of the auditorium
          const hq = geo.footprints?.find(f => f.id === 'hall')?.points;
          if (hq && o.y < 7.5 && typeof select !== 'undefined' && typeof applyView === 'function') {
            let insideAuditorium = false;
            for (let i = 0, j = hq.length - 1; i < hq.length; j = i++) {
              const a = hq[i], b = hq[j];
              if (((a[1] > o.z) !== (b[1] > o.z)) && (o.x < (b[0] - a[0]) * (o.z - a[1]) / (b[1] - a[1]) + a[0])) {
                insideAuditorium = !insideAuditorium;
              }
            }
            if (insideAuditorium && select.value !== 'hall' && select.value !== 'stage' && select.value !== 'stageplan') {
              select.value = 'hall';
              applyView();
            } else if (!insideAuditorium && (select.value === 'hall' || select.value === 'stage')) {
              select.value = 'campus';
              applyView();
            }
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















        // Auto-update duty when officer walks into a new duty zone (unless user set custom duty)
        if (['officer', 'hhmd', 'binocular', 'radio'].includes(o.kind)) {
          if (!o.customDuty) {
            const autoDuty = depGetAutoDuty(o.x, o.y, o.z, o.kind);
            if (autoDuty && autoDuty !== o.duty) {
              o.duty = autoDuty;
              depSyncDropdownLabels(o);
            }
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















      // Animate vehicle wheels (Ambulance / Fire Brigade)







      if (node?.g?.userData?.wheels && isMoving) {







        const wheelRadius = o.kind === 'firebrigade' ? 0.52 : 0.38;







        const wheelRot = (moveSpeed * dt) / wheelRadius;







        for (const w of node.g.userData.wheels) {







          w.rotation.x += wheelRot;







        }







        needsDraw = true;







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







          : o.kind === 'firebrigade' ? 2.5







          : o.kind === 'ambulance' ? 1.85







          : o.kind === 'dfmd' ? 1.8







          : o.kind === 'cctv' || o.kind === 'light' ? 2.2







          : o.kind === 'barricade' ? 0.9







          : o.kind === 'square_box' ? 0.8







          : o.kind === 'qbelt' ? 0.8







          : 0.6;







        const distBehind = o.kind === 'parking' ? 18.0 : o.kind === 'firebrigade' ? 9.2







          : o.kind === 'ambulance' ? 6.8







          : isOfficerLike ? 3.8







          : ['barricade','dfmd'].includes(o.kind) ? 4.5







          : 3.2;







        const heightAbove = o.kind === 'firebrigade' ? 3.4







          : o.kind === 'ambulance' ? 2.4







          : isOfficerLike ? 1.2







          : 1.5;















        const eye = new THREE.Vector3(o.x, o.y + itemHeight, o.z);







        const idealCam = eye.clone().addScaledVector(dir, -distBehind).add(new THREE.Vector3(0, heightAbove, 0));







        const lookDist = o.kind === 'firebrigade' ? 4.8 : (o.kind === 'ambulance' ? 3.8 : 2.0);







        const targetLook = eye.clone().addScaledVector(dir, lookDist);















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















  // Live emergency vehicle strobe lights animation







  const nowBeaconSec = Date.now() * 0.008;







  for (const {item, g} of depNodes) {







    if (g?.userData?.beacons) {







      for (const b of g.userData.beacons) {







        const pulse = Math.sin(nowBeaconSec * b.speed + b.phase) > 0.15;







        b.mat.emissiveIntensity = pulse ? b.intensity : 0.08;







      }







      needsDraw = true;







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
        if (!o.customDuty) {
          o.duty=depGetAutoDuty(o.x, o.y, o.z, o.kind);
        }
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















  // Spacebar: Take off for helicopter / Jump for officer!



  if (key === ' ' || key === 'spacebar' || e.code === 'Space') {



    if (depSelected) {



      const o = depItems.find(o => o.id === depSelected);



      if (o) {



        e.preventDefault();



        e.stopPropagation();



        if (o.kind !== 'helicopter') {



          triggerOfficerJump(o);



        }



        return;



      }



    }



  }







  // Right Control / Control: Landing for helicopter!



  if (e.code === 'ControlRight' || (key === 'control' && e.location === 2) || key === 'controlright') {



    depKeysDown['controlright'] = true;



    depKeysDown['control'] = true;



    if (depSelected) {



      const o = depItems.find(o => o.id === depSelected);



      if (o && o.kind === 'helicopter') {



        e.preventDefault();



        e.stopPropagation();



        return;



      }



    }



  } else if (key === 'control') {



    depKeysDown['control'] = true;



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



  if (e.code === 'ControlRight' || (key === 'control' && e.location === 2) || key === 'controlright') {



    depKeysDown['controlright'] = false;



    depKeysDown['control'] = false;



  } else if (key === 'control') {



    depKeysDown['control'] = false;



  }







  if (['w','a','s','d','arrowup','arrowdown','arrowleft','arrowright','q','e','shift'].includes(key)) {







    if (depSelected) depStore();







  }







});















window.addEventListener('blur', () => {







  for (const k in depKeysDown) {







    depKeysDown[k] = false;







  }







});















function depHit(e){

  const r = canvas.getBoundingClientRect(), raycaster = new THREE.Raycaster();

  raycaster.setFromCamera(new THREE.Vector2((e.clientX - r.left) / r.width * 2 - 1, 1 - (e.clientY - r.top) / r.height * 2), camera);



  // 1. Direct 3D intersection on all deployed items (Helicopter, Officer, Ambulance, Fire Brigade, etc.)

  const hits = raycaster.intersectObject(depGroup, true);

  for (const h of hits) {

    if (!h.object.visible && !h.object.userData.isHitBox) continue;

    let obj = h.object;

    while (obj && !obj.userData.depId && obj !== depGroup) {

      obj = obj.parent;

    }

    if (obj?.userData?.depId) {

      return obj.userData.depId;

    }

  }



  // 2. Also detect clicks directly on the helipad circle

  if (typeof clickable !== 'undefined' && clickable.length) {

    const venueHits = raycaster.intersectObjects(clickable.filter(m => m.visible && m.parent.visible), false);

    if (venueHits.length > 0) {

      const p = venueHits[0].point;

      const distToHelipad = Math.hypot(p.x - (-21.82), p.z - (-164.66));

      if (distToHelipad <= 18.0) {

        const heli = depItems.find(o => o.kind === 'helicopter');

        if (heli) return heli.id;

      }

    }

  }



  return null;

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

    updateTabLock();

    const id = depHit(e);

    if(id){

      depChoose(id, true);

      return;

    }

    if(depSelected){

      depDeselect(true);

      return;

    }

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















depReady=true;depBuild();if(typeof restoreStaticHelicopter==='function'){try{restoreStaticHelicopter();}catch(e){}}















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







    if(local&&local.items&&local.items.length>=(backendItems?backendItems.length:0)&&localTime>backendTime+2000){







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







  if(depBackendURL&&depItems.length>0){







    const payload=depPayload();







    const body=JSON.stringify({revision:depRevision,plan:payload});







    try{







      if(navigator.sendBeacon){







        const blob=new Blob([body],{type:'application/json'});







        navigator.sendBeacon(depBackendURL,blob);







      }else{







        fetch(depBackendURL,{







          method:'POST',







          headers:{'Content-Type':'application/json','X-GMS-Plan':'1'},







          body:body,







          keepalive:true







        });







      }







    }catch(e){}







  }







}







window.addEventListener('beforeunload',depSaveBeforeLeave);







window.addEventListener('pagehide',depSaveBeforeLeave);















depUI('retry').onclick=()=>depBackendReady?depFlush():depLoadBackend();







depLoadBackend();























// ============================================================================







// 🎖️ VVIP SIMULATION PROTOCOL (Helicopter, Motorcade, Barricades & Main Stage Arrival)







// ============================================================================







var vvipActive = false;







let vvipPhase = 0; // 1: Heli flight/landing, 2: Walk to road, 3: Motorcade transit, 4: Gate barricade/stop, 5: Hall walk & stage seating, 6: Completed







let vvipPhaseTimer = 0;







let vvipWalkCycle = 0;







let vvipGroup = null;







let vvipHeli = null;







let vvipFemale = null;







let vvipEscort1 = null;







let vvipEscort2 = null;







let vvipCar = null;







let vvipRenderSettings=null;







let vvipBarricades = null;







let vvipRoutePolice = null;







let vvipStageChair = null;







let vvipSavedCamera = null;







let vvipSavedTarget = null;







vvipSavedView = null;







vvipHiddenHelicopterMatrices = [];















function hideStaticHelicopter() {







  vvipHiddenHelicopterMatrices = [];







  const zeroMatrix = new THREE.Matrix4().makeScale(0, 0, 0);







  scene.traverse(node => {







    if (node.isInstancedMesh && node.userData && Array.isArray(node.userData.items)) {







      node.userData.items.forEach((item, idx) => {







        if (item.name && item.name.includes('Parked helicopter')) {







          const original = new THREE.Matrix4();







          node.getMatrixAt(idx, original);







          vvipHiddenHelicopterMatrices.push({ mesh: node, index: idx, matrix: original });







          node.setMatrixAt(idx, zeroMatrix);







          node.instanceMatrix.needsUpdate = true;







        }







      });







    }







  });







}















function restoreStaticHelicopter() {







  vvipHiddenHelicopterMatrices.forEach(({ mesh, index, matrix }) => {







    mesh.setMatrixAt(index, matrix);







    mesh.instanceMatrix.needsUpdate = true;







  });







  vvipHiddenHelicopterMatrices = [];







}















function buildVvipHelicopter() {







  const g = new THREE.Group();







  







  // Fuselage body (aerodynamic)







  const bodyUpper = new THREE.Mesh(geos.box, depMaterials.heliWhite);







  bodyUpper.position.set(0, 1.8, 0);







  bodyUpper.scale.set(1.9, 1.3, 5.2);







  bodyUpper.castShadow = true;







  g.add(bodyUpper);







  







  const bodyNose = new THREE.Mesh(geos.sphereSmooth, depMaterials.heliWhite);







  bodyNose.position.set(0, 1.7, 2.5);







  bodyNose.scale.set(0.94, 0.7, 1.2);







  bodyNose.castShadow = true;







  g.add(bodyNose);







  







  const bodyLower = new THREE.Mesh(geos.box, depMaterials.heliNavy);







  bodyLower.position.set(0, 1.15, 0.1);







  bodyLower.scale.set(1.85, 0.65, 4.8);







  bodyLower.castShadow = true;







  g.add(bodyLower);







  







  // Gold cheatline stripe







  const stripe = new THREE.Mesh(geos.box, depMaterials.vipGold);







  stripe.position.set(0, 1.48, 0.1);







  stripe.scale.set(1.92, 0.1, 4.9);







  g.add(stripe);







  







  // Cockpit canopy tinted glass







  const cockpit = new THREE.Mesh(geos.sphereSmooth, depMaterials.vipGlass);







  cockpit.position.set(0, 1.85, 2.0);







  cockpit.scale.set(0.92, 0.65, 1.3);







  g.add(cockpit);







  







  // Passenger side windows







  for (let z of [-0.6, 0.4]) {







    const winL = new THREE.Mesh(geos.box, depMaterials.vipGlass);







    winL.position.set(-0.96, 1.85, z);







    winL.scale.set(0.04, 0.5, 0.7);







    g.add(winL);







    const winR = winL.clone();







    winR.position.x = 0.96;







    g.add(winR);







  }







  







  // Tail boom & vertical stabilizer







  const tailBoom = new THREE.Mesh(geos.cylinder, depMaterials.heliWhite);







  tailBoom.position.set(0, 1.85, -4.5);







  tailBoom.rotation.x = Math.PI / 2;







  tailBoom.scale.set(0.35, 4.6, 0.35);







  tailBoom.castShadow = true;







  g.add(tailBoom);







  







  const tailFin = new THREE.Mesh(geos.box, depMaterials.heliNavy);







  tailFin.position.set(0, 2.7, -6.6);







  tailFin.rotation.x = -0.25;







  tailFin.scale.set(0.12, 1.5, 1.0);







  tailFin.castShadow = true;







  g.add(tailFin);







  







  // Tail rotor







  const tailRotorGrp = new THREE.Group();







  tailRotorGrp.position.set(0.12, 3.2, -6.9);







  const trBlade1 = new THREE.Mesh(geos.box, depMaterials.heliRotor);







  trBlade1.scale.set(0.04, 1.1, 0.12);







  const trBlade2 = trBlade1.clone();







  trBlade2.rotation.x = Math.PI / 2;







  tailRotorGrp.add(trBlade1, trBlade2);







  g.add(tailRotorGrp);







  g.userData.tailRotor = tailRotorGrp;







  







  // Main Rotor Mast & Assembly







  const mast = new THREE.Mesh(geos.cylinder, depMaterials.vipChrome);







  mast.position.set(0, 2.65, 0.4);







  mast.scale.set(0.12, 0.7, 0.12);







  g.add(mast);







  







  const mainRotorGrp = new THREE.Group();







  mainRotorGrp.position.set(0, 3.0, 0.4);







  







  // 4 rotor blades with aerodynamic cuffs and yellow tips







  for (let i = 0; i < 4; i++) {







    const bGrp = new THREE.Group();







    bGrp.rotation.y = (i * Math.PI) / 2;







    const blade = new THREE.Mesh(geos.box, depMaterials.heliRotor);







    blade.position.set(0, 0, 2.7);







    blade.scale.set(0.24, 0.04, 5.0);







    blade.castShadow = true;







    const tip = new THREE.Mesh(geos.box, depMaterials.barricadeYellow);







    tip.position.set(0, 0, 5.1);







    tip.scale.set(0.25, 0.042, 0.4);







    bGrp.add(blade, tip);







    mainRotorGrp.add(bGrp);







  }







  g.add(mainRotorGrp);







  g.userData.mainRotor = mainRotorGrp;







  







  // Spinning semi-transparent rotor disc for motion blur







  const discGeo = new THREE.CircleGeometry(5.4, 32);







  const discMat = new THREE.MeshBasicMaterial({







    color: 0x27272a,







    transparent: true,







    opacity: 0.28,







    side: THREE.DoubleSide







  });







  const rotorDisc = new THREE.Mesh(discGeo, discMat);







  rotorDisc.rotation.x = Math.PI / 2;







  rotorDisc.position.set(0, 3.01, 0.4);







  g.add(rotorDisc);







  g.userData.rotorDisc = rotorDisc;







  







  // Tubular landing skids







  for (let sign of [-1, 1]) {







    const skid = new THREE.Mesh(geos.cylinder, depMaterials.vipChrome);







    skid.position.set(sign * 1.05, 0.12, 0.2);







    skid.rotation.x = Math.PI / 2;







    skid.scale.set(0.06, 5.2, 0.06);







    skid.castShadow = true;







    g.add(skid);







    







    // Front upturned skid tip







    const tip = new THREE.Mesh(geos.sphereSmooth, depMaterials.vipChrome);







    tip.position.set(sign * 1.05, 0.35, 2.7);







    tip.scale.set(0.06, 0.18, 0.12);







    g.add(tip);







    







    // Cross struts connecting skid to body







    for (let z of [-1.2, 1.4]) {







      const strut = new THREE.Mesh(geos.cylinder, depMaterials.vipChrome);







      strut.position.set(sign * 0.55, 0.55, z);







      strut.rotation.z = sign * -0.55;







      strut.scale.set(0.05, 1.1, 0.05);







      g.add(strut);







    }







  }







  







  // Nav strobes (left red, right green, tail white)







  const strobeL = new THREE.Mesh(geos.sphereSmooth, depMaterials.vipBeaconRed);







  strobeL.position.set(-1.1, 1.5, 0);







  strobeL.scale.set(0.08, 0.08, 0.08);







  const strobeR = new THREE.Mesh(geos.sphereSmooth, depMaterials.vipBeaconBlue);







  strobeR.position.set(1.1, 1.5, 0);







  strobeR.scale.set(0.08, 0.08, 0.08);







  const strobeTail = new THREE.Mesh(geos.sphereSmooth, depMaterials.white);







  strobeTail.position.set(0, 3.5, -6.6);







  strobeTail.scale.set(0.1, 0.1, 0.1);







  g.add(strobeL, strobeR, strobeTail);







  







  return g;







}















function buildFemaleVvip() {







  const g = new THREE.Group();







  







  // Head & Face







  const head = new THREE.Mesh(geos.sphereSmooth, depMaterials.skin);







  head.position.set(0, 1.58, 0);







  head.scale.set(0.12, 0.14, 0.12);







  head.castShadow = true;







  g.add(head);







  







  // Hair bun (royal chignon with gajra flower garland)







  const hair = new THREE.Mesh(geos.sphereSmooth, depMaterials.hair);







  hair.position.set(0, 1.61, -0.05);







  hair.scale.set(0.13, 0.13, 0.12);







  g.add(hair);







  







  const gajra = new THREE.Mesh(geos.torus, depMaterials.white);







  gajra.position.set(0, 1.58, -0.14);







  gajra.rotation.y = Math.PI / 2;







  gajra.scale.set(0.07, 0.07, 0.03);







  g.add(gajra);







  







  // Gold earrings







  const earL = new THREE.Mesh(geos.sphereSmooth, depMaterials.vipGold);







  earL.position.set(-0.13, 1.56, 0);







  earL.scale.set(0.025, 0.04, 0.025);







  const earR = earL.clone();







  earR.position.x = 0.13;







  g.add(earL, earR);







  







  // Torso / Saree Blouse (Rich Maroon Silk)







  const torso = new THREE.Mesh(geos.cylinder, depMaterials.vipSaree);







  torso.position.set(0, 1.25, 0);







  torso.scale.set(0.18, 0.45, 0.13);







  torso.castShadow = true;







  g.add(torso);







  







  // Gold ceremonial necklace







  const neck = new THREE.Mesh(geos.torus, depMaterials.vipGold);







  neck.position.set(0, 1.42, 0.05);







  neck.rotation.x = 0.6;







  neck.scale.set(0.1, 0.1, 0.025);







  g.add(neck);







  







  // Flowing silk pallu draped across shoulder and cascading back







  const pallu = new THREE.Mesh(geos.box, depMaterials.vipPallu);







  pallu.position.set(0.08, 1.15, -0.08);







  pallu.rotation.z = -0.15;







  pallu.scale.set(0.16, 0.65, 0.05);







  pallu.castShadow = true;







  g.add(pallu);







  







  // Saree Waist & Golden border







  const waist = new THREE.Mesh(geos.cylinder, depMaterials.vipGold);







  waist.position.set(0, 1.02, 0);







  waist.scale.set(0.2, 0.08, 0.15);







  g.add(waist);







  







  // Full-length saree drape, maroon pallu and a gold lower border.







  const drape=new THREE.Mesh(new THREE.CylinderGeometry(.20,.30,.94,24),depMaterials.vipSaree);drape.position.y=.55;drape.castShadow=true;g.add(drape);







  const hem=new THREE.Mesh(new THREE.CylinderGeometry(.295,.30,.055,24),depMaterials.vipGold);hem.position.y=.105;g.add(hem);







  for(let i=-3;i<=3;i++){const pleat=new THREE.Mesh(geos.box,depMaterials.vipPallu);pleat.position.set(i*.035,.54,.245);pleat.scale.set(.012,.78,.018);g.add(pleat);}







  const sash=new THREE.Mesh(geos.box,depMaterials.vipPallu);sash.position.set(.015,1.25,.14);sash.rotation.z=-.5;sash.scale.set(.18,.52,.035);g.add(sash);







  // Legs (articulated for walking)







  const leftLegGrp = new THREE.Group();







  leftLegGrp.position.set(-0.09, 0.98, 0);







  const leftSaree = new THREE.Mesh(geos.cylinder, depMaterials.vipSaree);







  leftSaree.position.set(0, -0.45, 0);







  leftSaree.scale.set(0.095, 0.9, 0.095);







  leftSaree.castShadow = true;







  const leftGoldBorder = new THREE.Mesh(geos.cylinder, depMaterials.vipGold);







  leftGoldBorder.position.set(0, -0.86, 0);







  leftGoldBorder.scale.set(0.105, 0.08, 0.105);







  const leftFoot = new THREE.Mesh(geos.box, depMaterials.vipGold);







  leftFoot.position.set(0, -0.94, 0.06);







  leftFoot.scale.set(0.08, 0.06, 0.16);







  leftLegGrp.add(leftSaree, leftGoldBorder, leftFoot);







  g.add(leftLegGrp);







  







  const rightLegGrp = new THREE.Group();







  rightLegGrp.position.set(0.09, 0.98, 0);







  const rightSaree = leftSaree.clone();







  const rightGoldBorder = leftGoldBorder.clone();







  const rightFoot = leftFoot.clone();







  rightLegGrp.add(rightSaree, rightGoldBorder, rightFoot);







  g.add(rightLegGrp);







  







  // Arms (articulated for walking)







  const leftArmGrp = new THREE.Group();







  leftArmGrp.position.set(-0.22, 1.4, 0);







  const leftArm = new THREE.Mesh(geos.cylinder, depMaterials.skin);







  leftArm.position.set(0, -0.28, 0);







  leftArm.scale.set(0.045, 0.55, 0.045);







  const leftBangle = new THREE.Mesh(geos.torus, depMaterials.vipGold);







  leftBangle.position.set(0, -0.48, 0);







  leftBangle.rotation.x = Math.PI / 2;







  leftBangle.scale.set(0.05, 0.05, 0.015);







  leftArmGrp.add(leftArm, leftBangle);







  g.add(leftArmGrp);







  







  const rightArmGrp = new THREE.Group();







  rightArmGrp.position.set(0.22, 1.4, 0);







  const rightArm = leftArm.clone();







  const rightBangle = leftBangle.clone();







  rightArmGrp.add(rightArm, rightBangle);







  g.add(rightArmGrp);







  







  g.userData.leftLeg = leftLegGrp;







  g.userData.rightLeg = rightLegGrp;







  g.userData.leftArm = leftArmGrp;







  g.userData.rightArm = rightArmGrp;







  g.userData.baseY = 0;







  







  g.userData.animateWalk = function(phase) {







    const swing = Math.sin(phase) * 0.22;







    leftLegGrp.rotation.x = swing;







    rightLegGrp.rotation.x = -swing;







    leftArmGrp.rotation.x = -swing * 0.75;







    rightArmGrp.rotation.x = swing * 0.75;







  };







  







  g.userData.setSeated = function(seated) {







    if (seated) {







      leftLegGrp.rotation.x = -Math.PI / 2.3;







      rightLegGrp.rotation.x = -Math.PI / 2.3;







      leftArmGrp.rotation.x = -0.3;







      rightArmGrp.rotation.x = -0.3;







      g.position.y = 1.80 + 0.35; // Seated height on stage chair







    } else {







      leftLegGrp.rotation.x = 0;







      rightLegGrp.rotation.x = 0;







      leftArmGrp.rotation.x = 0;







      rightArmGrp.rotation.x = 0;







    }







  };







  







  return g;







}















function buildSecurityEscort() {







  const g = new THREE.Group();







  const head = new THREE.Mesh(geos.sphereSmooth, depMaterials.skin);







  head.position.set(0, 1.66, 0);







  head.scale.set(0.12, 0.14, 0.12);







  head.castShadow = true;







  g.add(head);







  







  const hair = new THREE.Mesh(geos.box, depMaterials.hair);







  hair.position.set(0, 1.74, -0.02);







  hair.scale.set(0.24, 0.08, 0.24);







  g.add(hair);







  







  const shades = new THREE.Mesh(geos.box, depMaterials.dark);







  shades.position.set(0, 1.67, 0.12);







  shades.scale.set(0.21, 0.05, 0.05);







  g.add(shades);







  







  const torso = new THREE.Mesh(geos.box, depMaterials.dark);







  torso.position.set(0, 1.25, 0);







  torso.scale.set(0.44, 0.6, 0.24);







  torso.castShadow = true;







  g.add(torso);







  







  const shirt = new THREE.Mesh(geos.box, depMaterials.white);







  shirt.position.set(0, 1.38, 0.11);







  shirt.scale.set(0.16, 0.28, 0.04);







  const tie = new THREE.Mesh(geos.box, depMaterials.red);







  tie.position.set(0, 1.3, 0.13);







  tie.scale.set(0.06, 0.25, 0.02);







  g.add(shirt, tie);







  







  const leftLeg = new THREE.Group();







  leftLeg.position.set(-0.12, 0.95, 0);







  const lMesh = new THREE.Mesh(geos.cylinder, depMaterials.dark);







  lMesh.position.set(0, -0.45, 0);







  lMesh.scale.set(0.09, 0.9, 0.09);







  lMesh.castShadow = true;







  leftLeg.add(lMesh);







  g.add(leftLeg);







  







  const rightLeg = new THREE.Group();







  rightLeg.position.set(0.12, 0.95, 0);







  const rMesh = lMesh.clone();







  rightLeg.add(rMesh);







  g.add(rightLeg);







  







  const leftArm = new THREE.Group();







  leftArm.position.set(-0.28, 1.45, 0);







  const laMesh = new THREE.Mesh(geos.cylinder, depMaterials.dark);







  laMesh.position.set(0, -0.28, 0);







  laMesh.scale.set(0.06, 0.55, 0.06);







  leftArm.add(laMesh);







  g.add(leftArm);







  







  const rightArm = new THREE.Group();







  rightArm.position.set(0.28, 1.45, 0);







  const raMesh = laMesh.clone();







  rightArm.add(raMesh);







  g.add(rightArm);







  







  g.userData.animateWalk = function(phase) {







    const swing = Math.sin(phase) * 0.38;







    leftLeg.rotation.x = swing;







    rightLeg.rotation.x = -swing;







    leftArm.rotation.x = -swing * 0.6;







    rightArm.rotation.x = swing * 0.6;







  };







  return g;







}















function buildVvipCar() {







  const g = new THREE.Group();







  







  // Lower body chassis (Luxury Obsidian Black)







  const chassis = new THREE.Mesh(geos.box, depMaterials.vipCar);







  chassis.position.set(0, 0.65, 0);







  chassis.scale.set(2.1, 0.7, 5.2);







  chassis.castShadow = true;







  g.add(chassis);







  







  // Upper cabin







  const cabin = new THREE.Mesh(geos.box, depMaterials.vipCar);







  cabin.position.set(0, 1.25, -0.2);







  cabin.scale.set(1.9, 0.65, 2.9);







  cabin.castShadow = true;







  g.add(cabin);







  







  // Tinted windshield & rear glass







  const frontGlass = new THREE.Mesh(geos.box, depMaterials.vipGlass);







  frontGlass.position.set(0, 1.22, 1.3);







  frontGlass.rotation.x = 0.35;







  frontGlass.scale.set(1.82, 0.6, 0.1);







  const rearGlass = new THREE.Mesh(geos.box, depMaterials.vipGlass);







  rearGlass.position.set(0, 1.22, -1.7);







  rearGlass.rotation.x = -0.35;







  rearGlass.scale.set(1.82, 0.6, 0.1);







  g.add(frontGlass, rearGlass);







  







  // Rear passenger door has its own front hinge and moves with its glass/handle.







  const doorPivot=new THREE.Group();doorPivot.position.set(-1.07,.4,-.05);g.add(doorPivot);







  for(const [y,z,h,mat] of [[.35,-.65,.65,depMaterials.vipCar],[.86,-.65,.48,depMaterials.vipGlass]]){







    const panel=new THREE.Mesh(geos.box,mat);panel.position.set(0,y,z);panel.scale.set(.065,h,1.25);doorPivot.add(panel);







  }







  const doorHandle=new THREE.Mesh(geos.box,depMaterials.vipChrome);doorHandle.position.set(-.055,.6,-1.07);doorHandle.scale.set(.06,.06,.25);doorPivot.add(doorHandle);







  g.userData.setPassengerDoor=t=>{doorPivot.rotation.y=THREE.MathUtils.smoothstep(t,0,1)*1.2;g.userData.doorOpen=t;};







  g.userData.passengerDoor=doorPivot;







  // Narrow cabin core leaves room for the hinged door; roof and opposite glass stay fixed.







  cabin.scale.x=1.72;







  for(const [x,z,len] of [[.96,-.2,2.7],[-.96,.65,1.0]]){







    const glass=new THREE.Mesh(geos.box,depMaterials.vipGlass);glass.position.set(x,1.25,z);glass.scale.set(.04,.5,len);g.add(glass);







  }







  g.userData.passengerPoint=()=>g.localToWorld(new THREE.Vector3(-1.65,0,-.75));















  // Chrome front grille







  const grille = new THREE.Mesh(geos.box, depMaterials.vipChrome);







  grille.position.set(0, 0.65, 2.62);







  grille.scale.set(1.2, 0.45, 0.08);







  g.add(grille);







  







  // Headlights & Taillights







  for (let sign of [-1, 1]) {







    const hl = new THREE.Mesh(geos.box, depMaterials.white);







    hl.position.set(sign * 0.78, 0.7, 2.62);







    hl.scale.set(0.35, 0.2, 0.08);







    g.add(hl);







    







    const tl = new THREE.Mesh(geos.box, depMaterials.red);







    tl.position.set(sign * 0.78, 0.75, -2.62);







    tl.scale.set(0.35, 0.18, 0.08);







    g.add(tl);







  }







  







  // VIP Official Flag mast on front left hood







  const mast = new THREE.Mesh(geos.cylinder, depMaterials.vipChrome);







  mast.position.set(-0.85, 1.2, 2.1);







  mast.scale.set(0.02, 0.6, 0.02);







  const flag = new THREE.Mesh(geos.box, depMaterials.red);







  flag.position.set(-0.85, 1.4, 2.22);







  flag.scale.set(0.02, 0.18, 0.25);







  g.add(mast, flag);







  







  // Roof-mounted VIP Flashing Beacon







  const beaconBase = new THREE.Mesh(geos.box, depMaterials.dark);







  beaconBase.position.set(0, 1.62, -0.2);







  beaconBase.scale.set(0.65, 0.06, 0.18);







  const beaconR = new THREE.Mesh(geos.cylinder, depMaterials.vipBeaconRed);







  beaconR.position.set(-0.2, 1.69, -0.2);







  beaconR.scale.set(0.08, 0.09, 0.08);







  const beaconB = new THREE.Mesh(geos.cylinder, depMaterials.vipBeaconBlue);







  beaconB.position.set(0.2, 1.69, -0.2);







  beaconB.scale.set(0.08, 0.09, 0.08);







  g.add(beaconBase, beaconR, beaconB);







  







  // 4 Alloy Wheels with tire rotation







  const wheels = [];







  const wheelPositions = [







    [-1.02, 0.38, 1.6],







    [1.02, 0.38, 1.6],







    [-1.02, 0.38, -1.6],







    [1.02, 0.38, -1.6]







  ];







  wheelPositions.forEach(pos => {







    const wGrp = new THREE.Group();







    wGrp.position.fromArray(pos);







    const tire = new THREE.Mesh(geos.cylinder, depMaterials.dark);







    tire.rotation.z = Math.PI / 2;







    tire.scale.set(0.38, 0.28, 0.38);







    tire.castShadow = true;







    const rim = new THREE.Mesh(geos.cylinder, depMaterials.vipChrome);







    rim.rotation.z = Math.PI / 2;







    rim.scale.set(0.24, 0.3, 0.24);







    wGrp.add(tire, rim);







    g.add(wGrp);







    wheels.push(wGrp);







  });







  g.userData.wheels = wheels;







  







  g.userData.rollWheels = function(deltaDist) {







    const rad = deltaDist / 0.38;







    wheels.forEach(w => {







      w.rotation.x += rad;







    });







  };







  







  return g;







}















function buildRouteOfficer(salute = false) {







  const g = new THREE.Group();







  const head = new THREE.Mesh(geos.sphereSmooth, depMaterials.skin);







  head.position.set(0, 1.66, 0);







  head.scale.set(0.12, 0.14, 0.12);







  head.castShadow = true;







  g.add(head);







  







  const cap = new THREE.Mesh(geos.cylinder, depMaterials.blue);







  cap.position.set(0, 1.76, 0);







  cap.scale.set(0.15, 0.07, 0.15);







  const capBand = new THREE.Mesh(geos.cylinder, depMaterials.red);







  capBand.position.set(0, 1.73, 0);







  capBand.scale.set(0.155, 0.025, 0.155);







  const visor = new THREE.Mesh(geos.box, depMaterials.dark);







  visor.position.set(0, 1.72, 0.13);







  visor.scale.set(0.18, 0.02, 0.08);







  g.add(cap, capBand, visor);







  







  const torso = new THREE.Mesh(geos.box, depMaterials.khaki);







  torso.position.set(0, 1.25, 0);







  torso.scale.set(0.42, 0.58, 0.22);







  torso.castShadow = true;







  const belt = new THREE.Mesh(geos.box, depMaterials.dark);







  belt.position.set(0, 0.98, 0);







  belt.scale.set(0.44, 0.08, 0.24);







  const buckle = new THREE.Mesh(geos.box, depMaterials.yellow);







  buckle.position.set(0, 0.98, 0.125);







  buckle.scale.set(0.08, 0.07, 0.02);







  g.add(torso, belt, buckle);







  







  for (let sign of [-1, 1]) {







    const leg = new THREE.Mesh(geos.cylinder, depMaterials.trousers);







    leg.position.set(sign * 0.11, 0.48, 0);







    leg.scale.set(0.09, 0.92, 0.09);







    leg.castShadow = true;







    const boot = new THREE.Mesh(geos.box, depMaterials.dark);







    boot.position.set(sign * 0.11, 0.05, 0.04);







    boot.scale.set(0.1, 0.09, 0.2);







    g.add(leg, boot);







  }







  







  const leftArm = new THREE.Mesh(geos.cylinder, depMaterials.khaki);







  leftArm.position.set(-0.26, 1.2, 0);







  leftArm.scale.set(0.065, 0.52, 0.065);







  g.add(leftArm);







  







  const rightArm = new THREE.Mesh(geos.cylinder, depMaterials.khaki);







  if (salute) {







    rightArm.position.set(0.24, 1.48, 0.06);







    rightArm.rotation.z = -1.1;







    rightArm.rotation.y = 0.4;







    rightArm.scale.set(0.06, 0.48, 0.06);







  } else {







    rightArm.position.set(0.26, 1.2, 0);







    rightArm.scale.set(0.065, 0.52, 0.065);







  }







  g.add(rightArm);







  return g;







}















function buildRoadBarricades() {







  const g = new THREE.Group();







  







  function makeBarricade(x, y, z, angle) {







    const b = new THREE.Group();







    b.position.set(x, y, z);







    b.rotation.y = angle;







    







    const frame = new THREE.Mesh(geos.box, depMaterials.barricadeYellow);







    frame.position.set(0, 0.65, 0);







    frame.scale.set(3.6, 1.1, 0.12);







    frame.castShadow = true;







    b.add(frame);







    







    // Alert beacon







    const beacon = new THREE.Mesh(geos.cylinder, depMaterials.vipBeaconRed);







    beacon.position.set(0, 1.3, 0);







    beacon.scale.set(0.12, 0.18, 0.12);







    b.add(beacon);







    







    for (let sign of [-1, 1]) {







      const leg = new THREE.Mesh(geos.box, depMaterials.barricadeDark);







      leg.position.set(sign * 1.6, 0.15, 0);







      leg.scale.set(0.15, 0.3, 0.85);







      b.add(leg);







    }







    







    const cop = buildRouteOfficer(true);







    cop.position.set(1.9, 0, 0.4);







    cop.rotation.y = -Math.PI / 2;







    b.add(cop);







    







    return b;







  }







  







  // North barricade across main road (at X = -32, Z = -65)







  const bNorth = makeBarricade(-32, 0, -65, 0);







  // South barricade across main road (at X = 8, Z = -65)







  const bSouth = makeBarricade(8, 0, -65, 0);







  







  g.add(bNorth, bSouth);







  return g;







}















function buildRoutePolice() {







  const g = new THREE.Group();







  // Helipad perimeter guards







  const heliGuards = [







    [-42, 0.36, -145, 0.8],







    [-45, 0.36, -182, 0.8],







    [-2, 0.36, -185, -0.8],







    [3, 0.36, -148, -0.8]







  ];







  heliGuards.forEach(([x, y, z, rot]) => {







    const p = buildRouteOfficer(false);







    p.position.set(x, y, z);







    p.rotation.y = rot;







    g.add(p);







  });







  







  // Helipad road access guards







  const roadGuards = [







    [-21, 0.36, -138, 0.2],







    [-17, 0.36, -138, -0.2]







  ];







  roadGuards.forEach(([x, y, z, rot]) => {







    const p = buildRouteOfficer(true);







    p.position.set(x, y, z);







    p.rotation.y = rot;







    g.add(p);







  });







  







  // Main gate guards







  const gateGuards = [







    [-15.5, 0.36, -65, Math.PI / 2],







    [-10.0, 0.36, -65, -Math.PI / 2]







  ];







  gateGuards.forEach(([x, y, z, rot]) => {







    const p = buildRouteOfficer(true);







    p.position.set(x, y, z);







    p.rotation.y = rot;







    g.add(p);







  });







  







  // Auditorium entry guards







  const auditGuards = [







    [-18.5, 0.36, 1.86, 0],







    [-21.5, 0.36, 1.86, 0]







  ];







  auditGuards.forEach(([x, y, z, rot]) => {







    const p = buildRouteOfficer(true);







    p.position.set(x, y, z);







    p.rotation.y = rot;







    g.add(p);







  });







  







  // Stage side guards







  const stageGuards = [







    [-41.5, 1.80, -47.0, Math.PI / 2],







    [-35.5, 1.80, -47.0, -Math.PI / 2]







  ];







  stageGuards.forEach(([x, y, z, rot]) => {







    const p = buildRouteOfficer(false);







    p.position.set(x, y, z);







    p.rotation.y = rot;







    g.add(p);







  });







  







  return g;







}















function buildStageChair() {







  const g = new THREE.Group();







  const seat = new THREE.Mesh(geos.box, depMaterials.stageSofaRed);







  seat.position.set(0, 0.5, 0);







  seat.scale.set(1.4, 0.35, 1.1);







  seat.castShadow = true;







  g.add(seat);







  







  const back = new THREE.Mesh(geos.box, depMaterials.stageSofaRed);







  back.position.set(0, 1.3, -0.45);







  back.scale.set(1.4, 1.3, 0.25);







  back.castShadow = true;







  g.add(back);







  







  const crown = new THREE.Mesh(geos.box, depMaterials.stageSofaGold);







  crown.position.set(0, 1.98, -0.45);







  crown.scale.set(1.45, 0.12, 0.28);







  g.add(crown);







  







  for (let sign of [-1, 1]) {







    const arm = new THREE.Mesh(geos.box, depMaterials.stageSofaGold);







    arm.position.set(sign * 0.75, 0.85, 0);







    arm.scale.set(0.18, 0.45, 1.15);







    g.add(arm);







    







    for (let z of [-0.4, 0.4]) {







      const leg = new THREE.Mesh(geos.cylinder, depMaterials.stageSofaGold);







      leg.position.set(sign * 0.65, 0.16, z);







      leg.scale.set(0.05, 0.32, 0.05);







      g.add(leg);







    }







  }







  return g;







}















// Helper: Linear interpolation for 3D coordinates







function lerpCoord(p1, p2, t) {







  return [







    p1[0] + (p2[0] - p1[0]) * t,







    p1[1] + (p2[1] - p1[1]) * t,







    p1[2] + (p2[2] - p1[2]) * t







  ];







}















// Helper: Multi-waypoint path interpolation







function interpolateWaypoints(waypoints, tTotal) {







  const count = waypoints.length - 1;







  const scaled = Math.max(0, Math.min(count, tTotal * count));







  const idx = Math.min(count - 1, Math.floor(scaled));







  const tSub = scaled - idx;







  const pA = waypoints[idx];







  const pB = waypoints[idx + 1];







  const pos = lerpCoord(pA, pB, tSub);







  const angle = Math.atan2(pB[0] - pA[0], pB[2] - pA[2]);







  return { pos, angle };







}















function updateVvipHUD(stageNum, title, msg) {







  const hud = root.querySelector('#vvip-hud');







  if (!hud) return;







  const hudKey=stageNum+'|'+msg;







  if(hud.dataset.state===hudKey&&hud.style.display==='block')return;







  hud.dataset.state=hudKey;







  hud.style.display = 'block';







  const pill = hud.querySelector('#vvip-stage-pill');







  if (pill) pill.textContent = 'Phase ' + stageNum + '/5';







  const msgEl = hud.querySelector('#vvip-status-msg');







  if (msgEl) msgEl.innerHTML = msg;







  







  for (let i = 1; i <= 5; i++) {







    const step = hud.querySelector('#vvip-step-' + i);







    if (!step) continue;







    step.classList.remove('active', 'done');







    if (i < stageNum) step.classList.add('done');







    else if (i === stageNum) step.classList.add('active');







  }







}















let vvipHallPrepared=false;







let vvipRouteCache=null;







function vvipAuditoriumRoute(){







 if(vvipRouteCache)return vvipRouteCache;







 const find=prefix=>data.objects.find(o=>o.name.startsWith(prefix));







 const stage=find('Raised stage'),floor=find('Hall floor'),jambs=data.objects.filter(o=>o.name.startsWith('Side entrance metal jamb'));







 const entry=[jambs.reduce((a,o)=>a+o.p[0],0)/jambs.length,0,jambs.reduce((a,o)=>a+o.p[2],0)/jambs.length];







 const outer=data.objects.filter(o=>o.name.startsWith('External black entry step')).sort((a,b)=>a.p[1]-b.p[1]);







 const stairs=data.objects.filter(o=>o.name.startsWith('Stage right side green stair')).sort((a,b)=>a.p[1]-b.p[1]);







 const floorY=floor.p[1]+floor.s[1]/2+.02,stageY=stage.p[1]+stage.s[1]/2+.02;







 const end=[stage.p[0],stageY,stage.p[2]-stage.s[2]/2+2];







 const gate=geo.helipadProposal.gate;







 const path=[[gate[0],.36,gate[1]-3],[gate[0],.36,gate[1]],[gate[0],.36,outer[0].p[2]],...outer.map(o=>[o.p[0],o.p[1]+o.s[1]/2+.02,o.p[2]]),[entry[0]-.7,floorY,outer[0].p[2]],[stairs[0].p[0],floorY,stairs[0].p[2]-1],...stairs.map(o=>[o.p[0],o.p[1]+o.s[1]/2+.02,o.p[2]]),[stairs.at(-1).p[0],stageY,end[2]],end];







 return (vvipRouteCache={path,end,stage});







}







function prepareVvipHall(){if(vvipHallPrepared)return;select.value='hall';applyView();controls.enabled=false;groups.roof.visible=false;vvipHallPrepared=true;}







function placeVvipOnActualStage(){prepareVvipHall();const {end}=vvipAuditoriumRoute();vvipFemale.visible=vvipEscort1.visible=vvipEscort2.visible=true;vvipFemale.userData.setSeated(false);vvipFemale.userData.animateWalk(0);vvipFemale.position.fromArray(end);vvipFemale.rotation.y=Math.PI;for(const [escort,side] of [[vvipEscort1,-1],[vvipEscort2,1]]){escort.position.set(end[0]+side*1.3,end[1],end[2]+.7);escort.rotation.y=Math.PI;escort.userData.animateWalk(0);}}















function startVvipSimulation() {







  if (vvipActive) return;







  vvipActive = true;







  vvipRenderSettings={ratio:renderer.getPixelRatio(),shadows:renderer.shadowMap.enabled};







  renderer.setPixelRatio(Math.min(devicePixelRatio,1));







  renderer.shadowMap.enabled=false;







  







  const vvipBtn = root.querySelector('#gms-vvip-btn');







  if (vvipBtn) vvipBtn.classList.add('active');







  







  // Save current camera view & controls target







  vvipSavedCamera = camera.position.clone();







  vvipSavedTarget = controls.target.clone();







  vvipSavedView = current;







  controls.enabled = false;







  







  // Ensure layers are visible







  if (groups.event) groups.event.visible = true;







  if (groups.context) groups.context.visible = true;







  







  // Hide static helicopter







  hideStaticHelicopter();







  







  // Create simulation group







  vvipGroup = new THREE.Group();







  scene.add(vvipGroup);







  







  vvipHeli = buildVvipHelicopter();







  vvipGroup.add(vvipHeli);







  







  vvipFemale = buildFemaleVvip();







  vvipFemale.visible = false;







  vvipGroup.add(vvipFemale);







  







  vvipEscort1 = buildSecurityEscort();







  vvipEscort1.visible = false;







  vvipGroup.add(vvipEscort1);







  







  vvipEscort2 = buildSecurityEscort();







  vvipEscort2.visible = false;







  vvipGroup.add(vvipEscort2);







  







  vvipCar = buildVvipCar();







  vvipCar.position.set(-19.77, 0.36, -142.11);







  vvipCar.rotation.y = 0.08;







  vvipGroup.add(vvipCar);







  







  vvipBarricades = buildRoadBarricades();







  vvipGroup.add(vvipBarricades);







  







  vvipRoutePolice = buildRoutePolice();







  vvipGroup.add(vvipRoutePolice);







  







  vvipStageChair=null; // No separate simulation chair; destination is the existing stage.







  vvipHallPrepared=false;







  







  vvipPhase = 1;







  vvipPhaseTimer = 0;







  vvipWalkCycle = 0;







  







  // Close any finish modal







  const fm = root.querySelector('#vvip-finish-modal');







  if (fm) fm.style.display = 'none';







  







  // Initial camera placement for helicopter in-flight view







  camera.position.set(-145, 95, -395);







  controls.target.set(-120, 80, -360);







  







  updateVvipHUD(1, 'Air Arrival', '🚁 VVIP Helicopter Bhodwal Majri Helipad par approach aur land ho raha hai...');







  draw();







}















function stopVvipSimulation() {







  if (!vvipActive) return;







  vvipActive = false;







  if(vvipRenderSettings){renderer.setPixelRatio(vvipRenderSettings.ratio);renderer.shadowMap.enabled=vvipRenderSettings.shadows;renderer.shadowMap.needsUpdate=true;vvipRenderSettings=null;}







  vvipPhase = 0;







  







  const vvipBtn = root.querySelector('#gms-vvip-btn');







  if (vvipBtn) vvipBtn.classList.remove('active');







  







  const hud = root.querySelector('#vvip-hud');







  if (hud) hud.style.display = 'none';







  







  const fm = root.querySelector('#vvip-finish-modal');







  if (fm) fm.style.display = 'none';







  







  // Clean up 3D group







  if (vvipGroup) {







    scene.remove(vvipGroup);







    vvipGroup = null;







  }







  







  // Restore static helicopter







  restoreStaticHelicopter();







  







  // Restore roof / views







  if(vvipSavedView){select.value=vvipSavedView;applyView();}







  if (groups.roof) groups.roof.visible = true;







  if (interiorLights) interiorLights.visible = false;







  







  // Restore camera & controls







  controls.enabled = true;







  if (vvipSavedCamera && vvipSavedTarget) {







    camera.position.copy(vvipSavedCamera);







    controls.target.copy(vvipSavedTarget);







  } else {







    current = 'campus';







    applyView();







  }







  controls.update();







  draw();







}















function advanceVvipPhase() {







  if (vvipPhase >= 5) {







    // Complete on the actual existing raised stage, including skip-to-end.







    placeVvipOnActualStage();







    vvipPhase = 6;







    const hud = root.querySelector('#vvip-hud');







    if (hud) hud.style.display = 'none';







    const fm = root.querySelector('#vvip-finish-modal');







    if (fm) fm.style.display = 'flex';







  } else {







    vvipPhase++;







    vvipPhaseTimer = 0;







  }







}















// Simulation Tick (called from window.__DEP_TICK)







function tickVvipSimulation(dt) {







  if (!vvipActive || !vvipGroup) return false;







  const follow=1-Math.exp(-6*dt),aim=1-Math.exp(-8*dt);







  vvipPhaseTimer += dt;







  vvipWalkCycle += dt * 6.5;







  







  // Rotor continuous spin & beacon blink







  if (vvipHeli && vvipHeli.userData.mainRotor) {







    const rotorSpeed = (vvipPhase === 1 && vvipPhaseTimer > 9.5) ? Math.max(2, 35 * (1 - (vvipPhaseTimer - 9.5) / 2.5)) : (vvipPhase === 1 ? 35 : 4);







    vvipHeli.userData.mainRotor.rotation.y += rotorSpeed * dt;







    if (vvipHeli.userData.tailRotor) vvipHeli.userData.tailRotor.rotation.x += rotorSpeed * 1.5 * dt;







    if (vvipHeli.userData.rotorDisc) vvipHeli.userData.rotorDisc.visible = (rotorSpeed > 15);







  }







  







  // Car beacons alternating blink







  if (vvipCar && vvipCar.userData.beaconR && vvipCar.userData.beaconB) {







    const blink = (Date.now() % 300) < 150;







    vvipCar.userData.beaconR.material.emissiveIntensity = blink ? 2.5 : 0.2;







    vvipCar.userData.beaconB.material.emissiveIntensity = blink ? 0.2 : 2.5;







  }







  







  // ==========================================







  // PHASE 1: Helicopter Air Approach & Landing (12s)







  // ==========================================







  if (vvipPhase === 1) {







    const dur = 12.0;







    const progress = Math.min(1.0, vvipPhaseTimer / dur);







    







    // Flight Path from far sky to Helipad







    const startPos = [-130, 85, -370];







    const landPos = [-24.93, 0.45, -168.39];







    







    const flyT = Math.min(1.0, progress / 0.82); // Flight touches down at 82%







    const easeT = flyT * flyT * (3 - 2 * flyT); // Smooth cubic ease







    







    const curX = startPos[0] + (landPos[0] - startPos[0]) * easeT;







    const curZ = startPos[2] + (landPos[2] - startPos[2]) * easeT;







    // Aerodynamic descent curve







    const curY = landPos[1] + (startPos[1] - landPos[1]) * Math.pow(1 - easeT, 1.8);







    







    vvipHeli.position.set(curX, curY, curZ);







    // User requested: "helicopter ud raha hai ve sidha rthe" -> keep level and aligned







    vvipHeli.rotation.set(0, -0.09, 0);







    







    // Camera smoothly tracking behind and alongside the helicopter







    const camOffset = [-18, 9, -24];







    const targetCamPos = new THREE.Vector3(curX + camOffset[0], Math.max(curY + camOffset[1], 3.8), curZ + camOffset[2]);







    camera.position.lerp(targetCamPos, follow);







    controls.target.lerp(new THREE.Vector3(curX, curY + 1.2, curZ), aim);







    







    updateVvipHUD(1, 'Air Arrival', '🚁 VVIP Helicopter Bhodwal Majri Helipad par approach aur land ho raha hai... (' + Math.round((1 - progress) * dur) + 's)');







    







    if (vvipPhaseTimer >= dur) {







      advanceVvipPhase();







    }







  }







  







  // ==========================================







  // PHASE 2: Disembark & Walk to Road (10s)







  // ==========================================







  else if (vvipPhase === 2) {







    const dur = 13.0;







    const progress = Math.min(1.0, vvipPhaseTimer / dur);







    







    vvipFemale.visible = true;







    vvipEscort1.visible = true;







    vvipEscort2.visible = true;







    







    // Red carpet path from helicopter to helipad road







    const startP = [-22.18, 0.36, -168.64];







    const doorPoint=vvipCar.userData.passengerPoint();







    const endP = [doorPoint.x,doorPoint.y,doorPoint.z];







    const walk=Math.min(1,progress/.68);







    const doorOpen=progress<.60?0:progress<.72?(progress-.60)/.12:progress<.88?1:1-(progress-.88)/.12;







    vvipCar.userData.setPassengerDoor(doorOpen);







    const boarding=THREE.MathUtils.clamp((progress-.76)/.12,0,1);







    vvipFemale.visible=boarding<1;vvipEscort1.visible=vvipEscort2.visible=progress<.91;







    







    const curPos = lerpCoord(startP, endP, walk);







    const angle = Math.atan2(endP[0] - startP[0], endP[2] - startP[2]);







    







    const seat=vvipCar.localToWorld(new THREE.Vector3(-.45,0,-.75));







    const boarded=lerpCoord(curPos,[seat.x,seat.y,seat.z],boarding);







    vvipFemale.position.fromArray(boarded);







    vvipFemale.rotation.y = angle;







    vvipFemale.userData.animateWalk(walk<1||boarding>0?vvipWalkCycle:0);







    







    // Escorts flanking behind







    const leftOffset = [-1.1, 0, -1.0];







    const rightOffset = [1.1, 0, -1.0];







    vvipEscort1.position.set(curPos[0] + leftOffset[0], curPos[1], curPos[2] + leftOffset[2]);







    vvipEscort1.rotation.y = angle;







    vvipEscort1.userData.animateWalk(vvipWalkCycle);







    







    vvipEscort2.position.set(curPos[0] + rightOffset[0], curPos[1], curPos[2] + rightOffset[2]);







    vvipEscort2.rotation.y = angle;







    vvipEscort2.userData.animateWalk(vvipWalkCycle);







    







    // Camera: Zoomed in close tracking the Female VVIP ("vvip apr zoom rhe sth sth aagye chale")







    const camTarget = new THREE.Vector3(curPos[0], curPos[1] + 1.25, curPos[2]);







    const camPos = new THREE.Vector3(curPos[0] - 3.8, curPos[1] + 2.2, curPos[2] + 5.5);







    camera.position.lerp(camPos, follow);







    controls.target.lerp(camTarget, aim);







    







    updateVvipHUD(2, 'Disembark & Walk', (progress<.60?'VVIP car ki taraf aa rahi hain':progress<.76?'PSO ke saath rear passenger door khul raha hai':progress<.88?'VVIP gaadi mein baith rahi hain':'Passenger door band ho raha hai'));







    







    if (vvipPhaseTimer >= dur) {







      advanceVvipPhase();







    }







  }







  







  // ==========================================







  // PHASE 3: VIP Motorcade Transit to Main Gate (14s)







  // ==========================================







  else if (vvipPhase === 3) {







    const dur = 14.0;







    const progress = Math.min(1.0, vvipPhaseTimer / dur);







    







    vvipCar.userData.setPassengerDoor(0);







    // VVIP boarded into car







    vvipFemale.visible = false;







    vvipEscort1.visible = false;







    vvipEscort2.visible = false;







    







    // Road waypoints from helipad road to main gate







    const waypoints = [







      [-19.77, 0.36, -142.11],







      [-17.50, 0.36, -115.00],







      [-14.46, 0.36, -83.67],







      [-13.50, 0.36, -72.00]







    ];







    







    const { pos, angle } = interpolateWaypoints(waypoints, progress);







    







    // Calculate distance rolled for wheels







    if (vvipCar.userData.lastPos) {







      const dist = Math.hypot(pos[0] - vvipCar.userData.lastPos[0], pos[2] - vvipCar.userData.lastPos[2]);







      vvipCar.userData.rollWheels(dist);







    }







    vvipCar.userData.lastPos = pos;







    







    vvipCar.position.set(pos[0], pos[1], pos[2]);







    vvipCar.rotation.y = angle;







    







    // Camera: Smooth pursuit motorcade tracking







    const forward = new THREE.Vector3(Math.sin(angle), 0, Math.cos(angle));







    const camPos = new THREE.Vector3(pos[0] - forward.x * 9 - 4.5, pos[1] + 3.8, pos[2] - forward.z * 9);







    camera.position.lerp(camPos, follow);







    controls.target.lerp(new THREE.Vector3(pos[0], pos[1] + 1.1, pos[2]), aim);







    







    updateVvipHUD(3, 'Motorcade Transit', '🚘 VIP Motorcade helipad road se Main Campus Gate ki taraf badh raha hai... (' + Math.round((1 - progress) * dur) + 's)');







    







    if (vvipPhaseTimer >= dur) {







      advanceVvipPhase();







    }







  }







  







  // ==========================================







  // PHASE 4: Main Gate Barricades & Stop (6s)







  // ==========================================







  else if (vvipPhase === 4) {







    const dur = 8.0;







    const progress = Math.min(1.0, vvipPhaseTimer / dur);







    







    // Car stopped just before main gate







    vvipCar.position.set(-13.50, 0.36, -72.00);







    vvipCar.rotation.y = 0.12;







    







    // VVIP & escorts disembarking from car







    vvipFemale.visible = progress>.22;







    vvipEscort1.visible = true;







    vvipEscort2.visible = true;







    







    const doorOpen=progress<.22?progress/.22:progress<.68?1:1-(progress-.68)/.32;







    vvipCar.userData.setPassengerDoor(doorOpen);







    const doorPoint=vvipCar.userData.passengerPoint();







    const startP = [doorPoint.x,doorPoint.y,doorPoint.z];







    const stepP = [-13.00, 0.36, -68.00];







    const seat=vvipCar.localToWorld(new THREE.Vector3(-.45,0,-.75));







    const curPos = progress<.38?lerpCoord([seat.x,seat.y,seat.z],startP,THREE.MathUtils.clamp((progress-.22)/.16,0,1)):lerpCoord(startP,stepP,THREE.MathUtils.clamp((progress-.38)/.42,0,1));







    







    vvipFemale.position.set(curPos[0], curPos[1], curPos[2]);







    vvipFemale.rotation.y = 0.1;







    if (progress < 0.6) vvipFemale.userData.animateWalk(vvipWalkCycle);







    







    vvipEscort1.position.set(curPos[0] - 0.9, curPos[1], curPos[2] - 0.9);







    vvipEscort1.rotation.y = 0.1;







    vvipEscort2.position.set(curPos[0] + 0.9, curPos[1], curPos[2] - 0.9);







    vvipEscort2.rotation.y = 0.1;







    







    // Camera: Elevated framing showing barricades blocking both sides of main road







    const camPos = new THREE.Vector3(-20, 3.6, -80);







    const camTarget = new THREE.Vector3(-14.5, 1.3, -71);







    camera.position.lerp(camPos, follow);







    controls.target.lerp(camTarget, aim);







    







    updateVvipHUD(4, 'Main Gate Block', (progress<.22?'VVIP ke utarne se pehle passenger door khul raha hai':progress<.68?'VVIP PSOs ke saath gaadi se utar rahi hain':'VVIP door se door hain; passenger door band ho raha hai'));







    







    if (vvipPhaseTimer >= dur) {







      advanceVvipPhase();







    }







  }







  







  // ==========================================







  // PHASE 5: Auditorium Entrance & Main Stage Arrival (24s)







  // ==========================================







  else if (vvipPhase === 5) {







    prepareVvipHall();







    vvipCar.userData.setPassengerDoor(0);







    const dur=24,progress=Math.min(1,vvipPhaseTimer/dur),route=vvipAuditoriumRoute(),walk=Math.min(1,progress/.9);







    const {pos,angle}=interpolateWaypoints(route.path,walk);







    if(walk<1){







      vvipFemale.userData.setSeated(false);vvipFemale.userData.animateWalk(vvipWalkCycle);vvipFemale.position.fromArray(pos);vvipFemale.rotation.y=angle;







      for(const [escort,side,delay] of [[vvipEscort1,-1,.018],[vvipEscort2,1,.035]]){const e=interpolateWaypoints(route.path,Math.max(0,walk-delay));escort.position.set(e.pos[0]+Math.cos(e.angle)*side*.65,e.pos[1],e.pos[2]-Math.sin(e.angle)*side*.65);escort.rotation.y=e.angle;escort.userData.animateWalk(vvipWalkCycle);}







    }else placeVvipOnActualStage();







    const actual=vvipFemale.position;const camPos=new THREE.Vector3(actual.x-3,actual.y+2.3,actual.z-5.5),camTarget=actual.clone().add(new THREE.Vector3(0,1.05,0));camera.position.lerp(camPos,follow);controls.target.lerp(camTarget,aim);







    updateVvipHUD(5,'Auditorium main stage','Saree-clad female VVIP aur PSO escorts auditorium mein side stairs se main stage par pahunch rahe hain.');







    if(vvipPhaseTimer>=dur)advanceVvipPhase();







  }







  







  // ==========================================







  // PHASE 6: Completed (Gentle Stage Orbit)







  // ==========================================







  else if (vvipPhase === 6) {







    const orbitT = vvipPhaseTimer * 0.15;







    const end=vvipAuditoriumRoute().end,stageC=new THREE.Vector3(end[0],end[1]+1,end[2]);







    camera.position.set(stageC.x+Math.sin(orbitT)*4,stageC.y+2,stageC.z-8);







    controls.target.copy(stageC);







  }







  







  return true;







}















// Bind VVIP UI Event Listeners







function initVvipUI() {







  const vvipBtn = root.querySelector('#gms-vvip-btn');







  if (vvipBtn) {







    vvipBtn.addEventListener('click', () => {







      if (vvipActive) stopVvipSimulation();







      else startVvipSimulation();







    });







  }







  







  const skipBtn = root.querySelector('#vvip-skip-btn');







  if (skipBtn) {







    skipBtn.addEventListener('click', advanceVvipPhase);







  }







  







  const exitBtn = root.querySelector('#vvip-exit-btn');







  if (exitBtn) {







    exitBtn.addEventListener('click', stopVvipSimulation);







  }







  







  const replayBtn = root.querySelector('#vvip-replay-btn');







  if (replayBtn) {







    replayBtn.addEventListener('click', () => {







      stopVvipSimulation();







      setTimeout(startVvipSimulation, 100);







    });







  }







  







  const doneBtn = root.querySelector('#vvip-done-btn');







  if (doneBtn) {







    doneBtn.addEventListener('click', stopVvipSimulation);







  }







}















if (document.readyState === 'loading') {







  document.addEventListener('DOMContentLoaded', initVvipUI);







} else {







  initVvipUI();







}

















// =========================================================================
// DUPLICATE SELECTED ITEM ENGINE
// =========================================================================
function depDuplicateSelectedItem() {
  if (!depSelected) return;
  const cur = depItems.find(o => o.id === depSelected);
  if (!cur) return;

  const sameKindItems = depItems.filter(o => o && o.kind === cur.kind);
  const count = sameKindItems.length + 1;

  let newName = '';
  if (cur.kind === 'officer') {
    newName = `Officer ${count}`;
  } else if (cur.kind === 'hhmd') {
    newName = `HHMD Officer ${count}`;
  } else if (cur.kind === 'binocular') {
    newName = `Spotter Officer ${count}`;
  } else if (cur.kind === 'radio') {
    newName = `Radio Officer ${count}`;
  } else if (cur.kind === 'ambulance') {
    newName = `Ambulance ${count}`;
  } else if (cur.kind === 'firebrigade') {
    newName = `Fire Tender ${count}`;
  } else if (cur.kind === 'qbelt') {
    newName = `Q-Belt Barrier ${count}`;
  } else if (cur.kind === 'parking') {
    newName = `Vehicle Parking #${count}`;
  } else if (cur.kind === 'square_box') {
    newName = `Item Box ${count}`;
  } else {
    newName = `${cur.name || cur.kind} ${count}`;
  }

  // Slightly offset position (+1.5m to the right/side of current facing angle or in X/Z)
  const angleRad = ((cur.angle || 0) + 90) * (Math.PI / 180);
  const offsetDist = 1.5;
  const newX = Math.round((cur.x + Math.cos(angleRad) * offsetDist) * 100) / 100;
  const newZ = Math.round((cur.z + Math.sin(angleRad) * offsetDist) * 100) / 100;
  const newY = typeof getSurfaceHeight === 'function' ? getSurfaceHeight(newX, newZ, cur.y) : cur.y;
  const newDuty = cur.duty || (typeof depGetAutoDuty === 'function' ? depGetAutoDuty(newX, newY, newZ, cur.kind) : 'Security post');

  const newId = 'post-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 6);

  const newItem = {
    id: newId,
    kind: cur.kind,
    name: newName,
    x: newX,
    y: newY,
    z: newZ,
    angle: cur.angle || 0,
    duty: newDuty,
    customDuty: !!cur.customDuty,
    belt: '',
    mobile: '',
    status: cur.status || 'Active'
  };
  if (newItem.duty && typeof depRegisterCustomDuty === 'function') {
    depRegisterCustomDuty(newItem.duty);
  }

  depItems.push(newItem);
  depStore();
  depBuild();
  depChoose(newItem.id, true);

  if (typeof depShowToast === 'function') {
    depShowToast(`➕ ${newItem.name} (${newItem.duty}) added!`);
  } else if (depUI('status')) {
    depUI('status').textContent = `➕ ${newItem.name} added.`;
  }
}
window.depDuplicateSelectedItem = depDuplicateSelectedItem;

// =========================================================================
// OFFICER & EQUIPMENT EDIT DIALOG ENGINE (Triggered ONLY via ✏️ icon)
// =========================================================================
let currentDialogItemId = null;

function depShowToast(msg) {
  let toast = document.getElementById('dep-live-toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'dep-live-toast';
    toast.className = 'dep-toast';
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.classList.add('show');
  clearTimeout(toast._hideTimer);
  toast._hideTimer = setTimeout(() => {
    toast.classList.remove('show');
  }, 3200);
}
window.depShowToast = depShowToast;

function openOfficerDialog(itemId) {
  const targetId = itemId || depSelected;
  if (!targetId) return;
  const item = depItems.find(o => o.id === targetId);
  if (!item) return;
  currentDialogItemId = targetId;

  // Set title & symbol (Minimalist UI)
  const symEl = document.getElementById('dep-dlg-symbol');
  const titleTextEl = document.getElementById('dep-dlg-title-text');
  const badgeEl = document.getElementById('dep-dlg-badge');
  const isOfficer = item.kind === 'officer' || item.kind === 'hhmd' || item.kind === 'binocular' || item.kind === 'radio';
  if (symEl) symEl.textContent = depSymbols[item.kind] || '👮';
  if (titleTextEl) titleTextEl.textContent = isOfficer ? 'Officer Details' : 'Equipment Details';
  if (badgeEl) badgeEl.textContent = item.name || '';

  // Fill input fields with current values
  const nameInput = document.getElementById('dep-dlg-name');
  const beltInput = document.getElementById('dep-dlg-belt');
  const mobileInput = document.getElementById('dep-dlg-mobile');
  const dutyInput = document.getElementById('dep-dlg-duty');

  if (nameInput) nameInput.value = item.name || '';
  if (beltInput) beltInput.value = item.belt || '';
  if (mobileInput) mobileInput.value = item.mobile || '';
  if (dutyInput) dutyInput.value = item.duty || '';

  // Show modal
  const modal = document.getElementById('dep-officer-modal');
  if (modal) {
    modal.style.display = 'flex';
    setTimeout(() => {
      if (nameInput) {
        nameInput.focus();
        nameInput.select();
      }
    }, 60);
  }
}
window.openOfficerDialog = openOfficerDialog;

function closeOfficerDialog() {
  const modal = document.getElementById('dep-officer-modal');
  if (modal) modal.style.display = 'none';
  currentDialogItemId = null;
  if (document.activeElement && typeof document.activeElement.blur === 'function') {
    document.activeElement.blur();
  }
  if (typeof depKeysDown !== 'undefined') {
    for (const k in depKeysDown) {
      depKeysDown[k] = false;
    }
  }
  if (typeof renderer !== 'undefined' && renderer && renderer.domElement) {
    renderer.domElement.tabIndex = 0;
    renderer.domElement.focus();
  }
  window.focus();
}
window.closeOfficerDialog = closeOfficerDialog;

function saveOfficerDialog() {
  if (!currentDialogItemId) return;
  const item = depItems.find(o => o.id === currentDialogItemId);
  if (!item) return;

  const nameInput = document.getElementById('dep-dlg-name');
  const beltInput = document.getElementById('dep-dlg-belt');
  const mobileInput = document.getElementById('dep-dlg-mobile');
  const dutyInput = document.getElementById('dep-dlg-duty');

  const oldName = item.name;
  const newName = nameInput ? nameInput.value.trim() : item.name;
  const newBelt = beltInput ? beltInput.value.trim() : (item.belt || '');
  const newMobile = mobileInput ? mobileInput.value.trim() : (item.mobile || '');
  const newDuty = dutyInput ? dutyInput.value.trim() : (item.duty || '');

  item.name = newName || oldName;
  item.belt = newBelt;
  item.mobile = newMobile;
  item.duty = newDuty;
  if (newDuty) {
    item.customDuty = true;
    if (typeof depRegisterCustomDuty === 'function') {
      depRegisterCustomDuty(newDuty);
    }
  }

  // Sync to left/right inspector inputs if active
  if (depUI('name')) depUI('name').value = item.name;
  if (depUI('belt')) depUI('belt').value = item.belt;
  if (depUI('mobile')) depUI('mobile').value = item.mobile;
  if (depUI('duty')) depUI('duty').value = item.duty;

  // Update dropdown labels & markers
  depSyncDropdownLabels(item);

  // Persist to localStorage & backend SQLite immediately
  depStore();
  depBuild();
  depChoose(item.id, false);

  closeOfficerDialog();
  depShowToast(`Saved ${item.name}`);
}
window.saveOfficerDialog = saveOfficerDialog;

// Bind Dialog events when DOM is ready
function setupOfficerDialogEvents() {
  const modal = document.getElementById('dep-officer-modal');
  const backdrop = document.getElementById('dep-officer-backdrop');
  const closeX = document.getElementById('dep-dlg-close-x');
  const cancelBtn = document.getElementById('dep-dlg-cancel-btn');
  const form = document.getElementById('dep-officer-dialog-form');

  if (backdrop) backdrop.addEventListener('click', closeOfficerDialog);
  if (closeX) closeX.addEventListener('click', closeOfficerDialog);
  if (cancelBtn) cancelBtn.addEventListener('click', closeOfficerDialog);
  if (form) {
    form.addEventListener('submit', e => {
      e.preventDefault();
      saveOfficerDialog();
    });
  }

  // Open Edit Details dialog on ✏️ button, Officer Name click, or Duty click
  const triggerEditDialog = e => {
    e.preventDefault();
    e.stopPropagation();
    openOfficerDialog(depSelected);
  };

  const titleRow = depPeekHead.querySelector('.dep-peek-title-row');
  const titleEl = depPeekHead.querySelector('#dep-peek-title');
  const badgeEl = depPeekHead.querySelector('#dep-peek-duty-badge');
  const editBtn = depPeekHead.querySelector('#dep-peek-edit');

  if (titleRow) {
    titleRow.addEventListener('pointerdown', e => e.stopPropagation());
    titleRow.addEventListener('click', triggerEditDialog);
  }
  if (titleEl) {
    titleEl.addEventListener('pointerdown', e => e.stopPropagation());
    titleEl.addEventListener('click', triggerEditDialog);
  }
  if (badgeEl) {
    badgeEl.addEventListener('pointerdown', e => e.stopPropagation());
    badgeEl.addEventListener('click', triggerEditDialog);
  }
  if (editBtn) {
    editBtn.addEventListener('pointerdown', e => e.stopPropagation());
    editBtn.addEventListener('click', triggerEditDialog);
  }

  // Bind + button to duplicate selected item
  const minBtn = depPeekHead.querySelector('#dep-peek-min');
  if (minBtn) {
    minBtn.addEventListener('pointerdown', e => e.stopPropagation());
    minBtn.addEventListener('click', e => {
      e.preventDefault();
      e.stopPropagation();
      depDuplicateSelectedItem();
    });
  }

  // Keyboard shortcut (ESC closes dialog)
  window.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      const m = document.getElementById('dep-officer-modal');
      if (m && m.style.display !== 'none') {
        e.preventDefault();
        e.stopPropagation();
        closeOfficerDialog();
      }
    }
  });
}

// Call setup immediately or on ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', setupOfficerDialogEvents);
} else {
  setTimeout(setupOfficerDialogEvents, 100);
}

