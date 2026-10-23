import urllib.request

url = "http://localhost:8080/samagam-3d.html"
req = urllib.request.Request(url, headers={'Range': 'bytes=0-1000'})
try:
    with urllib.request.urlopen(req) as resp:
        print("HTTP Status:", resp.status)
        print("Content preview:")
        print(resp.read().decode('utf-8', errors='ignore')[:300])
except Exception as e:
    print("Error:", e)
