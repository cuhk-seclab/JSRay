import json

script = {}
with open("self.log", "r") as f:
    for line in f.readlines():
        if line.strip() == "":
            continue
        l = json.loads(line)
        domain = l["domain"]

        if domain not in script:
            script[domain] = {}
        script[domain][l["hash"]] = 1

rank = {}
for k, v in script.items():
    rank[k] = len(v)

rank = sorted(rank.items(), key=lambda item: item[1], reverse=True)
print(rank[0:10])
