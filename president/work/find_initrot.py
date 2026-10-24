with open('79-th-nirankari-sant-samagam-bhodwal/work/deployment.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('initialRotY')
while idx != -1:
    print(text[idx-100:idx+200].encode('ascii', errors='replace').decode('ascii'))
    idx = text.find('initialRotY', idx+1)
