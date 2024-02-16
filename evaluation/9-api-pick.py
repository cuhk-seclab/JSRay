import glob
import json
import os
import random

blacklist = set()
with open("out.log", "r") as f:
    for line in f.readlines():
        if line.strip() == "":
            continue
        l = json.loads(line)
        domain = l["domain"]
        blacklist.add(domain)

site = set()
for i in glob.glob("../data/log/*.log"):
    site.add(os.path.basename(i).removesuffix(".log"))

site = list(site - blacklist)
print(len(site))

random_seed = 114514  # for reply
random.shuffle(site)
picked = random.sample(site, 226854)

with open("base.txt", "w") as f:
    for i in picked:
        f.write(f"{i}\n")
