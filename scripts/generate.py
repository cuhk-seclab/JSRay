import glob
import json
import os

data_folder = "./data"
site_cnt = 0

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
    "StorageArea::Contains",
    "BatteryManager::getBattery",
    "MediaDevices::getDisplayMedia",
    "Sensor::Sensor",
    "WindowPerformance::eventCounts",
    "WindowPerformance::memory",
    "WindowPerformance::navigation",
    "WindowPerformance::timing",
    "XMLHttpRequest::XMLHttpRequest",
    "Request::Request",
]
api2key = {key2api[i]: i for i in range(len(key2api))}


# 1 id -> cid, 2 id <- cid, 3 else
def check_relation(script, id, cid):
    cur = id
    while cur != 0:
        cur = script[cur]["pid"]
        if cur == cid:
            return 1
    cur = cid
    while cur != 0:
        cur = script[cur]["pid"]
        if cur == id:
            return 2
    return 3


for logFile in glob.glob(f"{data_folder}/log/*.log"):
    base = os.path.basename(logFile)
    domain = base.removesuffix(".log")
    site_cnt += 1
    print(site_cnt, logFile)

    output = []
    script = {}
    script_hash = {}
    last_remove = {}
    last_script = {}
    with open(f"{data_folder}/script/{base}", "r") as f:
        try:
            for line in f.readlines():
                # internal scripts
                if (
                    line.startswith("1eb69d8315d70e835ea6e148fc3a2e5a")
                    or line.startswith("c4ca4238a0b923820dcc509a6f75849b")
                    or line.startswith("846f9194339b6372a3e4610d62301bd1")
                    or line.startswith("032a90075652c365fe002cb51ebccfc5")
                ):
                    continue
                sp = line.strip().split(",")
                script_hash[int(sp[1])] = sp[0]
        except:
            continue
    with open(logFile, "r") as f:
        try:
            for line in f.readlines():
                if line.strip() == "":
                    continue
                # fix json format
                try:
                    if '"category":"warning"' in line and ',"src":' in line:
                        if "fired_event" in line:
                            src = line[
                                line.find(',"src":"') + 8 : line.find('","fired_event')
                            ]
                            line = (
                                line[: line.find(',"src":"') + 8]
                                + line[line.find('","fired_event') :]
                            )
                        else:
                            src = line[
                                line.find(',"src":"') + 8 : line.find('","parentID')
                            ]
                            line = (
                                line[: line.find(',"src":"') + 8]
                                + line[line.find('","parentID') :]
                            )
                        l = json.loads(line)
                        l["src"] = src
                    else:
                        l = json.loads(line)
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
                                    domain in l["src"]
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
                    if l["category"] == "warning":
                        id = l["parentID"]
                        cid = 0
                        if "id" in l:
                            cid = l["id"]
                            if cid == -1:
                                cid = id
                        else:
                            for k, v in script.items():
                                if v["src"] in l["src"] or l["src"] in v["src"]:
                                    cid = k
                                    break
                        if id == 0 or cid == 0:
                            continue
                        if id == cid:
                            ty = 0
                        else:
                            ty = check_relation(script, id, cid)
                        attr = "Attribute" in last_remove["func"]
                        if attr or l["tag"].lower() != "script":
                            ok = False
                            for k in script[id]["event"]:
                                if k in l["fired_event"].lower():
                                    ok = True
                                    break
                            if not ok:
                                continue
                        output.append(
                            {
                                "domain": domain,
                                "src": script[id]["src"],
                                "hash": script_hash[id],
                                "direct": not ("indirectTag" in l),
                                "third": script[id]["third"],
                                "cthird": script[cid]["third"],
                                "type": ty,
                                "attr": attr,
                                "static": script[cid]["pid"] == 0,
                                "api": script[id]["api"],
                                "capi": script[cid]["api"],
                            }
                        )

                except:
                    continue
        except:
            continue
    # print(output)
    with open("out.log", "a") as fout:
        for i in output:
            fout.write(json.dumps(i) + "\n")

print("Total sites:", site_cnt)
