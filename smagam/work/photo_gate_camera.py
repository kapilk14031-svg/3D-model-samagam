from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
s=s.replace("function enterWorldFeature(item,walk=false,inside=false){if(!item)return;", "function enterWorldFeature(item,walk=false,inside=false){if(!item)return;if(!walk&&['G01','G02'].includes(item.id)){enterPhotoGateView(item.id);return}sceneEl.classList.remove('photo-gate-view');",1)
s=s.replace("function go(view){activeDetailItem=null;", "function go(view){sceneEl.classList.remove('photo-gate-view');activeDetailItem=null;",1)
s=s.replace("function setConcept(on){if(on&&depFollowState)", "function setConcept(on){if(on)sceneEl.classList.remove('photo-gate-view');if(on&&depFollowState)",1)
addon='''
function enterPhotoGateView(id){const item=conceptItems.find(v=>v.id===id);if(!item)return;setConcept(false);exitNavigation();depPanel.hidden=true;depDutyCard.hidden=true;depMode=null;depRoutebar.hidden=true;pandalInterior=false;cutaway=false;orbit=false;anim=null;topView=false;target=[item.world[0],10,item.world[2]];yaw=Math.PI/2;elevation=.055;distance=100;sceneEl.classList.add('photo-gate-view');resize();document.getElementById('sceneModeLabel').textContent=item.name+' · Photo reference';dirty=true;sceneEl.scrollIntoView({block:'start'})}
const photoViewStyle=document.createElement('style');photoViewStyle.textContent='.scene.photo-gate-view{height:calc(100svh - 12px)!important;min-height:360px}.scene.photo-gate-view .notice,.scene.photo-gate-view .hint{display:none}';document.head.append(photoViewStyle);
for(const[id,label]of[['G01','Gate 1 · photo view'],['G02','Gate 2 · photo view']]){const b=document.createElement('button');b.textContent=label;b.onclick=()=>enterPhotoGateView(id);document.querySelector('[data-view="gates"]').after(b)}
function photoGateHash(){if(location.hash==='#gate1')enterPhotoGateView('G01');if(location.hash==='#gate2')enterPhotoGateView('G02')}window.addEventListener('hashchange',photoGateHash);setTimeout(photoGateHash,0);
'''
s=s.replace('</script>',addon+'\n</script>')
p.write_text(s,encoding='utf-8')
