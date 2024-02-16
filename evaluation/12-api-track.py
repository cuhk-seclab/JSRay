import json

cnt = 0
with open("normal.log", "w") as res:
    with open("base.txt", "r") as f:
        for line in f.readlines():
            if line.strip() == "":
                continue
            line = line.strip()
            cnt += 1
            print(cnt)

            script = {}
            with open(f"../data/log/{line}.log", "r") as ff:
                try:
                    for ll in ff.readlines():
                        if ll.strip() == "":
                            continue
                        l = json.loads(ll)
                        if l["category"] == "Script":
                            if l["id"] not in script:
                                if len(l["src"]) != 0:
                                    script[l["id"]] = l["src"]
                except:
                    continue
            for i in script.values():
                if i != "<anonymous>":
                    res.write(
                        json.dumps(
                            {
                                "domain": line,
                                "src": i,
                            }
                        )
                        + "\n"
                    )
