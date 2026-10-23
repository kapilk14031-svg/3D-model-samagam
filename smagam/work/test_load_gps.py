import json
import csv
from pathlib import Path

smagam_dir = Path("79-th-nirankari-sant-samagam-bhodwal/smagam")
points_csv = smagam_dir / "outputs/google-maps-aligned-points.csv"
dep_json = smagam_dir / "outputs/samagam-duty-deployment.json"
viewer_html = smagam_dir / "work/viewer-pdf.html"

# Load 41 points
with open(points_csv, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    pts = []
    for r in reader:
        pts.append({
            "index": int(r.get("\ufeffIndex") or r.get("Index")),
            "category": r["Category"],
            "name": r["Name"],
            "lat": float(r["Latitude"]),
            "lon": float(r["Longitude"]),
            "x": round(float(r["Model_X"]), 2),
            "z": round(float(r["Model_Z"]), 2),
            "url": r["Google_Maps_URL"]
        })

print(f"Loaded {len(pts)} GPS points.")

# Load deployment
with open(dep_json, "r", encoding="utf-8") as f:
    deployment = json.load(f)

print(f"Loaded deployment with {len(deployment.get('units', []))} units.")
