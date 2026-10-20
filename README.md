# 79th Nirankari Sant Samagam — The Samagam Atlas

Open samagam-3d.html in a WebGL browser. This is an offline interactive 3D artifact; no CDN is required. The adjacent reference image is needed to display the original plan.

## Current edition

The supplied traffic plan (drawing date 14-10-2026) governs internal layout. The venue pin is 29.179636 N, 77.0261412 E. Google Maps provides corridor/location context; the scene is not a Google 3D extraction or a georeferenced survey.

136 indexed source entries include P1–P5, two I-PARKING pockets, O PARKING, two SC parking pockets, pandal, exhibition, offices, langar, toilets, alighting points, gates, roads, printed width annotations, HT towers, railway/station, villages, petrol pump, police chowki, nursery, waste land, parcel outlines, title block and all 11 legend entries. Source annotation near the footbridge is preserved without inventing its surveyed footprint. The local Gate 3 flyover and separate southern underpass replace the former remote flyover candidate in this edition.

## Premium presentation

Cream curved fabric canopies, wine valances, gold trim, roof ribs, representative carpet panels, stage details, planters and lanterns. Navy-and-gold controls, day/evening lighting, orbit/pan/zoom, open roofs and searchable detail register. Choose an ID in the register to focus its position. Architectural styling and representative vehicles do not establish actual event installation designs or quantities.

## Completeness and reading limits

The complete original PDF and a full-page reference image are included. All tiny source print and symbols remain available there. Indexed entries are a reconstruction register, not a guarantee that every blurred character has been deciphered. Some source linework and route arrows are simplified in 3D. Heights, global scale, ramp dimensions and unprinted widths are assumed. Parking capacity and individual residential tent locations/counts cannot be established from this plan.

Review entries:
- B11: LANGAR — Label readable; internal subdivision of shared outline uncertain. Label above S/D office area; shared/adjacent outline retained
- B13: SPECIAL RESIDENCE — Small label; transcription needs review. Small print read visually; check source crop for exact spelling
- B14: TOILET (READING UNCERTAIN) — Very small text; transcription needs review. Narrow service block
- B16: UNCLEAR PLOT LABEL U03 — Unclear label; do not treat transcription as confirmed. Tiny two-line label beside petrol pump; retained as a review item
- B22: PDF SMALL LABEL U01 — Unclear label; retained for review. Tiny two-line label west of northern langar; original pixels preserved
- B23: PDF SMALL LABEL U02 — Unclear label; retained for review. Narrow vertical strip inside eastern service block; original pixels preserved

The two small service-block readings SPECIAL RESIDENCE and TOILET remain tentative; U01/U02/U03 retain unreadable text without guessing. Repeated width labels are indexed by road segment; inspect the source for exact punctuation/units.

## Files

- samagam-3d.html — main interactive viewer
- samagam-schematic.glb — editable geometry
- scene-data.json — objects, labels, route families and metadata
- pdf-detail-register.csv / .json — source detail checklist
- model-inventory.csv — geometry linked to source IDs
- source-traffic-plan.pdf — original supplied PDF
- pdf-reference-plan.jpg — complete visual reference
- samagam-premium-preview.png — rendered current presentation

Older preview and context files outside the current ZIP are superseded by this PDF edition. Routes are reconstructed diagram families, not an operational traffic approval.

## Second visual audit

See pdf-comparison-audit.md for omissions found and corrected, plus remaining source limits. The detail register now contains 136 unique entries.

## Road and facility detail edition

Roads now use continuous joined meshes, road-edge lines, lane separators, shoulders, a raised NH44 median and illustrative roadside lights. The local flyover has a continuous sloped deck, parapets, pier crossheads and deck markings. The traced source centre lines are retained; painted lane details and road equipment are illustrative.

Buildings have plinths, entrances, canopies, eaves, corner trim, glazing or langar ventilation panels. Pandal canopy supports include interior trusses, tie beams, ridge seams and guy lines. Parking uses inset bays, more detailed representative cars/buses and two-wheelers. Vehicle geometry is clipped to parking footprints; quantities are illustrative and are not actual capacities or inventories.

## Height adjustment

