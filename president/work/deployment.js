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







const depSymbols={qrt:'🚙',xray:'🧳',armed_officer:'👮‍✈️',officer:'👮',_dummy:'👮',barricade:'🚧',binocular:'🔭',dfmd:'🚪',hhmd:'🔍',radio:'📻',cone:'⚠️',cctv:'📹',light:'💡',square_box:'📦',ambulance:'🚑',firebrigade:'🚒',qbelt:'🎗️',parking:'🅿️',helipad:'🚁'};







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

  if ((key === 'delete' || key === 'backspace') && depSelected) {
    e.preventDefault();
    e.stopPropagation();
    if (typeof depDeleteItemById === 'function') {
      depDeleteItemById(depSelected);
    } else {
      depReturnView();
      depItems = depItems.filter(o => o.id !== depSelected);
      depSelected = null;
      depPlace = false;
      depStore(true);
      depBuild();
    }
    return;
  }







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
  if(kind==='cctv') return '24x7 CCTV Video Surveillance';
  if(kind==='qrt') return 'QRT standby & rapid response';
  if(kind==='xray') return 'Baggage screening / X-Ray inspection';
  if(kind==='armed_officer') return 'Armed security / escort cordon';
  if(kind==='helipad') return 'Helipad security & landing cordon';
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
  depStore(true);
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







