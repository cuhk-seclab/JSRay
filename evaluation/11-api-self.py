import json

d11dstorage = 0
d11dstorageN = 0
d11dprivacy = 0
d11dprivacyN = 0
d11gstorage = 0
d11gstorageN = 0
d11gprivacy = 0
d11gprivacyN = 0

d33dstorage = 0
d33dstorageN = 0
d33dprivacy = 0
d33dprivacyN = 0
d33gstorage = 0
d33gstorageN = 0
d33gprivacy = 0
d33gprivacyN = 0

d13dstorage = 0
d13dstorageN = 0
d13dprivacy = 0
d13dprivacyN = 0
d13gstorage = 0
d13gstorageN = 0
d13gprivacy = 0
d13gprivacyN = 0

d31dstorage = 0
d31dstorageN = 0
d31dprivacy = 0
d31dprivacyN = 0
d31gstorage = 0
d31gstorageN = 0
d31gprivacy = 0
d31gprivacyN = 0

nettot = 0


def calcapi(api):
    ns = 0
    np = 0
    net = False
    global nettot
    for k, v in api.items():
        if int(k) <= 15:
            ns += v
        elif int(k) <= 22:
            np += v
        else:
            nettot += v
            net = True
    if net:
        return ns, ns, np, np
    else:
        return ns, 0, np, 0


def sumapi(api):
    cnt = 0
    for k, v in api.items():
        if int(k) <= 22:
            cnt += v
    return cnt


optot = 0
tot = 0
with open("self.log", "r") as f:
    for line in f.readlines():
        if line.strip() == "":
            continue
        l = json.loads(line)
        domain = l["domain"]
        tot += 1

        if not l["third"] and not l["cthird"]:
            ns, nsn, np, npn = calcapi(l["capi"])
            d11dstorage += ns
            d11dstorageN += nsn
            d11dprivacy += np
            d11dprivacyN += npn
            optot += sumapi(l["capi"])

            ns, nsn, np, npn = calcapi(l["api"])
            d11gstorage += ns
            d11gstorageN += nsn
            d11gprivacy += np
            d11gprivacyN += npn
            optot += sumapi(l["api"])
        if l["third"] and l["cthird"]:
            ns, nsn, np, npn = calcapi(l["capi"])
            d33dstorage += ns
            d33dstorageN += nsn
            d33dprivacy += np
            d33dprivacyN += npn
            optot += sumapi(l["capi"])

            ns, nsn, np, npn = calcapi(l["api"])
            d33gstorage += ns
            d33gstorageN += nsn
            d33gprivacy += np
            d33gprivacyN += npn
            optot += sumapi(l["api"])
        if not l["third"] and l["cthird"]:
            ns, nsn, np, npn = calcapi(l["capi"])
            d13dstorage += ns
            d13dstorageN += nsn
            d13dprivacy += np
            d13dprivacyN += npn
            optot += sumapi(l["capi"])

            ns, nsn, np, npn = calcapi(l["api"])
            d13gstorage += ns
            d13gstorageN += nsn
            d13gprivacy += np
            d13gprivacyN += npn
            optot += sumapi(l["api"])
        if l["third"] and not l["cthird"]:
            ns, nsn, np, npn = calcapi(l["capi"])
            d31dstorage += ns
            d31dstorageN += nsn
            d31dprivacy += np
            d31dprivacyN += npn
            optot += sumapi(l["capi"])

            ns, nsn, np, npn = calcapi(l["api"])
            d31gstorage += ns
            d31gstorageN += nsn
            d31gprivacy += np
            d31gprivacyN += npn
            optot += sumapi(l["api"])

print(
    f"{d11dstorage/(tot)} {d11dstorageN/(tot)} {d11dprivacy/(tot)} {d11dprivacyN/(tot)}"
)
print(
    f"{d11gstorage/(tot)} {d11gstorageN/(tot)} {d11gprivacy/(tot)} {d11gprivacyN/(tot)}"
)
print(
    f"{d33dstorage/(tot)} {d33dstorageN/(tot)} {d33dprivacy/(tot)} {d33dprivacyN/(tot)}"
)
print(
    f"{d33gstorage/(tot)} {d33gstorageN/(tot)} {d33gprivacy/(tot)} {d33gprivacyN/(tot)}"
)
print(
    f"{d13dstorage/(tot)} {d13dstorageN/(tot)} {d13dprivacy/(tot)} {d13dprivacyN/(tot)}"
)
print(
    f"{d13gstorage/(tot)} {d13gstorageN/(tot)} {d13gprivacy/(tot)} {d13gprivacyN/(tot)}"
)
print(
    f"{d31dstorage/(tot)} {d31dstorageN/(tot)} {d31dprivacy/(tot)} {d31dprivacyN/(tot)}"
)
print(
    f"{d31gstorage/(tot)} {d31gstorageN/(tot)} {d31gprivacy/(tot)} {d31gprivacyN/(tot)}"
)
print(
    f"avg: {optot/tot/2}, netavg:{nettot/tot/2}",
)
