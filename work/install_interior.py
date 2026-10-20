from pathlib import Path
root=Path(__file__).resolve().parents[1];p=root/'work/viewer-pdf.html';s=p.read_text(encoding='utf-8')
assert 'function enterPandalInterior' not in s
s=s.replace('function go(view){', "function go(view){if(view==='interior'){enterPandalInterior();return}pandalInterior=false;",1)
s=s.replace('function setConcept(on){conceptMode=on;', 'function setConcept(on){if(on)pandalInterior=false;conceptMode=on;',1)
s=s.replace('function openConcept3D(item){setConcept(false);', "function openConcept3D(item){if(item.category==='pandal'){enterPandalInterior();return}pandalInterior=false;setConcept(false);",1)
s=s.replace("const item=conceptSelected;openConcept3D(item);anim=null;target=[...item.world]", "const item=conceptSelected;openConcept3D(item);pandalInterior=false;anim=null;target=[...item.world]",1)
s=s.replace("document.getElementById('street').onclick=()=>{if(streetMode)", "document.getElementById('street').onclick=()=>{if(pandalInterior){pandalInterior=false;target=[...presets.pandal.target]}if(streetMode)",1)
s=s.replace('if(shadowOK&&shadowKey!==lastShadowKey)', 'if(shadowOK&&!pandalInterior&&shadowKey!==lastShadowKey)',1)
old='drawBuffers(prog,false);if(streetMode)drawAK();drawSimulation();drawDirectionGlow();placeLabels();placeAKName();updateMini();dirty=false'
new="if(pandalInterior){drawPandalInterior();labelNodes.forEach(({el})=>el.style.display='none')}else{drawBuffers(prog,false);if(streetMode)drawAK();drawSimulation();drawDirectionGlow();placeLabels()}placeAKName();updateMini();dirty=false"
assert old in s;s=s.replace(old,new,1)
s=s.replace('elevation=Math.max(.12,Math.min(1.565,elevation+dy*.005))','elevation=Math.max(pandalInterior?-.12:.12,Math.min(1.565,elevation+dy*.005))',1)
addon=(root/'work/pandal_interior.js').read_text(encoding='utf-8');s=s.replace('const initial=presets.pandal;',addon+'\nconst initial=presets.pandal;',1)
p.write_text(s,encoding='utf-8');print('Pandal Open 3D now opens a reference-inspired immersive interior')
