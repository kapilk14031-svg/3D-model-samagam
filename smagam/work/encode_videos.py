from pathlib import Path
import subprocess,json,sys
root=Path(__file__).resolve().parents[1];folder=root/'outputs/videos'
files={
 'guided':('samagam-guided-60s.webm','01-Samagam-Guided-Tour-60s.mp4','Samagam Atlas - Guided Venue Tour'),
 'cinematic':('samagam-vip-cinematic-60s.webm','02-VIP-Convoy-Cinematic-60s.mp4','Samagam - Three Car VIP Convoy'),
 'street':('samagam-ak-street-60s.webm','03-AK-Street-Walkthrough-60s.mp4','Samagam - AK Street Experience')}
for key in sys.argv[1:] or files:
    source,name,title=files[key]
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(folder/source),'-i',str(root/'work/ambient-score.wav'),'-t','60','-map','0:v:0','-map','1:a:0','-vf','fps=30,tpad=stop_mode=clone:stop_duration=1,eq=contrast=1.025:saturation=0.93','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-af','volume=1.8,afade=t=in:st=0:d=2,afade=t=out:st=57:d=3','-c:a','aac','-b:a','160k','-movflags','+faststart','-metadata','title='+title,'-metadata','comment=Illustrative 3D venue and operations simulation; not an official traffic/security plan. Original ambient score.',str(folder/name)],check=True)
    data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration,size:stream=codec_name,width,height,r_frame_rate','-of','json',str(folder/name)]))
    assert abs(float(data['format']['duration'])-60)<.05
    assert data['streams'][0]['width']==1280 and data['streams'][0]['height']==720
    assert any(s['codec_name']=='aac' for s in data['streams'])
    (root/'work'/('verify-'+key+'.json')).write_text(json.dumps(data,indent=2),encoding='utf-8')
    print(name,': 60 seconds, 1280x720, H.264 + AAC verified',flush=True)
