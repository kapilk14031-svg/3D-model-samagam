# 3D Model Projects & Site Studies

This repository contains two distinct 3D geospatial and site-planning projects:

---

## 1. `smagam/` — 79th Nirankari Sant Samagam
- **Title:** The Samagam Atlas & Interactive 3D Venue Model
- **Location:** Bhodwal Majri, Haryana (`29.179636° N, 77.0261412° E`)
- **Key Features:**
  - Full-venue interactive 3D model with day/evening lighting and orbit/walk physics.
  - Complete police duty deployment plan with officer click-cards, patrol routes, and vehicle views.
  - Pandal, langar, residential tent zones, footbridges, NH-44 connectivity, railway station, and parking zones (P1–P5, SC, O-Parking).
  - Main viewer: `smagam/outputs/samagam-3d.html`.

---

## 2. `president/` — Gyan Mansarovar & Proposed VVIP / President Visit Study
- **Title:** Gyan Mansarovar — Satellite & Photo-Informed 3D Architectural Study
- **Location:** Bhodwal Majri / Panipat, Haryana (`29.413077° N, 76.848831° E`)
- **Key Features:**
  - Interactive 3D reconstruction of the Gyan Mansarovar complex (Revision 8).
  - Sculpted Lotus meditation pavilion with curved dome, petal tiers, stairs, and entrance.
  - Main western roofed auditorium, southern residential block with porticos, and surrounding road alignment.
  - Georeferenced footprints (`site-footprints.geojson`, `gyan-mansarovar-google-earth.kmz`, `georeference.json`).
  - Proposed VVIP / President visit layout layer (lounge, medical/support, dining, reception canopy, illustrative parking).
  - Main viewer: `president/outputs/gyan-mansarovar-3d.html` and 3D asset `president/outputs/gyan-mansarovar-concept.glb`.

---

## Repository Structure

```
.
├── README.md               # Repository navigation & overview
├── .gitignore              # Ignored large media, archives, and caches
├── smagam/                 # 79th Nirankari Sant Samagam Atlas & Police Deployment
│   ├── outputs/
│   │   ├── samagam-3d.html
│   │   └── ...
│   └── work/
└── president/              # Gyan Mansarovar 3D Study & VVIP Arrangement
    ├── outputs/
    │   ├── gyan-mansarovar-3d.html
    │   ├── gyan-mansarovar-concept.glb
    │   ├── READ-ME.txt
    │   └── ...
    └── work/
```
