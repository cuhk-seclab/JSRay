import json

key2api = [
    "Document::cookie",
    "Document::setCookie",
    "Credential::Credential",
    "CredentialsContainer::get",
    "CredentialsContainer::store",
    "CredentialsContainer::create",
    "IDBFactory::GetDatabaseInfo",
    "IDBFactory::OpenInternal",
    "IDBFactory::DeleteDatabaseInternal",
    "StorageArea::length",
    "StorageArea::key",
    "StorageArea::getItem",
    "StorageArea::setItem",
    "StorageArea::removeItem",
    "StorageArea::clear",
    "StorageArea::Contains",  # 15
    "BatteryManager::getBattery",
    "MediaDevices::getDisplayMedia",
    "Sensor::Sensor",
    "WindowPerformance::eventCounts",
    "WindowPerformance::memory",
    "WindowPerformance::navigation",
    "WindowPerformance::timing",  # 22
    "XMLHttpRequest::XMLHttpRequest",
    "Request::Request",
]
api2key = {key2api[i]: i for i in range(len(key2api))}


def sumapi(api):
    cnt = 0
    for v in api.values():
        cnt += v
    return cnt


nettot = 0
optot = 0
cnt = 0
scriptcnt = 0
n1storage = 0
n1storageN = 0
n1privacy = 0
n1privacyN = 0
n3storage = 0
n3storageN = 0
n3privacy = 0
n3privacyN = 0
with open("base.txt", "r") as f:
    for line in f.readlines():
        if line.strip() == "":
            continue
        line = line.strip()

        cnt += 1
        print(cnt)
        script = {}
        script_hash = {}
        last_remove = {}
        last_script = {}
        with open(f"../data/script/{line}.log", "r") as ff:
            try:
                for ll in ff.readlines():
                    # internal scripts
                    if (
                        ll.startswith("1eb69d8315d70e835ea6e148fc3a2e5a")
                        or ll.startswith("c4ca4238a0b923820dcc509a6f75849b")
                        or ll.startswith("846f9194339b6372a3e4610d62301bd1")
                        or ll.startswith("032a90075652c365fe002cb51ebccfc5")
                    ):
                        continue
                    sp = ll.strip().split(",")
                    script_hash[int(sp[1])] = sp[0]
                    scriptcnt += 1
            except:
                continue

        with open(f"../data/log/{line}.log", "r") as ff:
            try:
                for ll in ff.readlines():
                    if ll.strip() == "":
                        continue
                    # fix json format
                    try:
                        if '"category":"warning"' in ll and ',"src":' in ll:
                            if "fired_event" in ll:
                                src = ll[
                                    ll.find(',"src":"') + 8: ll.find('","fired_event')
                                ]
                                ll = (
                                    ll[: ll.find(',"src":"') + 8]
                                    + ll[ll.find('","fired_event'):]
                                )
                            else:
                                src = ll[
                                    ll.find(',"src":"') + 8: ll.find('","parentID')
                                ]
                                ll = (
                                    ll[: ll.find(',"src":"') + 8]
                                    + ll[ll.find('","parentID'):]
                                )
                            l = json.loads(ll)
                            l["src"] = src
                        else:
                            l = json.loads(ll)
                    except:
                        continue
                    # internal ones
                    if (
                        l["category"] == "API"
                        and l["function"] == "WindowPerformance::timing"
                        and l["parentID"] == 0
                    ):
                        continue
                    if (
                        l["category"] == "API"
                        and l["function"] == "WindowPerformance::eventCounts"
                        and l["parentID"] == 0
                    ):
                        continue

                    try:
                        if l["category"] == "Script":
                            if l["id"] not in script:
                                script[l["id"]] = {
                                    "src": l["src"],
                                    "pid": l["parentID"],
                                    "third": not (
                                        line in l["src"]
                                        or "<anonymous>" in l["src"]
                                        or l["src"] == ""
                                    ),
                                    "event": [],
                                    "api": {},
                                }
                            last_script = l
                        if l["category"] == "API" and l["parentID"] != 0:
                            apiid = api2key[l["function"]]
                            if apiid not in script[l["parentID"]]["api"]:
                                script[l["parentID"]]["api"][apiid] = 0
                            script[l["parentID"]]["api"][apiid] += 1
                        if l["category"] == "dom":
                            last_remove = l
                        if (
                            l["category"] == "event"
                            and l["function"] == "JSBasedEventListener::Invoke"
                        ):
                            script[last_script["id"]]["event"].append(
                                l["event_type"].lower()
                            )
                    except:
                        continue
            except:
                continue
        for i in script.values():
            ns = 0
            np = 0
            net = False
            for k, v in i["api"].items():
                if k <= 15:
                    ns += v
                elif k <= 22:
                    np += v
                else:
                    nettot += v
                    net = True
            if i["third"]:
                n3storage += ns
                n3privacy += np
                if net:
                    n3storageN += ns
                    n3privacyN += np
            else:
                n1storage += ns
                n1privacy += np
                if net:
                    n1storageN += ns
                    n1privacyN += np
            optot += ns + np

print("Script cnt:", scriptcnt)
print(
    f"First: {n1storage/(scriptcnt)} {n1storageN/(scriptcnt)} {n1privacy/(scriptcnt)} {n1privacyN/(scriptcnt)}"
)
print(
    f"Third: {n3storage/(scriptcnt)} {n3storageN/(scriptcnt)} {n3privacy/(scriptcnt)} {n3privacyN/(scriptcnt)}"
)
print(
    f"avg: {optot/scriptcnt}, netavg:{nettot/scriptcnt}",
)
