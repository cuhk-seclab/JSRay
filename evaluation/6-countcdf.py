import json

hash = {}
with open("self.log", "r") as f:
    for line in f.readlines():
        if line.strip() == "":
            continue
        l = json.loads(line)
        domain = l["domain"]
        if l["hash"] not in hash:
            hash[l["hash"]] = []
        if domain not in hash[l["hash"]]:
            hash[l["hash"]].append(domain)
whash = {}
for k, v in hash.items():
    if len(v) > 1:
        whash[k] = 1
assert len(whash) == 6262

cnt = 0
with open("self.log", "r") as f:
    for line in f.readlines():
        if line.strip() == "":
            continue
        l = json.loads(line)
        if l["hash"] in whash:
            cnt += 1
print(f"More than more domains script deletion:{cnt}/{cnt/1596796}")
