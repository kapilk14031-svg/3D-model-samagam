# Coordinate alignment — revision 4

The new ZIP contains three Google Earth screenshots with printed geographic
grids. They have no EXIF GPS tags. The displayed graticule, rather than an
assumed screenshot scale, was used to register this revision.

- Datum/frame: WGS84, geographic coordinates in longitude/latitude order.
- Model origin: 76.848831° E, 29.413077° N, the supplied Google Maps place pin.
- Model axes: +X east, +Y up, +Z south; units are metres.
- No surveyed ground altitude is available. Vertical origin and heights remain
  illustrative; they must not be interpreted as absolute elevations.

Forty intersections of displayed one-arcsecond latitude/longitude lines were
used in an affine pixel-to-coordinate fit. Latitude label assignment was checked
against the second, north-up screenshot and a separately displayed Google Maps
coordinate at the lotus pavilion. The fitted pavilion position agrees with that
map point to about one metre. **This checks registration consistency, not
one-metre ground-survey accuracy.** Both sources can share imagery/geolocation
errors, and pixel selection, digitisation and source-image age add uncertainty.

## Changes

The hall envelope and garden were fitted to individually digitised footprints;
the lotus pavilion and gate were anchored to points in the registered image.
Adjacent west roofs, the eastern blue roof, the south rear wing, the southwest
construction block and the small red-roof structure were added or repositioned.
The screenshot-visible roof arrays and light-coloured garden objects are also
represented. Those light objects have unknown function/date and can be toggled.

The main road and core circulation centrelines were redrawn in the same frame.
Road widths, curb/drain construction and detailed gate dimensions still need
field measurement. Extra surrounding land outside the registered crop retains
schematic context status.

White solid scalloped arcade panels now replace the earlier overlapping arch
outlines. Pink columns, white plaster, green-faced lighting niches, name boards
and open white gate leaves follow the ground-photo/video design. Unseen faces,
portraits, obscured wording and interior rooms have not been invented as exact
replicas. Photo-level texture, every architectural detail and a complete room
inventory are not established by these references.

## Compatible outputs

- `gyan-mansarovar-concept.glb`: 3D model with an embedded georeference record
  in `asset.extras`; local metre coordinates, with the origin/axis definition.
- `site-footprints.geojson`: WGS84 footprint polygons, road centrelines and pin.
- `gyan-mansarovar-google-earth.kmz`: Google Earth overlay and footprint traces.
- `registered-satellite-reference.jpg` with `.jgw` and `.prj`: WGS84 raster crop.
- `georeference.json`: calibration controls, transforms and provenance.

Use **Satellite + registered footprints** in the interactive viewer to compare
the digitised outlines with the provided image. Click the reference or a 3D
object to read its estimated WGS84 position. Blue traces indicate core features;
orange traces indicate adjacent blocks; green lines indicate roads.

These outputs support reference review and planning. They do not certify legal
boundaries, structural dimensions, occupancy capacity or that every hidden room,
utility or facility has been recorded.
