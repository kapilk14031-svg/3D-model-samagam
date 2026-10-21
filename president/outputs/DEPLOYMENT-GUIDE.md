# Police deployment editor

Open the running local viewer: http://127.0.0.1:8794/outputs/gyan-mansarovar-3d.html

To restart later, run `start-deployment.cmd` with Python installed. The server binds only to 127.0.0.1. It stores the plan in `../work/deployment.sqlite3`, outside the downloadable site files. Keep that file when moving/restarting this installation. No external database/cloud synchronization is configured.

## Use

- The handwritten page contains **13 numbered duty entries**. Each has one placeholder officer, with blank belt and mobile fields. This is a draft editing example, not a staffing count or approved positioning plan. VIP toilet/lounge/parking locations and other operational placements are not verified room assignments.
- Choose **Add type → Add & place**, click a floor/road/roof surface, then **Place here**. Cancel dismisses that point; Esc cancels placement. The nearest visible surface is checked: clicks blocked by a tree/wall do not select ground behind it. A blue circle marks the exact selected base point, with leaders connecting displaced labels. A roof click sets base height on that surface. All positions and heights can also be edited numerically.
- Click an officer/equipment icon or its 3D model to select it. **W/A/S/D** move north/west/south/east by 0.25 m; Shift uses 1 m. Text-entry fields keep normal typing. Rotate with ±15° buttons or enter a facing angle (0° north).
- Officers wear dark blue with rounded bodies/limbs, caps, shoulder tabs and belt details. Their visual height is back to approximately 1.8 m (the requested doubled size was reverted). First-person camera height is approximately 1.65 m. Barricades, binoculars, DFMD, HHMD/HFMD, radio, cones, CCTV and search lights have individual 3D representations. Nearby icons separate on screen to stay clickable; their screen labels can be offset from the exact model point.
- Hover over an icon or model for name, belt number, duty and mobile. Click a quick field to edit; leaving it saves. The full editor also saves field changes; Apply changes commits explicitly.
- First person uses an approximate 1.65 m eye height and selected facing. Third person looks from behind the officer. Return to map restores the previous camera. Nearby icons remain selectable. This is a visual check of the simplified model, not a certified visibility analysis.
- Backend status confirms each committed save. Add, deletion, position, rotation, type and detail edits persist in SQLite and reload from it. Pending/failed saves are shown and can be retried. A stale second tab is rejected rather than silently overwriting newer data.
- Export deployment JSON for backup; import restores a compatible plan with the same origin. Browser storage is a fallback when the backend is unavailable; that fallback is explicitly marked and is not a backend save. The embedded chat preview does not connect to this localhost backend.

## Duty labels transcribed into editable fields

1. Outer perimeter duty
2. Binocular duty — rooftop
3. Lotus duty
4. Inner cordon duty
5. Outer cordon duty
6. Main gate — DFMD / HHMD
7. Naka & barricade duty
8. Auditorium main stage duty
9. Auditorium seating duty
10. VIP parking duty
11. VIP toilet duty
12. VIP lounge duty
13. Hall gate duty

Some handwriting is unclear; compare `deployment-reference/duty-note.jpg` and edit the labels as needed. Two barricades, a DFMD, a handheld detector and binoculars are initially shown as draft equipment. Adding a duty does not claim that its building location is verified.

## Validation

Verified in the browser: editing officer fields, reload persistence, map placement confirmation, equipment type/rotation/deletion, W/S officer movement, A/D equipment movement, quick-field editing and both officer camera views. Temporary test entries were removed. Five isolated backend tests cover SQLite persistence, updates/deletion, stale revision rejection, invalid payloads, same-origin checks and JSON headers. Venue geometry regression checks and JavaScript syntax checks passed.

The static venue GLB remains separate; editable deployment is stored in the database / JSON and rendered by this viewer.

Pan sensitivity is 3× the earlier setting (2.4 versus 0.8), with faster damping response.

Icons and leader lines now use camera-to-officer/equipment visibility against opaque walls, roofs, ceilings and other modeled structural solids. Hidden objects can still be selected from the list. Glass and deliberately removed cutaway geometry do not hide labels. The base circle also respects depth. Verified from the hall: only the two interior duty icons remained visible; exterior equipment and rooftop icons were hidden. This visibility is limited to the reconstruction geometry.

Barricades were moved from the gate frontage to the road at both boundary-corner projections (west/east), following the user correction. Their orientations follow the road normal. Saved in backend revision 18; all other deployment items preserved.

Latest display change: deployment markers now show only their small symbol, with no names or leader lines. Hover/click opens a compact editable four-row popup above that icon; equipment omits belt/mobile fields. First/third person and Move remain available in the popup, with other controls in the full editor. Verified in hall view: two plain officer symbols, zero leader-line elements, compact popup above selected officer. Existing backend deployment was preserved.
