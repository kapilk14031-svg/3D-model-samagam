import json

with open("79-th-nirankari-sant-samagam-bhodwal/smagam/outputs/scene-data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

gps_objs = [o for o in data["objects"] if "gps" in str(o.get("featureId", "")).lower() or "gps" in str(o.get("name", "")).lower()]
print(f"Total GPS objects: {len(gps_objs)}")
kinds = {}
layers = {}
for o in gps_objs:
    k = o.get("kind", "unknown")
    l = o.get("layer", "unknown")
    kinds[k] = kinds.get(k, 0) + 1
    layers[l] = layers.get(l, 0) + 1

print("Kinds:", kinds)
print("Layers:", layers)
print("Sample object:", gps_objs[0])
