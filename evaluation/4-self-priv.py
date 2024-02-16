import json

tot = 0
case1d1 = 0
case3d3 = 0
case1d3 = 0
case3d1 = 0
site1d1 = {}
site3d3 = {}
site1d3 = {}
site3d1 = {}
with open("out.log", "r") as f:
    for line in f.readlines():
        if line.strip() == "":
            continue
        l = json.loads(line)
        domain = l["domain"]

        if l["type"] != 3:
            tot += 1
            if l["third"] and l["cthird"]:
                case3d3 += 1
                site3d3[domain] = 1
            if l["third"] and not l["cthird"]:
                case3d1 += 1
                site3d1[domain] = 1
            if not l["third"] and l["cthird"]:
                case1d3 += 1
                site1d3[domain] = 1
            if not l["third"] and not l["cthird"]:
                case1d1 += 1
                site1d1[domain] = 1


casetot = case1d1 + case1d3 + case3d1 + case3d3
sitetot = len(site1d1) + len(site1d3) + len(site3d1) + len(site3d3)
print("Total:", tot)
print(
    f"1d1: {case1d1} & {case1d1*100/casetot} & {len(site1d1)} & {len(site1d1)*100/sitetot}"
)
print(
    f"3d3: {case3d3} & {case3d3*100/casetot} & {len(site3d3)} & {len(site3d3)*100/sitetot}"
)
print(
    f"1d3: {case1d3} & {case1d3*100/casetot} & {len(site1d3)} & {len(site1d3)*100/sitetot}"
)
print(
    f"3d1: {case3d1} & {case3d1*100/casetot} & {len(site3d1)} & {len(site3d1)*100/sitetot}"
)