User-requested visual height increase: pandal/tent structure +25%, building/toilet/station structures +30%. Footprints and horizontal positions retained. Sloped truss members stretched vertically with endpoints preserved in plan. Heights remain illustrative.

## Ground finish

Empty ground in the interactive viewer now has layered grass, dry turf, exposed soil patches and fine procedural grain. This is illustrative surface styling. Roads, parking and building surfaces keep their materials. The GLB retains a grass-coloured base; the procedural ground shader is part of the HTML viewer.

## Gate decoration and dark roads

All six source gates have illustrative ceremonial pillars, ivory/gold arches, wine fabric trim, lanterns, floral urns and sign boards, oriented across their approaches. Gate numbers/names remain in the source register. Gates have a separate visibility layer and Decorated gates camera. NH44, internal roads and the local flyover deck use darker charcoal surfaces, with lane/edge markings retained. Gate styling is not an approved design or a measured structural drawing.

## Direction palette

Route lines and arrow families now use deeper maroon, blue and green shades at the user request. The legend uses matching shades. Original PDF colour values remain in source_color fields of the detail register, and the original scan is unchanged.

## Current user-requested appearance

- S/D Office: four-floor chocolate-brown facade with separate window rows and floor bands.
- Special Residence: a modern flat-roof building, glazed facade, terrace, pergola and planters.
- Police chowki: red walls and blue roof/entrance detailing; distinct langar roof blocks: dark blue.
- Boundary/parcel walls: three times the former height; the low pandal divider remains unchanged.
- Pandal: golden-brown fabric, warm emission and roof-edge glow. The roof is narrowed by 14% and inset from the highway; its closest corner is 52.31 assumed model units from the NH44 centreline (paved half-width 18).
- Gates: dark orange and warm glow. Dimensions are half of the preceding enlarged gate version (1.5x original decorative gates). Gate 3 is additionally narrowed to clear the police chowki; all decorative parts were checked against that footprint.
- Coloured direction lines/arrows have additive glow, with a Route glow toggle. Pandal glow has a separate toggle. Both are on by default. Exported GLB materials include emission; external viewers need their own bloom to show a halo.

These are user-directed design appearances, not new facts extracted from the PDF. Source uncertainty and relative plan geometry remain documented in pdf-comparison-audit.md. The S/D/LANGAR shared source outline still has uncertain internal division; floor styling does not resolve that drawing ambiguity.

## User-added sleeping camp, petrol-pump styling and VIP access

117 small black sleeping tents were added at the user's request: 48 beside the U01 plinth and 69 beside/behind the northern and middle langar blocks. Walking aisles, ground sheets, guy lines and sleeping mats are illustrative. Tent layout centres are in sleeping-tent-layout.json. Guy-line envelope checks clear traced roads, walls and occupied building/parking polygons. Counts describe this proposed model, not actual installed tents or capacity. Sleeping tents have a separate visibility layer and camera.

The petrol pump now has a user-requested IndianOil-style orange/white canopy, kiosk, dispensers and sign. The PDF only identifies PETROL PUMP; IndianOil is user-requested branding, not independently verified operator information.

The PDF explicitly shows Invited Guests / V.I.P. Parking and green route family L11, along with I-PARKING pockets. It does not explicitly name a VIP gate. A separate user-proposed VIP access gate was added at the I-PARKING approach near Gate 2, with a visible PROPOSED label. Representative parked cars were cleared from the immediate opening. This does not rename Gate 2 or make it exclusively VIP.

## Current edition — 19 October 2026

This section supersedes the earlier black-tent and amusement proposals described above.

The user supplied a 560 x 759 image of the **75th Nirankari Sant Samagam accommodation plan**. Its compact tent rows, lanes and pink/blue/green block markings are adapted as a **user-proposed accommodation concept** around the retained 79th traffic-plan geometry. Original image and a rotated reading copy are included. Exact legacy allocations are not recoverable from this resolution, and the reference is a different event/year. Only readable Ground B, Ground C and Ground D names are used. Tent IDs are model IDs, not official allocation numbers.

Black sleeping tents and the R18 amusement rides have been replaced by ivory residential tent blocks, including the former ride parcel and additional vacant rear parcels. Existing roads, parking, main pandal, buildings, rail and source wall/gate clearances are reserved. Roof-to-wall/gate intersections were checked and corrected.

