from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8').replace("yaw=Math.PI/2;elevation=.055;distance=100;", "yaw=Math.PI/2;elevation=.035;distance=70;")
p.write_text(s,encoding='utf-8')