depPeekHead.innerHTML='<div class="dep-peek-title-row" id="dep-peek-title-row" title="Click to edit details" style="cursor:pointer;"><span id="dep-peek-title" class="dep-peek-title" title="Click to edit officer details" style="cursor:pointer;">👮 Post Information</span><span id="dep-peek-duty-badge" class="dep-peek-duty-badge" title="Click to edit duty & details" style="cursor:pointer;"></span></div><div class="dep-peek-controls"><button type="button" id="dep-peek-edit" class="dep-peek-btn-icon" title="Edit details" style="display:none;">✏️</button><button type="button" id="dep-peek-min" class="dep-peek-btn-icon" title="Duplicate post / Add another (+1)">+</button><button type="button" id="dep-peek-del" class="dep-peek-btn-icon btn-danger-soft" title="Delete post">🗑️</button><button type="button" id="dep-peek-close" class="dep-peek-btn-icon" title="Close">✕</button></div>';















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







    if(minBtn){minBtn.textContent='+';minBtn.title='Duplicate post / Add another (+1)';}







    depPeekBody.style.display='none';







  }else{







    depPeek.classList.remove('minimized');







    if(minBtn){minBtn.textContent='+';minBtn.title='Duplicate post / Add another (+1)';}







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







    depStore(true);







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















function depValid(items){
  if (!Array.isArray(items) || items.length > 2000) return false;
  if (items.length === 0) return true;
  const ids = new Set();
  for (const o of items) {
    if (!o || typeof o.id !== 'string' || !o.id || ids.has(o.id)) return false;
    ids.add(o.id);
    if (!o.kind || !depTypes.includes(o.kind)) return false;
    for (const k of ['x','y','z','angle']) {
      const v = Number(o[k]);
      if (!Number.isFinite(v)) return false;
      o[k] = v;
    }
    if (Math.abs(o.x) > 10000 || Math.abs(o.z) > 10000 || o.y < -100 || o.y > 500) return false;
    for (const k of ['name','duty','belt','mobile']) {
      if (o[k] === undefined || o[k] === null) o[k] = '';
      else if (typeof o[k] !== 'string') o[k] = String(o[k]);
    }
  }
  return true;
}















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







if (initialLocal && Array.isArray(initialLocal.items) && depValid(initialLocal.items) && initialLocal.items.length > 0) {
  depItems = initialLocal.items;
} else if (depInitialPlan && Array.isArray(depInitialPlan.items) && depValid(depInitialPlan.items) && depInitialPlan.items.length > 0) {
  depItems = JSON.parse(JSON.stringify(depInitialPlan.items));
} else {
  depItems = depSeed();
}
depItems=(depItems||[]).filter(o=>o&&o.kind!=='helicopter');
depItems.forEach(o => {
  if (o) {
    // If officer or equipment is sunken below ground/floor, elevate immediately
    if (typeof getSurfaceHeight === 'function') {
      const properFloorY = getSurfaceHeight(o.x, o.z, o.y);
      if (properFloorY > o.y + 0.04) {
        o.y = properFloorY;
      }
    }
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















function depStore(immediate = true){
  try{
    const record={version:1,savedAt:Date.now(),origin:[geo.originLongitude,geo.originLatitude],items:depItems};
    localStorage.setItem(depStorage,JSON.stringify(record));







    depUI('status').textContent='✅ Auto-saved · '+depItems.filter(o=>o.kind==='officer').length+' officers · '+depItems.filter(o=>o.kind!=='officer').length+' equipment';







  }catch(e){console.warn('localStorage save warning:',e);}







  depQueue(immediate);







}















const depMaterials={







  vipSaree:new THREE.MeshStandardMaterial({color:0xf1eadd,roughness:0.55}),







  vipGold:new THREE.MeshStandardMaterial({color:0xf59e0b,roughness:0.25,metalness:0.75}),







  vipPallu:new THREE.MeshStandardMaterial({color:0x8e293b,roughness:0.5}),







  vipCar:new THREE.MeshStandardMaterial({color:0x090b0e,roughness:0.08,metalness:0.96}),







  vipGlass:new THREE.MeshStandardMaterial({color:0x1e293b,roughness:0.1,metalness:0.9,transparent:true,opacity:0.85}),







  vipChrome:new THREE.MeshStandardMaterial({color:0xe2e8f0,roughness:0.1,metalness:0.95}),







  vipBeaconRed:new THREE.MeshStandardMaterial({color:0xef4444,emissive:0xdc2626,emissiveIntensity:2.5}),







  vipBeaconBlue:new THREE.MeshStandardMaterial({color:0x3b82f6,emissive:0x2563eb,emissiveIntensity:2.5}),







  heliWhite:new THREE.MeshStandardMaterial({color:0xf8fafc,roughness:0.3}),







  heliNavy:new THREE.MeshStandardMaterial({color:0x0f172a,roughness:0.3,metalness:0.3}),







  heliRotor:new THREE.MeshStandardMaterial({color:0x27272a,roughness:0.5}),







  barricadeYellow:new THREE.MeshStandardMaterial({color:0xfacc15,roughness:0.28,metalness:0.25}),







  barricadeDark:new THREE.MeshStandardMaterial({color:0x1e293b,roughness:0.5}),







  stageSofaRed:new THREE.MeshStandardMaterial({color:0x881337,roughness:0.6}),







  stageSofaGold:new THREE.MeshStandardMaterial({color:0xd97706,roughness:0.25,metalness:0.75}),















  khaki:new THREE.MeshStandardMaterial({color:0xc8a870,roughness:0.72}), // Real Indian Police Khaki uniform shirt







  trousers:new THREE.MeshStandardMaterial({color:0xab8954,roughness:0.75}), // Khaki trousers







  dark:new THREE.MeshStandardMaterial({color:0x111827,roughness:0.22,metalness:0.25}), // Polished black leather boots, holster, belt, visor







  yellow:new THREE.MeshStandardMaterial({color:0xf59e0b,roughness:0.15,metalness:0.92}), // Brass stars, insignia, buckle







  skin:new THREE.MeshStandardMaterial({color:0xc48c66,roughness:0.75}), // Realistic Indian skin tone







  red:new THREE.MeshStandardMaterial({color:0xb91c1c,roughness:0.5}), // Officer cap red ribbon band







  blue:new THREE.MeshStandardMaterial({color:0x1d3557,roughness:0.6}), // Navy blue cap crown / DFMD / equipment







  white:new THREE.MeshStandardMaterial({color:0xffffff,roughness:0.55}), // Whistle cord / name text







  hair:new THREE.MeshStandardMaterial({color:0x1c1917,roughness:0.9}), // Neat hair







  lathi:new THREE.MeshStandardMaterial({color:0x6e3c1b,roughness:0.4}), // Polished wood baton







  hhmdBody:new THREE.MeshStandardMaterial({color:0x1b1f24,roughness:0.42,metalness:0.12}), // Tactical matte polycarbonate scanner casing







  hhmdGrip:new THREE.MeshStandardMaterial({color:0x0c0e11,roughness:0.88,metalness:0.04}), // Non-slip textured rubber handle grip







  hhmdSwitch:new THREE.MeshStandardMaterial({color:0xd92d20,roughness:0.35,metalness:0.15}), // Red power/sensitivity toggle slider







  hhmdSpeaker:new THREE.MeshStandardMaterial({color:0x333b47,roughness:0.45,metalness:0.4}), // Audio buzzer sound emitter grille







  hhmdLedGreen:new THREE.MeshStandardMaterial({color:0x22c55e,emissive:0x15803d,emissiveIntensity:2.5,roughness:0.2}), // Power ON green LED







  hhmdLedAmber:new THREE.MeshStandardMaterial({color:0xf59e0b,emissive:0xb45309,emissiveIntensity:1.2,roughness:0.2}), // Ready/Standby amber LED







  hhmdLedRed:new THREE.MeshStandardMaterial({color:0xef4444,emissive:0xb91c1c,emissiveIntensity:2.5,roughness:0.2}), // Alarm metal-detect red LED







  hhmdStripe:new THREE.MeshStandardMaterial({color:0xfacc15,roughness:0.35,metalness:0.1}), // High-visibility hazard yellow band







  whiteBody:new THREE.MeshStandardMaterial({color:0xf8fafc,roughness:0.25,metalness:0.1}), // Gloss white vehicle body







  fireRed:new THREE.MeshStandardMaterial({color:0xef4444,roughness:0.2,metalness:0.2}), // Tactical fire engine signal red







  chrome:new THREE.MeshStandardMaterial({color:0xd8dee9,roughness:0.15,metalness:0.85}), // Polished chrome & stainless steel







  glassTint:new THREE.MeshStandardMaterial({color:0x1e293b,roughness:0.12,metalness:0.6,transparent:true,opacity:0.75}), // Tinted glass







  tireRubber:new THREE.MeshStandardMaterial({color:0x111315,roughness:0.92,metalness:0.05}), // Black rubber tire tread







  shutterMetal:new THREE.MeshStandardMaterial({color:0x94a3b8,roughness:0.45,metalness:0.65}), // Ribbed equipment roller shutter







  stanchionChrome:new THREE.MeshStandardMaterial({color:0xe2e8f0,roughness:0.12,metalness:0.9}), // Polished queue stanchion







  qbeltRibbon:new THREE.MeshStandardMaterial({color:0xdc2626,emissive:0x991b1b,emissiveIntensity:0.35,roughness:0.4,metalness:0.1}), // High-tension red nylon webbing







  crateWood:new THREE.MeshStandardMaterial({color:0x8b5a2b,roughness:0.78,metalness:0.05}), // Heavy cargo crate wood







  crateTrim:new THREE.MeshStandardMaterial({color:0x272e39,roughness:0.38,metalness:0.7}),
  // Helipad Materials (Exact match to circular helipad in detail_helipad.py)
  padConcrete:new THREE.MeshStandardMaterial({color:0x4b535d,roughness:0.85}),
  padOuterRim:new THREE.MeshStandardMaterial({color:0xcbd5e1,roughness:0.75}),
  padAsphalt:new THREE.MeshStandardMaterial({color:0x2c323c,roughness:0.90}),
  padLineWhite:new THREE.MeshStandardMaterial({color:0xffffff,roughness:0.50}),
  padLineDark:new THREE.MeshStandardMaterial({color:0x181e24,roughness:0.80}),
  padLineYellow:new THREE.MeshStandardMaterial({color:0xfacc15,roughness:0.40,metalness:0.2}),
  padDashedRed:new THREE.MeshStandardMaterial({color:0xef4444,roughness:0.60}),
  padLightTurquoise:new THREE.MeshStandardMaterial({color:0x2dd4bf,emissive:0x14b8a6,emissiveIntensity:2.5,roughness:0.2}),
  padLightMetal:new THREE.MeshStandardMaterial({color:0x475569,roughness:0.35,metalness:0.7}),
  padPoleDark:new THREE.MeshStandardMaterial({color:0x27272a,roughness:0.60,metalness:0.4}),
  padPoleYellow:new THREE.MeshStandardMaterial({color:0xfacc15,roughness:0.35,metalness:0.3}),
  padWindsockOrange:new THREE.MeshStandardMaterial({color:0xf97316,roughness:0.70}),
  padWindsockWhite:new THREE.MeshStandardMaterial({color:0xf8fafc,roughness:0.70}),
  // PTZ Surveillance CCTV Camera Materials (Ultra-Realistic Industrial Spec)
  cctvMastGalv: new THREE.MeshStandardMaterial({color: 0x9ba3af, roughness: 0.38, metalness: 0.68}),
  cctvBasePad: new THREE.MeshStandardMaterial({color: 0x3f444c, roughness: 0.88}),
  cctvAnchorBolt: new THREE.MeshStandardMaterial({color: 0xd1d5db, roughness: 0.22, metalness: 0.88}),
  cctvEnclosureWhite: new THREE.MeshStandardMaterial({color: 0xf1f5f9, roughness: 0.28, metalness: 0.15}),
  cctvHousingCharcoal: new THREE.MeshStandardMaterial({color: 0x1e293b, roughness: 0.35, metalness: 0.45}),
  cctvDomeSmoked: new THREE.MeshStandardMaterial({color: 0x070c14, roughness: 0.04, metalness: 0.98, transparent: true, opacity: 0.82}),
  cctvLensGlass: new THREE.MeshStandardMaterial({color: 0x0f172a, roughness: 0.06, metalness: 0.92}),
  cctvLensAR: new THREE.MeshStandardMaterial({color: 0x1d4ed8, roughness: 0.08, metalness: 0.95, emissive: 0x1e3a8a, emissiveIntensity: 0.45}),
  cctvLensAperture: new THREE.MeshStandardMaterial({color: 0x000000, roughness: 0.9, metalness: 0.1}),
  cctvIRLed: new THREE.MeshStandardMaterial({color: 0x7e22ce, emissive: 0x6b21a8, emissiveIntensity: 1.8, roughness: 0.3}),
  cctvLedGreen: new THREE.MeshStandardMaterial({color: 0x22c55e, emissive: 0x16a34a, emissiveIntensity: 2.8, roughness: 0.2}),
  cctvLedRed: new THREE.MeshStandardMaterial({color: 0xef4444, emissive: 0xdc2626, emissiveIntensity: 3.2, roughness: 0.2}),
  cctvConduitFlex: new THREE.MeshStandardMaterial({color: 0x64748b, roughness: 0.45, metalness: 0.65}),
  cctvHazardYellow: new THREE.MeshStandardMaterial({color: 0xfacc15, roughness: 0.35, metalness: 0.15}),
  cctvCopperGround: new THREE.MeshStandardMaterial({color: 0xb45309, roughness: 0.3, metalness: 0.85}),
 // Reinforced steel corner brackets







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







function depCreateHhmdDecalCanvas(flipped=false){
 const c=document.createElement('canvas');c.width=256;c.height=1024;const ctx=c.getContext('2d');
 ctx.fillStyle='#101316';ctx.fillRect(0,0,256,1024);ctx.strokeStyle='#7b8285';ctx.lineWidth=7;ctx.strokeRect(10,10,236,1004);
 ctx.save();ctx.translate(128,512);ctx.rotate(-Math.PI/2);ctx.fillStyle='#e3ed55';ctx.textAlign='center';ctx.textBaseline='middle';ctx.font='bold 90px Arial';ctx.fillText('SUPER SCANNER',0,0,950);ctx.restore();return c;
}
const depHhmdCanvas=depCreateHhmdDecalCanvas(false);
const depHhmdDecalFrontTex=new THREE.CanvasTexture(depHhmdCanvas);
depHhmdDecalFrontTex.anisotropy=8;
const depHhmdDecalFront=new THREE.MeshStandardMaterial({
  map:depHhmdDecalFrontTex,roughness:1,metalness:0,
  polygonOffset:true,polygonOffsetFactor:-2.0,polygonOffsetUnits:-4.0,depthWrite:true,side:THREE.DoubleSide
});
const depHhmdBackCanvas=depCreateHhmdDecalCanvas(true);
const depHhmdDecalBackTex=new THREE.CanvasTexture(depHhmdBackCanvas);
depHhmdDecalBackTex.anisotropy=8;
const depHhmdDecalBack=new THREE.MeshStandardMaterial({
  map:depHhmdDecalBackTex,roughness:1,metalness:0,
  polygonOffset:true,polygonOffsetFactor:-2.0,polygonOffsetUnits:-4.0,depthWrite:true,side:THREE.DoubleSide
});















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







// Ambulance Hood Decal - Forward-Facing Bold Red AMBULANCE
const depAmbHoodCanvas=document.createElement('canvas');depAmbHoodCanvas.width=512;depAmbHoodCanvas.height=128;
const dahc=depAmbHoodCanvas.getContext('2d');
dahc.clearRect(0,0,512,128);
dahc.fillStyle='#dc2626';
dahc.fillRect(236,10,40,40);
dahc.clearRect(236,22,40,16);dahc.clearRect(248,10,16,40);
dahc.fillRect(238,24,36,12);dahc.fillRect(250,12,12,36);
dahc.font='900 52px Arial, sans-serif';dahc.textAlign='center';dahc.textBaseline='middle';
dahc.fillText('AMBULANCE',256,92);
const depAmbulanceHoodDecal=new THREE.MeshStandardMaterial({
  map:new THREE.CanvasTexture(depAmbHoodCanvas),
  transparent:true,opacity:1.0,roughness:0.25,metalness:0.1,side:THREE.FrontSide,
  polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-4,depthWrite:true
});

// Ambulance Front Nose Decal - Bold Red AMBULANCE with Red Crosses
const depAmbFrontCanvas=document.createElement('canvas');depAmbFrontCanvas.width=512;depAmbFrontCanvas.height=128;
const dafc=depAmbFrontCanvas.getContext('2d');
dafc.clearRect(0,0,512,128);
dafc.fillStyle='#dc2626';
dafc.fillRect(28,44,48,16);dafc.fillRect(44,28,16,48);
dafc.fillRect(436,44,48,16);dafc.fillRect(452,28,16,48);
dafc.font='900 68px Arial, sans-serif';dafc.textAlign='center';dafc.textBaseline='middle';
dafc.fillText('AMBULANCE',256,54);
const depAmbulanceFrontDecal=new THREE.MeshStandardMaterial({
  map:new THREE.CanvasTexture(depAmbFrontCanvas),
  transparent:true,opacity:1.0,roughness:0.25,metalness:0.1,side:THREE.FrontSide,
  polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-4,depthWrite:true
});

// Ambulance Rear Doors Decal - Bold Red AMBULANCE with Red Crosses
const depAmbRearCanvas=document.createElement('canvas');depAmbRearCanvas.width=512;depAmbRearCanvas.height=128;
const darc=depAmbRearCanvas.getContext('2d');
darc.clearRect(0,0,512,128);
darc.fillStyle='#dc2626';
darc.fillRect(28,44,48,16);darc.fillRect(44,28,16,48);
darc.fillRect(436,44,48,16);darc.fillRect(452,28,16,48);
darc.font='900 64px Arial, sans-serif';darc.textAlign='center';darc.textBaseline='middle';
darc.fillText('AMBULANCE',256,50);
darc.font='bold 22px Arial, sans-serif';
darc.fillText('EMERGENCY 108 · 102',256,92);
const depAmbulanceRearDecal=new THREE.MeshStandardMaterial({
  map:new THREE.CanvasTexture(depAmbRearCanvas),
  transparent:true,opacity:1.0,roughness:0.25,metalness:0.1,side:THREE.FrontSide,
  polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-4,depthWrite:true
});

// Fire Engine Front Visor Decal - Massive Bold Yellow FIRE BRIGADE
const depFireVisorCanvas=document.createElement('canvas');depFireVisorCanvas.width=1024;depFireVisorCanvas.height=192;
const dfvc=depFireVisorCanvas.getContext('2d');
dfvc.clearRect(0,0,1024,192);
dfvc.fillStyle='#0f172a';dfvc.fillRect(16,16,992,160);
dfvc.strokeStyle='#facc15';dfvc.lineWidth=8;dfvc.strokeRect(20,20,984,152);
dfvc.fillStyle='#facc15';dfvc.font='900 108px Arial, sans-serif';dfvc.textAlign='center';dfvc.textBaseline='middle';
dfvc.fillText('FIRE BRIGADE',512,96);

const depFireVisorDecal=new THREE.MeshStandardMaterial({
  map:new THREE.CanvasTexture(depFireVisorCanvas),
  transparent:true,opacity:1.0,roughness:0.3,metalness:0.1,side:THREE.FrontSide,
  polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-4,depthWrite:true
});

// Fire Engine Front Caution Plate - Massive Bold Yellow FIRE BRIGADE (matching rear plate!)
const depFireFrontPlateCanvas=document.createElement('canvas');depFireFrontPlateCanvas.width=1024;depFireFrontPlateCanvas.height=256;
const dfpc=depFireFrontPlateCanvas.getContext('2d');
dfpc.clearRect(0,0,1024,256);
dfpc.fillStyle='#facc15';dfpc.fillRect(0,0,1024,256);
dfpc.fillStyle='#dc2626';
for(let x=-256;x<=1024;x+=64){
  dfpc.beginPath();
  dfpc.moveTo(x,256);dfpc.lineTo(x+64,0);dfpc.lineTo(x+96,0);dfpc.lineTo(x+32,256);
  dfpc.fill();
}
// Central Caution Plate
dfpc.fillStyle='#0f172a';dfpc.fillRect(80,36,864,184);
dfpc.strokeStyle='#facc15';dfpc.lineWidth=8;dfpc.strokeRect(84,40,856,176);
dfpc.fillStyle='#facc15';dfpc.font='900 88px Arial, sans-serif';dfpc.textAlign='center';dfpc.textBaseline='middle';
dfpc.fillText('FIRE BRIGADE',512,108);
dfpc.fillStyle='#fef08a';dfpc.font='bold 34px sans-serif';dfpc.textAlign='center';dfpc.textBaseline='middle';
dfpc.fillText('अग्नि शमन सेवा · EMERGENCY 101',512,172);

const depFireFrontPlateDecal=new THREE.MeshStandardMaterial({
  map:new THREE.CanvasTexture(depFireFrontPlateCanvas),
  roughness:0.4,metalness:0.1,side:THREE.FrontSide,
  polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-4,depthWrite:true
});

// Fire Engine Rear Tailgate Chevrons Decal - Prominent Bold Yellow FIRE BRIGADE
const depFireChevCanvas=document.createElement('canvas');depFireChevCanvas.width=512;depFireChevCanvas.height=256;
const dfc=depFireChevCanvas.getContext('2d');
dfc.fillStyle='#facc15';dfc.fillRect(0,0,512,256);
dfc.fillStyle='#dc2626';
for(let x=-256;x<=512;x+=64){
  dfc.beginPath();
  dfc.moveTo(x,256);dfc.lineTo(x+64,0);dfc.lineTo(x+96,0);dfc.lineTo(x+32,256);
  dfc.fill();
}
// Central Caution Box
dfc.fillStyle='#0f172a';dfc.fillRect(40,68,432,120);
dfc.strokeStyle='#facc15';dfc.lineWidth=6;dfc.strokeRect(44,72,424,112);
dfc.fillStyle='#facc15';dfc.font='900 52px Arial, sans-serif';dfc.textAlign='center';
dfc.fillText('FIRE BRIGADE',256,120);
dfc.fillStyle='#fef08a';dfc.font='bold 22px sans-serif';
dfc.fillText('अग्नि शमन सेवा · EMERGENCY 101',256,158);

const depFireChevronDecal=new THREE.MeshStandardMaterial({
  map:new THREE.CanvasTexture(depFireChevCanvas),
  roughness:0.4,metalness:0.1,
  polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-4
});















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








// =========================================================================
// =========================================================================
// =========================================================================
// HIGH-RESOLUTION VEHICLE TEXT DECALS (Ambulance Red & Fire Brigade Yellow)
// =========================================================================
let _depVehicleDecalMats = null;
function depGetDecalMaterials() {
  if (_depVehicleDecalMats) return _depVehicleDecalMats;
  _depVehicleDecalMats = {};

  function drawRedCross(ctx, cx, cy, sz) {
    ctx.fillStyle = '#dc2626';
    ctx.fillRect(cx - sz / 6, cy - sz / 2, sz / 3, sz);
    ctx.fillRect(cx - sz / 2, cy - sz / 6, sz, sz / 3);
  }

  // 1. Ambulance Side Decal - Crisp White Background, Red Borders, Red Crosses, Bold Red "AMBULANCE"
  const ambSideCanvas = document.createElement('canvas');
  ambSideCanvas.width = 1024;
  ambSideCanvas.height = 256;
  const asc = ambSideCanvas.getContext('2d');
  asc.fillStyle = '#ffffff';
  asc.fillRect(0, 0, 1024, 256);
  asc.lineWidth = 14;
  asc.strokeStyle = '#dc2626';
  asc.strokeRect(10, 10, 1004, 236);
  drawRedCross(asc, 95, 128, 95);
  drawRedCross(asc, 929, 128, 95);
  asc.fillStyle = '#dc2626';
  asc.font = '900 120px "Arial Black", Arial, sans-serif';
  asc.textAlign = 'center';
  asc.textBaseline = 'middle';
  asc.fillText('AMBULANCE', 512, 128);

  const texAmbSide = new THREE.CanvasTexture(ambSideCanvas);
  _depVehicleDecalMats.ambSide = new THREE.MeshStandardMaterial({
    map: texAmbSide,
    roughness: 0.25,
    metalness: 0.05,
    side: THREE.FrontSide,
    polygonOffset: true,
    polygonOffsetFactor: -3,
    polygonOffsetUnits: -6
  });

  // 2. Ambulance Front Decal - Bold Red "AMBULANCE"
  const ambFrontCanvas = document.createElement('canvas');
  ambFrontCanvas.width = 1024;
  ambFrontCanvas.height = 256;
  const afc = ambFrontCanvas.getContext('2d');
  afc.fillStyle = '#ffffff';
  afc.fillRect(0, 0, 1024, 256);
  afc.lineWidth = 14;
  afc.strokeStyle = '#dc2626';
  afc.strokeRect(10, 10, 1004, 236);
  drawRedCross(afc, 90, 128, 90);
  drawRedCross(afc, 934, 128, 90);
  afc.fillStyle = '#dc2626';
  afc.font = '900 124px "Arial Black", Arial, sans-serif';
  afc.textAlign = 'center';
  afc.textBaseline = 'middle';
  afc.fillText('AMBULANCE', 512, 128);

  const texAmbFront = new THREE.CanvasTexture(ambFrontCanvas);
  _depVehicleDecalMats.ambFront = new THREE.MeshStandardMaterial({
    map: texAmbFront,
    roughness: 0.25,
    metalness: 0.05,
    side: THREE.FrontSide,
    polygonOffset: true,
    polygonOffsetFactor: -3,
    polygonOffsetUnits: -6
  });

  // 3. Ambulance Rear Decal - Bold Red "AMBULANCE"
  const ambRearCanvas = document.createElement('canvas');
  ambRearCanvas.width = 1024;
  ambRearCanvas.height = 256;
  const arc = ambRearCanvas.getContext('2d');
  arc.fillStyle = '#ffffff';
  arc.fillRect(0, 0, 1024, 256);
  arc.lineWidth = 14;
  arc.strokeStyle = '#dc2626';
  arc.strokeRect(10, 10, 1004, 236);
  drawRedCross(arc, 90, 128, 90);
  drawRedCross(arc, 934, 128, 90);
  arc.fillStyle = '#dc2626';
  arc.font = '900 120px "Arial Black", Arial, sans-serif';
  arc.textAlign = 'center';
  arc.textBaseline = 'middle';
  arc.fillText('AMBULANCE', 512, 128);

  const texAmbRear = new THREE.CanvasTexture(ambRearCanvas);
  _depVehicleDecalMats.ambRear = new THREE.MeshStandardMaterial({
    map: texAmbRear,
    roughness: 0.25,
    metalness: 0.05,
    side: THREE.FrontSide,
    polygonOffset: true,
    polygonOffsetFactor: -3,
    polygonOffsetUnits: -6
  });

  // 4. Fire Brigade Front Decal - Bold Yellow "FIRE BRIGADE"
  const fireFrontCanvas = document.createElement('canvas');
  fireFrontCanvas.width = 1024;
  fireFrontCanvas.height = 256;
  const ffc = fireFrontCanvas.getContext('2d');
  ffc.fillStyle = '#0f172a';
  ffc.fillRect(0, 0, 1024, 256);
  ffc.lineWidth = 14;
  ffc.strokeStyle = '#facc15';
  ffc.strokeRect(12, 12, 1000, 232);
  ffc.lineWidth = 4;
  ffc.strokeStyle = '#fef08a';
  ffc.strokeRect(26, 26, 972, 204);
  ffc.fillStyle = '#facc15';
  ffc.font = '900 120px "Arial Black", Arial, sans-serif';
  ffc.textAlign = 'center';
  ffc.textBaseline = 'middle';
  ffc.fillText('FIRE BRIGADE', 512, 128);

  const texFireFront = new THREE.CanvasTexture(fireFrontCanvas);
  _depVehicleDecalMats.fireFront = new THREE.MeshStandardMaterial({
    map: texFireFront,
    roughness: 0.3,
    metalness: 0.1,
    side: THREE.FrontSide,
    polygonOffset: true,
    polygonOffsetFactor: -3,
    polygonOffsetUnits: -6
  });

  // 5. Fire Brigade Rear Decal - Bold Yellow "FIRE BRIGADE" with Safety Chevrons
  const fireRearCanvas = document.createElement('canvas');
  fireRearCanvas.width = 1024;
  fireRearCanvas.height = 256;
  const frc = fireRearCanvas.getContext('2d');
  frc.fillStyle = '#facc15';
  frc.fillRect(0, 0, 1024, 256);
  frc.fillStyle = '#dc2626';
  for (let x = -256; x <= 1024; x += 64) {
    frc.beginPath();
    frc.moveTo(x, 256);
    frc.lineTo(x + 64, 0);
    frc.lineTo(x + 104, 0);
    frc.lineTo(x + 40, 256);
    frc.fill();
  }
  frc.fillStyle = '#0f172a';
  frc.fillRect(60, 36, 904, 184);
  frc.lineWidth = 10;
  frc.strokeStyle = '#facc15';
  frc.strokeRect(66, 42, 892, 172);
  frc.fillStyle = '#facc15';
  frc.font = '900 115px "Arial Black", Arial, sans-serif';
  frc.textAlign = 'center';
  frc.textBaseline = 'middle';
  frc.fillText('FIRE BRIGADE', 512, 128);

  const texFireRear = new THREE.CanvasTexture(fireRearCanvas);
  _depVehicleDecalMats.fireRear = new THREE.MeshStandardMaterial({
    map: texFireRear,
    roughness: 0.3,
    metalness: 0.1,
    side: THREE.FrontSide,
    polygonOffset: true,
    polygonOffsetFactor: -3,
    polygonOffsetUnits: -6
  });

  return _depVehicleDecalMats;
}

function depAddDecal(g, mat, pos, size, rotY, rotX) {
  const geo = (typeof geos !== 'undefined' && geos.sign) ? geos.sign : new THREE.PlaneGeometry(1, 1);
  const mesh = new THREE.Mesh(geo, mat);
  mesh.position.fromArray(pos);
  mesh.scale.set(size[0], size[1], 1);
  if (rotY) mesh.rotation.y = rotY;
  if (rotX) mesh.rotation.x = rotX;
  mesh.renderOrder = 6;
  g.add(mesh);
  return mesh;
}

// =========================================================================
// 1. HIGH-INTENSITY MOBILE GENERATOR FLOODLIGHT TOWER (Heavy Industrial Spec)
// =========================================================================
function depBuildLight(g) {
  g.scale.setScalar(1);

  // 1. Mobile Trailer Chassis & Outrigger Stabilizers
  depPart(g, 'box', [0, 0.32, 0], [1.25, 0.16, 2.1], 'dark');
  // Trailer tongue / A-frame drawbar with ball hitch & jockey caster wheel
  depPart(g, 'box', [0, 0.28, -1.35], [0.42, 0.08, 0.75], 'dark');
  depPart(g, 'cylinder', [0, 0.18, -1.65], [0.08, 0.24, 0.08], 'chrome');
  depPart(g, 'cylinder', [0, 0.06, -1.65], [0.12, 0.06, 0.12], 'tireRubber');

  // 2 Rubber Road Wheels with Chrome Hubcaps
  for (const wx of [-0.72, 0.72]) {
    const wGroup = new THREE.Group();
    wGroup.position.set(wx, 0.36, 0.12);
    g.add(wGroup);
    const tire = depPart(wGroup, 'cylinder', [0, 0, 0], [0.36, 0.16, 0.36], 'tireRubber');
    tire.rotation.z = Math.PI / 2;
    const rim = depPart(wGroup, 'cylinder', [0, 0, 0], [0.22, 0.17, 0.22], 'chrome');
    rim.rotation.z = Math.PI / 2;
    depPart(g, 'box', [wx > 0 ? 0.68 : -0.68, 0.54, 0.12], [0.18, 0.22, 0.85], 'dark');
  }

  // 4 Diagonal Outrigger Stabilizer Arms with Screw Jack Footpads
  const outriggers = [
    [-0.95, -0.85], [0.95, -0.85],
    [-0.95, 0.95], [0.95, 0.95]
  ];
  for (const [ox, oz] of outriggers) {
    const leg = depPart(g, 'box', [ox * 0.65, 0.22, oz * 0.65], [0.08, 0.08, 0.65], 'dark');
    leg.rotation.y = Math.atan2(ox, oz);
    depPart(g, 'cylinder', [ox, 0.18, oz], [0.035, 0.32, 0.035], 'chrome');
    depPart(g, 'cylinder', [ox, 0.03, oz], [0.18, 0.04, 0.18], 'yellow');
  }

  // 2. Soundproof Acoustic Generator Enclosure (DG Set)
  depPart(g, 'box', [0, 0.76, 0], [1.12, 0.72, 1.82], 'yellow');
  depPart(g, 'box', [0, 0.76, -0.92], [0.82, 0.48, 0.04], 'dark');
  for (const sx of [-0.57, 0.57]) {
    depPart(g, 'box', [sx, 0.76, 0.05], [0.02, 0.55, 1.25], 'dark');
    depPart(g, 'box', [sx * 1.01, 0.76, -0.2], [0.02, 0.08, 0.04], 'chrome');
  }
  depPart(g, 'cylinder', [0.32, 1.22, -0.35], [0.055, 0.28, 0.055], 'dark');
  depPart(g, 'box', [0.32, 1.36, -0.33], [0.08, 0.02, 0.12], 'dark');

  // 3. Telescopic Steel Mast Tower (~4.2m elevation)
  depPart(g, 'box', [0, 1.25, 0.45], [0.32, 0.28, 0.35], 'dark');
  depPart(g, 'cylinder', [0.22, 1.25, 0.45], [0.08, 0.12, 0.08], 'yellow');
  depPart(g, 'box', [0, 2.05, 0.45], [0.18, 1.45, 0.18], 'dark');
  depPart(g, 'box', [0, 3.15, 0.45], [0.13, 1.35, 0.13], 'chrome');
  depPart(g, 'box', [0, 4.05, 0.45], [0.09, 1.25, 0.09], 'chrome');

  // Winch & heavy cable
  depPart(g, 'cylinder', [0, 1.8, 0.58], [0.08, 0.16, 0.08], 'dark');
  depPart(g, 'cylinder', [0, 2.8, 0.54], [0.015, 1.8, 0.015], 'dark');

  // 4. Floodlight Masthead Crossbar & 4 Stadium LED Floodlights
  depPart(g, 'box', [0, 4.45, 0.45], [1.95, 0.08, 0.08], 'dark');
  depPart(g, 'box', [0, 4.54, 0.45], [0.14, 0.10, 0.14], 'dark');

  const lampOffsets = [-0.82, -0.28, 0.28, 0.82];
  for (const lx of lampOffsets) {
    const lamp = new THREE.Group();
    lamp.position.set(lx, 4.38, 0.45);
    lamp.rotation.x = 0.42;
    g.add(lamp);

    depPart(lamp, 'cylinder', [0, 0.08, 0], [0.02, 0.14, 0.02], 'dark');
    depPart(lamp, 'box', [0, 0, 0.08], [0.34, 0.26, 0.14], 'dark');
    for (const fz of [0.04, 0.08, 0.12]) {
      depPart(lamp, 'box', [0, 0, fz], [0.32, 0.24, 0.015], 'chrome');
    }
    const lens = depPart(lamp, 'box', [0, 0, -0.01], [0.30, 0.22, 0.02], 'white');
    lens.material = new THREE.MeshStandardMaterial({
      color: 0xffffee,
      emissive: 0xfffee0,
      emissiveIntensity: 2.5
    });
    depPart(lamp, 'box', [0, 0.13, -0.04], [0.32, 0.02, 0.08], 'dark');
    depPart(lamp, 'box', [0, -0.13, -0.04], [0.32, 0.02, 0.08], 'dark');
    depPart(lamp, 'box', [-0.16, 0, -0.04], [0.02, 0.26, 0.08], 'dark');
    depPart(lamp, 'box', [0.16, 0, -0.04], [0.02, 0.26, 0.08], 'dark');
  }
}

// =========================================================================
// 2. EMERGENCY MEDICAL AMBULANCE (Force Traveller / 108 ALS High-Roof)
// =========================================================================
function depBuildAmbulance(g) {
  g.scale.setScalar(1);

  // 1. Heavy Underbody Chassis Frame & Bumpers
  depPart(g, 'box', [0, 0.32, 0], [1.78, 0.22, 5.0], 'dark');
  depPart(g, 'box', [0, 0.44, -2.58], [2.12, 0.36, 0.34], 'dark');
  depPart(g, 'box', [0, 0.38, -2.74], [1.35, 0.16, 0.06], 'dark');
  depPart(g, 'box', [0, 0.42, 2.52], [2.12, 0.22, 0.36], 'dark');
  depPart(g, 'box', [0, 0.54, 2.55], [1.75, 0.03, 0.32], 'chrome');

  // 2. Four Deep-Tread Rubber Tires & Steel Rims
  const wCoords = [
    [-0.98, 0.38, -1.55], [0.98, 0.38, -1.55],
    [-0.98, 0.38, 1.45], [0.98, 0.38, 1.45]
  ];
  for (const [wx, wy, wz] of wCoords) {
    const wGroup = new THREE.Group();
    wGroup.position.set(wx, wy, wz);
    g.add(wGroup);
    const tire = depPart(wGroup, 'cylinder', [0, 0, 0], [0.38, 0.24, 0.38], 'tireRubber');
    tire.rotation.z = Math.PI / 2;
    const rim = depPart(wGroup, 'cylinder', [0, 0, 0], [0.26, 0.25, 0.26], 'chrome');
    rim.rotation.z = Math.PI / 2;
    const hub = depPart(wGroup, 'cylinder', [wx > 0 ? 0.13 : -0.13, 0, 0], [0.10, 0.04, 0.10], 'dark');
    hub.rotation.z = Math.PI / 2;
    depPart(g, 'cylinder', [wx > 0 ? 1.04 : -1.04, wy + 0.18, wz], [0.46, 0.08, 0.46], 'dark');
    if (wz > 0) {
      depPart(g, 'box', [wx > 0 ? 0.98 : -0.98, 0.28, wz + 0.46], [0.24, 0.28, 0.03], 'dark');
    }
  }

  // 3. Front Cab Nose, Chrome Radiator Grille & Projector Headlights
  depPart(g, 'box', [0, 0.74, -2.62], [1.32, 0.34, 0.08], 'dark');
  depPart(g, 'box', [0, 0.78, -2.65], [1.05, 0.04, 0.04], 'chrome');
  depPart(g, 'box', [0, 0.70, -2.65], [1.05, 0.04, 0.04], 'chrome');
  depPart(g, 'cylinder', [0, 0.74, -2.66], [0.10, 0.02, 0.10], 'white');
  depPart(g, 'box', [0, 0.74, -2.68], [0.14, 0.04, 0.02], 'qbeltRibbon');
  depPart(g, 'box', [0, 0.74, -2.68], [0.04, 0.14, 0.02], 'qbeltRibbon');

  for (const hx of [-0.82, 0.82]) {
    depPart(g, 'box', [hx, 0.74, -2.59], [0.34, 0.22, 0.06], 'chrome');
    const lens = depPart(g, 'box', [hx, 0.74, -2.62], [0.32, 0.20, 0.02], 'white');
    lens.material = new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0xfef08a, emissiveIntensity: 1.2 });
    depPart(g, 'box', [hx > 0 ? hx + 0.14 : hx - 0.14, 0.74, -2.58], [0.08, 0.20, 0.07], 'yellow');
    depPart(g, 'cylinder', [hx, 0.44, -2.68], [0.07, 0.03, 0.07], 'yellow');
  }

  // 4. Aerodynamic Sloping Hood & Windshield
  depPart(g, 'box', [0, 1.08, -2.14], [2.02, 0.46, 1.05], 'whiteBody');
  depPart(g, 'box', [0, 1.32, -2.25], [1.25, 0.12, 0.02], 'qbeltRibbon');

  const ws = depPart(g, 'box', [0, 1.58, -1.56], [1.92, 0.82, 0.08], 'glassTint');
  ws.rotation.x = -0.48;
  for (const wipX of [-0.42, 0.36]) {
    const wiper = depPart(g, 'cylinder', [wipX, 1.36, -1.74], [0.012, 0.46, 0.012], 'dark');
    wiper.rotation.set(-0.48, 0, 0.28);
  }

  for (const mx of [-1.16, 1.16]) {
    depPart(g, 'cylinder', [mx > 0 ? mx - 0.08 : mx + 0.08, 1.48, -1.46], [0.02, 0.26, 0.02], 'dark');
    depPart(g, 'box', [mx, 1.48, -1.48], [0.10, 0.28, 0.08], 'dark');
    depPart(g, 'box', [mx, 1.48, -1.44], [0.08, 0.24, 0.01], 'chrome');
  }

  // 5. Patient Saloon Body & Aerodynamic High Roof
  depPart(g, 'box', [0, 1.46, 0.28], [2.10, 1.62, 3.95], 'whiteBody');
  depPart(g, 'rounded', [0, 2.32, 0.28], [2.04, 0.38, 3.90], 'whiteBody');

  // 6. Authentic 108 Emergency Medical Livery
  for (const sx of [-1.06, 1.06]) {
    depPart(g, 'box', [sx, 0.88, 0.28], [0.02, 0.24, 3.90], 'yellow');
    depPart(g, 'box', [sx, 1.02, 0.28], [0.02, 0.08, 3.90], 'qbeltRibbon');

    depPart(g, 'box', [sx, 1.72, 0.35], [0.02, 0.54, 2.75], 'glassTint');
    depPart(g, 'box', [sx * 1.01, 1.72, 0.35], [0.02, 0.56, 0.12], 'dark');

    depPart(g, 'box', [sx, 1.58, -1.25], [0.02, 0.52, 0.72], 'glassTint');
    depPart(g, 'box', [sx * 1.02, 1.15, -0.95], [0.02, 0.04, 0.14], 'dark');
    depPart(g, 'box', [sx * 1.02, 1.05, 1.25], [0.02, 0.04, 0.14], 'dark');
  }

  // 7. Roof Emergency Strobe Lightbar & Siren
  depPart(g, 'box', [0, 2.45, -1.25], [1.75, 0.10, 0.35], 'dark');
  const ledCols = ['vipBeaconRed', 'vipBeaconRed', 'white', 'vipBeaconBlue', 'vipBeaconBlue'];
  for (let i = 0; i < ledCols.length; i++) {
    const lx = -0.65 + i * 0.325;
    depPart(g, 'box', [lx, 2.47, -1.25], [0.28, 0.08, 0.30], ledCols[i]);
  }
  depPart(g, 'cylinder', [0, 2.42, -1.55], [0.12, 0.16, 0.12], 'chrome');
  depPart(g, 'box', [-0.85, 2.42, 2.15], [0.14, 0.08, 0.10], 'vipBeaconRed');
  depPart(g, 'box', [0.85, 2.42, 2.15], [0.14, 0.08, 0.10], 'vipBeaconBlue');
  depPart(g, 'box', [0, 2.46, 0.75], [0.95, 0.16, 1.45], 'whiteBody');

  // 8. Rear Patient Loading Twin Doors
  depPart(g, 'box', [0, 1.45, 2.26], [1.95, 1.55, 0.02], 'whiteBody');
  depPart(g, 'box', [0, 1.45, 2.27], [0.03, 1.55, 0.02], 'dark');
  for (const rx of [-0.48, 0.48]) {
    depPart(g, 'box', [rx, 1.72, 2.27], [0.65, 0.52, 0.02], 'glassTint');
  }
  for (const tx of [-0.98, 0.98]) {
    depPart(g, 'box', [tx, 1.15, 2.27], [0.08, 0.18, 0.02], 'vipBeaconRed');
    depPart(g, 'box', [tx, 0.92, 2.27], [0.08, 0.16, 0.02], 'yellow');
    depPart(g, 'box', [tx, 0.72, 2.27], [0.08, 0.12, 0.02], 'white');
  }

  // 9. Official Emergency Text Markings (Front, Rear & Both Sides in Bold Red)
  const ambDecals = depGetDecalMaterials();
  // Front Cab Hood Markings
  depAddDecal(g, ambDecals.ambFront, [0, 1.15, -2.68], [1.35, 0.28], Math.PI);
  // Sloping Cab Visor Markings
  depAddDecal(g, ambDecals.ambFront, [0, 2.14, -1.90], [1.45, 0.22], Math.PI, 0.45);
  // Rear Patient Twin Doors Markings
  depAddDecal(g, ambDecals.ambRear, [0, 1.25, 2.29], [1.55, 0.32], 0);
  // Right Flank Saloon Markings
  depAddDecal(g, ambDecals.ambSide, [1.07, 1.25, 0.28], [2.6, 0.36], Math.PI / 2);
  // Left Flank Saloon Markings
  depAddDecal(g, ambDecals.ambSide, [-1.07, 1.25, 0.28], [2.6, 0.36], -Math.PI / 2);
}

// =========================================================================
// 3. HEAVY-DUTY WATER & FOAM FIRE TENDER TRUCK (Tata/Leyland 6x4 Fire Engine)
// =========================================================================
function depBuildFireBrigade(g) {
  g.scale.setScalar(1);

  // 1. Heavy 6x4 Truck Chassis Frame & Massive Push Bumper
  depPart(g, 'box', [0, 0.42, 0], [2.10, 0.28, 7.6], 'dark');
  depPart(g, 'box', [0, 0.54, -3.85], [2.55, 0.44, 0.38], 'dark');
  for (const hx of [-0.75, 0.75]) {
    depPart(g, 'torus', [hx, 0.54, -4.06], [0.10, 0.03, 1], 'chrome');
  }
  depPart(g, 'box', [0, 0.48, 3.65], [2.52, 0.26, 0.42], 'dark');

  // 2. Six Heavy-Duty Truck Wheels (3 Axles: Front + Dual Rear Drive Axles)
  const twCoords = [
    [-1.18, 0.54, -2.55], [1.18, 0.54, -2.55],
    [-1.18, 0.54, 1.65], [1.18, 0.54, 1.65],
    [-1.18, 0.54, 2.95], [1.18, 0.54, 2.95]
  ];
  for (const [wx, wy, wz] of twCoords) {
    const wGroup = new THREE.Group();
    wGroup.position.set(wx, wy, wz);
    g.add(wGroup);
    const tire = depPart(wGroup, 'cylinder', [0, 0, 0], [0.52, 0.28, 0.52], 'tireRubber');
    tire.rotation.z = Math.PI / 2;
    const rim = depPart(wGroup, 'cylinder', [0, 0, 0], [0.35, 0.29, 0.35], 'fireRed');
    rim.rotation.z = Math.PI / 2;
    const hub = depPart(wGroup, 'cylinder', [wx > 0 ? 0.15 : -0.15, 0, 0], [0.14, 0.04, 0.14], 'chrome');
    hub.rotation.z = Math.PI / 2;
    depPart(g, 'cylinder', [wx > 0 ? 1.22 : -1.22, wy + 0.22, wz], [0.62, 0.12, 0.62], 'dark');
  }

  // 3. Forward-Control Crew Cab (Vibrant Signal Red)
  depPart(g, 'box', [0, 1.58, -2.45], [2.48, 1.75, 2.45], 'fireRed');
  depPart(g, 'box', [0, 0.95, -3.72], [1.85, 0.52, 0.08], 'dark');
  depPart(g, 'box', [0, 1.02, -3.75], [1.45, 0.06, 0.04], 'chrome');
  depPart(g, 'box', [0, 0.90, -3.75], [1.45, 0.06, 0.04], 'chrome');

  for (const hx of [-0.98, 0.98]) {
    depPart(g, 'box', [hx, 0.95, -3.70], [0.36, 0.26, 0.06], 'chrome');
    const hl = depPart(g, 'box', [hx, 0.95, -3.74], [0.32, 0.22, 0.02], 'white');
    hl.material = new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0xfef08a, emissiveIntensity: 1.2 });
    depPart(g, 'box', [hx > 0 ? hx + 0.15 : hx - 0.15, 0.95, -3.71], [0.10, 0.22, 0.06], 'yellow');
  }

  const ws = depPart(g, 'box', [0, 1.88, -3.58], [2.32, 0.85, 0.08], 'glassTint');
  ws.rotation.x = -0.12;
  depPart(g, 'box', [0, 2.36, -3.62], [2.38, 0.14, 0.22], 'dark');
  for (const wpX of [-0.75, 0, 0.75]) {
    const wip = depPart(g, 'cylinder', [wpX, 1.62, -3.68], [0.015, 0.52, 0.015], 'dark');
    wip.rotation.set(-0.12, 0, 0.18);
  }

  for (const sx of [-1.26, 1.26]) {
    depPart(g, 'box', [sx, 1.88, -3.0], [0.02, 0.62, 0.85], 'glassTint');
    depPart(g, 'box', [sx, 1.88, -2.0], [0.02, 0.62, 0.85], 'glassTint');
    depPart(g, 'cylinder', [sx * 1.02, 1.45, -3.45], [0.02, 0.95, 0.02], 'chrome');
    depPart(g, 'cylinder', [sx * 1.02, 1.45, -1.55], [0.02, 0.95, 0.02], 'chrome');
    depPart(g, 'box', [sx, 0.65, -2.5], [0.16, 0.08, 2.2], 'chrome');

    depPart(g, 'cylinder', [sx > 0 ? sx - 0.12 : sx + 0.12, 1.82, -3.42], [0.025, 0.65, 0.025], 'dark');
    depPart(g, 'box', [sx, 1.82, -3.45], [0.12, 0.44, 0.18], 'dark');
    depPart(g, 'box', [sx, 1.82, -3.38], [0.10, 0.40, 0.02], 'chrome');
  }

  depPart(g, 'box', [0, 2.54, -3.15], [2.10, 0.12, 0.38], 'dark');
  for (let i = 0; i < 6; i++) {
    const lx = -0.85 + i * 0.34;
    depPart(g, 'box', [lx, 2.58, -3.15], [0.28, 0.10, 0.32], (i < 3 ? 'vipBeaconRed' : 'vipBeaconBlue'));
  }
  for (const hx of [-0.42, 0.42]) {
    depPart(g, 'cylinder', [hx, 2.58, -3.55], [0.06, 0.48, 0.06], 'chrome');
    depPart(g, 'cylinder', [hx, 2.58, -3.78], [0.11, 0.06, 0.11], 'chrome');
  }

  // 4. Heavy Equipment Saloon Body & Roll-up Silver Shutters
  depPart(g, 'box', [0, 1.72, 1.05], [2.48, 1.95, 4.85], 'fireRed');
  depPart(g, 'box', [0, 1.35, 1.05], [2.52, 0.08, 4.85], 'white');

  for (const sx of [-1.26, 1.26]) {
    for (const bz of [-0.85, 0.85, 2.35]) {
      depPart(g, 'box', [sx, 1.62, bz], [0.02, 1.32, 1.25], 'shutterSilver');
      depPart(g, 'box', [sx * 1.01, 1.62, bz], [0.02, 1.36, 1.30], 'dark');
      depPart(g, 'box', [sx * 1.02, 1.05, bz], [0.02, 0.06, 0.45], 'chrome');
    }
  }

  // 5. Roof Heavy Equipment: Extendable Ladder & Water Monitor Gun
  depPart(g, 'box', [0, 2.74, 1.05], [2.32, 0.06, 4.70], 'dark');
  depPart(g, 'box', [-0.62, 2.92, 1.15], [0.55, 0.18, 4.40], 'shutterSilver');
  for (let rz = -0.8; rz <= 3.1; rz += 0.35) {
    depPart(g, 'cylinder', [-0.62, 2.92, rz], [0.025, 0.48, 0.025], 'chrome');
  }

  const monGroup = new THREE.Group();
  monGroup.position.set(0.48, 2.82, -0.65);
  g.add(monGroup);
  depPart(monGroup, 'cylinder', [0, 0.12, 0], [0.18, 0.24, 0.18], 'fireRed');
  depPart(monGroup, 'cylinder', [0, 0.28, 0], [0.10, 0.16, 0.10], 'chrome');
  depPart(monGroup, 'torus', [0, 0.32, 0], [0.12, 0.035, 1], 'yellow');
  const barrel = depPart(monGroup, 'cylinder', [0, 0.44, -0.25], [0.06, 0.65, 0.06], 'chrome');
  barrel.rotation.x = -Math.PI / 4;
  depPart(monGroup, 'cylinder', [0, 0.64, -0.46], [0.09, 0.16, 0.09], 'yellow');

  for (const hx of [-1.12, 1.12]) {
    depPart(g, 'cylinder', [hx, 2.82, 1.35], [0.075, 3.8, 0.075], 'dark');
    depPart(g, 'torus', [hx, 2.82, -0.45], [0.09, 0.03, 1], 'chrome');
    depPart(g, 'torus', [hx, 2.82, 3.15], [0.09, 0.03, 1], 'chrome');
  }

  // 6. Rear Pump Console & Discharge Valves
  depPart(g, 'box', [0, 1.85, 3.82], [1.45, 0.48, 0.08], 'dark');
  for (const vx of [-0.52, 0.52]) {
    depPart(g, 'cylinder', [vx, 1.62, 3.88], [0.08, 0.12, 0.08], 'chrome');
  }

  // 7. Official Emergency Text Markings (Front & Rear in Bold Yellow)
  const fireDecals = depGetDecalMaterials();
  // Front Roof Sunvisor Markings
  depAddDecal(g, fireDecals.fireFront, [0, 2.38, -3.67], [2.25, 0.26], Math.PI, 0.12);
  // Front Crew Cab Nose Plate Markings
  depAddDecal(g, fireDecals.fireFront, [0, 1.28, -3.75], [1.85, 0.30], Math.PI);
  // Rear Heavy Tailgate / Hazard Console Markings
  depAddDecal(g, fireDecals.fireRear, [0, 1.35, 3.86], [2.25, 0.48], 0);
}

// =========================================================================
// 4. MULTI-BAY VEHICLE PARKING FACILITY (Haryana Police Bus, VIP SUVs & Stalls)
// =========================================================================
function depBuildParking(g) { depBuildParkingLot(g); }
function depBuildParkingLot(g) {
  g.scale.setScalar(1.0);

  // 1. Heavy Asphalt Tarmac Ground Pavement (14.4m x 13.2m: 10 Bays in 2 Rows of 5)
  depPart(g, 'box', [0, 0.05, 0], [14.4, 0.10, 13.2], 'padAsphalt');

  // Perimeter Raised Concrete Curbing with Yellow/Black Safety Stripes
  depPart(g, 'box', [0, 0.14, -6.62], [14.6, 0.14, 0.22], 'dark');
  depPart(g, 'box', [0, 0.14, 6.62], [14.6, 0.14, 0.22], 'dark');
  depPart(g, 'box', [-7.22, 0.14, 0], [0.22, 0.14, 13.4], 'dark');
  depPart(g, 'box', [7.22, 0.14, 0], [0.22, 0.14, 13.4], 'dark');

  // 2. Central Driving Lane Separator (Yellow Line between Row 1 and Row 2)
  depPart(g, 'box', [0, 0.11, 0], [13.2, 0.015, 0.16], 'padLineYellow');

  // 3. ROW 1 (5 BAYS, NORTH: Bay 1 to 5, Z from -6.2 to -0.8)
  const bayXs = [-6.5, -3.9, -1.3, 1.3, 3.9, 6.5];
  const bayCenters = [-5.2, -2.6, 0.0, 2.6, 5.2];

  // White stall divider lines for Row 1
  for (const bx of bayXs) {
    depPart(g, 'box', [bx, 0.11, -3.6], [0.12, 0.015, 5.2], 'padLineWhite');
  }
  // Back curb stops for Row 1 (5 stalls)
  for (const cx of bayCenters) {
    depPart(g, 'box', [cx, 0.16, -5.9], [1.7, 0.12, 0.20], 'padLineYellow');
  }

  // 4. ROW 2 (5 BAYS, SOUTH: Bay 6 to 10, Z from 0.8 to 6.2)
  // White stall divider lines for Row 2
  for (const bx of bayXs) {
    depPart(g, 'box', [bx, 0.11, 3.6], [0.12, 0.015, 5.2], 'padLineWhite');
  }
  // Back curb stops for Row 2 (5 stalls)
  for (const cx of bayCenters) {
    depPart(g, 'box', [cx, 0.16, 5.9], [1.7, 0.12, 0.20], 'padLineYellow');
  }

  // Row 1 & 2 Entrance Line Markings
  depPart(g, 'box', [0, 0.11, -1.1], [13.0, 0.015, 0.10], 'padLineWhite');
  depPart(g, 'box', [0, 0.11, 1.1], [13.0, 0.015, 0.10], 'padLineWhite');

  // Directional Driving Arrows in Central Lane
  depPart(g, 'box', [-2.5, 0.11, 0], [1.2, 0.015, 0.12], 'padLineWhite');
  depPart(g, 'box', [2.5, 0.11, 0], [1.2, 0.015, 0.12], 'padLineWhite');

  // Blue & White "P" Parking Facility Signpost
  const pSign = new THREE.Group();
  pSign.position.set(-6.6, 0, 6.0);
  g.add(pSign);
  depPart(pSign, 'cylinder', [0, 1.25, 0], [0.045, 2.5, 0.045], 'chrome');
  depPart(pSign, 'box', [0, 2.45, 0], [0.65, 0.65, 0.05], 'blue');
  depPart(pSign, 'cylinder', [0, 2.45, 0.03], [0.28, 0.02, 0.28], 'white');
  depPart(pSign, 'box', [-0.06, 2.45, 0.045], [0.08, 0.35, 0.02], 'blue');
  depPart(pSign, 'torus', [0.02, 2.52, 0.045], [0.08, 0.03, 1], 'blue');

  // Solar LED Parking Floodlight Pole (Opposite Corner)
  const pole = new THREE.Group();
  pole.position.set(6.6, 0, -6.0);
  g.add(pole);
  depPart(pole, 'cylinder', [0, 2.2, 0], [0.06, 4.4, 0.06], 'chrome');
  depPart(pole, 'box', [0, 4.35, 0.2], [0.35, 0.08, 0.55], 'dark');
  depPart(pole, 'box', [0, 4.30, 0.2], [0.30, 0.02, 0.50], 'white');

  // 5. VEHICLES IN DESIGNATED BAYS (Leaving Bays 2, 4, 5 in Row 1 & Bays 6, 8, 9 in Row 2 completely OPEN)

  // --- VEHICLE 1 (Row 1, Bay 1: x = -5.2): Police Security Van ---
  const bus = new THREE.Group();
  bus.position.set(-5.2, 0, -3.6);
  g.add(bus);
  depPart(bus, 'box', [0, 0.30, 0], [2.15, 0.22, 5.2], 'dark');
  for (const bx of [-1.05, 1.05]) {
    for (const bz of [-1.7, 1.6]) {
      const bw = depPart(bus, 'cylinder', [bx, 0.38, bz], [0.38, 0.22, 0.38], 'tireRubber');
      bw.rotation.z = Math.PI / 2;
      const rim = depPart(bus, 'cylinder', [bx, 0.38, bz], [0.24, 0.23, 0.24], 'dark');
      rim.rotation.z = Math.PI / 2;
    }
  }
  depPart(bus, 'box', [0, 1.45, 0], [2.20, 1.70, 5.15], 'darkBlue');
  depPart(bus, 'box', [0, 1.10, 0], [2.22, 0.28, 5.18], 'white');
  depPart(bus, 'box', [0, 0.95, 0], [2.23, 0.08, 5.20], 'vipBeaconRed');
  const bws = depPart(bus, 'box', [0, 1.62, -2.58], [2.05, 0.85, 0.06], 'glassTint');
  bws.rotation.x = -0.08;
  for (const sx of [-1.11, 1.11]) {
    depPart(bus, 'box', [sx, 1.65, 0.20], [0.02, 0.65, 3.8], 'glassTint');
  }
  depPart(bus, 'box', [0, 2.38, 0.3], [1.35, 0.18, 1.8], 'white');
  depPart(bus, 'box', [0, 2.40, -2.3], [0.30, 0.10, 0.22], 'vipBeaconRed');

  // --- VEHICLE 2 (Row 1, Bay 3: x = 0.0): White VIP Fortuner SUV ---
  const suv1 = new THREE.Group();
  suv1.position.set(0.0, 0, -3.6);
  g.add(suv1);
  depPart(suv1, 'box', [0, 0.28, 0], [1.85, 0.18, 4.4], 'dark');
  for (const sx of [-0.95, 0.95]) {
    for (const sz of [-1.35, 1.35]) {
      const sw = depPart(suv1, 'cylinder', [sx, 0.38, sz], [0.38, 0.22, 0.38], 'tireRubber');
      sw.rotation.z = Math.PI / 2;
      const srim = depPart(suv1, 'cylinder', [sx, 0.38, sz], [0.24, 0.23, 0.24], 'chrome');
      srim.rotation.z = Math.PI / 2;
    }
  }
  depPart(suv1, 'box', [0, 0.85, 0], [1.88, 0.65, 4.45], 'whiteBody');
  depPart(suv1, 'box', [0, 1.38, 0.2], [1.68, 0.62, 2.65], 'whiteBody');
  const sws1 = depPart(suv1, 'box', [0, 1.32, -1.18], [1.55, 0.55, 0.05], 'glassTint');
  sws1.rotation.x = -0.42;
  depPart(suv1, 'box', [0, 0.72, -2.24], [1.32, 0.26, 0.05], 'chrome');
  for (const hx of [-0.68, 0.68]) {
    depPart(suv1, 'box', [hx, 0.74, -2.23], [0.26, 0.14, 0.04], 'white');
  }
  depPart(suv1, 'box', [0, 1.74, 0.25], [1.25, 0.06, 2.1], 'chrome');

  // --- VEHICLE 3 (Row 2, Bay 7: x = -2.6): Executive Administration Sedan ---
  const car = new THREE.Group();
  car.position.set(-2.6, 0, 3.6);
  car.rotation.y = Math.PI; // parked facing aisle
  g.add(car);
  depPart(car, 'box', [0, 0.24, 0], [1.78, 0.16, 4.3], 'dark');
  for (const cx of [-0.90, 0.90]) {
    for (const cz of [-1.32, 1.32]) {
      const cw = depPart(car, 'cylinder', [cx, 0.32, cz], [0.32, 0.20, 0.32], 'tireRubber');
      cw.rotation.z = Math.PI / 2;
      const crim = depPart(car, 'cylinder', [cx, 0.32, cz], [0.20, 0.21, 0.20], 'chrome');
      crim.rotation.z = Math.PI / 2;
    }
  }
  depPart(car, 'box', [0, 0.64, 0], [1.80, 0.46, 4.35], 'shutterSilver');
  depPart(car, 'box', [0, 1.08, 0.12], [1.58, 0.48, 2.25], 'shutterSilver');
  const cws = depPart(car, 'box', [0, 1.05, -1.05], [1.46, 0.46, 0.05], 'glassTint');
  cws.rotation.x = -0.55;
  const crws = depPart(car, 'box', [0, 1.05, 1.28], [1.46, 0.46, 0.05], 'glassTint');
  crws.rotation.x = 0.55;

  // --- VEHICLE 4 (Row 2, Bay 10: x = 5.2): Black Security Escort SUV ---
  const suv2 = new THREE.Group();
  suv2.position.set(5.2, 0, 3.6);
  suv2.rotation.y = Math.PI; // parked facing aisle
  g.add(suv2);
  depPart(suv2, 'box', [0, 0.28, 0], [1.85, 0.18, 4.4], 'dark');
  for (const sx of [-0.95, 0.95]) {
    for (const sz of [-1.35, 1.35]) {
      const sw = depPart(suv2, 'cylinder', [sx, 0.38, sz], [0.38, 0.22, 0.38], 'tireRubber');
      sw.rotation.z = Math.PI / 2;
      const srim = depPart(suv2, 'cylinder', [sx, 0.38, sz], [0.24, 0.23, 0.24], 'dark');
      srim.rotation.z = Math.PI / 2;
    }
  }
  depPart(suv2, 'box', [0, 0.85, 0], [1.88, 0.65, 4.45], 'dark');
  depPart(suv2, 'box', [0, 1.38, 0.2], [1.68, 0.62, 2.65], 'dark');
  const sws2 = depPart(suv2, 'box', [0, 1.32, -1.18], [1.55, 0.55, 0.05], 'glassTint');
  sws2.rotation.x = -0.42;
  depPart(suv2, 'box', [-0.35, 0.74, -2.24], [0.22, 0.08, 0.04], 'vipBeaconRed');
  depPart(suv2, 'box', [0.35, 0.74, -2.24], [0.22, 0.08, 0.04], 'vipBeaconBlue');
  depPart(suv2, 'box', [-0.25, 1.74, 0.25], [0.24, 0.06, 0.12], 'vipBeaconRed');
  depPart(suv2, 'box', [0.25, 1.74, 0.25], [0.24, 0.06, 0.12], 'vipBeaconBlue');
}

// =========================================================================
// 5. OFFICIAL VIP HELIPAD (ICAO Spec Elevated Apron, Chevrons, Tower & Lights)
// =========================================================================
function depBuildHelipad(g) {
  g.scale.setScalar(1);

  const padGroup = new THREE.Group();

  // 1. Concrete Outer Foundation Rim (18.6m diameter)
  const rimMesh = new THREE.Mesh(geos.cylinder, depMaterials.padOuterRim);
  rimMesh.position.set(0, 0.04, 0);
  rimMesh.scale.set(18.6, 0.08, 18.6);
  padGroup.add(rimMesh);

  // 2. Dark Asphalt Safety Shoulder Apron (17.4m diameter)
  const apronMesh = new THREE.Mesh(geos.cylinder, depMaterials.padAsphalt);
  apronMesh.position.set(0, 0.09, 0);
  apronMesh.scale.set(17.4, 0.04, 17.4);
  padGroup.add(apronMesh);

  // 3. Central Slate Concrete TLOF Landing Core (14.2m diameter)
  const coreMesh = new THREE.Mesh(geos.cylinder, depMaterials.padConcrete);
  coreMesh.position.set(0, 0.12, 0);
  coreMesh.scale.set(14.2, 0.03, 14.2);
  padGroup.add(coreMesh);

  // 4. Yellow Concentric Touchdown & Lift-Off (TLOF) Safety Ring
  const tlofRing = new THREE.Mesh(geos.torus, depMaterials.padLineYellow);
  tlofRing.position.set(0, 0.14, 0);
  tlofRing.rotation.x = Math.PI / 2;
  tlofRing.scale.set(6.2, 6.2, 1);
  padGroup.add(tlofRing);

  // 5. Official Bold White ICAO "H" (3.8m Tall, 2.8m Wide)
  const hBarL = new THREE.Mesh(geos.box, depMaterials.padLineWhite);
  hBarL.position.set(-1.15, 0.145, 0);
  hBarL.scale.set(0.48, 0.02, 3.8);
  padGroup.add(hBarL);

  const hBarR = new THREE.Mesh(geos.box, depMaterials.padLineWhite);
  hBarR.position.set(1.15, 0.145, 0);
  hBarR.scale.set(0.48, 0.02, 3.8);
  padGroup.add(hBarR);

  const hCross = new THREE.Mesh(geos.box, depMaterials.padLineWhite);
  hCross.position.set(0, 0.145, 0);
  hCross.scale.set(1.85, 0.02, 0.52);
  padGroup.add(hCross);

  // 6. Perimeter Red & White Hazard Chevrons (48 Radial Segments)
  const numChevrons = 48;
  const chevRadius = 8.05;
  for (let i = 0; i < numChevrons; i++) {
    const angle = (i / numChevrons) * Math.PI * 2;
    const mat = (i % 2 === 0) ? depMaterials.padDashedRed : depMaterials.padLineWhite;
    const chev = new THREE.Mesh(geos.box, mat);
    chev.position.set(Math.cos(angle) * chevRadius, 0.115, Math.sin(angle) * chevRadius);
    chev.rotation.y = -angle;
    chev.scale.set(0.24, 0.02, 0.88);
    padGroup.add(chev);
  }

  // 7. Eight High-Intensity Green LED Perimeter Landing Guidance Lights
  for (let i = 0; i < 8; i++) {
    const angle = (i / 8) * Math.PI * 2;
    const lx = Math.cos(angle) * 7.4;
    const lz = Math.sin(angle) * 7.4;

    const base = new THREE.Mesh(geos.cylinder, depMaterials.padLightMetal);
    base.position.set(lx, 0.15, lz);
    base.scale.set(0.26, 0.14, 0.26);
    padGroup.add(base);

    const greenLed = new THREE.Mesh(geos.sphereSmooth, depMaterials.padLightTurquoise);
    greenLed.position.set(lx, 0.25, lz);
    greenLed.scale.set(0.12, 0.12, 0.12);
    padGroup.add(greenLed);
  }

  // 8. Four Corner Perimeter Floodlight Towers
  const cornerAngles = [Math.PI / 4, 3 * Math.PI / 4, 5 * Math.PI / 4, 7 * Math.PI / 4];
  for (const cAngle of cornerAngles) {
    const tx = Math.cos(cAngle) * 9.5;
    const tz = Math.sin(cAngle) * 9.5;

    const tower = new THREE.Mesh(geos.cylinder, depMaterials.padLightMetal);
    tower.position.set(tx, 1.2, tz);
    tower.scale.set(0.08, 2.4, 0.08);
    padGroup.add(tower);

    const head = new THREE.Mesh(geos.box, depMaterials.padLightTurquoise);
    head.position.set(tx, 2.45, tz);
    head.scale.set(0.35, 0.22, 0.25);
    head.lookAt(0, 0.2, 0);
    padGroup.add(head);
  }

  // 9. Standard High-Visibility Orange & White Striped Windsock
  const windGroup = new THREE.Group();
  windGroup.position.set(9.2, 0, -2.5);

  const mast = new THREE.Mesh(geos.cylinder, depMaterials.padLightMetal);
  mast.position.set(0, 2.2, 0);
  mast.scale.set(0.06, 4.4, 0.06);
  windGroup.add(mast);

  const sockRing = new THREE.Mesh(geos.torus, depMaterials.padLightMetal);
  sockRing.position.set(0.3, 4.4, 0);
  sockRing.rotation.y = Math.PI / 2;
  sockRing.scale.set(0.25, 0.25, 1);
  windGroup.add(sockRing);

  const sockBase = new THREE.Mesh(geos.cylinder, depMaterials.padWindsockOrange);
  sockBase.position.set(0.85, 4.4, 0);
  sockBase.rotation.z = -Math.PI / 2;
  sockBase.scale.set(0.24, 0.75, 0.20);
  windGroup.add(sockBase);

  const sockTip = new THREE.Mesh(geos.cylinder, depMaterials.padWindsockWhite);
  sockTip.position.set(1.52, 4.4, 0);
  sockTip.rotation.z = -Math.PI / 2;
  sockTip.scale.set(0.20, 0.65, 0.15);
  windGroup.add(sockTip);

  padGroup.add(windGroup);
  g.add(padGroup);
}

// =========================================================================
// 6. RETRACTABLE Q-BELT QUEUE BARRIER (Flared Bell Bases, Chrome Posts, Red Webbing)
// =========================================================================
function depBuildQBelt(g, span = 2.0) {
  g.scale.setScalar(1);
  const curSpan = (typeof span === 'number' && span >= 0.5) ? span : 2.0;
  const half = curSpan / 2;

  for (const px of [-half, half]) {
    depPart(g, 'cylinder', [px, 0.024, 0], [0.38, 0.048, 0.38], 'stanchionChrome');
    depPart(g, 'torus', [px, 0.008, 0], [0.192, 0.014, 1], 'dark');
    depPart(g, 'cylinder', [px, 0.065, 0], [0.12, 0.045, 0.12], 'stanchionChrome');
    depPart(g, 'cylinder', [px, 0.52, 0], [0.052, 0.88, 0.052], 'stanchionChrome');

    depPart(g, 'cylinder', [px, 0.94, 0], [0.082, 0.14, 0.082], 'stanchionChrome');
    for (const rot of [0, Math.PI / 2, Math.PI, -Math.PI / 2]) {
      const slot = depPart(g, 'box', [px + Math.sin(rot) * 0.044, 0.94, Math.cos(rot) * 0.044], [0.012, 0.09, 0.022], 'dark');
      slot.rotation.y = rot;
    }
    depPart(g, 'sphereSmooth', [px, 1.03, 0], [0.052, 0.052, 0.052], 'stanchionChrome');
  }

  const ribbonLen = Math.max(0.1, curSpan - 0.09);
  depPart(g, 'box', [0, 0.94, 0], [ribbonLen, 0.062, 0.008], 'qbeltRibbon');

  depPart(g, 'box', [half - 0.045, 0.94, 0], [0.035, 0.078, 0.022], 'stanchionChrome');
  depPart(g, 'box', [-half + 0.045, 0.94, 0], [0.035, 0.078, 0.022], 'stanchionChrome');
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







    hhmd.position.set(0,-.61,-.16);







    hhmd.quaternion.copy(rightArm.quaternion).invert();







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























    // High-contrast security scanner decals (Front & Back)







        // High-visibility yellow safety band across paddle top


    // High-contrast Garrett SuperScanner decals (Front & Back - zero Z-fighting, non-mirrored)
    depPart(hhmd, 'sign', [0, .255, .0125], [.068, .22, 1], depHhmdDecalFront);
    const decalBack = depPart(hhmd, 'sign', [0, .255, -.0125], [.068, .22, 1], depHhmdDecalBack);
    decalBack.rotation.y = Math.PI;







  }







  else if(mode === 'radio'){
    rightArm.rotation.set(1.88,0,-.16);baseRightArmRotX=1.88;
    const radioHand=new THREE.Group();radioHand.position.set(-.075,-.44,-.18);radioHand.quaternion.copy(rightArm.quaternion).invert();rightArm.add(radioHand);
    const device=new THREE.Group();device.position.set(-.012,-.14,-.040);radioHand.add(device);
    depPart(device,'rounded',[0,.055,0],[.10,.19,.060],'hhmdGrip');
    const ant=depPart(device,'cylinder',[-.029,.30,0],[.007,.30,.007],'dark');ant.rotation.z=-.04;
    for(const x of [.005,.030])depPart(device,'cylinder',[x,.163,0],[.010,.028,.010],'dark');
    for(let y=.065;y<=.13;y+=.012)depPart(device,'box',[0,y,-.032],[.073,.004,.004],'hhmdSpeaker');
    depPart(device,'box',[0,.035,-.033],[.055,.028,.004],'glassTint');
    for(const x of [-.02,0,.02])for(const y of [-.012,.006])depPart(device,'box',[x,y,-.033],[.010,.008,.004],'hhmdSpeaker');
    depPart(device,'box',[-.052,.07,0],[.008,.04,.028],'hhmdSpeaker');
    depPart(device,'sphereSmooth',[.03,.14,-.034],[.004,.004,.003],'hhmdLedGreen');
    depPart(radioHand,'rounded',[.040,-.005,-.045],[.025,.070,.035],'skin');
    depPart(radioHand,'rounded',[-.062,-.015,-.040],[.020,.045,.026],'skin');
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















// New deployable visual equipment; shared editor and backend lifecycle.
function depBuildRifle(g,y=1.06,z=-.30,lmg=false){
 depPart(g,'box',[.05,y,z],[.12,.13,.40],'dark');
 depPart(g,'box',[.05,y,z+.30],[.10,.12,.26],'dark');
 const barrel=depPart(g,'cylinder',[.05,y,z-.43],[.026,lmg?.65:.48,.026],'dark');barrel.rotation.x=Math.PI/2;
 depPart(g,'box',[.05,y-.16,z-.03],[.07,.24,.12],'dark');
 depPart(g,'box',[.05,y+.09,z-.08],[.04,.05,.12],'dark');
 if(lmg){depPart(g,'box',[.20,y-.12,z],[.24,.20,.25],'dark');for(const x of [-.14,.24]){const leg=depPart(g,'box',[x,y-.18,z-.57],[.025,.35,.025],'chrome');leg.rotation.z=x<0?-.4:.4;}}
}
function depBuildArmedOfficer(g){
 depBuildOfficer(g,'officer');
 const baton=[];g.traverse(m=>{if(m.isMesh&&m.material===depMaterials.lathi)baton.push(m);});for(const m of baton)m.parent.remove(m);
 const rifle=new THREE.Group();rifle.position.set(.12,1.02,-.28);rifle.rotation.y=Math.PI/2;rifle.rotation.z=-.30;g.add(rifle);
 depBuildRifle(rifle,0,0,false);
}
function depBuildQRT(g){
 if(!depBuildQRT.bodyMat)depBuildQRT.bodyMat=new THREE.MeshStandardMaterial({color:0x10151b,metalness:.65,roughness:.28});
 const body=depBuildQRT.bodyMat;
 const part=(p,s,m=body,shape='box')=>depPart(g,shape,p,s,m);
 part([0,.48,0],[1.85,.24,4.35],'dark');
 part([0,.91,0],[1.93,.64,4.25]);
 part([0,1.29,-1.50],[1.91,.23,1.30]);
 part([0,1.14,1.88],[1.92,.55,.15]);
 for(const x of [-.94,.94]){
  part([x,1.12,.30],[.08,.58,2.9]);
  part([x,1.70,.30],[.045,.76,2.75],'glassTint');
  for(const z of [-1.02,-.10,1.05,1.73])part([x,1.70,z],[.09,.85,.09]);
  part([x,2.10,.30],[.10,.10,2.94]);
  part([x*1.10,.56,.15],[.22,.12,2.78],'chrome');
  for(const z of [-.55,.67]){part([x*1.025,1.19,z],[.045,.06,.23],'chrome');part([x*1.035,.97,z],[.028,.035,1.03],'chrome');}
  part([x*1.14,1.61,-.98],[.21,.19,.29]);
 }
 const windshield=part([0,1.72,-1.04],[1.76,.77,.035],'glassTint');windshield.rotation.x=-.25;
 for(const x of [-.89,.89]){const pillar=part([x,1.72,-1.04],[.085,.85,.07]);pillar.rotation.x=-.25;}
 part([0,1.70,1.80],[1.78,.69,.035],'glassTint');
 part([0,2.12,-.53],[1.94,.12,1.45]);part([0,2.12,1.56],[1.94,.12,.55]);
 for(const x of [-.76,.76])part([x,2.12,.61],[.40,.12,1.6]);
 for(const x of [-.77,.77])part([x,2.25,.32],[.055,.07,2.70],'dark');
 for(const x of [-1.02,1.02])for(const z of [-1.32,1.36]){
  const w=part([x,.48,z],[.46,.25,.46],'tireRubber','cylinder');w.rotation.z=Math.PI/2;
  const rim=part([x*1.13,.48,z],[.30,.04,.30],'chrome','cylinder');rim.rotation.z=Math.PI/2;
  for(let i=0;i<5;i++){const a=i*Math.PI*2/5;part([x*1.16,.48+.18*Math.sin(a),z+.18*Math.cos(a)],[.018,.09,.10],'dark');}
  part([x*.91,.99,z],[.17,.08,.98]);
 }
 part([0,.57,-2.19],[2.02,.28,.19]);part([0,.83,-2.21],[.88,.32,.035],'dark');
 for(let x=-.36;x<.4;x+=.12)part([x,.85,-2.24],[.045,.24,.025],'chrome');
 for(const x of [-.72,.72]){part([x,1.02,-2.17],[.43,.28,.06],'glassTint');for(const dx of [-.10,.10])part([x+dx,1.02,-2.21],[.075,.075,.035],'white','sphereSmooth');part([x,.62,-2.29],[.12,.12,.035],'white','sphereSmooth');part([x,1.20,2.0],[.17,.43,.04],'red');}
 part([0,.63,-2.30],[.48,.12,.025],'white');
 part([0,2.25,-.72],[1.05,.06,.26],'dark');part([-.28,2.32,-.72],[.48,.12,.24],'vipBeaconRed');part([.28,2.32,-.72],[.48,.12,.24],'vipBeaconBlue');
 for(const [x,y,z,scale] of [[.46,.25,-.40,.78],[0,1.32,.72,.84]]){
  const man=new THREE.Group();depBuildOfficer(man,'officer');
  man.traverse(m=>{if(m.isMesh&&(m.material===depMaterials.khaki||m.material===depMaterials.trousers))m.material=depMaterials.blue;});
  man.scale.setScalar(scale);man.position.set(x,y,z);g.add(man);
 }
 part([0,2.28,.36],[.055,.38,.055],'chrome','cylinder');
 const mount=new THREE.Group();depBuildRifle(mount,2.58,.20,true);g.add(mount);
 for(const x of [-.48,.48]){part([x,2.63,.72],[.07,.83,.97],'dark');for(const z of [.30,1.11])part([x,2.63,z],[.08,.73,.025],'shutterMetal');}
 part([0,2.21,.72],[1.13,.09,1.15],'dark');
 if(!depBuildQRT.labelMat){const c=document.createElement('canvas');c.width=512;c.height=256;const ctx=c.getContext('2d');ctx.clearRect(0,0,512,256);ctx.fillStyle='#f04444';ctx.textAlign='center';ctx.font='bold 66px Arial';ctx.fillText('GURUGRAM',256,100);ctx.fillText('POLICE',256,182);const tex=new THREE.CanvasTexture(c);tex.encoding=THREE.sRGBEncoding;depBuildQRT.labelMat=new THREE.MeshStandardMaterial({map:tex,transparent:true,side:THREE.DoubleSide,roughness:.7});}
 for(const side of [-1,1]){const label=part([side*.99,1.08,-.53],[.82,.40,1],depBuildQRT.labelMat,'sign');label.rotation.y=side*Math.PI/2;}
}
function depBuildXray(g){
 depPart(g,'box',[0,.88,0],[1.14,.18,3.2],'chrome');
 depPart(g,'box',[0,.99,0],[.91,.05,3.35],'dark');
 for(const x of [-.58,.58])depPart(g,'box',[x,1.45,0],[.20,1.02,1.35],'blue');
 depPart(g,'box',[0,1.98,0],[1.36,.18,1.35],'blue');
 for(const x of [-.43,.43])for(const z of [-1.25,1.25])depPart(g,'box',[x,.43,z],[.09,.86,.09],'chrome');
 for(const z of [-.71,.71])for(let x=-.40;x<.45;x+=.10)depPart(g,'box',[x,1.49,z],[.085,.80,.025],'dark');
 for(let z=-1.5;z<1.55;z+=.15)depPart(g,'box',[0,1.025,z],[.88,.018,.018],'shutterMetal');
 depPart(g,'box',[.91,1.0,.20],[.48,.10,.65],'chrome');
 depPart(g,'box',[.91,1.36,.35],[.48,.35,.06],'dark');
 depPart(g,'box',[.91,1.36,.313],[.40,.27,.012],'blue');
 depPart(g,'box',[.91,1.08,-.03],[.39,.025,.18],'dark');
 depPart(g,'box',[0,1.20,-1.14],[.46,.30,.48],'crateWood');
 depPart(g,'box',[0,1.38,-1.14],[.18,.06,.05],'dark');
 for(const z of [-.75,.75])depPart(g,'box',[.60,1.84,z],[.08,.08,.06],'hhmdLedGreen');
}


// =========================================================================
// ULTRA-REALISTIC PTZ SURVEILLANCE CCTV SPEED DOME CAMERA BUILDER
// =========================================================================
function depBuildCCTV(g) {
  g.scale.setScalar(1);

  // 1. Concrete Foundation Plinth & Anchor Assembly
  depPart(g, 'box', [0, 0.05, 0], [0.65, 0.10, 0.65], 'cctvBasePad');
  depPart(g, 'cylinder', [0, 0.11, 0], [0.42, 0.025, 0.42], 'cctvMastGalv');

  // 4 Heavy-duty structural hex anchor bolts & nuts
  const boltRadius = 0.16;
  for (let a = 0; a < 4; a++) {
    const ang = (a * Math.PI) / 2 + Math.PI / 4;
    const bx = Math.cos(ang) * boltRadius;
    const bz = Math.sin(ang) * boltRadius;
    depPart(g, 'cylinder', [bx, 0.135, bz], [0.032, 0.035, 0.032], 'cctvAnchorBolt');
    depPart(g, 'cylinder', [bx, 0.165, bz], [0.018, 0.030, 0.018], 'cctvAnchorBolt');
  }

  // 4 Triangular gusset stiffener ribs
  for (let a = 0; a < 4; a++) {
    const ang = (a * Math.PI) / 2;
    const gx = Math.cos(ang) * 0.11;
    const gz = Math.sin(ang) * 0.11;
    const rib = depPart(g, 'box', [gx, 0.22, gz], [0.02, 0.20, 0.14], 'cctvMastGalv');
    rib.rotation.y = ang;
  }

  // 2. Galvanized Tubular Steel Mast
  depPart(g, 'cylinder', [0, 1.01, 0], [0.14, 1.78, 0.14], 'cctvMastGalv'); // Lower mast
  depPart(g, 'cylinder', [0, 1.90, 0], [0.165, 0.08, 0.165], 'cctvHousingCharcoal'); // Transition collar
  depPart(g, 'cylinder', [0, 1.90, 0], [0.175, 0.02, 0.175], 'cctvAnchorBolt');
  depPart(g, 'cylinder', [0, 2.645, 0], [0.105, 1.41, 0.105], 'cctvMastGalv'); // Upper mast
  depPart(g, 'cylinder', [0, 3.36, 0], [0.13, 0.03, 0.13], 'cctvHousingCharcoal'); // Mast top cap

  // Lightning Surge Arrestor spike atop the mast
  depPart(g, 'cylinder', [0, 3.55, 0], [0.015, 0.38, 0.015], 'cctvCopperGround');
  const spikeTip = new THREE.Mesh(new THREE.ConeGeometry(0.015, 0.08, 16), depMaterials.cctvCopperGround);
  spikeTip.position.set(0, 3.78, 0);
  g.add(spikeTip);

  // 3. Weatherproof IP67 Power & PoE+ Junction Box
  const jbX = 0, jbY = 1.25, jbZ = 0.17;
  depPart(g, 'box', [0, jbY + 0.12, 0.07], [0.22, 0.03, 0.04], 'cctvHousingCharcoal');
  depPart(g, 'box', [0, jbY - 0.12, 0.07], [0.22, 0.03, 0.04], 'cctvHousingCharcoal');
  depPart(g, 'box', [jbX, jbY, jbZ], [0.26, 0.36, 0.16], 'cctvEnclosureWhite');
  depPart(g, 'box', [jbX, jbY, jbZ + 0.082], [0.25, 0.34, 0.012], 'whiteBody');
  depPart(g, 'box', [jbX - 0.125, jbY + 0.10, jbZ + 0.075], [0.015, 0.04, 0.02], 'cctvHousingCharcoal');
  depPart(g, 'box', [jbX - 0.125, jbY - 0.10, jbZ + 0.075], [0.015, 0.04, 0.02], 'cctvHousingCharcoal');
  depPart(g, 'box', [jbX + 0.122, jbY, jbZ + 0.075], [0.015, 0.05, 0.02], 'cctvAnchorBolt');

  const hazardMesh = new THREE.Mesh(new THREE.ConeGeometry(0.045, 0.08, 3), depMaterials.cctvHazardYellow);
  hazardMesh.position.set(jbX, jbY + 0.04, jbZ + 0.09);
  hazardMesh.rotation.z = Math.PI;
  g.add(hazardMesh);

  depPart(g, 'sphereSmooth', [jbX + 0.07, jbY - 0.08, jbZ + 0.09], [0.010, 0.010, 0.010], 'cctvLedGreen');
  depPart(g, 'cylinder', [jbX - 0.05, jbY - 0.195, jbZ], [0.022, 0.035, 0.022], 'cctvAnchorBolt');
  depPart(g, 'cylinder', [jbX + 0.05, jbY - 0.195, jbZ], [0.022, 0.035, 0.022], 'cctvAnchorBolt');

  // Flexible metallic conduit hose running up the pole
  const condX = 0.075, condZ = 0.06;
  depPart(g, 'cylinder', [condX, 2.25, condZ], [0.022, 1.80, 0.022], 'cctvConduitFlex');
  for (let cy = 1.6; cy <= 3.0; cy += 0.45) {
    depPart(g, 'box', [condX * 0.7, cy, condZ * 0.7], [0.05, 0.02, 0.03], 'cctvHousingCharcoal');
  }

  // 4. Heavy-Duty Cantilever Gooseneck Pendant Arm
  const armBaseY = 3.12;
  depPart(g, 'cylinder', [0, armBaseY, 0], [0.14, 0.16, 0.14], 'cctvHousingCharcoal');
  depPart(g, 'cylinder', [-0.07, armBaseY, 0], [0.02, 0.04, 0.02], 'cctvAnchorBolt');
  depPart(g, 'cylinder', [0.07, armBaseY, 0], [0.02, 0.04, 0.02], 'cctvAnchorBolt');

  const armLength = 0.52, armZCenter = 0.28;
  const armPipe = depPart(g, 'cylinder', [0, armBaseY + 0.05, armZCenter], [0.048, armLength, 0.048], 'cctvEnclosureWhite');
  armPipe.rotation.x = Math.PI / 2;

  const strut = depPart(g, 'cylinder', [0, armBaseY - 0.10, 0.18], [0.022, 0.32, 0.022], 'cctvHousingCharcoal');
  strut.rotation.x = -Math.PI / 4;

  const camZ = 0.56, elbowY = armBaseY + 0.05;
  depPart(g, 'sphereSmooth', [0, elbowY, camZ - 0.02], [0.06, 0.06, 0.06], 'cctvEnclosureWhite');
  depPart(g, 'cylinder', [0, elbowY - 0.09, camZ], [0.046, 0.12, 0.046], 'cctvEnclosureWhite');

  const pendantY = elbowY - 0.16;
  depPart(g, 'cylinder', [0, pendantY, camZ], [0.11, 0.04, 0.11], 'cctvHousingCharcoal');
  depPart(g, 'cylinder', [0, pendantY - 0.025, camZ], [0.125, 0.015, 0.125], 'cctvAnchorBolt');

  // 5. PTZ Speed Dome Camera Body & Sunshield Visor
  const camOriginY = pendantY - 0.04;
  depPart(g, 'cylinder', [0, camOriginY - 0.04, camZ], [0.14, 0.06, 0.14], 'cctvEnclosureWhite');

  const midHousing = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.21, 0.14, 32), depMaterials.cctvEnclosureWhite);
  midHousing.position.set(0, camOriginY - 0.12, camZ);
  g.add(midHousing);

  depPart(g, 'cylinder', [0, camOriginY - 0.19, camZ], [0.215, 0.035, 0.215], 'cctvHousingCharcoal');
  for (let v = 0; v < 8; v++) {
    const vang = (v * Math.PI) / 4;
    const vx = Math.cos(vang) * 0.218;
    const vz = camZ + Math.sin(vang) * 0.218;
    const vslot = depPart(g, 'box', [vx, camOriginY - 0.19, vz], [0.008, 0.022, 0.035], 'dark');
    vslot.rotation.y = -vang;
  }

  depPart(g, 'cylinder', [0, camOriginY - 0.23, camZ], [0.235, 0.06, 0.235], 'cctvEnclosureWhite');
  depPart(g, 'cylinder', [0, camOriginY - 0.255, camZ], [0.237, 0.015, 0.237], 'blue');

  const visorLip = depPart(g, 'box', [0, camOriginY - 0.24, camZ + 0.15], [0.28, 0.04, 0.12], 'cctvEnclosureWhite');
  visorLip.rotation.x = 0.18;

  depPart(g, 'sphereSmooth', [-0.07, camOriginY - 0.21, camZ + 0.20], [0.009, 0.009, 0.009], 'cctvLedGreen');
  depPart(g, 'sphereSmooth', [0.07, camOriginY - 0.21, camZ + 0.20], [0.009, 0.009, 0.009], 'cctvLedRed');

  depPart(g, 'cylinder', [0, camOriginY - 0.275, camZ], [0.228, 0.025, 0.228], 'cctvHousingCharcoal');
  for (let s = 0; s < 6; s++) {
    const sang = (s * Math.PI) / 3;
    const sx = Math.cos(sang) * 0.225;
    const sz = camZ + Math.sin(sang) * 0.225;
    depPart(g, 'cylinder', [sx, camOriginY - 0.275, sz], [0.008, 0.028, 0.008], 'cctvAnchorBolt');
  }

  // 6. Motorized Gimbal Turret & Optical Zoom Lens Assembly
  const gimbalY = camOriginY - 0.29;
  const panTurntable = new THREE.Group();
  panTurntable.position.set(0, gimbalY, camZ);
  g.add(panTurntable);

  const tplate = new THREE.Mesh(geos.cylinder, depMaterials.cctvHousingCharcoal);
  tplate.scale.set(0.18, 0.018, 0.18);
  panTurntable.add(tplate);

  const forkL = new THREE.Mesh(geos.box, depMaterials.cctvHousingCharcoal);
  forkL.position.set(-0.10, -0.07, 0);
  forkL.scale.set(0.025, 0.14, 0.09);
  panTurntable.add(forkL);

  const forkR = new THREE.Mesh(geos.box, depMaterials.cctvHousingCharcoal);
  forkR.position.set(0.10, -0.07, 0);
  forkR.scale.set(0.025, 0.14, 0.09);
  panTurntable.add(forkR);

  const bcapL = new THREE.Mesh(geos.cylinder, depMaterials.cctvAnchorBolt);
  bcapL.rotation.z = Math.PI / 2;
  bcapL.position.set(-0.115, -0.07, 0);
  bcapL.scale.set(0.022, 0.015, 0.022);
  panTurntable.add(bcapL);

  const bcapR = new THREE.Mesh(geos.cylinder, depMaterials.cctvAnchorBolt);
  bcapR.rotation.z = Math.PI / 2;
  bcapR.position.set(0.115, -0.07, 0);
  bcapR.scale.set(0.022, 0.015, 0.022);
  panTurntable.add(bcapR);

  // Central Camera Optical Core (surveillance pitch downward ~22°)
  const tiltCradle = new THREE.Group();
  tiltCradle.position.set(0, -0.07, 0);
  tiltCradle.rotation.x = 0.38;
  panTurntable.add(tiltCradle);

  const tcore = new THREE.Mesh(geos.sphereSmooth, depMaterials.cctvLensGlass);
  tcore.scale.set(0.085, 0.085, 0.085);
  tiltCradle.add(tcore);

  // Stepped Main Zoom Lens Barrel projecting forward
  const barrel1 = new THREE.Mesh(geos.cylinder, depMaterials.cctvLensGlass);
  barrel1.rotation.x = Math.PI / 2;
  barrel1.position.set(0, 0, 0.05);
  barrel1.scale.set(0.052, 0.08, 0.052);
  tiltCradle.add(barrel1);

  const barrelRing = new THREE.Mesh(geos.cylinder, depMaterials.cctvHousingCharcoal);
  barrelRing.rotation.x = Math.PI / 2;
  barrelRing.position.set(0, 0, 0.08);
  barrelRing.scale.set(0.056, 0.025, 0.056);
  tiltCradle.add(barrelRing);

  const lensBezel = new THREE.Mesh(geos.cylinder, depMaterials.vipChrome);
  lensBezel.rotation.x = Math.PI / 2;
  lensBezel.position.set(0, 0, 0.10);
  lensBezel.scale.set(0.054, 0.012, 0.054);
  tiltCradle.add(lensBezel);

  const frontGlass = new THREE.Mesh(geos.cylinder, depMaterials.cctvLensAR);
  frontGlass.rotation.x = Math.PI / 2;
  frontGlass.position.set(0, 0, 0.106);
  frontGlass.scale.set(0.046, 0.005, 0.046);
  tiltCradle.add(frontGlass);

  const pupil = new THREE.Mesh(geos.cylinder, depMaterials.cctvLensAperture);
  pupil.rotation.x = Math.PI / 2;
  pupil.position.set(0, 0, 0.108);
  pupil.scale.set(0.024, 0.003, 0.024);
  tiltCradle.add(pupil);

  // Dual High-Power Infrared (IR) Matrix Arrays flanking the lens
  for (const irSide of [-1, 1]) {
    const irPanel = new THREE.Mesh(geos.box, depMaterials.cctvHousingCharcoal);
    irPanel.position.set(irSide * 0.058, 0, 0.07);
    irPanel.scale.set(0.035, 0.065, 0.015);
    tiltCradle.add(irPanel);

    for (let iy = -0.022; iy <= 0.022; iy += 0.018) {
      for (let ix = -0.010; ix <= 0.010; ix += 0.014) {
        const irLed = new THREE.Mesh(geos.sphereSmooth, depMaterials.cctvIRLed);
        irLed.position.set(irSide * 0.058 + ix, iy, 0.078);
        irLed.scale.set(0.004, 0.004, 0.004);
        tiltCradle.add(irLed);
      }
    }
  }

  // Active REC / Tally LED on the turret face
  const turretRec = new THREE.Mesh(geos.sphereSmooth, depMaterials.cctvLedRed);
  turretRec.position.set(0, 0.040, 0.095);
  turretRec.scale.set(0.006, 0.006, 0.006);
  tiltCradle.add(turretRec);

  // Ambient daylight photocell sensor eye
  const photocell = new THREE.Mesh(geos.cylinder, depMaterials.cctvAnchorBolt);
  photocell.rotation.x = Math.PI / 2;
  photocell.position.set(0, -0.040, 0.095);
  photocell.scale.set(0.006, 0.008, 0.006);
  tiltCradle.add(photocell);

  // Store turntable reference for dynamic idle pan sweep & REC blink
  g.userData.cctvTurret = panTurntable;
  g.userData.cctvTilt = tiltCradle;
  g.userData.cctvRecLed = turretRec;

  // 7. Smoked Optical Dome Acrylic Bubble
  const domeRadius = 0.215;
  const domeGeo = new THREE.SphereGeometry(domeRadius, 32, 24, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2);
  const domeMesh = new THREE.Mesh(domeGeo, depMaterials.cctvDomeSmoked);
  domeMesh.position.set(0, camOriginY - 0.28, camZ);
  g.add(domeMesh);
}