P5 now has an approximate parking area on the opposite side of NH44, with representative bays, cars/buses and local access. The PDF gives P5 as a textual annotation near the foot-overbridge/local bus stop, without a boundary polygon. The displayed area and local lane are schematic, not a surveyed parking limit. An official event-page search did not supply a P5 boundary; no unsupported boundary claim is made.

A highway frontage wall has been added on the venue side. Total wall height is half the current main gate height, including coping; six gaps reserve four gate approaches and two additional access points. This is user-requested geometry, not a newly discovered source boundary.

The northern langar block, U01 plinth, associated stepped boundary and two HT-line symbols were aligned again against enlarged source crops. Accommodation placement was re-fitted after those corrections.

The Bhodwal Majri station has a detailed dark-brown facade, platform-side canopy, entrance, windows, benches and nameboards; rail/sleepers are dark brown. Architecture and dimensions remain illustrative.

**Current residential module count: 2600.** This describes this proposed model, not actual installed tents, beds or capacity.

Coverage re-check: seven additional interior parcel groups now contain residential rows, including the diagonal-road triangle, central parcels, rear langar parcels and northern pocket beside P3. Cross aisles and traced roads, parking, buildings, gates and source walls remain reserved. Added modules follow the reference colour treatment; no unreadable allocation names were invented.


## Interactive navigation

Street view: press Street view, then click a road or open area in the overhead map. Drag to look around at a fixed illustrative eye height; W/A/S/D, keyboard arrows, onscreen arrows, or the mouse wheel move through the model. Choose position relocates the viewpoint; Exit street returns to the map. This is a 3D model walkthrough, not Google Street View photography. It does not simulate collisions or follow elevated flyover decks.

Rectangle zoom: press Rectangle zoom, then drag a rectangle around an area. The selected ground area fills the overhead view with a small margin. The mode ends after a successful selection. Esc cancels. Plus/minus controls also zoom; in street mode they move forward/backward.

Browser checks: street placement, forward movement, exit/return, rectangle drag and resulting zoom rendered successfully without console errors. JavaScript syntax check passed.

## Surface and lighting edition

The interactive viewer adds distance-faded procedural canvas weave/folds, plaster variation, asphalt grain, wood grain, view-dependent glazing, atmospheric sky/clouds, sunlight and haze. Tent entrance support poles and thresholds are actual exported geometry. Textures and sky are viewer shaders, not baked GLB textures. Geometry remains illustrative; this improves visual realism without claiming surveyed construction detail. Street/rectangle controls remain available.

## Surface and lighting edition

The interactive viewer adds distance-faded procedural canvas weave/folds, plaster variation, asphalt grain, wood grain, view-dependent glazing, atmospheric sky/clouds, sunlight and haze. Tent entrance support poles and thresholds are actual exported geometry. Textures and sky are viewer shaders, not baked GLB textures. Geometry remains illustrative; this improves visual realism without claiming surveyed construction detail. Street/rectangle controls remain available.

## Surface and lighting edition

The interactive viewer adds distance-faded procedural canvas weave/folds, plaster variation, asphalt grain, wood grain, view-dependent glazing, atmospheric sky/clouds, sunlight and haze. Tent entrance support poles and thresholds are actual exported geometry. Textures and sky are viewer shaders, not baked GLB textures. Geometry remains illustrative; this improves visual realism without claiming surveyed construction detail. Street/rectangle controls remain available.

## Surface and lighting edition

The interactive viewer adds distance-faded procedural canvas weave/folds, plaster variation, asphalt grain, wood grain, view-dependent glazing, atmospheric sky/clouds, sunlight and haze. Tent entrance support poles and thresholds are actual exported geometry. Textures and sky are viewer shaders, not baked GLB textures. Geometry remains illustrative; this improves visual realism without claiming surveyed construction detail. Street/rectangle controls remain available.

## Surface and lighting edition

The interactive viewer adds distance-faded procedural canvas weave/folds, plaster variation, asphalt grain, wood grain, view-dependent glazing, atmospheric sky/clouds, sunlight and haze. Tent entrance support poles and thresholds are actual exported geometry. Textures and sky are viewer shaders, not baked GLB textures. Geometry remains illustrative; this improves visual realism without claiming surveyed construction detail. Street/rectangle controls remain available.

