from pathlib import Path
p=Path(__file__).with_name('viewer-v2.html');s=p.read_text(encoding='utf-8')
s=s.replace('SPATIAL STUDY / VERSION 02','SPATIAL STUDY / EAST CONTEXT')
s=s.replace('<button data-view="parking">Arrival plaza<em>Parking & buses</em></button>', '<button data-view="parking">Arrival plaza<em>Parking & buses</em></button><button data-view="east">Across highway<em>Haldana & fields</em></button>')
s=s.replace('<label class="layer"><span><i></i>Nearby context</span>', '<label class="layer"><span><i style="background:#b0b89a"></i>Across NH-44</span><input type="checkbox" data-layer="east" checked></label><label class="layer"><span><i></i>Nearby context</span>')
old="let vv=verts.map(v=>v.map((q,i)=>o.p[i]+q*o.s[i]-(o.kind==='box'&&i===1?o.s[1]/2:0)));"
new="let vv=verts.map(v=>{let x=v[0]*o.s[0],z=v[2]*o.s[2],a=o.rotY||0;return [o.p[0]+x*Math.cos(a)+z*Math.sin(a),o.p[1]+v[1]*o.s[1]-(o.kind==='box'?o.s[1]/2:0),o.p[2]-x*Math.sin(a)+z*Math.cos(a)]});"
assert old in s;s=s.replace(old,new)
s=s.replace("overview:{target:[0,0,0],yaw:.66,elevation:.88,distance:3150}","overview:{target:[430,0,0],yaw:.30,elevation:.95,distance:3900}")
s=s.replace("const presets={", "const presets={east:{target:[1200,0,-100],yaw:-.55,elevation:.9,distance:2050},")
s=s.replace("if(!show)continue;const p=projected(l.p)","if(!show||hidden.has(l.layer))continue;const p=projected(l.p)")
s=s.replace("Grounds A · B · C · D</b>","Grounds A–D + NH-44 east side</b>")
s=s.replace("No Google imagery or mesh is embedded.","East-side context: Google Maps labels and satellite land cover checked 18 October 2026 show agricultural/open plots, Woodland factory outlet, Two Brother Holding, Singla Farm House, warehouse premises and the Haldana settlement/stadium. Buildings are approximate masses; field parcels and access-road alignments are generalized. No opposite-side event parking is verified. No Google imagery or mesh is embedded.")
p.write_text(s,encoding='utf-8')