function depCreateEquipmentMesh(kind, extra) {







  const g = new THREE.Group();







  if(kind==='qrt'){depBuildQRT(g);} else if(kind==='xray'){depBuildXray(g);} else if(kind==='armed_officer'){depBuildArmedOfficer(g);} else if (kind === 'officer' || kind === 'hhmd' || kind === 'binocular' || kind === 'radio') {







    depBuildOfficer(g, kind);







  } else if (kind === 'helipad') {
    depBuildHelipad(g);
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
    const span = (extra && typeof extra.span === 'number') ? extra.span : (typeof extra === 'number' ? extra : 2.0);
    depBuildQBelt(g, span);
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
    depBuildCCTV(g);
  } else if (kind === 'light') {
    depBuildLight(g);
  } else {







    depPart(g, 'box', [0, 0.5, 0], [1, 1, 1], 'dark');







  }







  return g;







}







window.depCreateEquipmentMesh = depCreateEquipmentMesh;















  for(const item of depItems){

    const g = depCreateEquipmentMesh(item.kind, item);

    g.position.set(item.x, item.y, item.z);

    g.rotation.y = -item.angle * Math.PI / 180;

    g.userData.depId = item.id;

    g.traverse(child => {

      child.userData.depId = item.id;

    });



    // Invisible hitBox so clicking anywhere on or around helicopter registers immediately

    if (item.kind === 'cctv') {
      const hitBox = new THREE.Mesh(new THREE.BoxGeometry(1.2, 3.8, 1.2), new THREE.MeshBasicMaterial({visible: false}));
      hitBox.position.set(0, 1.9, 0.25);
      hitBox.userData.depId = item.id;
      hitBox.userData.isHitBox = true;
      g.add(hitBox);
    }
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







    const isOfficerLike = ['officer','armed_officer','hhmd','binocular','radio'].includes(peekItem.kind);







    const canFirstPerson = isOfficerLike || peekItem.kind === 'qrt' || peekItem.kind === 'ambulance' || peekItem.kind === 'firebrigade';







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







    const isOfficerLike = ['officer','armed_officer','hhmd','binocular','radio'].includes(item.kind);







    const headHeight = isOfficerLike ? 2.15 : (item.kind==='cctv'?3.85:(item.kind==='firebrigade'?3.4:(item.kind==='ambulance'?2.7:(item.kind==='dfmd'?2.3:1.6))));







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
  if (typeof updateGtaMinimap === 'function') updateGtaMinimap(0.016);







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







  if (typeof updateQBeltUI === 'function') updateQBeltUI(o);
  depUI('editkind').value=o.kind;







  for(const k of ['name','duty','belt','mobile','x','y','z','angle'])depUI(k).value=typeof o[k]==='number'?Math.round(o[k]*100)/100:o[k];







  const isOfficerLike = ['officer','armed_officer','hhmd','binocular','radio'].includes(o.kind);







  const canFirstPerson = isOfficerLike || o.kind === 'qrt' || o.kind === 'ambulance' || o.kind === 'firebrigade';







  for(const k of ['belt','mobile']) depUI(k).disabled=!isOfficerLike;







  depUI('first').disabled = !canFirstPerson;







  depUI('third').disabled = false;















  updateOfficerHud(o);







  const isVehicle = o.kind === 'ambulance' || o.kind === 'firebrigade';







  if (o.kind === 'cctv') {
    depUI('status').textContent = '📹 ' + o.name + ' Active · 360° Motorized Pan-Tilt-Zoom · 4K UHD Live Feed | Move/Rotate: W/S/A/D, Q/E';
  } else if (o.kind === 'helicopter') {



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







  const name = kind === 'qrt' ? `QRT Open Gypsy ${count}`
    : kind === 'xray' ? `X-Ray Scanner ${count}`
    : kind === 'armed_officer' ? `T.A.O ${count}`
    : kind === 'officer' ? `Officer ${count}`







    : kind === 'hhmd' ? `HHMD Officer ${count}`







    : kind === 'binocular' ? `Spotter Officer ${count}`







    : kind === 'radio' ? `Radio Officer ${count}`







    : kind === 'helipad' ? `Helipad H-${count}`
    : kind === 'ambulance' ? `Ambulance ${count}`







    : kind === 'firebrigade' ? `Fire Tender ${count}`



    : kind === 'helicopter' ? `VIP Helicopter ${count}`







    : kind === 'qbelt' ? `Q-Belt Barrier ${count}`







    : kind === 'helicopter' ? `VIP Helicopter ${count}`
      : kind === 'parking' ? `Vehicle Parking #${count}`
      : kind === 'square_box' ? `Item Box ${count}`







    : kind === 'cctv' ? `PTZ CCTV Camera ${count}`
      : `${kind.toUpperCase()} #${count}`;







  const duty = kind === 'officer' ? 'Security post'







    : kind === 'hhmd' ? 'Main gate — DFMD / HHMD'







    : kind === 'binocular' ? 'Binocular duty — rooftop'







    : kind === 'radio' ? 'Control & wireless duty'







    : kind === 'helipad' ? 'Helipad security & landing cordon'
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







  const isOfficerLike = o.kind === 'officer' || o.kind === '_dummy' || (o.kind && o.kind.startsWith('officer_')) || ['hhmd','binocular','radio'].includes(o.kind);
  const itemHeight = isOfficerLike ? 1.65
    : o.kind === 'firebrigade' ? 2.5
    : o.kind === 'ambulance' ? 1.85
    : o.kind === 'dfmd' ? 1.8
    : o.kind === 'cctv' || o.kind === 'light' ? 2.2
    : o.kind === 'barricade' ? 0.9
    : o.kind === 'square_box' ? 0.8
    : o.kind === 'qbelt' ? 0.8
    : o.kind === 'parking' ? 1.0
    : o.kind === 'helipad' ? 0.5
    : 0.6;
  const distBehind = o.kind === 'helipad' ? 36.0
    : o.kind === 'parking' ? 24.0
    : o.kind === 'firebrigade' ? 9.2
    : o.kind === 'ambulance' ? 6.8
    : isOfficerLike ? 3.8
    : ['barricade','dfmd'].includes(o.kind) ? 4.5
    : 3.2;
  const heightAbove = o.kind === 'helipad' ? 24.0
    : o.kind === 'parking' ? 16.0
    : o.kind === 'firebrigade' ? 3.4
    : o.kind === 'ambulance' ? 2.4
    : isOfficerLike ? 1.2
    : 1.5;















  const angle=o.angle*Math.PI/180,dir=new THREE.Vector3(Math.sin(angle),0,-Math.cos(angle));







  let eyeY = o.y + itemHeight;







  if(mode === 'first'){
    if(o.kind === 'ambulance') eyeY = o.y + 1.62;
    if(o.kind === 'firebrigade') eyeY = o.y + 2.15;
    if(o.kind === 'helipad') eyeY = o.y + 4.0;
    if(o.kind === 'parking') eyeY = o.y + 2.5;







  }







  const eye = new THREE.Vector3(o.x, eyeY, o.z);







  if(mode === 'first'){







    if(o.kind === 'ambulance') eye.addScaledVector(dir, 1.2);







    if(o.kind === 'firebrigade') eye.addScaledVector(dir, 2.1);







  }







  const idealCam = mode==='first' ? eye : eye.clone().addScaledVector(dir,-distBehind).add(new THREE.Vector3(0,heightAbove,0));







  const lookDistance = o.kind === 'helipad' ? 12.0 : (o.kind === 'parking' ? 10.0 : (o.kind==='firebrigade' ? 4.8 : (o.kind==='ambulance' ? 3.8 : (mode==='first' ? 10 : 2.0))));







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
  if (typeof updateQBeltUI === 'function') updateQBeltUI(null);







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
window.__camera = camera;
window.__controls = controls;
window.__depView = depView;
try { Object.defineProperty(window, "__depItems", { get: () => depItems, configurable: true }); } catch(e){ window.__depItems = depItems; }
try { Object.defineProperty(window, "__depSelected", { get: () => depSelected, configurable: true }); } catch(e){}
window.__depChoose = depChoose;







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







    const name = kind === 'qrt' ? `QRT Open Gypsy ${count}`
    : kind === 'xray' ? `X-Ray Scanner ${count}`
    : kind === 'armed_officer' ? `T.A.O ${count}`
    : kind === 'officer' ? `Officer ${count}`







      : kind === 'hhmd' ? `HHMD Officer ${count}`







      : kind === 'binocular' ? `Spotter Officer ${count}`







      : kind === 'radio' ? `Radio Officer ${count}`







      : kind === 'helipad' ? `Helipad H-${count}`
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







      : kind === 'helipad' ? 'Helipad security & landing cordon'
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
  // If character is below roof level (< 7m), cast from safe clearance below ceiling (6.2m)
  // so we stay underneath ceilings/roofs inside buildings like the auditorium while clearly detecting all raised stages, porches and landings!
  const startY = currentY < 7.0 ? 6.2 : (currentY + 3.0);
  const rayOrigin = new THREE.Vector3(x, startY, z);
  const ray = new THREE.Raycaster(rayOrigin, new THREE.Vector3(0, -1, 0), 0.05, 50);
  const targets = (typeof clickable !== 'undefined' ? clickable : []).filter(m => m.visible && m.parent.visible && m !== depGroup);
  const hits = ray.intersectObjects(targets, false);
  for (const h of hits) {
    if (h.face && h.face.normal && h.face.normal.y > 0.25) {
      if (currentY < 7.0 && h.point.y > 6.8) continue; // Skip roof/ceiling surfaces when walking on ground/floor
      // Ignore hanging lamps, speakers, buntings, lintels, or high ceiling fixtures below 6.8m
      const hitObj = h.object;
      const hitItem = hitObj?.userData?.items && hitObj.userData.items[h.instanceId];
      const hitName = (hitItem?.name || hitObj?.name || '').toLowerCase();
      if (
        hitName.includes('speaker') ||
        hitName.includes('light') ||
        hitName.includes('bunting') ||
        hitName.includes('garland') ||
        hitName.includes('lintel') ||
        hitName.includes('truss') ||
        hitName.includes('beam') ||
        hitName.includes('canopy') ||
        hitName.includes('arch') ||
        hitName.includes('tree') ||
        hitName.includes('foliage') ||
        hitName.includes('signboard') ||
        hitName.includes('board') ||
        (currentY < 2.5 && h.point.y > 2.3)
      ) {
        continue;
      }
      let foundY = h.point.y;
      // Hall / Auditorium floor floor-level guarantee:
      // Inside the hall building footprint (X: -57.3 to -19.8, Z: -56.1 to 13.5), floor is at least 1.00m
      if (x >= -57.3 && x <= -19.8 && z >= -56.1 && z <= 13.5) {
        foundY = Math.max(foundY, 1.00);
      }
      // Auditorium side entrance porch landing (X: -19.9 to -17.6, Z: -6.5 to 1.5): floor is at least 1.06m
      if (x >= -19.9 && x <= -17.6 && z >= -6.5 && z <= 1.5) {
        foundY = Math.max(foundY, 1.06);
      }
      // Raised stage platform guarantee (X: -53.8 to -23.2, Z: 1.8 to 10.5):
      if (x >= -53.8 && x <= -23.2 && z >= 1.8 && z <= 10.5) {
        foundY = Math.max(foundY, 2.10);
      }
      // Left stage stairs transition corridor (X: -55.5 to -49.5, Z: 0.5 to 4.5):
      if (x >= -55.5 && x <= -49.5 && z >= 0.5 && z <= 4.5) {
        const stairFloor = z >= 2.0 ? 2.10 : (z >= 1.5 ? 1.85 : 1.35);
        foundY = Math.max(foundY, stairFloor);
      }
      // Right stage stairs transition corridor (X: -27.0 to -21.5, Z: 0.5 to 4.5):
      if (x >= -27.0 && x <= -21.5 && z >= 0.5 && z <= 4.5) {
        const stairFloor = z >= 2.0 ? 2.10 : (z >= 1.5 ? 1.85 : 1.35);
        foundY = Math.max(foundY, stairFloor);
      }
      return foundY;
    }
  }
  // Architectural fallbacks if ray misses geometry:
  if (x >= -53.8 && x <= -23.2 && z >= 1.8 && z <= 10.5) {
    return 2.10; // Raised stage floor
  }
  if (x >= -55.5 && x <= -49.5 && z >= 0.5 && z <= 4.5) {
    return z >= 2.0 ? 2.10 : (z >= 1.5 ? 1.85 : 1.35); // Left stage stairs
  }
  if (x >= -27.0 && x <= -21.5 && z >= 0.5 && z <= 4.5) {
    return z >= 2.0 ? 2.10 : (z >= 1.5 ? 1.85 : 1.35); // Right stage stairs
  }
  if (x >= -57.3 && x <= -19.8 && z >= -56.1 && z <= 13.5) {
    return 1.00; // Auditorium floor
  }
  if (x >= -19.9 && x <= -17.6 && z >= -6.5 && z <= 1.5) {
    return 1.06; // Entrance porch landing
  }
  return 0.36; // Default ground plane level
}















const depKeysDown = {};
window.__depKeysDown = depKeysDown;
window.__getSurfaceHeight = getSurfaceHeight;







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
















// =========================================================================
// GTA-Style Tactical Radar Navigation Minimap HUD
// =========================================================================
let gtaRadarZoom = 2.4; // Pixels per meter (~35-40m visible radius around player)
let gtaSweepAngle = 0;

function updateGtaMinimap(dt = 0.016) {
  const container = root.querySelector('#dep-gta-minimap-container');
  if (!container) return;

  const targetId = (typeof depSelected !== 'undefined') ? depSelected : null;
  if (!targetId) {
    if (container.style.display !== 'none') container.style.display = 'none';
    return;
  }
  const o = depItems.find(x => x.id === targetId);
  if (!o) {
    if (container.style.display !== 'none') container.style.display = 'none';
    return;
  }

  // Reveal minimap HUD
  if (container.style.display === 'none') {
    container.style.display = 'block';
  }

  const canvas = root.querySelector('#dep-gta-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  const w = canvas.width;  // 352
  const h = canvas.height; // 352
  const cx = w / 2;
  const cy = h / 2;
  const R = cx - 4; // Outer radar radius in canvas px (~172px)

  // Radar heading & sweep
  gtaSweepAngle = (gtaSweepAngle + (dt || 0.016) * 2.0) % (Math.PI * 2);
  const playerHeadingRad = ((o.angle || 0) * Math.PI) / 180;

  // 1. Clear & clip circular radar area
  ctx.save();
  ctx.clearRect(0, 0, w, h);
  ctx.beginPath();
  ctx.arc(cx, cy, R, 0, Math.PI * 2);
  ctx.clip();

  // 2. Tactical Radar Background (Dark gradient)
  const grad = ctx.createRadialGradient(cx, cy, 4, cx, cy, R);
  grad.addColorStop(0, 'rgba(15, 23, 42, 0.94)');
  grad.addColorStop(0.75, 'rgba(12, 19, 36, 0.97)');
  grad.addColorStop(1, 'rgba(8, 12, 22, 1.0)');
  ctx.fillStyle = grad;
  ctx.fill();

  // 3. Rotating Radar Sweep Beam (GTA / Military radar effect)
  ctx.save();
  ctx.translate(cx, cy);
  ctx.rotate(gtaSweepAngle);
  const sweepGrad = ctx.createRadialGradient(0, 0, 0, 0, 0, R);
  sweepGrad.addColorStop(0, 'rgba(56, 189, 248, 0.40)');
  sweepGrad.addColorStop(1, 'rgba(56, 189, 248, 0.0)');
  ctx.fillStyle = sweepGrad;
  ctx.beginPath();
  ctx.moveTo(0, 0);
  ctx.arc(0, 0, R, -0.42, 0);
  ctx.closePath();
  ctx.fill();
  ctx.restore();

  // 4. Concentric Range Rings (15m, 30m, 50m)
  const ringDistances = [15, 30, 50];
  ctx.strokeStyle = 'rgba(56, 189, 248, 0.20)';
  ctx.lineWidth = 1.2;
  for (const d of ringDistances) {
    const rPx = d * gtaRadarZoom;
    if (rPx < R) {
      ctx.beginPath();
      ctx.arc(cx, cy, rPx, 0, Math.PI * 2);
      ctx.stroke();
    }
  }

  // Crosshairs
  ctx.strokeStyle = 'rgba(56, 189, 248, 0.12)';
  ctx.beginPath();
  ctx.moveTo(cx - R, cy); ctx.lineTo(cx + R, cy);
  ctx.moveTo(cx, cy - R); ctx.lineTo(cx, cy + R);
  ctx.stroke();

  // 5. Transform into Player Local Coordinates (Heading-Up Mode)
  // Forward faces UP on the radar screen!
  ctx.save();
  ctx.translate(cx, cy);
  ctx.rotate(playerHeadingRad);
  ctx.scale(gtaRadarZoom, gtaRadarZoom);
  ctx.translate(-o.x, -o.z);

  // 5.1 Draw Roads (from geo.roads)
  if (typeof geo !== 'undefined' && geo && geo.roads) {
    for (const r of geo.roads) {
      if (!r.points || r.points.length < 2) continue;
      ctx.beginPath();
      ctx.moveTo(r.points[0][0], r.points[0][1]);
      for (let i = 1; i < r.points.length; i++) {
        ctx.lineTo(r.points[i][0], r.points[i][1]);
      }
      ctx.strokeStyle = '#334155';
      ctx.lineWidth = r.width || 6;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      ctx.stroke();

      // Centerline
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.35)';
      ctx.lineWidth = 0.5;
      ctx.stroke();
    }
  }

  // 5.2 Draw Helipad Access Road (to Main Gate)
  if (typeof geo !== 'undefined' && geo && geo.helipadProposal && geo.helipadProposal.gate) {
    const hGate = geo.helipadProposal.gate;
    ctx.beginPath();
    ctx.moveTo(6.39, -308.2);
    ctx.lineTo(hGate[0], hGate[1]);
    ctx.strokeStyle = '#334155';
    ctx.lineWidth = 5.5;
    ctx.stroke();
  }

  // 5.3 Draw Building Footprints (from geo.footprints)
  if (typeof geo !== 'undefined' && geo && geo.footprints) {
    for (const fp of geo.footprints) {
      if (!fp.points || fp.points.length < 3) continue;
      ctx.beginPath();
      ctx.moveTo(fp.points[0][0], fp.points[0][1]);
      for (let i = 1; i < fp.points.length; i++) {
        ctx.lineTo(fp.points[i][0], fp.points[i][1]);
      }
      ctx.closePath();
      if (fp.id === 'hall') {
        ctx.fillStyle = 'rgba(30, 58, 138, 0.55)'; // Auditorium
        ctx.strokeStyle = 'rgba(96, 165, 250, 0.85)';
      } else if (fp.id === 'pavilion') {
        ctx.fillStyle = 'rgba(180, 83, 9, 0.50)'; // Lotus
        ctx.strokeStyle = 'rgba(251, 191, 36, 0.85)';
      } else if (fp.id === 'garden') {
        ctx.fillStyle = 'rgba(22, 101, 52, 0.35)'; // Garden
        ctx.strokeStyle = 'rgba(74, 222, 128, 0.65)';
      } else {
        ctx.fillStyle = 'rgba(51, 65, 85, 0.45)';
        ctx.strokeStyle = 'rgba(148, 163, 184, 0.65)';
      }
      ctx.lineWidth = 0.9;
      ctx.fill();
      ctx.stroke();
    }
  }

  // 5.4 Draw Helipads on Radar
  // Campus Helipad:
  ctx.beginPath();
  ctx.arc(6.39, -308.2, 16.5, 0, Math.PI * 2);
  ctx.fillStyle = 'rgba(51, 65, 85, 0.65)';
  ctx.fill();
  ctx.strokeStyle = 'rgba(250, 204, 21, 0.85)';
  ctx.lineWidth = 1.2;
  ctx.stroke();
  ctx.fillStyle = '#ffffff';
  ctx.font = 'bold 9px sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText('H', 6.39, -308.2);

  // Deployed Helipads:
  for (const it of depItems) {
    if (it.kind === 'helipad' && it.id !== o.id) {
      ctx.beginPath();
      ctx.arc(it.x, it.z, 16.5, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(51, 65, 85, 0.65)';
      ctx.fill();
      ctx.strokeStyle = 'rgba(56, 189, 248, 0.85)';
      ctx.lineWidth = 1.2;
      ctx.stroke();
      ctx.fillStyle = '#38bdf8';
      ctx.font = 'bold 9px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('H', it.x, it.z);
    }
  }

  ctx.restore(); // Restore back to radar center (cx, cy)

  // 6. Draw Radar Blips for Other Deployed Posts (with GTA Edge Clamping!)
  for (const it of depItems) {
    if (it.id === o.id) continue;

    const dx = it.x - o.x;
    const dz = it.z - o.z;
    const dist = Math.hypot(dx, dz);

    const worldAngle = Math.atan2(dx, -dz);
    const radarAngle = worldAngle - playerHeadingRad;
    const rDistPx = dist * gtaRadarZoom;

    let bx, by;
    const isClamped = (rDistPx > (R - 8));
    if (isClamped) {
      bx = cx + (R - 8) * Math.sin(radarAngle);
      by = cy - (R - 8) * Math.cos(radarAngle);
    } else {
      bx = cx + rDistPx * Math.sin(radarAngle);
      by = cy - rDistPx * Math.cos(radarAngle);
    }

    let blipColor = '#38bdf8';
    let blipSize = 3.8;
    if (it.kind === 'officer' || it.kind === 'hhmd' || it.kind === 'binocular' || it.kind === 'radio') {
      blipColor = '#0284c7';
      blipSize = 4.2;
    } else if (it.kind === 'ambulance') {
      blipColor = '#ef4444';
      blipSize = 4.8;
    } else if (it.kind === 'firebrigade') {
      blipColor = '#f97316';
      blipSize = 4.8;
    } else if (it.kind === 'helipad' || it.kind === 'helicopter') {
      blipColor = '#22c55e';
      blipSize = 5.2;
    } else if (it.kind === 'parking') {
      blipColor = '#a855f7';
      blipSize = 4.6;
    } else {
      blipColor = '#facc15';
      blipSize = 3.5;
    }

    ctx.save();
    ctx.beginPath();
    ctx.arc(bx, by, blipSize, 0, Math.PI * 2);
    ctx.fillStyle = blipColor;
    ctx.shadowColor = blipColor;
    ctx.shadowBlur = isClamped ? 7 : 4;
    ctx.fill();
    ctx.restore();
  }

  // 7. Draw Controlled Player Blip (Center of Radar)
  ctx.save();
  ctx.translate(cx, cy);

  // Field of vision cone pointing straight up
  ctx.beginPath();
  ctx.moveTo(0, 0);
  ctx.lineTo(-24, -58);
  ctx.lineTo(24, -58);
  ctx.closePath();
  const fovGrad = ctx.createLinearGradient(0, 0, 0, -58);
  fovGrad.addColorStop(0, 'rgba(56, 189, 248, 0.40)');
  fovGrad.addColorStop(1, 'rgba(56, 189, 248, 0.0)');
  ctx.fillStyle = fovGrad;
  ctx.fill();

  // Directional Arrow (Facing UP)
  ctx.beginPath();
  ctx.moveTo(0, -10);
  ctx.lineTo(8, 7);
  ctx.lineTo(0, 3.5);
  ctx.lineTo(-8, 7);
  ctx.closePath();
  ctx.fillStyle = '#ffffff';
  ctx.shadowColor = '#38bdf8';
  ctx.shadowBlur = 8;
  ctx.fill();
  ctx.strokeStyle = '#0284c7';
  ctx.lineWidth = 1.5;
  ctx.stroke();

  ctx.restore();

  // 8. Outer Compass Ring & North Indicator
  ctx.restore(); // Restore unclipped context

  // Draw Outer Border Ring
  ctx.beginPath();
  ctx.arc(cx, cy, R, 0, Math.PI * 2);
  ctx.strokeStyle = 'rgba(56, 189, 248, 0.75)';
  ctx.lineWidth = 2.5;
  ctx.stroke();

  // North (N) Indicator on Rim (Points to true world North)
  const northAngle = -playerHeadingRad;
  const nx = cx + (R - 2) * Math.sin(northAngle);
  const ny = cy - (R - 2) * Math.cos(northAngle);

  ctx.save();
  ctx.translate(nx, ny);
  ctx.rotate(northAngle);

  // Red arrowhead pointing towards North
  ctx.beginPath();
  ctx.moveTo(0, -6);
  ctx.lineTo(4, 3);
  ctx.lineTo(-4, 3);
  ctx.closePath();
  ctx.fillStyle = '#ef4444';
  ctx.shadowColor = '#ef4444';
  ctx.shadowBlur = 6;
  ctx.fill();

  // Letter "N"
  ctx.fillStyle = '#ffffff';
  ctx.font = 'bold 9px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('N', 0, 11);

  ctx.restore();

  // 9. Update Location & Coordinate Badges
  const locBadge = root.querySelector('#dep-gta-loc-badge');
  if (locBadge) {
    const dutyText = (o.duty || 'CAMPUS PATROL').toUpperCase();
    locBadge.textContent = `${depSymbols[o.kind] || '📍'} ${o.name || 'POST'} · ${dutyText}`;
  }

  const coordsEl = root.querySelector('#dep-gta-coords');
  if (coordsEl) {
    coordsEl.textContent = `X: ${Math.round(o.x * 10) / 10} | Z: ${Math.round(o.z * 10) / 10}`;
  }

  const headingEl = root.querySelector('#dep-gta-heading');
  if (headingEl) {
    headingEl.textContent = `${Math.round(o.angle || 0)}°`;
  }
}
window.updateGtaMinimap = updateGtaMinimap;

function initGtaMinimapEvents() {
  const zoomIn = root.querySelector('#dep-gta-zoom-in');
  const zoomOut = root.querySelector('#dep-gta-zoom-out');
  if (zoomIn) {
    zoomIn.addEventListener('pointerdown', e => e.stopPropagation());
    zoomIn.addEventListener('click', e => {
      e.stopPropagation();
      gtaRadarZoom = Math.min(4.5, gtaRadarZoom * 1.35);
      updateGtaMinimap(0);
    });
  }
  if (zoomOut) {
    zoomOut.addEventListener('pointerdown', e => e.stopPropagation());
    zoomOut.addEventListener('click', e => {
      e.stopPropagation();
      gtaRadarZoom = Math.max(0.9, gtaRadarZoom / 1.35);
      updateGtaMinimap(0);
    });
  }
}
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initGtaMinimapEvents);
} else {
  setTimeout(initGtaMinimapEvents, 100);
}

