import json

with open("79-th-nirankari-sant-samagam-bhodwal/smagam/outputs/samagam-duty-deployment.json", "r", encoding="utf-8") as f:
    dep = json.load(f)

print("Version:", dep.get("version"))
print("Units count:", len(dep.get("units", [])))
print("Sample unit with GPS:", [u for u in dep["units"] if "gps" in u.get("id", "").lower() or "lat" in u.get("notes", "").lower()][:3])
