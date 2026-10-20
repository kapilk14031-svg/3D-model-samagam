from pathlib import Path
import json
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8');addon=Path('work/deployment_panel.js').read_text(encoding='utf-8').replace('__DUTY_SEED__',json.dumps(json.loads(Path('work/deployment-seed.json').read_text(encoding='utf-8')),ensure_ascii=False,separators=(',',':')))
pos=s.index('function focusFeature(f)');s=s[:pos]+addon+'\n'+s[pos:]
s=s.replace('drawSimulation();drawDirectionGlow();placeLabels()', 'drawSimulation();drawDeployment();drawDeploymentSigns();drawDirectionGlow();placeLabels();placeDeploymentIcons()',1)
s=s.replace('updateAK(dt);if(anim)', 'updateAK(dt);deploymentTick(dt);if(anim)',1)
s=s.replace('function walkBlockedAt(x,z,y){', 'function walkBlockedAt(x,z,y){if(deploymentCollision(x,z,y))return true;',1)
s=s.replace("small=Math.hypot(e.clientX-pointer.sx,e.clientY-pointer.sy)<5;if(boxMode)", "small=Math.hypot(e.clientX-pointer.sx,e.clientY-pointer.sy)<5;if(small&&deploymentPick(x,y)){pointer=null;return}if(boxMode)",1)
p.write_text(s,encoding='utf-8')
Path('outputs/deployment-supplied-roster.json').write_text(Path('work/deployment-seed.json').read_text(encoding='utf-8'),encoding='utf-8')
