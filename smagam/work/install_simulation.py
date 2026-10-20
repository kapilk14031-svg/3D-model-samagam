from pathlib import Path
import json
root=Path(__file__).resolve().parents[1];p=root/'work/viewer-pdf.html';s=p.read_text(encoding='utf-8')
assert 'function recordFilm' not in s
s=s.replace('</style>','''#miniMap{position:absolute;right:16px;bottom:220px;width:176px;height:176px;border-radius:50%;z-index:3;pointer-events:none;box-shadow:0 3px 20px #09232466}#miniMap[hidden]{display:none}#filmStatus{font-size:11px;color:#e9c98b;line-height:1.5;margin:12px 0}#filmStatus a{color:#ffecba}@media(max-width:760px){#miniMap{width:136px;height:136px;bottom:215px;right:10px}}
</style>''',1)
s=s.replace('<div id="akBadge"','<canvas id="miniMap" aria-label="Live circular model map showing AK position" hidden></canvas><div id="akBadge"',1)
s=s.replace('<button id="tour">','<button id="vipSim" aria-pressed="false">VIP simulation</button><button id="tour">',1)
s=s.replace('<div id="status"','<button id="recordFilm" class="smallbutton">Record 60s guided video</button><div id="filmStatus" role="status"></div><div id="status"',1)
s=s.replace('function resize(){const r=', 'function resize(){if(filmRecording)return;const r=')
s=s.replace('if(streetMode)drawAK();drawDirectionGlow();','if(streetMode)drawAK();drawSimulation();drawDirectionGlow();')
s=s.replace('placeAKName();dirty=false','placeAKName();updateMini();dirty=false')
s=s.replace('last=t;updateAK(dt);', 'last=t;if(cinematicTick(t,dt)){requestAnimationFrame(frame);return}updateAK(dt);')
addon=(root/'work/simulation_video.js').read_text(encoding='utf-8')
addon=addon.replace("const idx=filmShots.findIndex(s=>t>=s.start&&t<s.end)","const idx=Math.max(0,t>=60?7:filmShots.findIndex(s=>t>=s.start&&t<s.end))")
addon=addon.replace("MediaRecorder.isTypeSupported('video/webm;codecs=vp9')?'video/webm;codecs=vp9':'video/webm;codecs=vp8'","'video/webm;codecs=vp8'")
s=s.replace('const initial=presets.pandal;',addon+'\nconst initial=presets.pandal;',1)
p.write_text(s,encoding='utf-8')
out=root/'outputs';old=(out/'samagam-3d.html').read_text(encoding='utf-8');shapes=old.split(',SHAPES=',1)[1].split(';\nconst canvas',1)[0]
s=s.replace('__SCENE__',json.dumps(json.loads((out/'scene-data.json').read_text(encoding='utf-8')),separators=(',',':'))).replace('__SHAPES__',shapes)
(out/'samagam-3d.html').write_text(s,encoding='utf-8');(root/'work/viewer-check.js').write_text(s.split('<script>',1)[1].split('</script>',1)[0],encoding='utf-8')
print('Circular position map, VIP/police simulation and guided film controls installed')
