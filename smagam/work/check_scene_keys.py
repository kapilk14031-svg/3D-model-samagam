import json

with open("79-th-nirankari-sant-samagam-bhodwal/smagam/outputs/scene-data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Keys in scene-data.json:", list(data.keys()))
for k in data:
    val = data[k]
    if isinstance(val, list):
        print(f"  {k}: list of length {len(val)}")
        if len(val) > 0 and isinstance(val[0], dict):
            print(f"    sample item keys: {list(val[0].keys())}")
            # check if any item has gps or category
            gps_items = [x for x in val if "gps" in str(x).lower()]
            print(f"    items with 'gps': {len(gps_items)}")
    elif isinstance(val, dict):
        print(f"  {k}: dict with keys {list(val.keys())[:10]}")
