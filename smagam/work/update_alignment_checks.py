from pathlib import Path
root=Path(__file__).parent
p=root/'viewer-pdf.html';s=p.read_text(encoding='utf-8');s=s.replace('target=[item.world[0],10,item.world[2]];yaw=Math.PI/2;elevation=.035','target=[item.world[0],10,item.world[2]];yaw=(item.source?.gateAlignment?.angle??-Math.PI/2)+Math.PI;elevation=.035');p.write_text(s,encoding='utf-8')
p=root/'test_photo_gates.py';s=p.read_text(encoding='utf-8').replace("p=[f['world'][0],0,f['world'][2]+side*15]","a=f.get('gateAlignment',{}).get('angle',-math.pi/2);p=[f['world'][0]+math.cos(a)*side*15,0,f['world'][2]-math.sin(a)*side*15]");p.write_text(s,encoding='utf-8')
p=root/'test_photo_gate_walk.py';s=p.read_text(encoding='utf-8').replace('const x=f.world[0],z=f.world[2]+side*15,y=', 'const a=f.gateAlignment?.angle??-Math.PI/2,x=f.world[0]+Math.cos(a)*side*15,z=f.world[2]-Math.sin(a)*side*15,y=');p.write_text(s,encoding='utf-8')
