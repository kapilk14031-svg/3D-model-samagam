from pathlib import Path
import subprocess,json,zipfile
root=Path(__file__).resolve().parents[1];out=root/'outputs';folder=out/'videos';info=[]
for p in sorted(folder.glob('*.mp4')):
    data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration,size:stream=codec_name,width,height,r_frame_rate','-of','json',str(p)]))
    assert abs(float(data['format']['duration'])-60)<.05
    assert data['streams'][0]['codec_name']=='h264'
    assert data['streams'][0]['width']==1280 and data['streams'][0]['height']==720 and data['streams'][0]['r_frame_rate']=='30/1'
    assert any(s['codec_name']=='aac' for s in data['streams'])
    info.append({'file':p.name,**data})
assert len(info)==3
(folder/'video-verification.json').write_text(json.dumps(info,indent=2),encoding='utf-8')
for p in folder.glob('*.webm'):
    dest=root/'work/video-renders'/p.name
    if dest.exists():dest.unlink()
    p.rename(dest)
archive=out/'samagam-3d-package.zip'
with zipfile.ZipFile(archive) as z:names=z.namelist()
names=list(dict.fromkeys(names+['source/refresh_video_package.py','source/video_contact_sheets.py']))
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for name in names:
        p=root/'work'/name.removeprefix('source/') if name.startswith('source/') else out/name
        if p.exists():z.write(p,name)
print('Three final MP4s verified and complete package refreshed')
