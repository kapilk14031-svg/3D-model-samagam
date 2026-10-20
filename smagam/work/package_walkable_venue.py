from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
from zipfile import ZipFile,ZIP_DEFLATED
import json,math
root=Path.cwd();out=root/'outputs'
# Check that no visual route strip bridges a discontinuity across a parcel.
data=json.loads((out/'scene-data.json').read_text(encoding='utf-8'))
assert len(data['features'])==136
assert len(data['meta']['underpasses'])==2
assert data['meta']['s04_footbridge']['stair_run']==24
assert all(r['width']==.55 and all(math.dist(a,b)<=12.001 for a,b in zip(r['points'],r['points'][1:])) for r in data['routes'])
sheet=Image.new('RGB',(1280,980),'#163b40');draw=ImageDraw.Draw(sheet)
items=[('AK-B01.png','AK IN THE MAIN PANDAL'),('AK-H03.png','OPEN UNDERPASS'),('footbridge.png','SHORTER STAIRS / WALKABLE BRIDGE'),('roads.png','THIN ROAD PATHS / DRAG TO PAN')]
for i,(name,label) in enumerate(items):
 im=Image.open(out/'walkthrough-preview'/name).convert('RGB');im=ImageOps.fit(im,(624,438));x=8+(i%2)*640;y=8+(i//2)*490;sheet.paste(im,(x,y));draw.text((x+8,y+450),label,fill='#f2d59b')
sheet.save(out/'samagam-walkable-venue-preview.jpg',quality=92)
p=out/'README.md';s=p.read_text(encoding='utf-8');a=s.index('## Interactive concept map and close-up scenes');s=s[:a]+'''## Walkable venue update — 19 October 2026
Features on the concept map open at their actual positions within the complete venue. Pandal seating/stage/aisle, three langar interiors and the police compound now share the main venue coordinate system. Gates, parking, road points, residential grounds and station remain in that same world. AK can travel between them. Residential tents have real wall panels, open doorways and cots; the station and police building have entrance openings. These illustrative browser interiors are not baked into the static GLB.

Controls: left-drag pans the model. Drag / Pan switches to Rotate model; Shift-drag provides the alternate action. In Street view, drag rotates the camera, W/S moves, A/D strafes, Q/E turns and Shift runs. The destination selector offers facilities and both footbridge stairs. Wheel zoom follows the cursor in the map/orbit view; AK mode adjusts the follow-camera distance. The circular mini-map follows AK.

AK uses a spatial collision grid and a capsule radius to stop at walls, closed building sides, tent panels, parked vehicles and other solid props. Movement slides along obstacles and is subdivided to prevent tunnelling. Simulation cars and barricades are checked when the VIP simulation is enabled. Stair/bridge surfaces control elevation; rails constrain movement. This is an interactive architectural concept, not a game-grade physics or surveyed pedestrian accessibility model.

H03 and H04 underpasses now have open transverse roads, portal columns, retaining walls and an overhead slab, with continuous elevated NH44 approaches. The frontage wall reserves two additional underpass access openings. The footbridge retains its 60-unit span; each stair run is reduced from 48 to 24 assumed units, with shorter landings and more headroom. AK can ascend, cross the deck and descend the opposite stairs.

Route strips are 0.55 units wide, snapped onto road axes and raised just above their surface, including elevated highway sections. Disconnected nearest-road projections are separated rather than drawing lines across parcels. Glow is limited to a narrow 2-unit maximum halo. These are visual route families; the original PDF legend remains the source of traffic-plan content.

Verification: JS syntax; movement smoothness/frame-rate checks; swept wall collision and clearance; both stair ascent/descent; full bridge crossing; 136 source IDs and 2600 tent roofs; route width and continuity checks. Browser verified AK entering a tent, walking the H03 underpass, reaching the bridge deck at 24.6 units, stopping at a rail, and click-drag panning. No browser console errors observed.

Preview: samagam-walkable-venue-preview.jpg and walkthrough-preview/. Earlier photos and MP4 films depict the earlier edition.
''';p.write_text(s,encoding='utf-8')
with (out/'verification.txt').open('a',encoding='utf-8') as f:f.write('\nWalkable venue: 136 IDs; 2600 tents retained; 2 corrected portals; 24-unit stair runs; .55-unit path strips; path discontinuities separated. Collision, bridge crossing, smooth movement and JS syntax tests passed. Browser: tent doorway, underpass walking, bridge deck height 24.6/rail stop and drag pan verified.\n')
archive=out/'samagam-3d-package.zip'
with ZipFile(archive) as z:members=z.namelist()
new=['samagam-walkable-venue-preview.jpg']+['walkthrough-preview/'+p.name for p in (out/'walkthrough-preview').glob('*.png')]+['source/'+n for n in ['world_facilities.js','walk_physics.js','underpass_details.py','aligned_routes.py','test-walk-physics.cjs','test_walk_physics.py','test_full_crossing.py','test-cursor-zoom.cjs','drag_pan.py']]
with ZipFile(archive,'w',ZIP_DEFLATED) as z:
 for name in dict.fromkeys(members+new):
  path=root/'work'/name[7:] if name.startswith('source/') else out/name
  if path.is_file():z.write(path,name)
print('Route/metadata checks passed; preview, README and complete package refreshed')
