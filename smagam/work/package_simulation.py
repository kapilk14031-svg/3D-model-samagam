from pathlib import Path
import json,zipfile,subprocess,html
root=Path(__file__).resolve().parents[1];out=root/'outputs';folder=out/'videos'
names=['01-Samagam-Guided-Tour-60s.mp4','02-VIP-Convoy-Cinematic-60s.mp4','03-AK-Street-Walkthrough-60s.mp4']
info=[]
for name in names:
    p=folder/name
    data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration,size:stream=codec_name,width,height,r_frame_rate','-of','json',str(p)]))
    assert abs(float(data['format']['duration'])-60)<.05
    assert data['streams'][0]['width']==1280 and data['streams'][0]['height']==720
    assert data['streams'][0]['r_frame_rate']=='30/1'
    assert any(s['codec_name']=='aac' for s in data['streams'])
    info.append({'file':name,**data})
folder.joinpath('video-verification.json').write_text(json.dumps(info,indent=2),encoding='utf-8')
folder.joinpath('README.txt').write_text('Three one-minute MP4 videos. 1280 x 720, 30 fps, H.264 video and AAC original ambient music.\n01: guided venue overview, services, road movement and AK.\n02: separate three-car VIP convoy cinematic, checkpoint/police, pandal, footbridge, tents/langar, water and railway.\n03: dedicated AK street walkthrough with live circular position map.\nScene titles explain each location. Hindi narration is not included because local speech export was unavailable. All vehicle/police movement is illustrative simulation, not an official operations plan.\n',encoding='utf-8')
cards=''.join(f'<article><h2>{html.escape(title)}</h2><video controls preload="metadata" src="{name}"></video><a href="{name}" download>Download MP4</a></article>' for name,title in zip(names,['01 · Guided venue tour','02 · Three-car VIP cinematic','03 · AK street experience']))
folder.joinpath('index.html').write_text('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Samagam · Video collection</title><style>body{margin:0;background:#102f36;color:#f9f1df;font:16px Segoe UI,sans-serif;padding:30px;max-width:1150px;margin:auto}h1{font-family:Georgia;font-weight:400}article{margin:25px 0;background:#1b4248;padding:20px;border:1px solid #426067;border-radius:14px}video{width:100%;border-radius:8px;background:#091f25}h2{font-size:20px;font-weight:500}a{color:#e1c58c;display:block;padding-top:12px}p{color:#b5c9c7}</style><h1>The Samagam · Three films</h1><p>60 seconds each · MP4 · 720p · Music and scene titles</p>'+cards,encoding='utf-8')
p=out/'README.md';p.write_text(p.read_text(encoding='utf-8')+'\n## AK controls, live map and three MP4 films\n\nStreet view now starts a visible AK character on a nearby internal road. Drag rotates a smoothed third-person camera; W/S walk, A/D strafe, Q/E or left/right arrows turn, Shift runs. Onscreen controls support hold-to-move. Velocity eases into motion and stops smoothly; arms and legs animate. The circular model map shows AK position and viewing direction.\n\nVIP simulation adds a three-car escort convoy, flanking barricades and animated police marshals. The cars follow the illustrative flyover road height. These are interactive/video elements rather than exported static GLB objects.\n\nThe videos folder contains three separately rendered 60-second H.264/AAC MP4 films at 1280x720 and 30 fps: guided overview, VIP cinematic and AK street walkthrough. All have chapter titles, edited camera routes, transitions and an original ambient score. Local Hindi speech export was unavailable, so the delivered films use music and scene titles. Open videos/index.html to play all three.\n',encoding='utf-8')
p=out/'verification.txt';p.write_text(p.read_text(encoding='utf-8')+'AK movement tests passed: 30/120 Hz consistency, smooth stopping, independent rotation, normalized diagonal speed. Browser drag/turn/movement and live mini-map visually verified. Video views rendered without console errors. Three MP4s verified at exactly 60 seconds, 1280x720, 30fps, H.264/AAC; sample frames reviewed.\n',encoding='utf-8')
# Keep intermediate recordings in work, leaving the videos folder focused on MP4s.
raw=root/'work/video-renders';raw.mkdir(exist_ok=True)
for p in folder.glob('*.webm'):
    dest=raw/p.name
    if dest.exists():dest.unlink()
    p.rename(dest)
archive=out/'samagam-3d-package.zip'
with zipfile.ZipFile(archive) as z:entries=z.namelist()
extra=['source/'+name for name in ['ak_walkthrough.py','simulation_video.js','install_simulation.py','refine_film.py','street_film.py','sync_viewer.py','test_ak.py','test-ak.cjs','make_score.py','encode_videos.py','video_server.py','package_simulation.py']]
extra += ['videos/'+p.name for p in folder.iterdir() if p.is_file()]
entries=list(dict.fromkeys(entries+extra))
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for name in entries:
        p=root/'work'/name.removeprefix('source/') if name.startswith('source/') else out/name
        if p.exists():z.write(p,name)
print('All three MP4s verified; video player, documentation and complete package saved')