## Surface and lighting edition

The interactive viewer adds distance-faded procedural canvas weave/folds, plaster variation, asphalt grain, wood grain, view-dependent glazing, atmospheric sky/clouds, sunlight and haze. Tent entrance support poles and thresholds are actual exported geometry. Textures and sky are viewer shaders, not baked GLB textures. Geometry remains illustrative; this improves visual realism without claiming surveyed construction detail. Street/rectangle controls remain available.

## Surface and lighting edition

The interactive viewer adds distance-faded procedural canvas weave/folds, plaster variation, asphalt grain, wood grain, view-dependent glazing, atmospheric sky/clouds, sunlight and haze. Tent entrance support poles and thresholds are actual exported geometry. Textures and sky are viewer shaders, not baked GLB textures. Geometry remains illustrative; this improves visual realism without claiming surveyed construction detail. Street/rectangle controls remain available.

## Surface and lighting edition

The interactive viewer adds distance-faded procedural canvas weave/folds, plaster variation, asphalt grain, wood grain, view-dependent glazing, atmospheric sky/clouds, sunlight and haze. Tent entrance support poles and thresholds are actual exported geometry. Textures and sky are viewer shaders, not baked GLB textures. Geometry remains illustrative; this improves visual realism without claiming surveyed construction detail. Street/rectangle controls remain available.

Pandal roof refinement: subdivided fabric shell with soft sag between supports, tension folds and raised stitched seams; golden-brown styling retained. Ground now uses an earth-brown GLB base and mainly soil/dry-earth shading with sparse grass patches and subdued grit in the viewer. The canopy stays within its previous fitted footprint.

## Surface and lighting edition

The interactive viewer adds distance-faded procedural canvas weave/folds, plaster variation, asphalt grain, wood grain, view-dependent glazing, atmospheric sky/clouds, sunlight and haze. Tent entrance support poles and thresholds are actual exported geometry. Textures and sky are viewer shaders, not baked GLB textures. Geometry remains illustrative; this improves visual realism without claiming surveyed construction detail. Street/rectangle controls remain available.

Ground material refinement: irregular layered loam/dust patches, subdued dry vegetation, close-range mineral grains and pebbles, and filtered distant detail. These are procedural viewer materials, not surveyed land cover or baked GLB textures. Browser rendering and JavaScript syntax verified.

Latest pandal/bridge revision: one continuous curved pandal roof replaces four transverse bays; supporting steel/ribs/trusses are black. S04 has a user-proposed covered pedestrian crossing over NH44, with railings and two stair approaches. Its deck length was halved from 136 to 68 assumed model units and both stair/support assemblies moved to its new ends. Exact bridge dimensions are illustrative, not measured or approved. S04 Foot overbridge opens a dedicated view.

Railway edition: one illustrative locomotive and six passenger coaches are positioned along the traced railway axis beside Bhodwal Majri station. Windows, bogies, wheels, couplings, doors and roof equipment are model geometry. This depicts a stationary illustrative train, not an actual train service or timetable.

Latest pandal/bridge revision: one continuous curved pandal roof replaces four transverse bays; supporting steel/ribs/trusses are black. S04 has a user-proposed covered pedestrian crossing over NH44, with railings and two stair approaches. Its deck length is now 60 assumed model units, reduced from the previous 68 and both stair/support assemblies moved to its new ends. Exact bridge dimensions are illustrative, not measured or approved. S04 Foot overbridge opens a dedicated view.

Water supply: user-proposed cluster in a vacant service parcel near the nursery-side area, with one raised blue supply tank, two ground buffer tanks, braced steel tower, access ladder, tank bands, hatch, pipes and valve. Tank capacities and distribution are illustrative. The pad was checked against source road/wall/facility clearances and residential modules. Water supply tanks opens a dedicated camera.

## AK controls, live map and three MP4 films

Street view now starts a visible AK character on a nearby internal road. Drag rotates a smoothed third-person camera; W/S walk, A/D strafe, Q/E or left/right arrows turn, Shift runs. Onscreen controls support hold-to-move. Velocity eases into motion and stops smoothly; arms and legs animate. The circular model map shows AK position and viewing direction.

