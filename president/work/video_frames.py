from pathlib import Path
import subprocess,json,shutil
from PIL import Image,ImageOps,ImageDraw
ff=Path(shutil.which('ffmpeg')); probe=ff.with_name('ffprobe.exe')
files=sorted(Path('work/references').glob('*.mp4'))
sheet=Image.new('RGB',(1050,220*len(files)),'white');draw=ImageDraw.Draw(sheet)
for i,f in enumerate(files):
    result=json.loads(subprocess.check_output([str(probe),'-v','quiet','-show_format','-of','json',str(f)]))
    duration=float(result['format']['duration'])
    print(f.name,round(duration,1),'seconds')
    for j,t in enumerate([.15,.5,.85]):
        dest=Path(f'work/video-{i+1}-{j+1}.jpg')
        subprocess.run([str(ff),'-v','error','-y','-ss',str(duration*t),'-i',str(f),'-frames:v','1','-vf','scale=340:190:force_original_aspect_ratio=decrease',str(dest)],check=True)
        im=Image.open(dest);sheet.paste(im,(j*350,i*220));draw.text((j*350+4,i*220+193),f'Video {i+1} / {round(duration*t,1)} sec',fill='black')
sheet.save('work/video-contact.jpg')
