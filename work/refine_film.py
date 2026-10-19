from pathlib import Path
import json
root=Path(__file__).resolve().parents[1];p=root/'work/viewer-pdf.html';s=p.read_text(encoding='utf-8')
s=s.replace('<button id="recordFilm"', '<button id="recordMovie" class="smallbutton">Record VIP cinematic film</button><button id="recordFilm"',1)
s=s.replace('let simulationOn=false,simTime=0,filmRecording=false',"let filmMode='guided';let simulationOn=false,simTime=0,filmRecording=false",1)
s=s.replace('p:[a[0]+dx*t,1.2,a[2]+dz*t]', 'p:[a[0]+dx*t,roadLevel(a[2]+dz*t),a[2]+dz*t]')
pos=s.index('function pathPose(')
s=s[:pos]+'''function roadLevel(z){const u=1000-z/1.4;return 1.2+10*Math.max(0,Math.min(1,(u-913)/48,(1252-u)/50))}
'''+s[pos:]
s=s.replace("index===2?'#161e27'", "index===1?'#101925'")
s=s.replace('for(let i=0;i<5;i++){const d=convoyProgress-i*22', 'for(let i=0;i<3;i++){const d=convoyProgress-i*22')
s=s.replace('i===0||i===4','i===0||i===2')
# Make police checkpoints prominent from the low cinematic camera.
s=s.replace("simMesh(out,'box',[270.5,2.1,z],[15,.95,.5]", "simMesh(out,'box',[270.5,2.7,z],[15,1.2,.5]")
pos=s.index('function filmCamera(t)')
shots='''const movieShots=[
{start:0,end:5,title:'VIP MOVEMENT · THE SAMAGAM',sub:'A three-car escort convoy · Bhodwal Majri · Illustrative simulation',target:[200,0,150],d:[1500,1000],y:[.65,.9],e:[.9,.7]},
{start:5,end:15,title:'THREE-CAR VIP CONVOY',sub:'Lead escort · VIP vehicle · Rear escort',target:null,d:[105,85],y:[.9,1.55],e:[.38,.3]},
{start:15,end:23,title:'POLICE CHECKPOINT & CONTROL',sub:'Gate 2 arrival · Open driving lane · Barricades and working marshals',target:[277,4,137],d:[110,100],y:[1.1,.2],e:[.35,.28]},
{start:23,end:31,title:'THE MAIN PANDAL',sub:'Single curved canopy · Black steel structure · VIP access and parking',target:[180,9,310],d:[520,420],y:[.9,.35],e:[.72,.5]},
{start:31,end:38,title:'FOOT-OVERBRIDGE & HIGHWAY',sub:'S04 pedestrian crossing · P5 parking · Multi-angle road view',target:DATA.meta.s04_footbridge.anchor,d:[270,200],y:[.4,1.35],e:[.62,.36]},
{start:38,end:45,title:'TENTS, LANGAR & RESIDENTIAL GROUNDS',sub:'Colour-coded accommodation · Service roads · Dining facilities',target:[-320,4,130],d:[1050,850],y:[.4,.9],e:[1,.75]},
{start:45,end:51,title:'WATER SUPPLY INFRASTRUCTURE',sub:'Raised supply tank · Ground buffer tanks · Maintenance access',target:DATA.meta.water_supply.anchor,d:[135,110],y:[.45,1.4],e:[.46,.33]},
{start:51,end:60,title:'RAILWAY CONNECTION',sub:'Bhodwal Majri station · Passenger train · Venue transport context',target:[-875,4,-20],d:[430,290],y:[1.3,1.7],e:[.58,.35]}
];
'''
s=s[:pos]+shots+s[pos:]
s=s.replace("const idx=Math.max(0,t>=60?7:filmShots.findIndex(s=>t>=s.start&&t<s.end)),shot=filmShots[idx<0?7:idx]", "const shots=filmMode==='cinematic'?movieShots:filmShots;const idx=Math.max(0,t>=60?7:shots.findIndex(s=>t>=s.start&&t<s.end)),shot=shots[idx<0?7:idx]")
s=s.replace('streetMode=t>=48;',"streetMode=filmMode==='guided'&&t>=48;")
s=s.replace("c.fillText('The Samagam Atlas',640,321)","c.fillText(filmMode==='cinematic'?'VIP Arrival · The Samagam':'The Samagam Atlas',640,321)")
s=s.replace('async function recordFilm(){',"async function recordFilm(mode='guided'){filmMode=mode;")
s=s.replace("link.download='samagam-guided-60s.webm'", "link.download=filmMode==='cinematic'?'samagam-vip-cinematic-60s.webm':'samagam-guided-60s.webm'")
s=s.replace("'http://127.0.0.1:8767/video'", "'http://127.0.0.1:8767/'+(filmMode==='cinematic'?'cinematic':'video')")
s=s.replace("document.getElementById('recordFilm').onclick=recordFilm;", "document.getElementById('recordFilm').onclick=()=>recordFilm('guided');document.getElementById('recordMovie').onclick=()=>recordFilm('cinematic');")
p.write_text(s,encoding='utf-8')
out=root/'outputs';old=(out/'samagam-3d.html').read_text(encoding='utf-8');shapes=old.split(',SHAPES=',1)[1].split(';\nconst canvas',1)[0]
s=s.replace('__SCENE__',json.dumps(json.loads((out/'scene-data.json').read_text(encoding='utf-8')),separators=(',',':'))).replace('__SHAPES__',shapes)
(out/'samagam-3d.html').write_text(s,encoding='utf-8');(root/'work/viewer-check.js').write_text(s.split('<script>',1)[1].split('</script>',1)[0],encoding='utf-8')
print('Three-car convoy with flyover height following and separate cinematic shot list installed')