VIP simulation adds a three-car escort convoy, flanking barricades and animated police marshals. The cars follow the illustrative flyover road height. These are interactive/video elements rather than exported static GLB objects.

The videos folder contains three separately rendered 60-second H.264/AAC MP4 films at 1280x720 and 30 fps: guided overview, VIP cinematic and AK street walkthrough. All have chapter titles, edited camera routes, transitions and an original ambient score. Local Hindi speech export was unavailable, so the delivered films use music and scene titles. Open videos/index.html to play all three.

Seven distinct 1600x1000 JPG model views are saved in photos/: overview, pandal, footbridge/VIP side, accommodation, water tanks, railway/train and AK street view with live map. Open photos/index.html for the album, or use samagam-7-jpg-photos.zip.


## Walkable venue update — 19 October 2026
Features on the concept map open at their actual positions within the complete venue. Pandal seating/stage/aisle, three langar interiors and the police compound now share the main venue coordinate system. Gates, parking, road points, residential grounds and station remain in that same world. AK can travel between them. Residential tents have real wall panels, open doorways and cots; the station and police building have entrance openings. These illustrative browser interiors are not baked into the static GLB.

Controls: left-drag pans the model. Drag / Pan switches to Rotate model; Shift-drag provides the alternate action. In Street view, drag rotates the camera, W/S moves, A/D strafes, Q/E turns and Shift runs. The destination selector offers facilities and both footbridge stairs. Wheel zoom follows the cursor in the map/orbit view; AK mode adjusts the follow-camera distance. The circular mini-map follows AK.

AK uses a spatial collision grid and a capsule radius to stop at walls, closed building sides, tent panels, parked vehicles and other solid props. Movement slides along obstacles and is subdivided to prevent tunnelling. Simulation cars and barricades are checked when the VIP simulation is enabled. Stair/bridge surfaces control elevation; rails constrain movement. This is an interactive architectural concept, not a game-grade physics or surveyed pedestrian accessibility model.

H03 and H04 underpasses now have open transverse roads, portal columns, retaining walls and an overhead slab, with continuous elevated NH44 approaches. The frontage wall reserves two additional underpass access openings. The footbridge retains its 60-unit span; each stair run is reduced from 48 to 24 assumed units, with shorter landings and more headroom. AK can ascend, cross the deck and descend the opposite stairs.

Route strips are 0.55 units wide, snapped onto road axes and raised just above their surface, including elevated highway sections. Disconnected nearest-road projections are separated rather than drawing lines across parcels. Glow is limited to a narrow 2-unit maximum halo. These are visual route families; the original PDF legend remains the source of traffic-plan content.

Verification: JS syntax; movement smoothness/frame-rate checks; swept wall collision and clearance; both stair ascent/descent; full bridge crossing; 136 source IDs and 2600 tent roofs; route width and continuity checks. Browser verified AK entering a tent, walking the H03 underpass, reaching the bridge deck at 24.6 units, stopping at a rail, and click-drag panning. No browser console errors observed.

Preview: samagam-walkable-venue-preview.jpg and walkthrough-preview/. Earlier photos and MP4 films depict the earlier edition.

## Editable police deployment — 19 October 2026
162 supplied duty records, editable shifts/strength and separate incharges, models, staff identities, routes and local persistence. Directly click a deployed 3D body for its identity/duty card; drag the body to relocate it. Moving vehicle routes translate with the model. Individual staff markers remain included within their parent strength. Unknown names are explicitly unassigned. See deployment-guide.md; samagam-duty-deployment.json is the positioned backup and CSV is the shift review. 33 off-site/unconfirmed records remain unplaced for user positioning.

Machaan, Morcha and barricades have HARYANA POLICE signs. Rider/QRT/patrol routes support animation. NH44 paths now retain a 1.35 CSS-pixel minimum core at overview scales with a restrained glow, above the road surface.

Verified: 162-record seed/count semantics, unknown shift handling, female subset validation, route animation/return/translation, individual-marker counting, 3D ray picking and misses, JavaScript syntax. Native browser verified CRUD, route animation/persistence, icon dragging, direct Machaan body click/drag and Undo; no console errors.

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
