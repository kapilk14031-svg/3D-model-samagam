from pathlib import Path
import json,zipfile,html,shutil
import numpy as np
root=Path(__file__).resolve().parents[1];out=root/'outputs'
geo=json.loads((out/'georeference.json').read_text(encoding='utf-8'));gj=json.loads((out/'site-footprints.geojson').read_text(encoding='utf-8'));fit=np.array(geo['pixelToLonLat'])
# World file for the full-resolution cropped JPEG: pixel centres, WGS84 degrees.
c=np.array([150.5,150.5,1])@fit
world=[fit[0,0],fit[0,1],fit[1,0],fit[1,1],c[0],c[1]]
(out/'registered-satellite-reference.jgw').write_text('\n'.join(f'{v:.14f}' for v in world)+'\n',encoding='ascii')
(out/'registered-satellite-reference.prj').write_text('GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433],AUTHORITY["EPSG","4326"]]',encoding='ascii')
def lonlat(u,v):return (np.array([u,v,1])@fit).tolist()
kml=['<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2"><Document><name>Gyan Mansarovar — registered reference study</name><description>Screenshot-graticule registration, not ground survey. Heights and unseen details unverified.</description>']
kml.append('<Style id="core"><LineStyle><color>ffba6d00</color><width>2</width></LineStyle><PolyStyle><fill>0</fill></PolyStyle></Style><Style id="context"><LineStyle><color>ff246bcc</color><width>2</width></LineStyle><PolyStyle><fill>0</fill></PolyStyle></Style>')
corners=[lonlat(u,v) for u,v in [(150,700),(1370,700),(1370,150),(150,150)]]
kml.append('<GroundOverlay><name>Supplied Google Earth screenshot — registered crop</name><visibility>1</visibility><Icon><href>registered-satellite-reference.jpg</href></Icon><gx:LatLonQuad><coordinates>'+ ' '.join(f'{lon},{lat}' for lon,lat in corners)+'</coordinates></gx:LatLonQuad></GroundOverlay>')
for f in gj['features']:
    g=f['geometry'];p=f['properties'];kml.append('<Placemark><name>'+html.escape(p.get('name',f['id']))+'</name><description>'+html.escape(p.get('status','Displayed reference only'))+'</description><styleUrl>#'+('context' if p.get('group')=='context' else 'core')+'</styleUrl>')
    if g['type']=='Polygon':
        coords=g['coordinates'][0];kml.append('<Polygon><altitudeMode>clampToGround</altitudeMode><outerBoundaryIs><LinearRing><coordinates>'+ ' '.join(f'{lon},{lat},0' for lon,lat in coords)+'</coordinates></LinearRing></outerBoundaryIs></Polygon>')
    elif g['type']=='LineString':kml.append('<LineString><tessellate>1</tessellate><coordinates>'+' '.join(f'{lon},{lat},0' for lon,lat in g['coordinates'])+'</coordinates></LineString>')
    else:kml.append('<Point><coordinates>'+','.join(str(x) for x in g['coordinates'])+',0</coordinates></Point>')
    kml.append('</Placemark>')
kml.append('</Document></kml>');doc=''.join(kml)
(out/'gyan-mansarovar-registered.kml').write_text(doc,encoding='utf-8')
with zipfile.ZipFile(out/'gyan-mansarovar-google-earth.kmz','w',zipfile.ZIP_DEFLATED) as z:
    z.writestr('doc.kml',doc);z.write(out/'registered-satellite-reference.jpg','registered-satellite-reference.jpg')
(out/'source-map-references').mkdir(exist_ok=True)
for p in (root/'work/new-references').glob('*.jpeg'):shutil.copyfile(p,out/'source-map-references'/p.name)
shutil.copyfile(Path(r'C:\Users\HP\Pictures\Screenshots\Screenshot 2026-10-20 101847.png'),out/'source-map-references/desktop-satellite-reference.png')
print('GeoJSON features:',len(gj['features']),'pavilion cross-check difference:',geo['coordinateCrossCheck']['differenceMetres'],'m')
