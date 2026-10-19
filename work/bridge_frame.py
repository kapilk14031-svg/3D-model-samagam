from pathlib import Path
p=Path(__file__).with_name('viewer-v2.html');s=p.read_text(encoding='utf-8').replace('p.distance=Math.max(290,245/aspect)','p.distance=Math.max(245,215/(sceneEl.clientWidth/sceneEl.clientHeight))').replace('min="350" max="3600"','min="130" max="5500"')
p.write_text(s,encoding='utf-8')
