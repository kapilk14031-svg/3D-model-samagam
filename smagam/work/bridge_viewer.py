from pathlib import Path
p=Path(__file__).with_name('viewer-v2.html');s=p.read_text(encoding='utf-8')
s=s.replace('Overbridge<em>NH-44 crossing</em>','Bridge close-up<em>Deck · stairs · railings</em>')
s=s.replace("pointer=null,anim=null,last=0;","pointer=null,anim=null,last=0,bridgeFocus=false;")
s=s.replace("bridge:{target:[640,5,360],yaw:-.9,elevation:.48,distance:330}","bridge:{target:[640,6,365],yaw:.08,elevation:.32,distance:290}")
s=s.replace("const p=presets[view];topView=view==='top';", "const p={...presets[view]};bridgeFocus=view==='bridge';if(bridgeFocus){p.distance=Math.max(290,245/aspect);hidden.delete('bridges');document.querySelector('[data-layer=bridges]').checked=true;document.getElementById('labels').checked=true;canvas.scrollIntoView({block:'center',behavior:'smooth'})}topView=view==='top';")
s=s.replace("if(!show||hidden.has(l.layer))continue;", "if(!show||hidden.has(l.layer))continue;if(l.bridgeDetail&&!bridgeFocus)continue;if(bridgeFocus&&!['bridges'].includes(l.layer)&&!l.text.includes('NH-44'))continue;")
# Hide trees and coloured proposal arrows around the bridge only in its detail
# view. This changes display clarity, never the model geometry or inventory.
s=s.replace("function visible(b){return !hidden.has(b.layer)", "function visible(b){if(bridgeFocus&&['landscape','traffic','pedestrian','emergency'].includes(b.layer))return false;return !hidden.has(b.layer)")
s=s.replace("scene-toolbar>*{pointer-events:auto}","scene-toolbar>*{pointer-events:auto}")
s=s.replace('Grounds A–D + NH-44 east side</b>', 'Grounds A–D + NH-44 east side</b>')
s=s.replace("document.getElementById('selection').style.display='none';dirty=true}", "document.getElementById('selection').style.display='none';document.querySelector('.location b').textContent=bridgeFocus?'NH-44 · pedestrian overbridge':'Grounds A–D + NH-44 east side';document.querySelector('.location').lastChild.textContent=bridgeFocus?'Approximate structure · deck, stairs and railings':'Local schematic · NH-44 / rail corridor';dirty=true}")
p.write_text(s,encoding='utf-8')