window.__DEP_TICK = function(dt) {
  if (typeof updateGtaMinimap === 'function') { updateGtaMinimap(dt); }








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



        if (node.g.userData.cctvTurret) {
          const t = performance.now() * 0.001;
          // Smooth +/-35 degree motorized surveillance sweep
          node.g.userData.cctvTurret.rotation.y = Math.sin(t * 0.6) * 0.62;
          if (node.g.userData.cctvRecLed) {
            const pulse = (Math.sin(t * 4.0) + 1) * 0.5;
            node.g.userData.cctvRecLed.material.emissiveIntensity = 1.8 + pulse * 2.2;
          }
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
      else if (o.kind === 'helipad') turnSpeed = 55;
      else if (o.kind === 'parking') turnSpeed = 45;
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







      } else if (o.kind === 'helipad') {
        baseFwdSpeed = 7.0;
        sprintFwdSpeed = 15.0;
        baseBackSpeed = 5.0;
      } else if (o.kind === 'parking') {
        baseFwdSpeed = 6.0;
        sprintFwdSpeed = 13.0;
        baseBackSpeed = 4.5;
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







      const isFallingFree = !depOfficerJump.isJumping && o.y > groundUnder + 0.38;















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
        // Hard ground clamp: prevent any officer or item from ever sinking beneath solid ground/floor
        if (o.y < groundUnder) {
          o.y = groundUnder;
        }







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
                             hitName.includes('post') || hitName.includes('handrail') || hitName.includes('support') ||
                             hitName.includes('stage') || hitName.includes('fascia') || hitName.includes('platform') ||
                             hitName.includes('podium') || hitName.includes('deck') || hitName.includes('landing') ||
                             hitName.includes('ramp') || hitName.includes('riser') || hitName.includes('tread') ||
                             hitName.includes('skirt') || hitName.includes('pillar') || hitName.includes('flower') ||
                             hitName.includes('scallop') || hitName.includes('bell') || hitName.includes('wreath') ||
                             hitName.includes('jamb') || hitName.includes('curtain') || hitName.includes('carpet') ||
                             hitName.includes('aisle') || hitName.includes('open') || hitName.includes('foyer') ||
                             hitName.includes('chair') || hitName.includes('seat') || hitName.includes('table') ||
                             hitName.includes('sofa') || hitName.includes('bench') || hitName.includes('mat') ||
                             hitName.includes('gate') || hitName.includes('joint') || hitName.includes('beam') ||
                             hitName.includes('arch') || hitName.includes('road') || hitName.includes('curb') ||
                             hitName.includes('border') || hitName.includes('expansion') || hitName.includes('canopy');
          // If the obstacle is a low step/stage edge and surfaceNext is a walkable floor/ledge (<= 1.25m above current Y), it is passable
          const isWalkableLedge = (surfaceNext <= o.y + 1.25) && (wallHits[0].point.y <= surfaceNext + 0.15);
          if (!isPassable && !isWalkableLedge) {
            wallBlocked = true;
          }
        }

        if (wallBlocked && (!depOfficerJump.isJumping || o.y < surfaceNext - 0.2)) {
          depUI('status').textContent = '⚠️ Blocked by obstacle / wall! Press SPACE to jump over.';
        } else if (o.kind === 'helipad' || o.kind === 'parking' || heightDiff <= 1.25) {







          // Normal stair step, curb or ground ramp: climb on top smoothly!







          o.x = nextX;







          o.z = nextZ;







          if (!depOfficerJump.isJumping) {







            const stepDecay = 1 - Math.exp(-22 * dt);







            o.y = THREE.MathUtils.lerp(o.y, surfaceNext, stepDecay);
            if (o.y < surfaceNext) {
              o.y = surfaceNext;
            }
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







        const isOfficerLike = o.kind === 'officer' || o.kind === '_dummy' || (o.kind && o.kind.startsWith('officer_')) || ['hhmd','binocular','radio'].includes(o.kind);
        const itemHeight = isOfficerLike ? 1.65
          : o.kind === 'firebrigade' ? 2.5
          : o.kind === 'ambulance' ? 1.85
          : o.kind === 'dfmd' ? 1.8
          : o.kind === 'cctv' || o.kind === 'light' ? 2.2
          : o.kind === 'barricade' ? 0.9
          : o.kind === 'square_box' ? 0.8
          : o.kind === 'qbelt' ? 0.8
          : o.kind === 'parking' ? 1.0
          : o.kind === 'helipad' ? 0.5
          : 0.6;
        const distBehind = o.kind === 'helipad' ? 36.0
          : o.kind === 'parking' ? 24.0
          : o.kind === 'firebrigade' ? 9.2
          : o.kind === 'ambulance' ? 6.8
          : isOfficerLike ? 3.8
          : ['barricade','dfmd'].includes(o.kind) ? 4.5
          : 3.2;
        const heightAbove = o.kind === 'helipad' ? 24.0
          : o.kind === 'parking' ? 16.0
          : o.kind === 'firebrigade' ? 3.4
          : o.kind === 'ambulance' ? 2.4
          : isOfficerLike ? 1.2
          : 1.5;















        const eye = new THREE.Vector3(o.x, o.y + itemHeight, o.z);







        const idealCam = eye.clone().addScaledVector(dir, -distBehind).add(new THREE.Vector3(0, heightAbove, 0));







        const lookDist = o.kind === 'helipad' ? 12.0 : (o.kind === 'parking' ? 10.0 : (o.kind === 'firebrigade' ? 4.8 : (o.kind === 'ambulance' ? 3.8 : 2.0)));







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
        depPlace=false;depNew=null;depStore(true);depBuild();depChoose(o.id);







      }







    }







    depCandidate=null;depConfirm.hidden=true;







  };







  depConfirm.appendChild(b);







}















