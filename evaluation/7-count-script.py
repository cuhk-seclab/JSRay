import json
from urllib.parse import urlparse, urlunparse

dom = {}
script = {}
with open("self.log", "r") as f:
    for line in f.readlines():
        if line.strip() == "":
            continue
        l = json.loads(line)
        domain = l["domain"]

        src = l["src"]
        if src.startswith("http"):
            path = urlparse(src)
            dm = path.netloc
            path = urlunparse(path._replace(query=""))
            if path not in script:
                script[path] = {}
            script[path][domain] = 1
            if dm not in dom:
                dom[dm] = {}
            dom[dm][domain] = 1

rank = {}
for k, v in script.items():
    rank[k] = len(v)

rank = sorted(rank.items(), key=lambda item: item[1], reverse=True)
print(rank[0:10])

rank = {}
for k, v in dom.items():
    rank[k] = len(v)

rank = sorted(rank.items(), key=lambda item: item[1], reverse=True)
print(rank[0:10])

cnt = 0
site = {}
with open("self.log", "r") as f:
    for line in f.readlines():
        if line.strip() == "":
            continue
        l = json.loads(line)
        domain = l["domain"]

        src = l["src"]
        if "www.googletagmanager.com/gtm.js" in src:
            cnt += 1
        else:
            site[domain] = 1
print(cnt)
print(len(site))
