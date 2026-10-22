from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
marker='for(const o of DATA.objects){if([\'B01\',\'B09\',\'B10\',\'B12\',\'B17\',\'W29\'].includes(o.featureId))continue;'
assert marker in s
addon='''let photoGateOpen=false;
function photoGateOpened(o){const leaf=o.photoLeaf;if(!leaf)return o;const a=leaf.turn,c=Math.cos(a),s=Math.sin(a),dx=o.p[0]-leaf.pivot[0],dz=o.p[2]-leaf.pivot[2];return{...o,p:[leaf.pivot[0]+dx*c+dz*s,o.p[1],leaf.pivot[2]-dx*s+dz*c],rotY:(o.rotY||0)+a,photoGateState:'open'}}
const photoGateRenderObjects=DATA.objects.flatMap(o=>o.photoLeaf?[{...o,photoGateState:'closed'},photoGateOpened(o)]:[o]);
'''
s=s.replace(marker,addon+marker.replace('of DATA.objects','of photoGateRenderObjects'),1)
s=s.replace("?'roof':'body');if(!groups.has(key))", "?'roof':'body')+(o.photoGateState?'|photo-'+o.photoGateState:'');if(!groups.has(key))",1)
s=s.replace("roof:key.endsWith('|roof'),buffer:b", "roof:key.endsWith('|roof'),photoGateState:key.endsWith('|photo-open')?'open':key.endsWith('|photo-closed')?'closed':null,buffer:b",1)
s=s.replace("function visible(b){return !hidden.has(b.layer)", "function visible(b){return (!b.photoGateState||b.photoGateState===(photoGateOpen?'open':'closed'))&&!hidden.has(b.layer)",1)
s=s.replace("const shadowKey=String(evening)+String(cutaway)+", "const shadowKey=String(photoGateOpen)+String(evening)+String(cutaway)+",1)
a=s.index('function ensureWalkPhysics(){');b=s.index('\nfunction ',a+8);part=s[a:b].replace('for(const o of DATA.objects)', 'for(const original of DATA.objects){const o=photoGateOpen&&original.photoLeaf?photoGateOpened(original):original;').replace("original;{if(","original;if(")
# The replacement supplies the existing loop's brace.
assert 'original;if(' in part
s=s[:a]+part+s[b:]
button='''
const photoGateButton=document.createElement('button');photoGateButton.id='photoGateToggle';photoGateButton.textContent='Open gates 1–2';photoGateButton.setAttribute('aria-pressed','false');document.getElementById('cutaway').before(photoGateButton);photoGateButton.onclick=()=>{photoGateOpen=!photoGateOpen;photoGateButton.textContent=photoGateOpen?'Close gates 1–2':'Open gates 1–2';photoGateButton.setAttribute('aria-pressed',String(photoGateOpen));walkPhysicsReady=false;walkGrid.clear();walkFloors.clear();lastShadowKey='';dirty=true};
'''
pos=s.index('// Vehicle-mounted first-person')
s=s[:pos]+button+s[pos:]
p.write_text(s,encoding='utf-8')