// Keyboard controls:







// =========================================================================
// Q-BELT RETRACTABLE STRETCH ENGINE ('O' to open/stretch, 'P' to reset/retract)
// =========================================================================
function stretchQBelt(item, newSpan) {
  if (!item || item.kind !== 'qbelt') return;
  const clamped = Math.max(0.8, Math.min(10.0, Math.round(newSpan * 10) / 10));
  const oldSpan = item.span || 2.0;
  item.span = clamped;

  // Dynamically update the 3D mesh safely without disposing shared geometries!
  const node = depNodes.find(n => n.item && n.item.id === item.id);
  if (node && node.g) {
    while (node.g.children.length > 0) {
      node.g.remove(node.g.children[0]);
    }
    depBuildQBelt(node.g, item.span);
    node.g.traverse(child => {
      child.userData.depId = item.id;
    });
    draw();
  } else {
    depBuild();
  }

  // Persist to localStorage / SQLite
  depStore();

  // Update UI indicators
  updateQBeltUI(item);

  // User feedback toast
  if (clamped > oldSpan) {
    if (typeof depShowToast === 'function') {
      depShowToast(`🎗️ Q-Belt Stretched (खुल गया): ${clamped.toFixed(1)} m · Press 'P' to reset back`);
    }
  } else if (clamped === 2.0) {
    if (typeof depShowToast === 'function') {
      depShowToast(`🎗️ Q-Belt Reset (वापिस वैसा हो गया): 2.0 m Standard`);
    }
  } else {
    if (typeof depShowToast === 'function') {
      depShowToast(`🎗️ Q-Belt Retracted: ${clamped.toFixed(1)} m`);
    }
  }
}
window.stretchQBelt = stretchQBelt;

