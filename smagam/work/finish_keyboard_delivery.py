from pathlib import Path
import zipfile,shutil
root=Path(__file__).resolve().parents[1];repo=root.parent;out=root/'outputs';delivery=repo/'outputs';work=root/'work'
p=work/'viewer-pdf.html';s=p.read_text(encoding='utf-8');s=s.replace("depEl('depViewThird').onclick=()=>depEnterVehicleView(depFollowState.id,'third');", "depEl('depViewThird').onclick=()=>{if(depFollowState.manual)depEnterObjectControl(depFollowState.id);else depEnterVehicleView(depFollowState.id,'third')};");p.write_text(s,encoding='utf-8')
notes='''
## Smooth controls, deployed-object third person and gate alignment — 22 October 2026

Model navigation: W/S forward/back, A/D strafe left/right, Q/E rotate, K/L zoom in/out, Z/X tilt up/down. Hold keys for smooth acceleration/deceleration; Shift moves faster. Movement follows the viewing direction. Text fields and browser modifier shortcuts are excluded; blur/hidden/focus changes clear held keys. AK retains its existing W/A/S/D walking and collision behavior. The sidebar includes a Keyboard controls guide.

Click a deployed object's icon, body or assigned officer to open its details and third-person control view. W/S move the selected object forward/back; A/D strafe relative to its facing; Q/E rotate it. Space jumps with gravity and returns to the ground without saving a raised height. Caps Lock (or Esc / Exit third person) exits. K/L zoom and Z/X tilt the follow camera; drag looks around. Moving vehicles pause their assigned route during manual placement. Moving/rotating also transforms their route so leaving control does not snap to the old position. Pause/Resume switches back to the existing route-follow mode. Positions save locally when movement settles, on explicit Save position and on exit; Undo remains available in Duty deployment. Jump is temporary and does not alter the saved ground level.

G01/G02 gate centres and angles now follow the highway boundary polyline. The complete photo-style assembly, opening-leaf pivots and labels move together; the wall openings meet the gates' boundary returns. The original printed source coordinates remain in the data for reference. The front-view camera uses each gate's aligned angle. Appearance and heights retain the previous photo design.

Verification: JS syntax; ten navigation keys; diagonal speed and 30/120fps behavior; smooth stopping and limits; form/blur guards; 11 deployment types; route-preserving move/rotate; temporary jump/landing; existing six moving-type pause/resume; 162 duty records and counts; direct model picking; gate alignment and all four open/closed AK collision portals. Native browser verified click-to-third-person, object move/rotate, Space input, Caps Lock exit, saved placement and both gate views, with no console errors. Test fixture uses a separate localStorage key; production duty positions were not changed for testing.
'''
for name in ['README.md','verification.txt']:
 p=out/name;p.write_text(p.read_text(encoding='utf-8')+notes,encoding='utf-8')
(delivery/'KEYBOARD-AND-OBJECT-CONTROLS.md').write_text(notes,encoding='utf-8')
for name in ['KEYBOARD-AND-OBJECT-CONTROLS.md','object-third-person-controls.jpg','gate-1-boundary-aligned.jpg','gate-2-boundary-aligned.jpg']:
 if (delivery/name).exists():shutil.copyfile(delivery/name,out/name)
print('Updated help, controls, delivery notes and preview copies')
