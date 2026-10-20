# Police deployment controls

Open samagam-3d.html and choose Duty deployment.

- Machaan, Morcha, QRT, rider, patrol car ya officer ke **3D body par click** karein: duty card khulega.
- Body par left mouse button daba kar drag karein: position badlegi aur local draft save hoga. Chhota icon bhi drag kar sakte hain.
- Moving rider/car drag ke dauran rukta hai; release par uska poora assigned route nayi position par shift hokar resume hota hai.
- Camera pan ke liye khaali ground drag karein; object ke upar Shift/right-drag camera ka alternate control hai.
- Officer card mein assigned naam, rank, role, shift aur duty dikhti hai. Naam na diya ho to Name not assigned dikhega.
- Edit officer / duty → staff field: Name | Rank | Role | Shift | Contact, har officer alag line mein. Save ke baad Create individual staff icons se alag clickable officer models banayein.
- Add, duplicate, delete, Undo, numeric X/Y/Z, rotation aur scale panel mein hain. Place on model se point select karke shift karein.
- Rider/QRT/patrol ke liye Draw route → model par points → Finish route. Speed aur loop/return editable hain.
- Models/icons, har model type, animation aur shift ke toggles diye hain.
- JSON export/import se backup aur transfer; CSV se shift-wise review. Browser ka local draft usi browser mein rehta hai.

Supplied roster ke 162 records retained hain. 33 off-site/unconfirmed points unplaced hain; panel se location dein. Main force, women subset, separate incharge aur extra staff alag fields hain. Unknown numbers/shifts blank hain. QRT-4 night incharge aur duplicate A-14 ki uncertainty notes mein retained hai. Positions conceptual hain. New routes manually assign karne hain; source mein na diye routes invent nahi kiye.

Static GLB mein dynamic deployment/interiors nahi hain; interactive HTML mein ye features available hain.

## Simple controls update
Choose a duty, then Place / Move on map. Click a model or pictogram for its small duty card. New duty opens a short object picker. The focused editor hides the full list; All duties returns to search. Strength, shift timing, coordinates, full staff and backup controls are collapsed. The first officer name/rank can be edited directly.

For rider, QRT or patrol car: Draw / change path, click road points, Start movement. Movement turns on automatically, and the camera opens at the vehicle. Speed/return/loop remain under route settings. All three use the same tested route animation. Native browser verified a patrol car moving along its assigned route, with a matching moving car icon; the temporary test model was removed.

## Point-first deployment
Duty deployment opens the panel and activates placement on the model. Click a place → choose the duty/model. Officer, barricade, Naka, Machaan and Morcha appear at that place as an unsaved preview. QRT, rider and patrol ask for a path; the clicked location is the first point. Add route points and choose Preview movement. Save changes commits the deployment to the local plan; Cancel draft restores the previous plan. Existing objects remain clickable and draggable. Edit details, delete and change position/path are available after saving; changing a position/path also previews before Save changes. The panel keeps the searchable supplied roster, advanced force fields and backups.

Native verification: static placement, explicit Save and reload persistence, later deletion; QRT route request, animated preview and cancel without persistence. Temporary test deployments removed.

## Officer click and bridge alignment — 20 October 2026
Original deployment icons retained; no extra officer-icon overlay. Directly click an officer body at Morcha, parking, Naka, gate, chowki, traffic or other deployed duty to open information. The card shows duty location, point, type, work, shift, name, rank and mobile. Unprovided names and numbers remain Not assigned. Name, rank, mobile, work and location are editable; existing illustrative officers have a separate local identity record, included in JSON export/import, without increasing planned force counts.

S04 footbridge is perpendicular to the local NH44 segment and centred on its axis. Span reduced from 60 to 42.5 illustrative model units, stair landings narrowed to 6 units. Stairs stay outside the 36-unit carriageway; the venue-side landing stays within the frontage wall clearance. Bridge/stair elevations and AK walking remain coordinated. Static GLB and interactive scene rebuilt.

Verified in native browser: no duplicate officer icons, Morcha officer body click, saved name/mobile/work shown in the card (test data undone), editable fields, corrected bridge view, no console errors. Geometry checks verify centre/orientation/lane/wall clearance; AK stair and full-crossing tests pass.

## Movement and nearby icons — 20 October 2026
Click a moving deployed model or its original icon once to pause; click again to resume from the same route position. The duty card displays Paused / Moving and also offers a Pause / Resume button. This applies to rider, QRT, patrol, foot patrol, ambulance and fire-vehicle routes. Static models only open their details. Pause is a runtime control; reloading restarts normal route playback.

Wide overview shows all applicable icons in view. Close views automatically limit icons to the area around the camera focus; AK street view limits them to nearby positions. No duplicate officer-icon layer is added. Officer bodies remain directly clickable even when distant duty icons are hidden.

Verification: native isolated patrol check confirmed click → Paused with unchanged icon position, second click → Moving with changed position. Main venue overview showed 128 icons, bridge close view 9 nearby icons. Unit tests covered pause/resume for six types, smooth route continuation, relocation while paused, static models, overview/zoom/street proximity. Temporary test drafts were not saved.

## Rider / QRT / patrol camera views — 20 October 2026
Click a deployed rider, QRT or patrol car (or its icon), then choose FPV view or Third-person view in its duty card. FPV looks from rider/driver height along the route; the selected vehicle body is hidden in FPV to keep the view clear. Third person follows behind the visible bike/car. Camera position and turns are smoothed.

Inside vehicle view: drag to look around, scroll or +/− to zoom, switch FPV / Third person, Pause / Resume, Reset camera, Exit vehicle view or Esc. The scene fits the available screen height. Entering a vehicle view resumes an assigned paused route; switching camera modes preserves the current pause state. With no route, the camera remains mounted at the parked vehicle and shows No route. Draw a route to enable movement. Exiting restores the previous model camera.

Verification: native camera-option card on the real QRT-1; isolated production-code checks of FPV and third person for rider, QRT and patrol; drag look-around/reset; Pause and camera-switch pause preservation; Exit restores normal view. No console errors. Unit checks cover vehicle/heading camera transforms, zoom, route displacement, short-angle smoothing; existing click-picking, pause/resume and nearby-icon regressions pass. Verification fixtures used a separate local-storage key; the user deployment plan was preserved.
