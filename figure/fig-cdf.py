import json

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import ticker

matplotlib.use("pgf")
matplotlib.rcParams.update(
    {
        "pgf.texsystem": "pdflatex",
        "font.family": "serif",
        "text.usetex": True,
        "font.size": 14,
        "pgf.rcfonts": False,
    }
)

hash = {}
with open("../evaluation/self.log", "r") as f:
    for line in f.readlines():
        if line.strip() == "":
            continue
        l = json.loads(line)
        domain = l["domain"]
        if l["hash"] not in hash:
            hash[l["hash"]] = []
        if domain not in hash[l["hash"]]:
            hash[l["hash"]].append(domain)
cnthash = {}
for k, v in hash.items():
    cnthash[k] = len(v)

res = {}
for k, v in cnthash.items():
    if v not in res:
        res[v] = 0
    res[v] += 1

x = []
y = []
tot = 0
check1 = 0
check2 = 0
res = {key: res[key] for key in sorted(res)}
for k, v in res.items():
    check1 += v
    check2 += k * v
    x.append(k)
    y.append(check1 / 142557)

print(check1)
print(check2)


plt.plot(x, y, color="b")
plt.xlabel("Number of Websites a Script is Included")
plt.ylabel("CDF")


plt.gcf().set_size_inches(9, 5)
plt.xscale("log")
plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter())
# plt.show()
plt.savefig("cdf-self-deleting.pgf", bbox_inches="tight")