function updateQBeltUI(item) {
  const floatHud = (typeof root !== 'undefined' && root) ? root.querySelector('#dep-qbelt-float-hud') : document.getElementById('dep-qbelt-float-hud');
  const floatSpan = (typeof root !== 'undefined' && root) ? root.querySelector('#qbelt-hud-span-txt') : document.getElementById('qbelt-hud-span-txt');
  const inspRow = (typeof root !== 'undefined' && root) ? root.querySelector('#dep-qbelt-inspector-row') : document.getElementById('dep-qbelt-inspector-row');
  const inspVal = (typeof root !== 'undefined' && root) ? root.querySelector('#dep-qbelt-inspector-val') : document.getElementById('dep-qbelt-inspector-val');

  if (item && item.kind === 'qbelt') {
    const s = (item.span || 2.0).toFixed(1) + ' m';
    if (floatHud) floatHud.style.display = 'flex';
    if (floatSpan) floatSpan.textContent = 'Length: ' + s;
    if (inspRow) inspRow.style.display = 'block';
    if (inspVal) inspVal.textContent = s;
  } else {
    if (floatHud) floatHud.style.display = 'none';
    if (inspRow) inspRow.style.display = 'none';
  }
}
window.updateQBeltUI = updateQBeltUI;

function initQBeltControls() {
  const floatStretch = (typeof root !== 'undefined' && root) ? root.querySelector('#qbelt-hud-stretch-btn') : document.getElementById('qbelt-hud-stretch-btn');
  const floatReset = (typeof root !== 'undefined' && root) ? root.querySelector('#qbelt-hud-reset-btn') : document.getElementById('qbelt-hud-reset-btn');
  const floatRetract = (typeof root !== 'undefined' && root) ? root.querySelector('#qbelt-hud-retract-btn') : document.getElementById('qbelt-hud-retract-btn');
  const inspStretch = (typeof root !== 'undefined' && root) ? root.querySelector('#dep-qbelt-insp-stretch') : document.getElementById('dep-qbelt-insp-stretch');
  const inspReset = (typeof root !== 'undefined' && root) ? root.querySelector('#dep-qbelt-insp-reset') : document.getElementById('dep-qbelt-insp-reset');

  const onStretch = (e) => {
    e.preventDefault();
    e.stopPropagation();
    const item = depSelected ? depItems.find(o => o.id === depSelected) : null;
    if (item && item.kind === 'qbelt') {
      const cur = item.span || 2.0;
      stretchQBelt(item, cur + 0.5);
    }
  };

  const onReset = (e) => {
    e.preventDefault();
    e.stopPropagation();
    const item = depSelected ? depItems.find(o => o.id === depSelected) : null;
    if (item && item.kind === 'qbelt') {
      const cur = item.span || 2.0;
      const next = (cur !== 2.0) ? 2.0 : 1.2;
      stretchQBelt(item, next);
    }
  };

  const onRetract = (e) => {
    e.preventDefault();
    e.stopPropagation();
    const item = depSelected ? depItems.find(o => o.id === depSelected) : null;
    if (item && item.kind === 'qbelt') {
      const cur = item.span || 2.0;
      stretchQBelt(item, cur - 0.5);
    }
  };

  if (floatStretch) floatStretch.addEventListener('click', onStretch);
  if (floatReset) floatReset.addEventListener('click', onReset);
  if (floatRetract) floatRetract.addEventListener('click', onRetract);
  if (inspStretch) inspStretch.addEventListener('click', onStretch);
  if (inspReset) inspReset.addEventListener('click', onReset);
}
setTimeout(initQBeltControls, 100);

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

  // Q-Belt stretch on 'O' (open/stretch) and reset on 'P' (vapis waisa ho jaaye)
  if (activeItem && activeItem.kind === 'qbelt') {
    if (key === 'o' || e.code === 'KeyO') {
      e.preventDefault();
      e.stopPropagation();
      const cur = activeItem.span || 2.0;
      const next = Math.min(10.0, Math.round((cur + 0.5) * 10) / 10);
      stretchQBelt(activeItem, next);
      return;
    }
    if (key === 'p' || e.code === 'KeyP') {
      e.preventDefault();
      e.stopPropagation();
      const cur = activeItem.span || 2.0;
      const next = (cur !== 2.0) ? 2.0 : 1.2;
      stretchQBelt(activeItem, next);
      return;
    }
  }















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







    if (depSelected) depStore(true);







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







depBackendURL=location.protocol.startsWith('http')?(location.origin+'/api/deployment'):'http://127.0.0.1:8794/api/deployment';















