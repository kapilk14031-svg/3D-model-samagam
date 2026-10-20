from pathlib import Path
import subprocess
root=Path(__file__).resolve().parents[1]
for i,name in enumerate(['01-Samagam-Guided-Tour-60s.mp4','02-VIP-Convoy-Cinematic-60s.mp4','03-AK-Street-Walkthrough-60s.mp4']):
    selection='+'.join('eq(n,'+str(n)+')' for n in [120,330,600,840,1020,1140,1380,1620])
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(root/'outputs/videos'/name),'-vf',"select='"+selection+"',scale=320:180,tile=4x2",'-frames:v','1',str(root/'work'/f'contact-video-{i+1}.jpg')],check=True)
print('Three video contact sheets saved')
