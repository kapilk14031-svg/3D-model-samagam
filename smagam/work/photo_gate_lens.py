from pathlib import Path
p=Path('work/viewer-pdf.html');s=p.read_text(encoding='utf-8')
s=s.replace("yaw=Math.PI/2;elevation=.035;distance=70;", "yaw=Math.PI/2;elevation=.035;distance=40;",1)
# Keep the whole facade in view while placing the camera ahead of roadside masts.
s=s.replace(":streetMode?1.05:.72", ":streetMode?1.05:sceneEl.classList.contains('photo-gate-view')?1.15:.72")
p.write_text(s,encoding='utf-8')
