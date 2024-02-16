import json

import matplotlib.pyplot as plt

site = {}
with open("../domains.txt", "r") as f:
    cnt = 1
    for line in f.readlines():
        if line.strip() == "":
            continue
        site[line.strip()] = cnt
        cnt += 1

self_website = [0] * 1000001
with open("../evaluation/self.log", "r") as f:
    for line in f.readlines():
        if line.strip() == "":
            continue
        l = json.loads(line)
        domain = l["domain"]
        self_website[site["https://" + domain]] = 1

x = [0]
y = [0]

step = 100
tot = 0
for i in range(int(1000000 / step)):
    for j in range(step):
        tot += self_website[1 + i * step + j]
    x.append((i + 1) * step)
    y.append(tot)

plt.plot(x, y, color="r")
plt.xlabel("Website Rank")
plt.ylabel("Self-deleting sites")

plt.show()
