import glob
import json
import os

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator

# matplotlib.use("pgf")
# matplotlib.rcParams.update(
#     {
#         "pgf.texsystem": "pdflatex",
#         "font.family": "serif",
#         "text.usetex": True,
#         "font.size": 14,
#         "pgf.rcfonts": False,
#     }
# )

site = {}
script = {}
with open("../domains.txt", "r") as f:
    cnt = 1
    for line in f.readlines():
        if line.strip() == "":
            continue
        site[line.strip()] = cnt
        script[line.strip()] = 0
        cnt += 1

with open("../evaluation/self.log", "r") as f:
    for line in f.readlines():
        if line.strip() == "":
            continue
        l = json.loads(line)
        domain = l["domain"]
        script["https://" + domain] += 1

self_script = [0] * 1000001
for k, v in site.items():
    self_script[v] = script[k]

# totscript = [0] * 1000001
# for sfile in glob.glob(f"../data/script/*.log"):
#     try:
#         with open(sfile, "r") as f:
#             base = os.path.basename(sfile).removesuffix(".log")
#             totscript[site["https://" + base]] = len(f.readlines())
#     except:
#         continue

x = []
y = []
z = []

step = 10000
for i in range(int(1000000 / step)):
    tot = 0
    totz = 0
    for j in range(step):
        tot += self_script[1 + i * step + j]
        # totz += totscript[1 + i * step + j]
    x.append((i + 1) * step)
    y.append(tot / step)
    z.append(totz / step)
    if i == 0 or i == int(1000000 / step) - 1:
        print(tot / step)

plt.plot(x, y, color="r")
plt.xlabel("Website Rank")
plt.ylabel("Average Number of Scripts")
x_major_locator = MultipleLocator(100000)
ax = plt.gca()
ax.xaxis.set_major_locator(x_major_locator)
plt.gcf().set_size_inches(9, 5)
# plt.show()
plt.savefig("average-self-deleting.pgf", bbox_inches="tight")
print(np.corrcoef(y, z))
print(max(y), min(y))
