import json

with open("79-th-nirankari-sant-samagam-bhodwal/smagam/outputs/scene-data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

gps_nodes = [n for n in data.get("nodes", []) if n.get("id", "").startswith("GPS_") or "GPS" in n.get("id", "")]
print("Total nodes:", len(data.get("nodes", [])))
print("GPS nodes:", len(gps_nodes))

# Check some categories
cats = {}
for n in gps_nodes:
    prefix = n["id"].split("_")[1] if "_" in n["id"] else "other"
    cats[prefix] = cats.get(prefix, 0) + 1

for k, v in sorted(cats.items()):
    print(f"  {k}: {v}")
