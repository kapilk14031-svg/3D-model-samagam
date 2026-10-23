import csv

with open("79-th-nirankari-sant-samagam-bhodwal/smagam/outputs/google-maps-aligned-points.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    print("Header:", header)
    for i, r in enumerate(reader):
        print(f"{i+1:2d}. {r}")
