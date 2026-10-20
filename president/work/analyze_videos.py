from pathlib import Path
import subprocess,json,shutil,math
from PIL import Image,ImageOps,ImageDraw
root=Path(__file__).resolve().parents[1]; ff=Path(shutil.which('ffmpeg'));probe=ff.with_name('ffprobe.exe')
dest=root/'work/video-review';dest.mkdir(exist_ok=True); records=[]; frames=[]
for i,f in enumerate(sorted((root/'work/references').glob('*.mp4'))):
    meta=json.loads(subprocess.check_output([str(probe),'-v','quiet','-show_format','-show_streams','-of','json',str(f)]))
    duration=float(meta['format']['duration']);vd=dest/f'video-{i+1:02d}';vd.mkdir(exist_ok=True)
    subprocess.run([str(ff),'-v','error','-y','-i',str(f),'-vf','fps=1/2,scale=640:400:force_original_aspect_ratio=decrease','-q:v','3',str(vd/'frame-%03d.jpg')],check=True)
    # Include first and last views as well as dense temporal coverage.
    for label,t in [('start',0),('end',max(0,duration-.2))]:
        subprocess.run([str(ff),'-v','error','-y','-ss',str(t),'-i',str(f),'-frames:v','1','-vf','scale=640:400:force_original_aspect_ratio=decrease',str(vd/f'{label}.jpg')],check=True)
    items=[(vd/'start.jpg',0)]+[(p,1+2*j) for j,p in enumerate(sorted(vd.glob('frame*.jpg')))]+[(vd/'end.jpg',duration-.2)]
    frames.extend([(i+1,p,t) for p,t in items]); records.append({'video':i+1,'file':f.name,'durationSeconds':duration,'reviewFrames':len(items),'coverage':'every 2 seconds plus start/end; visual review only'})
for page in range(math.ceil(len(frames)/20)):
    canvas=Image.new('RGB',(1440,1100),'#eeeae3');draw=ImageDraw.Draw(canvas)
    for j,(vid,p,t) in enumerate(frames[page*20:(page+1)*20]):
        x=j%4*360;y=j//4*220;im=ImageOps.contain(Image.open(p),(350,192));canvas.paste(im,(x+(350-im.width)//2,y));draw.text((x+5,y+196),f'V{vid}  {t:.1f}s  {p.stem}',fill='black')
    canvas.save(dest/f'review-{page+1:02d}.jpg',quality=88)
(dest/'inventory.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print(len(frames),'frames;',math.ceil(len(frames)/20),'review sheets');print(json.dumps(records,indent=2))