function depPayload(){







  const sanitized = JSON.parse(JSON.stringify(depItems));







  for (const item of sanitized) {







    item.x = Math.max(-4900, Math.min(4900, Math.round((Number(item.x) || 0) * 100) / 100));







    item.z = Math.max(-4900, Math.min(4900, Math.round((Number(item.z) || 0) * 100) / 100));







    item.y = Math.max(-50, Math.min(350, Math.round((Number(item.y) || 0) * 100) / 100));







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















function depQueue(immediate = true){
  if(!depBackendURL)return;
  depPending=depPayload();
  if(depUI('sync'))depUI('sync').textContent='Backend: auto-saving...';
  clearTimeout(depSaveTimer);
  if(immediate){
    depFlush();
  } else {
    depSaveTimer=setTimeout(depFlush,50);
  }







}















async function depFlush(){







  if(depSaving||!depPending||!depBackendURL)return;







  depSaving=true;







  const snapshot=depPending;







  depPending=null;







  try{







    const r=await fetch(depBackendURL,{







      method:'PUT',







      headers:{'Content-Type':'text/plain','X-GMS-Plan':'1'},







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
    try {
      localStorage.setItem(depStorage, JSON.stringify({
        version: 1,
        savedAt: new Date(result.updated || Date.now()).getTime(),
        origin: [geo.originLongitude, geo.originLatitude],
        items: depItems
      }));
    } catch(e) {}







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
    if (local && Array.isArray(local.items) && depValid(local.items) && (localTime > (backendTime + 2000) || backendItems === null)) {
      depItems = local.items;
      depBuild();
      depStore(true);
      if (depUI('sync')) depUI('sync').textContent = 'Auto-saved synced ' + depItems.length + ' items to DB (rev ' + depRevision + ')';
    } else if (backendItems !== null) {
      depItems = backendItems;
      depBuild();
      try {
        localStorage.setItem(depStorage, JSON.stringify({
          version: 1,
          savedAt: backendTime || Date.now(),
          origin: [geo.originLongitude, geo.originLatitude],
          items: depItems
        }));
      } catch (e) {}
      if (depUI('sync')) depUI('sync').textContent = 'Auto-saved loaded ' + depItems.length + ' items from DB (rev ' + depRevision + ')';
    } else if (local && Array.isArray(local.items) && depValid(local.items)) {
      depItems = local.items;
      depBuild();
      depStore(true);
    } else {
      depItems = depSeed();
      depBuild();
      depStore(true);
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







  if(depBackendURL){







    const payload=depPayload();







    const body=JSON.stringify({revision:depRevision,plan:payload});







    try{







      if(navigator.sendBeacon){







        const blob=new Blob([body],{type:'text/plain'});







        navigator.sendBeacon(depBackendURL,blob);







      }else{







        fetch(depBackendURL,{







          method:'POST',







          headers:{'Content-Type':'text/plain','X-GMS-Plan':'1'},







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







  







  vrHollowHeli(g,bodyUpper,bodyLower,stripe);
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







function prepareVvipHall(){if(vvipHallPrepared)return;const p=camera.position.clone(),t=controls.target.clone();select.value='hall';applyView();camera.position.copy(p);controls.target.copy(t);controls.enabled=false;groups.roof.visible=false;vvipHallPrepared=true;}







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







  vrInit();
  root.dataset.simulation="active";
  draw();







}















function stopVvipSimulation() {







  if (!vvipActive) return;







  vvipActive = false;
  delete root.dataset.simulation;
  if(vvipReal){for(const {shadow} of vvipReal.contacts){shadow.geometry.dispose();shadow.material.map.dispose();shadow.material.dispose();}vvipReal=null;}







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































// Simulation Tick (called from window.__DEP_TICK)
























// BEGIN REALISTIC REHEARSAL ENGINE
// Visual rehearsal engine. No aircraft performance or protective protocol certification.
var vvipReal;
function buildRoutePolice(){return new THREE.Group();} // Use the user's deployed officers, not duplicate scripted guards.
function buildRoadBarricades(){return new THREE.Group();} // Keep the actual editable barricade layer.
function vrClamp(t){return Math.max(0,Math.min(1,t));}
function vrEase(t){t=vrClamp(t);return t*t*(3-2*t);}
function vrMix(a,b,t){return a.map((v,i)=>v+(b[i]-v)*t);}
function vrBox(parent,mat,p,s){const m=new THREE.Mesh(geos.box,mat);m.position.fromArray(p);m.scale.fromArray(s);parent.add(m);return m;}
function vrSphere(parent,mat,p,s){const m=new THREE.Mesh(geos.sphereSmooth,mat);m.position.fromArray(p);m.scale.fromArray(s);parent.add(m);return m;}
function vrLimb(parent,mat,a,b,r){const m=new THREE.Mesh(geos.cylinder,mat);parent.add(m);m.userData.between=(a,b)=>{const v=new THREE.Vector3().subVectors(b,a);m.position.copy(a).add(b).multiplyScalar(.5);m.scale.set(r,v.length(),r);m.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),v.normalize());};return m;}
function vrActor(female=false){
 const g=new THREE.Group(),upper=new THREE.Group();g.add(upper);
 const cloth=female?depMaterials.vipSaree:depMaterials.dark,skin=depMaterials.skin;
 vrBox(upper,cloth,[0,.27,0],[female?.34:.43,.49,.23]);
 const head=vrSphere(upper,skin,[0,.68,0],[.115,.145,.112]);
 vrSphere(upper,depMaterials.hair,[0,.73,-.045],[.12,.105,.105]);
 vrSphere(upper,skin,[0,.67,.112],[.025,.03,.035]);
 if(female){
  vrSphere(upper,depMaterials.hair,[0,.66,-.14],[.085,.08,.07]);
  for(const x of [-.12,.12])vrSphere(upper,depMaterials.vipGold,[x,.64,0],[.018,.028,.018]);
  const sash=vrBox(upper,depMaterials.vipPallu,[.02,.28,.13],[.15,.52,.035]);sash.rotation.z=-.48;
 }else{
  vrBox(upper,depMaterials.white,[0,.34,.125],[.15,.32,.02]);
  vrBox(upper,depMaterials.dark,[0,.30,.14],[.045,.27,.02]);
  vrBox(upper,depMaterials.dark,[0,.70,.11],[.215,.04,.025]);
 }
 const pallu=female?vrBox(upper,depMaterials.vipPallu,[.15,.15,-.13],[.14,.68,.035]):null;
 const legs=[],arms=[];
 for(const side of [-1,1]){
  const thigh=vrLimb(g,cloth,null,null,.075),shin=vrLimb(g,cloth,null,null,.065);
  const foot=vrBox(g,female?depMaterials.vipGold:depMaterials.dark,[side*.1,.035,.04],[.12,.065,.23]);
  legs.push({side,thigh,shin,foot});
  const arm=new THREE.Group();arm.position.set(side*(female?.205:.255),.47,0);upper.add(arm);
  vrLimb(arm,cloth,null,null,.045).userData.between(new THREE.Vector3(),new THREE.Vector3(0,-.27,0));
  const fore=vrLimb(arm,skin,null,null,.036);fore.userData.between(new THREE.Vector3(0,-.27,0),new THREE.Vector3(0,-.5,.035));
  vrSphere(arm,skin,[0,-.51,.04],[.04,.055,.035]);arms.push(arm);
 }
 const skirt=female?new THREE.Mesh(new THREE.CylinderGeometry(.19,.285,.85,20,3,true),depMaterials.vipSaree):null;
 if(skirt){g.add(skirt);skirt.position.y=.48;const hem=new THREE.Mesh(new THREE.CylinderGeometry(.279,.287,.045,20,1,true),depMaterials.vipGold);hem.position.y=.075;g.add(hem);g.userData.hem=hem;}
 g.userData.pose=(distance=0,walk=0,seated=0,bend=0)=>{
  seated=vrClamp(seated);const run=g.userData.run||0,stride=.80+.80*run,phase=distance/stride*Math.PI*2;
  const hip=.86-.34*seated-.055*run;upper.position.y=hip;upper.rotation.x=bend*.42+.10*run;
  for(const l of legs){
   const q=(phase+(l.side===1?Math.PI:0))%(Math.PI*2),cycle=q/(Math.PI*2);
   // Planted half-stride, then a lifted recovery. Phase derives from travelled distance.
   const fraction=.60-.15*run,half=stride*fraction/2,stance=cycle<fraction,local=stance?cycle/fraction:(cycle-fraction)/(1-fraction);
   const z=(stance?half-half*2*local:-half+half*2*vrEase(local))*walk;
   const y=stance?0:Math.sin(local*Math.PI)*(.12+.07*run)*walk;
   const ankle=new THREE.Vector3(l.side*.10,.034+y,z+.36*seated);
   if(!seated&&g.parent===vvipGroup&&vvipReal){
    const c=Math.cos(g.rotation.y),s=Math.sin(g.rotation.y),wx=g.position.x+c*ankle.x+s*ankle.z,wz=g.position.z-s*ankle.x+c*ankle.z;
    const ground=vrSurface(wx,wz,g.position.y-.012)-g.position.y;
    ankle.y+=Math.max(-.24,Math.min(.24,ground));
   }
   const h=new THREE.Vector3(l.side*.10,hip,0),delta=ankle.clone().sub(h),len=Math.min(.815,Math.max(.1,delta.length()));
   const mid=h.clone().add(ankle).multiplyScalar(.5),height=Math.sqrt(Math.max(0,.415*.415-len*len/4));
   const normal=new THREE.Vector3(0,-delta.z,delta.y).normalize().multiplyScalar(-height);
   const knee=mid.add(normal);l.thigh.userData.between(h,knee);l.shin.userData.between(knee,ankle);
   l.foot.position.copy(ankle);l.foot.position.z+=.055;
  }
  arms.forEach((a,i)=>{a.rotation.x=(i?1:-1)*Math.sin(phase)*(.18+.22*run)*walk-.65*bend-.45*seated;});
  head.rotation.y=walk?Math.sin(distance*.6)*.025:Math.sin((vvipReal?.elapsed||0)*.7)*.035;
  if(skirt){skirt.position.set(0,.48-.18*seated,.15*seated);skirt.scale.set(1,1-.40*seated,1+.45*seated);skirt.rotation.x=-.30*seated;g.userData.hem.visible=seated<.15;}
  if(pallu)pallu.rotation.x=Math.sin(phase)*.035*walk;
 };
 g.userData.animateWalk=p=>g.userData.pose(p*1.05/(Math.PI*2),1,0,0);
 g.userData.setSeated=b=>g.userData.pose(0,0,b?1:0,0);
 g.userData.arms=arms;g.userData.upper=upper;
 g.userData.pose();return g;
}
function buildFemaleVvip(){return vrActor(true);}
function buildSecurityEscort(){return vrActor(false);}

function buildVvipCar(){
 const g=new THREE.Group(),m=depMaterials.vipCar,glass=depMaterials.vipGlass.clone();glass.transparent=true;glass.opacity=.32;glass.depthWrite=false;
 vrBox(g,m,[0,.39,0],[2.04,.18,5.1]); // cabin floor, no solid block across the doorway
 vrBox(g,m,[0,.76,1.94],[2.04,.62,1.22]);vrBox(g,m,[0,.72,-2.10],[2.04,.52,.94]);
 vrBox(g,m,[0,1.69,-.12],[1.93,.09,3.04]);
 for(const x of [-.96,.96])for(const z of [-1.62,-.05,1.32])vrBox(g,m,[x,1.19,z],[.07,1.0,.08]);
 for(const z of [-1.66,1.35])vrBox(g,glass,[0,1.30,z],[1.83,.62,.045]);
 const doors=[];
 for(const [side,z] of [[-1,-.80],[1,-.80],[1,.69],[-1,.69]]){
  const pivot=new THREE.Group();pivot.position.set(side*1.025,.48,z+.68);g.add(pivot);
  vrBox(pivot,m,[0,.24,-.68],[.065,.48,1.35]);vrBox(pivot,glass,[0,.83,-.68],[.04,.59,1.30]);
  vrBox(pivot,depMaterials.vipChrome,[side*.045,.45,-1.12],[.06,.06,.24]);
  doors.push({pivot,side,z,open:0});
 }
 const seats=[[-.46,.25,-.8],[.46,.25,-.8],[.46,.25,.69],[-.46,.25,.69]];
 for(const p of seats){vrBox(g,depMaterials.dark,[p[0],.67,p[2]],[.64,.16,.60]);vrBox(g,depMaterials.dark,[p[0],1.03,p[2]-.30],[.63,.65,.13]);}
 const wheels=[];
 for(const x of [-1.03,1.03])for(const z of [-1.65,1.65]){const w=new THREE.Group();w.position.set(x,.38,z);g.add(w);const tire=new THREE.Mesh(geos.cylinder,depMaterials.dark);tire.rotation.z=Math.PI/2;tire.scale.set(.38,.25,.38);w.add(tire);const rim=new THREE.Mesh(geos.cylinder,depMaterials.vipChrome);rim.rotation.z=Math.PI/2;rim.scale.set(.23,.27,.23);w.add(rim);wheels.push(w);}
 for(const x of [-.78,.78]){vrBox(g,depMaterials.white,[x,.78,2.57],[.36,.18,.04]);vrBox(g,depMaterials.red,[x,.72,-2.59],[.36,.17,.04]);}
 vrBox(g,depMaterials.vipChrome,[0,.70,2.57],[1.05,.32,.04]);
 // Neutral vehicle: no unsupported claim to an actual presidential vehicle or livery.
 const driver=vrActor(false);driver.userData.pose(0,0,1,0);driver.position.set(-.46,.25,.69);g.add(driver);
 g.userData.doors=doors;g.userData.seats=seats;g.userData.wheels=wheels;
 g.userData.setDoor=(i,t)=>{doors[i].open=vrClamp(t);doors[i].pivot.rotation.y=-doors[i].side*vrEase(t)*1.15;};
 g.userData.setPassengerDoor=t=>g.userData.setDoor(0,t);
 g.userData.passengerPoint=()=>vrWorld(g,[-1.85,0,-.80]);
 g.userData.rollWheels=d=>wheels.forEach(w=>w.rotation.x+=d/.38);
 return g;
}
function vrWorld(g,p){g.updateMatrixWorld(true);return g.localToWorld(new THREE.Vector3(...p));}
function vrHollowHeli(g,bodyUpper,bodyLower,stripe){
 g.remove(bodyUpper,bodyLower,stripe);
 vrBox(g,depMaterials.heliNavy,[0,1.03,0],[1.82,.12,3.7]);
 vrBox(g,depMaterials.heliWhite,[0,2.43,0],[1.90,.10,3.7]);
 vrBox(g,depMaterials.heliWhite,[0,1.72,-1.95],[1.83,1.45,.12]);
 vrBox(g,depMaterials.heliWhite,[.94,1.72,-.1],[.06,1.40,3.5]);
 for(const z of [-1.6,1.65])vrBox(g,depMaterials.heliWhite,[-.94,1.72,z],[.06,1.40,.60]);
 const door=new THREE.Group();door.position.set(-.98,1.08,1.30);g.add(door);
 vrBox(door,depMaterials.heliWhite,[0,.24,-.9],[.06,.48,1.8]);vrBox(door,depMaterials.vipGlass,[0,.95,-.9],[.045,.72,1.74]);
 vrBox(door,depMaterials.vipChrome,[-.05,.53,-1.5],[.06,.07,.23]);
 vrBox(g,depMaterials.vipChrome,[-1.18,.58,.3],[.43,.08,1.25]);
 g.userData.setDoor=t=>door.rotation.y=vrEase(t)*1.20;
 g.userData.door=door;
 // Correct visual navigation-light convention: port red, starboard green.
 const green=new THREE.MeshBasicMaterial({color:0x32d67b});vrSphere(g,green,[1.10,1.5,.3],[.08,.08,.08]);
 const pilot=vrActor(false);pilot.userData.pose(0,0,1,0);pilot.position.set(.38,1.02,1.5);g.add(pilot);g.userData.pilot=pilot;
}

function vrPath(points){
 const p=points.filter((p,i)=>!i||Math.hypot(...p.map((v,k)=>v-points[i-1][k]))>.001),lengths=[0];
 for(let i=1;i<p.length;i++)lengths.push(lengths.at(-1)+Math.hypot(...p[i].map((v,k)=>v-p[i-1][k])));
 return {p,lengths,total:lengths.at(-1)};
}
function vrRoundPath(points,radius=2){
 const out=[points[0]];
 for(let i=1;i<points.length-1;i++){
  const a=points[i-1],b=points[i],c=points[i+1],la=Math.hypot(...b.map((v,k)=>v-a[k])),lb=Math.hypot(...c.map((v,k)=>v-b[k])),trim=Math.min(radius,la*.25,lb*.25);
  const start=vrMix(b,a,trim/la),end=vrMix(b,c,trim/lb);out.push(start);
  for(let j=1;j<=10;j++){const t=j/10;out.push(start.map((v,k)=>(1-t)*(1-t)*v+2*(1-t)*t*b[k]+t*t*end[k]));}
 }
 out.push(points.at(-1));return vrPath(out);
}
function vrSample(path,d){
 d=Math.max(0,Math.min(path.total,d));let i=1;while(i<path.p.length-1&&path.lengths[i]<d)i++;
 const a=path.p[i-1],b=path.p[i],t=(d-path.lengths[i-1])/Math.max(.0001,path.lengths[i]-path.lengths[i-1]);
 return {pos:vrMix(a,b,t),angle:Math.atan2(b[0]-a[0],b[2]-a[2])};
}
function interpolateWaypoints(points,t){const path=vrPath(points);return vrSample(path,vrClamp(t)*path.total);}
function vrSurface(x,z,fallback=.16){
 let y=fallback;
 for(const o of vvipReal.surfaces){const dx=x-o.p[0],dz=z-o.p[2],r=o.rot||0,c=Math.cos(r),s=Math.sin(r),lx=c*dx-s*dz,lz=s*dx+c*dz;
  if(Math.abs(lx)<=o.s[0]/2+.015&&Math.abs(lz)<=o.s[2]/2+.015)y=Math.max(y,o.p[1]+o.s[1]/2);
 }
 const h=geo.helipadProposal;if(Math.hypot(x-h.centre[0],z-h.centre[1])<15.6)y=Math.max(y,.33);
 return y+.012;
}
function vrAngle(a,b,rate,dt){return a+Math.atan2(Math.sin(b-a),Math.cos(b-a))*(1-Math.exp(-rate*dt));}
function vrSegmentBox(a,b,o,radius=0){
 const bound=(o.s[0]+o.s[2])*.5+radius,vertical=o.s[1]*.5+radius;
 if(Math.max(a[0],b[0])<o.p[0]-bound||Math.min(a[0],b[0])>o.p[0]+bound||Math.max(a[2],b[2])<o.p[2]-bound||Math.min(a[2],b[2])>o.p[2]+bound||Math.max(a[1],b[1])<o.p[1]-vertical||Math.min(a[1],b[1])>o.p[1]+vertical)return null;
 const r=o.rot||0,c=Math.cos(r),s=Math.sin(r),local=p=>{const x=p[0]-o.p[0],z=p[2]-o.p[2];return [c*x-s*z,p[1]-o.p[1],s*x+c*z];};
 const u=local(a),v=local(b);let lo=0,hi=1;
 for(let k=0;k<3;k++){const extent=o.s[k]/2+radius,dir=v[k]-u[k];if(Math.abs(dir)<1e-7){if(Math.abs(u[k])>extent)return null;}else{let t1=(-extent-u[k])/dir,t2=(extent-u[k])/dir;if(t1>t2)[t1,t2]=[t2,t1];lo=Math.max(lo,t1);hi=Math.min(hi,t2);if(lo>hi)return null;}}
 return lo;
}
function vrBoxesOverlap(a,b,gap=0){
 if(Math.abs(a.p[1]-b.p[1])>(a.s[1]+b.s[1])/2+gap)return false;
 const axes=o=>[[Math.cos(o.rot||0),-Math.sin(o.rot||0)],[Math.sin(o.rot||0),Math.cos(o.rot||0)]],aa=axes(a),bb=axes(b),d=[b.p[0]-a.p[0],b.p[2]-a.p[2]];
 for(const axis of [...aa,...bb]){const dot=(u,v)=>u[0]*v[0]+u[1]*v[1],ra=Math.abs(dot(axis,aa[0]))*a.s[0]/2+Math.abs(dot(axis,aa[1]))*a.s[2]/2,rb=Math.abs(dot(axis,bb[0]))*b.s[0]/2+Math.abs(dot(axis,bb[1]))*b.s[2]/2;if(Math.abs(dot(d,axis))>ra+rb+gap)return false;}
 return true;
}
function vrVehicleSweep(a,b,heading,obstacle){
 const angle=heading-(obstacle.rot||0),c=Math.abs(Math.cos(angle)),s=Math.abs(Math.sin(angle));
 const expanded={...obstacle,s:[obstacle.s[0]+2*(c*1.1+s*2.7),obstacle.s[1]+1.65,obstacle.s[2]+2*(s*1.1+c*2.7)]};
 return vrSegmentBox([a[0],a[1]+.85,a[2]],[b[0],b[1]+.85,b[2]],expanded,.12)!==null;
}
function vrDynamicObstacles(ignore){
 const out=[];
 // Read deployment positions; never move or overwrite the user's saved deployment.
 for(const o of depItems){
  const node=depNodes.find(n=>n.item.id===o.id);if(node?.g.userData.vvipHidden)continue;
  const actual=node?.g.position||{x:o.x,y:o.y,z:o.z};
  const kind=o.kind,rot=(o.angle||0)*Math.PI/180;
  if(kind==='dfmd'){
   for(const x of [-.58,.58])out.push({p:[o.x+Math.cos(rot)*x,o.y+1.1,o.z-Math.sin(rot)*x],s:[.16,2.2,.40],rot});
   out.push({p:[o.x,o.y+2.2,o.z],s:[1.30,.18,.40],rot});
  }else{
   const person=['officer','armed_officer','hhmd','binocular','radio'].includes(kind),size=person?[.65,1.8,.65]:kind==='qrt'?[2.3,2.5,4.5]:kind==='xray'?[1.9,2.1,3.5]:kind==='ambulance'?[2.3,2.7,5.8]:kind==='firebrigade'?[2.6,3.6,7.2]:kind==='barricade'?[2.2,1.2,.7]:kind==='cone'?[.5,.8,.5]:[.8,1.3,.8];
   out.push({p:[actual.x,actual.y+size[1]/2,actual.z],s:size,rot,name:o.name,id:o.id});
  }
 }
 for(const actor of vvipReal.actors){if(actor===ignore||actor.parent!==vvipGroup)continue;out.push({p:[actor.position.x,actor.position.y+.85,actor.position.z],s:[.64,1.7,.64],rot:actor.rotation.y,name:actor.userData.role||'escort'});}
 if(vvipReal.host&&ignore!==vvipReal.host){const a=vvipReal.host;out.push({p:[a.position.x,a.position.y+.85,a.position.z],s:[.64,1.7,.64],rot:a.rotation.y});}
 return out;
}
function vrDoorMove(i,t,ignore){
 const door=vvipCar.userData.doors[i],turn=-door.side*vrEase(t)*1.15,point=vrWorld(vvipCar,[door.side*1.025-Math.sin(turn)*.68,1.05,door.z+.68-Math.cos(turn)*.68]);
 const box={p:point.toArray(),s:[.11,1.12,1.35],rot:vvipCar.rotation.y+turn};
 if([...vvipReal.walkObstacles,...vrDynamicObstacles(ignore)].some(o=>vrBoxesOverlap(box,o,.08))){vvipReal.blocked=true;return false;}
 vvipCar.userData.setDoor(i,t);return true;
}
function vrCamera(target,offset,dt){
 const aim=new THREE.Vector3(...target),desired=aim.clone().add(new THREE.Vector3(...offset));let nearest=1;
 for(const o of vvipReal.cameraObstacles){const hit=vrSegmentBox(target,desired.toArray(),o,.18);if(hit!==null&&hit>.025)nearest=Math.min(nearest,hit);}
 if(nearest<1)desired.copy(aim).lerp(desired,Math.max(.12,nearest-.04));
 desired.y=Math.max(desired.y,vrSurface(desired.x,desired.z,.15)+.40);
 // Check the actual interpolated position too, not only the desired shot.
 const candidate=camera.position.clone().lerp(desired,1-Math.exp(-4*dt));let blocked=false;
 for(const o of vvipReal.cameraObstacles)if(vrSegmentBox(target,candidate.toArray(),o,.12)!==null){blocked=true;break;}
 camera.position.copy(blocked?desired:candidate);controls.target.lerp(aim,1-Math.exp(-7*dt));
}
function vrMove(actor,path,d,speed,dt){
 const q=vrSample(path,d),last=actor.position.clone();
 const next=new THREE.Vector3(...q.pos);next.y=vrSurface(next.x,next.z,q.pos[1]-.012);
 // Ground-route collision guard at torso height. Pause instead of walking through a wall.
 const blockers=[...vvipReal.walkObstacles,...vrDynamicObstacles(actor),{p:[vvipCar.position.x,vvipCar.position.y+.85,vvipCar.position.z],s:[2.2,1.7,5.4],rot:vvipCar.rotation.y}];
 const obstruction=last.distanceTo(next)<2?blockers.find(o=>[.25,.70,1.25].some(h=>vrSegmentBox([last.x,last.y+h,last.z],[next.x,next.y+h,next.z],o,.15)!==null)):null;if(obstruction){if(!vvipReal.blocked){vvipReal.blockedName=(actor.userData.role||'person')+' → '+(obstruction.name||'nearby object');}vvipReal.blocked=true;return false;}
 actor.position.copy(next);actor.rotation.y=vrAngle(actor.rotation.y,q.angle,8,dt);
 actor.userData.distance=(actor.userData.distance||0)+last.distanceTo(next);
 actor.userData.run=vrClamp((speed-1.8)/1.3);actor.userData.pose(actor.userData.distance,speed>.02?Math.min(1,speed/.7):0,0,0);return true;
}
function vrAttach(actor,parent,p,seated=1){parent.add(actor);const scale=parent.getWorldScale(new THREE.Vector3());actor.scale.set(1/scale.x,1/scale.y,1/scale.z);actor.position.fromArray(p);actor.rotation.set(0,0,0);actor.userData.pose(0,0,seated,0);}
function vrDetach(actor){const pos=actor.getWorldPosition(new THREE.Vector3()),angle=actor.getWorldQuaternion(new THREE.Quaternion()),scale=actor.getWorldScale(new THREE.Vector3());vvipGroup.add(actor);actor.position.copy(pos);actor.quaternion.copy(angle);actor.scale.copy(scale);}
function vrContact(actor,size){
 const canvas=document.createElement('canvas');canvas.width=canvas.height=64;const cx=canvas.getContext('2d'),grad=cx.createRadialGradient(32,32,0,32,32,32);grad.addColorStop(0,'rgba(0,0,0,.28)');grad.addColorStop(1,'rgba(0,0,0,0)');cx.fillStyle=grad;cx.fillRect(0,0,64,64);
 const shadow=new THREE.Mesh(new THREE.PlaneGeometry(size[0],size[1]),new THREE.MeshBasicMaterial({map:new THREE.CanvasTexture(canvas),transparent:true,depthWrite:false}));shadow.rotation.x=-Math.PI/2;vvipGroup.add(shadow);vvipReal.contacts.push({actor,shadow});
}
function vrInit(){
 const h=geo.helipadProposal,gate=h.gate,carStart=h.vehicleAccess[0];
 const walls=data.objects.filter(o=>['box','rounded','cylinder'].includes(o.shape)&&/wall|column|pillar|pier|jamb|railing|roof|ceiling|tree trunk|fence|bollard|lamp post|bench/i.test(o.name)&&!(/paint|sign|stripe|coping|texture|shadow/i.test(o.name)));
 const furniture=data.objects.filter(o=>o.group==='interior'&&/sofa|Low stage table|chair.*(seat|back)/i.test(o.name));
 vvipReal={elapsed:0,t:0,contacts:[],blocked:false,actors:[vvipFemale,vvipEscort1,vvipEscort2],walkObstacles:[...walls.filter(o=>!/roof|ceiling/i.test(o.name)),...furniture],cameraObstacles:[...walls,...furniture],surfaces:data.objects.filter(o=>(o.shape==='box'||o.name.startsWith('Raised stage'))&&/Hall floor|Raised stage|External black entry step|Stage right side green stair|Auditorium red-carpet|Proposed red carpet|Core compound|main road.*surface|road asphalt|paved.*road/i.test(o.name)),carDistance:0,speed:0,rotor:35,completed:false};
 vvipCar.position.set(carStart[0],vrSurface(...[carStart[0],carStart[1]],.30),carStart[1]);
 const access=h.vehicleAccessPolyline||h.vehicleAccess;vvipCar.rotation.y=Math.atan2(access[1][0]-carStart[0],access[1][1]-carStart[1]);
 const heliScale=h.helicopterDisplayScale||1.45;vvipHeli.scale.setScalar(heliScale);if(vvipHeli.userData.pilot)vvipHeli.userData.pilot.scale.setScalar(1/heliScale);
 vvipReal.landing=[h.helicopterCentre[0],vrSurface(h.centre[0],h.centre[1],.33)-.06*heliScale,h.helicopterCentre[1]];
 vvipReal.heading=vvipCar.rotation.y;
 vvipHeli.position.set(vvipReal.landing[0]-9,18,vvipReal.landing[2]-50);vvipHeli.rotation.y=vvipReal.heading;
 for(const [i,a] of vvipReal.actors.entries()){a.userData.role=i?'PSO '+i:'VVIP';a.visible=true;vrAttach(a,vvipHeli,[-.30+i*.28,1.09,.1-i*.7],1);vrContact(a,[.75,.7]);}
 vrContact(vvipCar,[3.3,6.1]);vrContact(vvipHeli,[5,10]);
 const outer=data.objects.filter(o=>o.name.startsWith('External black entry step')).sort((a,b)=>a.p[1]-b.p[1]);
 const end=[gate[0],vrSurface(gate[0],outer[0].p[2],.30),outer[0].p[2]];
 // Stop parallel to the auditorium entry road; left passenger door faces the existing steps.
 const accessPoints=access.map(p=>[p[0],.312,p[1]]),join=h.roadConnectionCentre,frontage=h.campusRoadCentre;vvipReal.carPath=vrRoundPath([...accessPoints,...(join?[[join[0],.31,join[1]]]:[]),...(frontage?[[frontage[0],.31,frontage[1]]]:[]),[gate[0],.39,gate[1]+5],end],2);
 vvipReal.stageRoute=vrPath(vvipAuditoriumRoute().path);
 camera.position.set(vvipHeli.position.x-15,vvipHeli.position.y+7,vvipHeli.position.z-22);controls.target.copy(vvipHeli.position);
 root.querySelector('#vvip-skip-btn').textContent='Next chapter';
 const pause=root.querySelector('#vvip-pause-btn');if(pause){pause.textContent='Pause';pause.onclick=()=>{vvipReal.paused=!vvipReal.paused;if(vvipReal.paused)vvipReal.pauseStart=performance.now();else if(vvipReal.pauseStart)vvipReal.flightStart+=performance.now()-vvipReal.pauseStart;pause.textContent=vvipReal.paused?'Resume':'Pause';};}
 vvipReal.facing=[];for(const n of depNodes)if(['officer','armed_officer','hhmd','binocular','radio'].includes(n.item.kind))vvipReal.facing.push({node:n,angle:n.g.rotation.y});
 vvipReal.temporaryHidden=[];if(typeof gateController!=='undefined'){vvipReal.savedGateOpen=gateController.isOpen;gateController.open();}vvipReal.flightStart=performance.now();vrBuildLandingCarpet();vrBuildWelcome();
}
function vrBuildLandingCarpet(){
 const a=vrWorld(vvipHeli,[-2,0,.95]).toArray(),b=vrWorld(vvipCar,[-2.6,0,-1.35]).toArray();
 // Use landed helicopter coordinates, not its in-flight transform.
 const heading=vvipReal.heading,scale=geo.helipadProposal.helicopterDisplayScale||1.45,L=vvipReal.landing;
 a[0]=L[0]+Math.cos(heading)*(-2*scale)+Math.sin(heading)*(.95*scale);a[2]=L[2]-Math.sin(heading)*(-2*scale)+Math.cos(heading)*(.95*scale);
 const c=vrWorld(vvipCar,[-3.2,0,-4]).toArray(),points=[a,c,b];vvipReal.carpet=[];let accumulated=0;
 const material=new THREE.MeshStandardMaterial({color:0xa71c32,roughness:.95});
 for(let i=1;i<points.length;i++){const p=points[i-1],q=points[i],len=Math.hypot(q[0]-p[0],q[2]-p[2]),g=new THREE.Group();g.visible=false;vvipGroup.add(g);const strip=vrBox(g,material,[0,0,0],[1.5,.014,1]);for(const x of [-.73,.73])vrBox(g,depMaterials.vipGold,[x,.009,0],[.025,.005,1]);g.rotation.y=Math.atan2(q[0]-p[0],q[2]-p[2]);vvipReal.carpet.push({g,start:p,end:q,len,accumulated});accumulated+=len;}
 vvipReal.carpetLength=accumulated;
}
function vrRevealCarpet(t){for(const part of vvipReal.carpet){const length=Math.max(0,Math.min(part.len,vrEase(t)*vvipReal.carpetLength-part.accumulated));part.g.visible=length>.001;part.g.scale.z=Math.max(.001,length);const q=vrMix(part.start,part.end,length/part.len/2);part.g.position.set(q[0],vrSurface(q[0],q[2],.33)+.008,q[2]);}}
function vrBuildWelcome(){
 const R=vvipReal,end=vvipAuditoriumRoute().end;R.host=vrActor(false);R.host.position.set(end[0]+3.6,end[1],end[2]+1.3);R.host.rotation.y=-Math.PI/2;R.host.userData.pose();R.host.userData.arms[0].rotation.x=-.95;vvipGroup.add(R.host);vrContact(R.host,[.75,.7]);
 const bouquet=new THREE.Group();vrLimb(bouquet,new THREE.MeshStandardMaterial({color:0x3b7846}),null,null,.035).userData.between(new THREE.Vector3(0,0,0),new THREE.Vector3(0,.35,0));
 const colors=[0xe94973,0xffe3a5,0xc83949];for(let i=0;i<9;i++){const angle=i*Math.PI*2/9,r=i===8?0:.12;vrSphere(bouquet,new THREE.MeshStandardMaterial({color:colors[i%3],roughness:.85}),[Math.cos(angle)*r,.34+(i%2)*.05,Math.sin(angle)*r],[.075,.065,.075]);}
 const wrap=new THREE.Mesh(new THREE.ConeGeometry(.16,.25,12,1,true),depMaterials.vipGold);wrap.rotation.x=Math.PI;wrap.position.y=.18;bouquet.add(wrap);R.host.userData.arms[0].add(bouquet);bouquet.position.set(0,-.51,.04);R.bouquet=bouquet;
}
function vrRunEscorts(dt){
 for(let i=1;i<3;i++){const a=vvipReal.actors[i];if(a.parent!==vvipGroup)vrDetach(a);const target=vrWorld(vvipCar,[i===1?-3.2:3.2,0,-3.6]);target.y=vrSurface(target.x,target.z,.30);const distance=a.position.distanceTo(target);if(distance<.04){a.userData.pose();continue;}const speed=Math.min(3.6,Math.max(1.4,distance*2.0));
  const path=vrRouteAroundPeople(vrPath([a.position.toArray(),target.toArray()]),a);vrMove(a,path,Math.min(path.total,speed*dt),speed,dt);
 }
}
function vrRouteAroundPeople(path,actor){
 const people=[...vrDynamicObstacles(actor).filter(o=>o.id),...vvipReal.walkObstacles.filter(o=>o.s[0]<2&&o.s[2]<2&&o.s[1]>.25)],out=[path.p[0]];
 for(let i=1;i<path.p.length;i++){
  const b=path.p[i],a=out.at(-1),dx=b[0]-a[0],dz=b[2]-a[2],length=Math.hypot(dx,dz);if(length<.1){out.push(b);continue;}
  const forward=[dx/length,dz/length],normal=[-forward[1],forward[0]];
  const blocking=people.filter(o=>vrSegmentBox([a[0],a[1]+.85,a[2]],[b[0],b[1]+.85,b[2]],o,.36)!==null).sort((p,q)=>Math.hypot(p.p[0]-a[0],p.p[2]-a[2])-Math.hypot(q.p[0]-a[0],q.p[2]-a[2]));
  for(const obstacle of blocking){
   const radius=Math.hypot(obstacle.s[0],obstacle.s[2])*.5+.85;
   for(const side of [-1,1]){
    const p=[obstacle.p[0]-forward[0]*radius+normal[0]*side*radius,a[1],obstacle.p[2]-forward[1]*radius+normal[1]*side*radius],q=[obstacle.p[0]+forward[0]*radius+normal[0]*side*radius,a[1],obstacle.p[2]+forward[1]*radius+normal[1]*side*radius],points=[out.at(-1),p,q,b];
    const car={p:[vvipCar.position.x,vvipCar.position.y+.85,vvipCar.position.z],s:[2.2,1.7,5.4],rot:vvipCar.rotation.y};
    const blockers=[...vvipReal.walkObstacles,...people,car];let clear=true;
    for(let k=1;k<points.length&&clear;k++)for(const o of blockers){const hit=vrSegmentBox([points[k-1][0],points[k-1][1]+.85,points[k-1][2]],[points[k][0],points[k][1]+.85,points[k][2]],o,.34);if(hit!==null&&hit>.005){clear=false;break;}}
    if(clear){out.push(p,q);break;}
   }
  }
  out.push(b);
 }
 return vrPath(out);
}
function vrPrepareRoadDuty(){
 const R=vvipReal;if(vvipPhase>2)return;
 for(const {node:n} of R.facing){
  if(n.g.userData.vvipRoadPrepared)continue;
  n.g.userData.vvipRoadPrepared=true;
  let nearest=null,best=Infinity;
  for(let d=0;d<R.carPath.total;d+=.5){const q=vrSample(R.carPath,d),gap=Math.hypot(q.pos[0]-n.g.position.x,q.pos[2]-n.g.position.z);if(Math.abs(n.g.position.y-q.pos[1])<1.3&&gap<best){best=gap;nearest=q;}}
  if(!nearest||best>5.8)continue;
  const normal=[Math.cos(nearest.angle),-Math.sin(nearest.angle)],signed=(n.g.position.x-nearest.pos[0])*normal[0]+(n.g.position.z-nearest.pos[2])*normal[1],preferred=signed<0?-1:1;
  for(const side of [preferred,-preferred])for(const offset of [5.9,6.7,7.5]){
   if(n.g.userData.vvipRoadPositioned)break;
   const target=new THREE.Vector3(nearest.pos[0]+normal[0]*side*offset,n.g.position.y,nearest.pos[2]+normal[1]*side*offset),box={p:[target.x,target.y+.85,target.z],s:[.7,1.7,.7],rot:0};
   const occupied=R.walkObstacles.some(o=>vrSegmentBox(box.p,box.p,o,.42)!==null)||depNodes.some(other=>other!==n&&Math.abs(other.g.position.y-target.y)<1.3&&other.g.position.distanceTo(target)<1.2);
   if(!occupied){n.g.position.copy(target);n.g.userData.vvipYield=target.clone();n.g.userData.vvipRoadPositioned=true;}
  }
 }
}
function vrCruiseTarget(path,distance){
 const now=vrSample(path,distance),ahead=vrSample(path,Math.min(path.total,distance+7));
 const turn=Math.abs(Math.atan2(Math.sin(ahead.angle-now.angle),Math.cos(ahead.angle-now.angle)));
 return Math.min(2.4,turn>.45?1.0:turn>.20?1.6:2.4,Math.sqrt(Math.max(0,1.4*(path.total-distance))));
}
function vrSceneActors(dt){
 const R=vvipReal,vip=vvipFemale.getWorldPosition(new THREE.Vector3());
 if(typeof gateController!=='undefined'&&!gateController.isOpen)gateController.open();
 // Deployment can finish loading or rebuild after playback starts. Always follow live nodes.
 R.facing=depNodes.filter(n=>['officer','armed_officer','hhmd','binocular','radio'].includes(n.item.kind)).map(n=>R.facing.find(old=>old.node.g===n.g)||{node:n,angle:n.g.rotation.y});
 vrPrepareRoadDuty();
 const gate=geo.helipadProposal.gate;
 if(vvipPhase===3&&Math.hypot(vvipCar.position.x-gate[0],vvipCar.position.z-gate[1])<20){for(const n of depNodes)if(n.item.kind==='dfmd'&&Math.hypot(n.item.x-gate[0],n.item.z-gate[1])<22&&!n.g.userData.vvipHidden){n.g.userData.vvipHidden=true;n.g.visible=false;R.temporaryHidden.push(n);}}
 for(const {node:n} of R.facing){if(n.g.position.distanceTo(vip)<25&&(!n.g.userData.vvipYield||n.g.position.distanceTo(n.g.userData.vvipYield)<.05))n.g.rotation.y=vrAngle(n.g.rotation.y,Math.atan2(n.g.position.x-vip.x,n.g.position.z-vip.z),4,dt);}
 if(vvipPhase!==3){if(vvipPhase===4||vvipPhase===5)vrPedestrianYield();vrMoveYielders(dt);return;}
 // Animation-only yielding: keep existing saved duty positions untouched.
 for(const {node:n} of R.facing){
  const pos=n.g.position,car=vvipCar.position;if(pos.distanceTo(car)>16)continue;
  let nearest=null,best=Infinity;for(let d=R.carDistance;d<Math.min(R.carPath.total,R.carDistance+16);d+=.6){const q=vrSample(R.carPath,d),gap=Math.hypot(q.pos[0]-pos.x,q.pos[2]-pos.z);if(gap<best){best=gap;nearest=q;}}
  if(!nearest||best>3.6)continue;
  if(!n.g.userData.vvipYield){
   for(const side of [-1,1]){const target=new THREE.Vector3(nearest.pos[0]+Math.cos(nearest.angle)*side*3.3,pos.y,nearest.pos[2]-Math.sin(nearest.angle)*side*3.3),a=[pos.x,pos.y+.85,pos.z],b=[target.x,target.y+.85,target.z];
    if(!R.walkObstacles.some(o=>vrSegmentBox(a,b,o,.35)!==null)&&!vrDynamicObstacles().filter(o=>o.id!==n.item.id).some(o=>{const hit=vrSegmentBox(a,b,o,.35);return hit!==null&&hit>.02;})){n.g.userData.vvipYield=target;break;}}
  }
 }
 vrMoveYielders(dt);
}
function vrPedestrianYield(){
 const R=vvipReal,paths=vvipPhase===5?[R.stageRoute,...(R.followPaths||[])]:[];
 for(const {node:n} of R.facing){
  if(!R.actors.some(a=>a.parent===vvipGroup&&a.position.distanceTo(n.g.position)<7))continue;
  let closest=null,best=1.0;
  for(const path of paths){if(!path)continue;for(let d=0;d<path.total;d+=.4){const q=vrSample(path,d),gap=Math.hypot(q.pos[0]-n.g.position.x,q.pos[2]-n.g.position.z);if(Math.abs(q.pos[1]-n.g.position.y)<1&&gap<best){best=gap;closest=q;}}}
  if(!closest)continue;
  if(n.g.userData.vvipYield&&n.g.position.distanceTo(n.g.userData.vvipYield)>.08)continue;
  const pos=n.g.position,forward=[Math.sin(closest.angle),Math.cos(closest.angle)],normal=[Math.cos(closest.angle),-Math.sin(closest.angle)];
  for(const side of [-1,1])for(const ahead of [0,1.4,-1.4]){
   if(n.g.userData.vvipYield&&n.g.position.distanceTo(n.g.userData.vvipYield)>.08)break;
   const target=new THREE.Vector3(pos.x+normal[0]*side*1.4+forward[0]*ahead,pos.y,pos.z+normal[1]*side*1.4+forward[1]*ahead),a=[pos.x,pos.y+.85,pos.z],b=[target.x,target.y+.85,target.z];
   const obstacles=[...R.walkObstacles,...vrDynamicObstacles().filter(o=>o.id!==n.item.id)];
   if(!obstacles.some(o=>{const hit=vrSegmentBox(a,b,o,.34);return hit!==null&&hit>.01;})){n.g.userData.vvipYield=target;break;}
  }
 }
}
function vrMoveYielders(dt){
 const R=vvipReal;
 for(const {node:n} of R.facing){const target=n.g.userData.vvipYield;if(!target)continue;const delta=target.clone().sub(n.g.position),length=delta.length();if(length>.02){n.g.rotation.y=vrAngle(n.g.rotation.y,Math.atan2(delta.x,delta.z),5,dt);n.g.position.addScaledVector(delta.normalize(),Math.min(length,1.4*dt));const rig=n.g.userData.rig;if(rig){rig.walkPhase+=dt*7;rig.leftLeg.rotation.x=Math.sin(rig.walkPhase)*.35;rig.rightLeg.rotation.x=-Math.sin(rig.walkPhase)*.35;}}else{const rig=n.g.userData.rig;if(rig){rig.leftLeg.rotation.x=0;rig.rightLeg.rotation.x=0;}}}
}
function vrRestoreScene(){
 if(!vvipReal)return;
 if(typeof gateController!=='undefined'&&vvipReal.savedGateOpen!==undefined){if(vvipReal.savedGateOpen)gateController.open();else gateController.close();}
 for(const {node:n} of vvipReal.facing||[]){n.g.position.set(n.item.x,n.item.y,n.item.z);n.g.rotation.y=-n.item.angle*Math.PI/180;delete n.g.userData.vvipYield;delete n.g.userData.vvipRoadPrepared;delete n.g.userData.vvipRoadPositioned;}
 for(const n of vvipReal.temporaryHidden||[]){delete n.g.userData.vvipHidden;n.g.visible=true;}
}
function vrStagePaths(){
 const R=vvipReal,route=vvipAuditoriumRoute().path,end=vvipAuditoriumRoute().end,common=route[3];
 R.stageRoute=vrRouteAroundPeople(vrPath([vvipFemale.position.toArray(),...route.slice(3)]),vvipFemale);
 const near=p=>Math.hypot(...p.map((v,k)=>v-common[k]))<.05,commonIndex=R.stageRoute.p.findIndex(near),tail=R.stageRoute.p.slice(Math.max(0,commonIndex),-1);
 R.followPaths=R.actors.map((a,i)=>{
  if(!i)return R.stageRoute;
  const way=[];if(i===2){for(const local of [[3.2,0,-4.5],[-3.2,0,-4.5]]){const p=vrWorld(vvipCar,local).toArray();p[1]=vrSurface(p[0],p[2],.30);way.push(p);}}
  const prefix=vrRouteAroundPeople(vrPath([a.position.toArray(),...way,common]),a);
  return vrPath([...prefix.p,...tail.slice(1),...(i===1?[[route.at(-2)[0],end[1],.30],[end[0]-1.1,end[1],.30]]:[]),[end[0]+(i===1?-1.1:1.1),end[1],end[2]-.9]]);
 });
 const prefix=path=>{const i=path.p.findIndex(near);return i<0?0:path.lengths[i];},base=prefix(R.stageRoute);R.followOffsets=R.followPaths.map(path=>prefix(path)-base);R.walkDistance=0;R.followD=[0,0,0];R.speed=0;vrChange(5);
}
function vrWelcome(dt){
 const R=vvipReal,end=vvipAuditoriumRoute().end;
 if(!R.finalPaths){R.finalPaths=R.actors.map((a,i)=>i?vrPath([a.position.toArray(),[a.position.x,end[1],end[2]-1],[end[0]+(i===1?-2.4:2.4),end[1],end[2]-1]]):null);R.finalD=[0,0,0];}
 for(let i=1;i<3;i++){const path=R.finalPaths[i],d=Math.min(path.total,R.finalD[i]+1.4*dt);if(d>R.finalD[i]&&vrMove(R.actors[i],path,d,1.4,dt))R.finalD[i]=d;if(d>=path.total-.01){R.actors[i].userData.pose();R.actors[i].rotation.y=vrAngle(R.actors[i].rotation.y,Math.PI,3,dt);}}
 const ready=[1,2].every(i=>R.finalD[i]>=R.finalPaths[i].total-.01);
 if(ready&&!R.welcomePath){R.welcomePath=vrPath([R.host.position.toArray(),[R.host.position.x,end[1],end[2]],[end[0]+.85,end[1],end[2]]]);R.welcomeD=0;}
 if(R.welcomePath&&R.welcomeD<R.welcomePath.total-.01){const d=Math.min(R.welcomePath.total,R.welcomeD+1.05*dt);if(vrMove(R.host,R.welcomePath,d,1.05,dt))R.welcomeD=d;R.host.userData.arms[0].rotation.x=-.95;}
 if(R.welcomePath&&R.welcomeD>=R.welcomePath.total-.01){
  if(!R.handOver){R.handOver=0;const p=R.bouquet.getWorldPosition(new THREE.Vector3());vvipGroup.add(R.bouquet);R.bouquet.position.copy(p);R.flowerStart=p.clone();}
  R.handOver+=dt;R.host.userData.pose();R.host.rotation.y=vrAngle(R.host.rotation.y,-Math.PI/2,3,dt);R.host.userData.arms[0].rotation.x=-.95*(1-vrEase(R.handOver/2.5));
  vvipFemale.userData.pose();vvipFemale.userData.arms[0].rotation.x=-.95*vrEase(R.handOver/1.2);
  const target=vrWorld(vvipFemale.userData.arms[0],[0,-.51,.04]);if(!R.flowersReceived)R.bouquet.position.copy(R.flowerStart).lerp(target,vrEase(R.handOver/2));
  if(R.handOver>=2&&!R.flowersReceived){const p=R.bouquet.position.clone();vvipFemale.userData.arms[0].add(R.bouquet);R.bouquet.position.copy(vvipFemale.userData.arms[0].worldToLocal(p));R.flowersReceived=true;}
 }
 if(R.flowersReceived){vvipFemale.userData.arms[0].rotation.x=-.95;root.dataset.simulation='complete';}
 vvipFemale.rotation.y=vrAngle(vvipFemale.rotation.y,Math.PI,3,dt);vrCamera([end[0]+.35,end[1]+1,end[2]],[-3,1.5,-8],dt);
 updateVvipHUD(5,'Stage welcome',R.flowersReceived?'Bouquet received · Visual rehearsal complete · Replay / Exit':R.welcomePath?'Welcome on the existing stage — bouquet presentation':'Main stage reached — escorts taking their places');
}
function vrChange(phase){vvipPhase=phase;vvipPhaseTimer=0;vvipReal.t=0;vvipReal.jobs=null;vvipReal.blocked=false;}
function vrBeginTransfers(exitHeli){
 const order=[1,0,2];vvipReal.jobs=vvipReal.actors.map((actor,i)=>({actor,i,state:exitHeli?'heliWait':'open',t:exitHeli?-order.indexOf(i)*3.2:-i*.8,d:0,speed:0,done:false}));
 if(!exitHeli){vvipReal.jobs=vvipReal.jobs.filter(j=>j.i===0);vvipReal.jobs.forEach(j=>{j.outside=vrWorld(vvipCar,[-2.6,0,-1.35]).toArray();j.seat=vvipCar.userData.seats[0];});}
}
function vrTransfer(job,dt,fromHeli){
 const a=job.actor,i=job.i;job.t+=dt;if(job.t<0)return;
 const setState=s=>{job.state=s;job.t=0;};
 if(job.state==='heliWait'){
  if(vvipReal.rotor>.01)return;
  if(!vvipReal.heliDoorOpen||vvipReal.t<vvipReal.heliDoorOpenedAt+[1,0,2].indexOf(i)*4.6)return;
  vrDetach(a);job.start=a.position.toArray();setState('heliExit');
 }else if(job.state==='heliExit'){
  const door=vrWorld(vvipHeli,[-1.35,1.09,.40]).toArray(),step=vrWorld(vvipHeli,[-1.40,.64,.40]).toArray(),ground=vrWorld(vvipHeli,[-2.0,0,.95]).toArray();ground[1]=vrSurface(ground[0],ground[2],.33);
  const t=job.t,p=t<1.5?vrMix(job.start,door,vrEase(t/1.5)):t<2.8?vrMix(door,step,vrEase((t-1.5)/1.3)):vrMix(step,ground,vrEase((t-2.8)/1.7));
  a.position.fromArray(p);a.rotation.y=vrAngle(a.rotation.y,vvipReal.heading-Math.PI/2,6,dt);a.userData.pose(job.t*.45,t>1.5?1:0,1-vrEase(t/1.5),Math.sin(vrClamp(t/4.5)*Math.PI)*.5);
  if(t>=4.5){const side=i===2?1:-1,waiting=i===0?[-2.6,0,-1.35]:[side*(i===1?3.6:3.2),0,-3.6];job.outside=vrWorld(vvipCar,waiting).toArray();job.outside[1]=vrSurface(job.outside[0],job.outside[2],.30);
   const clearance=vrWorld(vvipCar,[side*(i===0?2.6:i===1?4.2:3.2),0,-4.0]).toArray();clearance[1]=vrSurface(clearance[0],clearance[2],.30);job.path=vrPath([ground,clearance,job.outside]);setState('walkCar');}
 }else if(job.state==='walkCar'){
  const remaining=job.path.total-job.d,target=Math.min(i===0?1.40:1.65,Math.sqrt(Math.max(0,2*1.1*remaining)));job.speed=Math.min(target,job.speed+1.1*dt);const next=Math.min(job.path.total,job.d+Math.max(.04,job.speed)*dt);
  if(vrMove(a,job.path,next,job.speed,dt))job.d=next;
  if(job.d>=job.path.total-.005){a.userData.pose(0);if(i>0){job.done=true;setState('escortReady');}else setState('open');}
 }else if(job.state==='open'){
  if(!vrDoorMove(i,vrClamp(job.t/1.2),a)){job.t-=dt;return;}
  if(job.t>=1.2){if(fromHeli){job.start=a.position.toArray();setState('board');}else{vrDetach(a);job.start=a.position.toArray();setState('exit');}}
 }else if(job.state==='board'){
  const seat=vrWorld(vvipCar,vvipCar.userData.seats[i]).toArray(),t=vrEase(job.t/2.8),threshold=vrWorld(vvipCar,[i===0?-1.2:1.2,.12,(i===2?.69:-.8)-.4]).toArray();a.position.fromArray(t<.5?vrMix(job.start,threshold,t*2):vrMix(threshold,seat,(t-.5)*2));a.rotation.y=vrAngle(a.rotation.y,vvipCar.rotation.y,4,dt);a.userData.pose(0,0,t,Math.sin(t*Math.PI)*.9);
  if(job.t>=2.8){vrAttach(a,vvipCar,vvipCar.userData.seats[i],1);setState('close');}
 }else if(job.state==='exit'){
  const t=vrEase(job.t/2.8),threshold=vrWorld(vvipCar,[i===0?-1.2:1.2,.12,(i===2?.69:-.8)-.4]).toArray();a.position.fromArray(t<.5?vrMix(job.start,threshold,t*2):vrMix(threshold,job.outside,(t-.5)*2));a.rotation.y=vrAngle(a.rotation.y,vvipCar.rotation.y,4,dt);a.userData.pose(0,0,1-t,Math.sin(t*Math.PI)*.9);
  if(job.t>=2.8){
   job.start=a.position.toArray();const front=vrWorld(vvipCar,[-3.2,0,-1.35]).toArray();front[1]=vrSurface(front[0],front[2],.30);job.path=vrPath([job.start,front]);job.d=0;job.speed=0;setState('clear');
  }
 }else if(job.state==='clear'){
  job.speed=Math.min(1.4,job.speed+1.0*dt);const next=Math.min(job.path.total,job.d+job.speed*dt);if(vrMove(a,job.path,next,job.speed,dt))job.d=next;
  if(job.d>=job.path.total-.005){a.userData.pose();setState('close');}
 }else if(job.state==='close'){
  if(!vrDoorMove(i,vrClamp(1-job.t/1.2),a)){job.t-=dt;return;}if(job.t>=1.2){job.done=true;setState('done');}
 }
}
function vrFlight(dt){
 const R=vvipReal,t=R.t,L=R.landing;
 // Slow final descent, level touchdown, then explicit visual shutdown before the cabin opens.
 if(t<6){const u=vrEase(t/6),p=vrMix([L[0]-9,18,L[2]-50],L,u);p[1]=L[1]+(18-L[1])*Math.pow(1-u,1.6);vvipHeli.position.fromArray(p);vvipHeli.rotation.x=Math.sin(Math.PI*vrClamp(t/6))*.035;}
 else{vvipHeli.position.fromArray(L);vvipHeli.rotation.x=0;R.rotor=35*(1-vrEase((t-8)/6));}
 const p=vvipHeli.position;vrCamera([p.x,p.y+1.6,p.z],[-13,6,-18],dt);
 updateVvipHUD(1,'Arrival & shutdown',t<6?'Helicopter approach — visual rehearsal':R.rotor>.01?'Landed — cabin closed while rotors stop':'Rotors stopped — cabin exit sequence');
 if(t>=14&&R.rotor<.01)vrChange(2);
}
function tickVvipSimulation(dt){
 if(!vvipActive||!vvipGroup||!vvipReal)return false;
 if(vvipReal.paused)return false;
 const R=vvipReal;if(!R.lastDiagnostic||R.elapsed-R.lastDiagnostic>.3){R.lastDiagnostic=R.elapsed;root.dataset.rehearsalState=JSON.stringify({phase:vvipPhase,walk:R.walkDistance,offset:R.followOffsets,follow:R.followD,actors:R.actors.map(a=>({role:a.userData.role,p:a.position.toArray()})),blocked:R.blockedName,car:vvipCar.position?.toArray?.(),carDistance:R.carDistance,carTotal:R.carPath?.total,speed:R.speed,dfmdCleared:R.temporaryHidden?.length||0});}R.blocked=false;dt=Math.min(.10,Math.max(0,dt));R.elapsed+=dt;R.t+=dt;vvipPhaseTimer=R.t;
 vrSceneActors(dt);
 if(vvipPhase===1){R.t=(performance.now()-R.flightStart)/1000;vrFlight(dt);}
 else if(vvipPhase===2||vvipPhase===4){
  const fromHeli=vvipPhase===2;if(!R.jobs)vrBeginTransfers(fromHeli);
  if(fromHeli){
   vrRevealCarpet(R.t/2);if(!R.heliDoorOpen){vvipHeli.userData.setDoor(vrClamp((R.t-2)/1.4));if(R.t>=3.4){R.heliDoorOpen=true;R.heliDoorOpenedAt=R.t;}}
  }
  for(const job of R.jobs)if(!job.done)vrTransfer(job,dt,fromHeli);
  const a=vvipFemale.getWorldPosition(new THREE.Vector3());vrCamera([a.x,a.y+1.05,a.z],[-5,2.4,-6.5],dt);
  if(fromHeli&&R.jobs.every(j=>!['heliWait','heliExit'].includes(j.state))){if(!R.heliCloseAt)R.heliCloseAt=R.t;vvipHeli.userData.setDoor(1-vrEase((R.t-R.heliCloseAt)/1.4));}
  const state=R.jobs[0].state,caption={heliWait:'Cabin door opening after rotor stop',heliExit:'Step down from cabin',walkCar:'Walk to the vehicle',open:'Vehicle stopped — passenger door opening',board:'Turn, bend and sit in vehicle',exit:'Stand and step out of vehicle',clear:'Walk clear of the door',close:'Door closing after clearance',done:'Waiting for all passengers'}[state];
  updateVvipHUD(vvipPhase,fromHeli?'Disembark & board':'Vehicle exit',R.blocked?'Waiting for clearance: '+R.blockedName:caption);
  if(R.jobs.every(j=>j.done)&&vvipCar.userData.doors.every(d=>d.open<.001)){
   if(fromHeli){R.speed=0;R.carDistance=0;vrChange(3);}else vrStagePaths();
  }
 }else if(vvipPhase===3){
  vrRunEscorts(dt);
  if(vvipFemale.parent!==vvipCar||vvipCar.userData.doors.some(d=>d.open>.001)){updateVvipHUD(3,'Waiting','Vehicle remains stopped until VVIP is seated and doors are closed');return true;}
  const remaining=R.carPath.total-R.carDistance,target=vrCruiseTarget(R.carPath,R.carDistance);R.speed+=Math.max(-.85*dt,Math.min(.65*dt,target-R.speed));const distance=Math.min(R.carPath.total,R.carDistance+Math.max(.015,R.speed)*dt),q=vrSample(R.carPath,distance),last=vvipCar.position.clone();
  const carTarget=[q.pos[0],vrSurface(q.pos[0],q.pos[2],.30),q.pos[2]];
  const blocker=[...R.walkObstacles,...vrDynamicObstacles()].find(o=>vrVehicleSweep(last.toArray(),carTarget,vvipCar.rotation.y,o));if(blocker){R.speed=0;R.blocked=true;updateVvipHUD(3,'Vehicle stopped','Vehicle stopped for clearance: '+(blocker.name||'nearby person or equipment'));return true;}
  vvipCar.position.fromArray(carTarget);vvipCar.rotation.y=vrAngle(vvipCar.rotation.y,q.angle,2.5,dt);vvipCar.userData.rollWheels(last.distanceTo(vvipCar.position));R.carDistance=distance;
  const p=vvipCar.position,ang=vvipCar.rotation.y;vrCamera([p.x,p.y+1,p.z],[-Math.sin(ang)*8-4,3,-Math.cos(ang)*8],dt);updateVvipHUD(3,'Vehicle transfer','Vehicle transfer — gradual acceleration and braking');
  if(distance>=R.carPath.total-.01&&R.speed<.18){R.speed=0;vrChange(4);}
 }else if(vvipPhase===5){
  if(!vvipHallPrepared){prepareVvipHall();groups.roof.visible=false;}
  const remain=R.stageRoute.total-R.walkDistance,target=Math.min(1.4,Math.sqrt(Math.max(0,1.6*remain)));R.speed+=Math.max(-1.0*dt,Math.min(.85*dt,target-R.speed));const d=Math.min(R.stageRoute.total,R.walkDistance+Math.max(.025,R.speed)*dt);
  if(vrMove(vvipFemale,R.stageRoute,d,R.speed,dt))R.walkDistance=d;
  for(let i=1;i<3;i++){if(R.walkDistance<R.stageRoute.total-.01&&R.actors[i].position.distanceTo(i===1?vvipFemale.position:R.actors[1].position)<1.4){R.actors[i].userData.pose();continue;}const path=R.followPaths[i],finished=R.walkDistance>=R.stageRoute.total-.01,desired=finished?path.total:Math.max(0,Math.min(path.total,R.walkDistance+R.followOffsets[i]-i*1.5)),travel=Math.min(desired,R.followD[i]+1.65*dt);if(travel>R.followD[i]&&vrMove(R.actors[i],path,travel,1.65,dt))R.followD[i]=travel;}
  const a=vvipFemale.position;vrCamera([a.x,a.y+1.05,a.z],[-3.5,2,-5.7],dt);updateVvipHUD(5,'Main stage',R.blocked?'Waiting for clearance: '+R.blockedName:'Walking through auditorium entry and side stairs to the existing stage');
  if(R.walkDistance>=R.stageRoute.total-.01){vvipFemale.userData.pose();if([1,2].every(i=>R.followD[i]>=R.followPaths[i].total-.01)){R.actors.forEach(a=>a.userData.pose(0));R.finishStart=R.elapsed;vrChange(6);}}
 }else if(vvipPhase===6){
  root.querySelector('#vvip-skip-btn').textContent='Replay';vrWelcome(dt);
 }
 if(vvipHeli.userData.mainRotor){vvipHeli.userData.mainRotor.rotation.y+=R.rotor*dt;vvipHeli.userData.tailRotor.rotation.x+=R.rotor*1.5*dt;vvipHeli.userData.rotorDisc.visible=R.rotor>15;}
 for(const {actor,shadow} of R.contacts){const p=actor.getWorldPosition(new THREE.Vector3());shadow.position.set(p.x,vrSurface(p.x,p.z,.15)+.006,p.z);shadow.visible=actor.parent===vvipGroup&&p.y-shadow.position.y<3;}
 // Pause/resume does not advance wall-clock animation time.
 return true;
}
function advanceVvipPhase(){
 // User-requested chapter skipping is an explicit edit, not hidden teleportation during playback.
 if(!vvipReal)return;
 if(vvipPhase===1){vvipHeli.position.fromArray(vvipReal.landing);vvipReal.rotor=0;vrChange(2);}
 else if(vvipPhase===2){vrAttach(vvipFemale,vvipCar,vvipCar.userData.seats[0],1);for(let i=1;i<3;i++){const actor=vvipReal.actors[i];vrDetach(actor);actor.position.copy(vrWorld(vvipCar,[i===1?-3.2:3.2,0,-3.6]));actor.userData.pose();}vvipCar.userData.setDoor(0,0);vvipHeli.userData.setDoor(0);vrRevealCarpet(1);vrChange(3);}
 else if(vvipPhase===3){const p=vrSample(vvipReal.carPath,vvipReal.carPath.total);vvipCar.position.fromArray(p.pos);vvipCar.rotation.y=p.angle;for(let i=1;i<3;i++){const actor=vvipReal.actors[i];actor.position.copy(vrWorld(vvipCar,[i===1?-3.2:3.2,0,-3.6]));actor.userData.pose();}vvipReal.speed=0;vrChange(4);}
 else if(vvipPhase===4){if(vvipFemale.parent!==vvipGroup)vrDetach(vvipFemale);vvipFemale.position.copy(vrWorld(vvipCar,[-3.2,0,-1.35]));vvipFemale.position.y=vrSurface(vvipFemale.position.x,vvipFemale.position.z,.30);vvipFemale.userData.pose();vvipCar.userData.setDoor(0,0);vrStagePaths();}
 else if(vvipPhase===5){placeVvipOnActualStage();vrChange(6);}
 else{stopVvipSimulation();startVvipSimulation();}
}

// END REALISTIC REHEARSAL ENGINE
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
  depStore(true);
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
  const isOfficer = item.kind === 'officer' || item.kind === 'armed_officer' || item.kind === 'hhmd' || item.kind === 'binocular' || item.kind === 'radio';
  const isHelipad = item.kind === 'helipad';
  if (symEl) symEl.textContent = depSymbols[item.kind] || '👮';
  if (titleTextEl) titleTextEl.textContent = isOfficer ? 'Officer Details' : (isHelipad ? 'Helipad Details' : (item.kind === 'qrt' ? 'QRT Vehicle Details' : (item.kind === 'xray' ? 'X-Ray Scanner Details' : 'Equipment Details')));
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
  depStore(true);
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


document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'hidden') {
    depSaveBeforeLeave();
  }
});
