from pathlib import Path
import json
root=Path(__file__).resolve().parents[1];p=root/'work/viewer-pdf.html';s=p.read_text(encoding='utf-8')
s=s.replace('<button id="recordMovie"','<button id="recordStreet" class="smallbutton">Record AK street film</button><button id="recordMovie"',1)
pos=s.index('function filmCamera(t)')
shots='''const streetShots=[
{start:0,end:8,title:'AK · THE STREET EXPERIENCE',sub:'A character-led journey through the Samagam model',path:[[135,1.3,394],[160,1.3,394]],d:[11,14],y:[1.57,1.9],e:[.24,.4]},
{start:8,end:16,title:'MAIN PANDAL · STREET APPROACH',sub:'Canopy detail · Black steel supports · Parking-side road',path:[[160,1.3,394],[185,1.3,394]],d:[18,24],y:[1.3,.5],e:[.6,.7]},
{start:16,end:24,title:'VIP ENTRANCE & POLICE CHECKPOINT',sub:'Gate 2 · Three-car convoy · Barricades and marshals',path:[[310,1.3,136],[281,1.3,136]],d:[15,19],y:[-1.2,-.4],e:[.35,.5]},
{start:24,end:32,title:'FOOTBRIDGE & NH-44',sub:'Pedestrian crossing · Road alignment · Opposite parking',path:[[380,1.3,240],[380,1.3,216]],d:[16,22],y:[-.8,.6],e:[.35,.55]},
{start:32,end:40,title:'RESIDENTIAL GROUNDS',sub:'Coloured tent rows · Internal roads · Langar-side movement',path:[[-570,1.3,-75],[-540,1.3,-75]],d:[14,20],y:[1.0,2.0],e:[.28,.55]},
{start:40,end:47,title:'WATER SUPPLY · CLOSE-UP',sub:'Elevated tank · Steel tower · Service access',path:[[-229,1.3,-334],[-223,1.3,-344]],d:[13,17],y:[.5,.9],e:[.32,.48]},
{start:47,end:54,title:'STATION & PASSENGER TRAIN',sub:'Bhodwal Majri · Railway-side walking view',path:[[-844,1.3,25],[-846,1.3,5]],d:[15,20],y:[-.8,-1.6],e:[.35,.5]},
{start:54,end:60,title:'YOUR POSITION · YOUR VIEW',sub:'AK · Smooth controls · Live circular position map',path:[[160,1.3,394],[177,1.3,394]],d:[20,42],y:[1.6,4.6],e:[.5,.95]}
];
'''
s=s[:pos]+shots+s[pos:]
s=s.replace("const shots=filmMode==='cinematic'?movieShots:filmShots", "const shots=filmMode==='street'?streetShots:filmMode==='cinematic'?movieShots:filmShots")
s=s.replace("streetMode=filmMode==='guided'&&t>=48", "streetMode=filmMode==='street'||(filmMode==='guided'&&t>=48)")
s=s.replace("if(streetMode){walker=[150+(t-48)*3", "if(streetMode&&filmMode==='street'){walker=shot.path[0].map((v,i)=>v+(shot.path[1][i]-v)*ease);heading=desiredHeading=shot.y[0]+(shot.y[1]-shot.y[0])*ease;pitch=desiredPitch=shot.e[0]+(shot.e[1]-shot.e[0])*ease;followDistance=shot.d[0]+(shot.d[1]-shot.d[0])*ease;actorHeading=Math.atan2(shot.path[1][0]-shot.path[0][0],-(shot.path[1][2]-shot.path[0][2]));moveVX=2;moveVZ=0;gaitPhase=t*7}else if(streetMode){walker=[150+(t-48)*3")
s=s.replace("filmMode==='cinematic'?'VIP Arrival · The Samagam':'The Samagam Atlas'", "filmMode==='street'?'Explore with AK':filmMode==='cinematic'?'VIP Arrival · The Samagam':'The Samagam Atlas'")
s=s.replace("link.download=filmMode==='cinematic'?'samagam-vip-cinematic-60s.webm':'samagam-guided-60s.webm'", "link.download=filmMode==='street'?'samagam-ak-street-60s.webm':filmMode==='cinematic'?'samagam-vip-cinematic-60s.webm':'samagam-guided-60s.webm'")
s=s.replace("filmMode==='cinematic'?'cinematic':'video'", "filmMode==='street'?'street':filmMode==='cinematic'?'cinematic':'video'")
s=s.replace("document.getElementById('recordMovie').onclick=()=>recordFilm('cinematic');", "document.getElementById('recordMovie').onclick=()=>recordFilm('cinematic');document.getElementById('recordStreet').onclick=()=>recordFilm('street');")
p.write_text(s,encoding='utf-8');out=root/'outputs';old=(out/'samagam-3d.html').read_text(encoding='utf-8');shapes=old.split(',SHAPES=',1)[1].split(';\nconst canvas',1)[0]
s=s.replace('__SCENE__',json.dumps(json.loads((out/'scene-data.json').read_text(encoding='utf-8')),separators=(',',':'))).replace('__SHAPES__',shapes)
(out/'samagam-3d.html').write_text(s,encoding='utf-8');(root/'work/viewer-check.js').write_text(s.split('<script>',1)[1].split('</script>',1)[0],encoding='utf-8')
print('Dedicated AK street film with eight close-up routes added')
