from pathlib import Path
import numpy as np,json,math
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[1]
src=root/'work/new-references/WhatsApp Image 2026-10-20 at 10.21.33 AM (1).jpeg'
im=Image.open(src).rotate(90,expand=True).convert('RGB'); a=np.array(im).astype(float)
gray=a.mean(axis=2); yellow=np.maximum(0,np.minimum(a[:,:,0],a[:,:,1])-a[:,:,2])
def best_line(axis,b0,s0,lo,hi,valid):
    # Maximise thin bright, slightly yellow graticule strokes against neighbours.
    best=(-1,None,None)
    if axis=='v':
        feature=gray-(np.roll(gray,4,1)+np.roll(gray,-4,1))/2
    else:feature=gray-(np.roll(gray,4,0)+np.roll(gray,-4,0))/2
    feature=np.clip(feature,0,90)*(np.clip(yellow/20,.2,1))
    t=np.array(valid)
    for slope in np.linspace(s0-.012,s0+.012,49):
        for b in np.arange(b0-12,b0+12,.5):
            pos=np.rint(b+slope*t).astype(int)
            if axis=='v':scores=feature[t,pos]
            else:scores=feature[pos,t]
            score=np.mean(np.minimum(scores,50))
            if score>best[0]:best=(float(score),float(b),float(slope))
    return best
# Labels assign the seconds values; fitted lines refine the selected pixel paths.
vl={};hl={}
for sec,b in [(52,333),(53,438),(54,543),(55,648),(56,753),(57,858),(58,963),(59,1068)]:
    vl[sec]=best_line('v',b,.04,0,0,list(range(5,215))+list(range(390,700)))
for sec,b in [(50,146),(49,264),(48,383),(47,501),(46,620)]:
    hl[sec]=best_line('h',b,-.04,0,0,list(range(160,690))+list(range(810,1350)))
gcps=[]
for lon,(_,bv,sv) in vl.items():
    for lat,(_,bh,sh) in hl.items():
        # u=bv+sv*v; v=bh+sh*u
        v=(bh+sh*bv)/(1-sh*sv);u=bv+sv*v
        gcps.append([u,v,76+50/60+lon/3600,29+24/60+lat/3600])
x=np.array([[u,v,1] for u,v,_,_ in gcps]);y=np.array([[lon,lat] for _,_,lon,lat in gcps]);fit=np.linalg.lstsq(x,y,rcond=None)[0]
res=x@fit-y
origin=[76.848831,29.413077];phi=math.radians(origin[1]);aa=6378137;e2=6.69437999014e-3
east_per_deg=math.pi/180*aa*math.cos(phi)/math.sqrt(1-e2*math.sin(phi)**2)
north_per_deg=math.pi/180*aa*(1-e2)/(1-e2*math.sin(phi)**2)**1.5
def local(u,v):
    lon,lat=np.array([u,v,1])@fit
    return [(lon-origin[0])*east_per_deg,(origin[1]-lat)*north_per_deg]
out={'source':src.name,'pixelOrientation':'source rotated 90 degrees counterclockwise into 1600x738 north-up working raster','pixelToLonLat':fit.tolist(),'originLongitude':origin[0],'originLatitude':origin[1],'eastMetresPerDegree':east_per_deg,'northMetresPerDegree':north_per_deg,'gridControlPoints':gcps,'fitResidualDegreesRMS':float(np.sqrt(np.mean(res**2))),'verticalGridFits':vl,'horizontalGridFits':hl,'method':'Manual seconds-label assignment; bright thin-line refinement; affine fit of displayed Google Earth graticule. Not a ground survey.'}
lotus_lon,lotus_lat=np.array([840,255,1])@fit
out['coordinateCrossCheck']={'feature':'lotus pavilion centre','googleMapsContextMenu':[76.849105,29.413563],'screenshotFit':[float(lotus_lon),float(lotus_lat)],'differenceMetres':float(math.hypot((lotus_lon-76.849105)*east_per_deg,(lotus_lat-29.413563)*north_per_deg)),'status':'Checks grid-label assignment against Google Maps UI; does not establish ground-survey accuracy.'}
(root/'work/georeference.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
draw=ImageDraw.Draw(im)
for lon,(_,b,s) in vl.items():draw.line([(b,0),(b+s*737,737)],fill='red',width=1)
for lat,(_,b,s) in hl.items():draw.line([(0,b),(1599,b+s*1599)],fill='cyan',width=1)
for u in range(0,1600,50):
    draw.line([(u,0),(u,737)],fill=(255,255,255),width=1)
    draw.text((u+2,16),str(u),fill='red')
for v in range(0,738,50):
    draw.line([(0,v),(1599,v)],fill=(255,255,255),width=1)
    draw.text((450,v+2),str(v),fill='red')
im.save(root/'work/calibration-review.png')
print('Fits:',vl,hl)
print('Approx local coordinates:',{n:local(*p) for n,p in {'hall':[585,400],'pavilion':[840,255],'residential':[750,590],'gate':[685,215]}.items()})
