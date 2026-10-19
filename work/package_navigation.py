from pathlib import Path
import zipfile
root=Path(__file__).resolve().parents[1];out=root/'outputs'
inject="image.toBlob(blob=>fetch('http://127.0.0.1:8766/preview',{method:'POST',headers:{'Content-Type':'image/png'},body:blob}).catch(()=>{}));"
p=out/'samagam-3d.html';p.write_text(p.read_text(encoding='utf-8').replace(inject,''),encoding='utf-8')
(out/'samagam-street-view.png').write_bytes((out/'samagam-premium-preview.png').read_bytes())
# Keep the main overview preview consistent with the accommodation edition.
(out/'samagam-premium-preview.png').write_bytes((out/'samagam-residential-reference.png').read_bytes())
p=out/'README.md';s=p.read_text(encoding='utf-8');s+='''

## Interactive navigation

Street view: press Street view, then click a road or open area in the overhead map. Drag to look around at a fixed illustrative eye height; W/A/S/D, keyboard arrows, onscreen arrows, or the mouse wheel move through the model. Choose position relocates the viewpoint; Exit street returns to the map. This is a 3D model walkthrough, not Google Street View photography. It does not simulate collisions or follow elevated flyover decks.

Rectangle zoom: press Rectangle zoom, then drag a rectangle around an area. The selected ground area fills the overhead view with a small margin. The mode ends after a successful selection. Esc cancels. Plus/minus controls also zoom; in street mode they move forward/backward.

Browser checks: street placement, forward movement, exit/return, rectangle drag and resulting zoom rendered successfully without console errors. JavaScript syntax check passed.
''';p.write_text(s,encoding='utf-8')
p=out/'verification.txt';p.write_text(p.read_text(encoding='utf-8')+'Street placement, walking, exit and rectangle-zoom drag checked in the browser; no console errors.\n',encoding='utf-8')
archive=out/'samagam-3d-package.zip'
with zipfile.ZipFile(archive) as z:names=z.namelist()
names=list(dict.fromkeys(names+['samagam-street-view.png','source/add_navigation.py','source/package_navigation.py']))
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for name in names:
        p=root/'work'/name.removeprefix('source/') if name.startswith('source/') else out/name
        if p.exists():z.write(p,name)
print('Navigation documentation, preview and package saved')
