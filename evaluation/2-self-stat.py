import json

delete_self = 0
delete_by_parent = 0
delete_by_child = 0
delete_by_other = 0
self_website = {}
self_script = {}
self_unique = {}
with open("out.log", "r") as f:
    for line in f.readlines():
        if line.strip() == "":
            continue
        l = json.loads(line)
        domain = l["domain"]

        if l["type"] == 0:
            delete_self += 1
        elif l["type"] == 1:
            delete_by_child += 1
        elif l["type"] == 2:
            delete_by_parent += 1
        else:
            delete_by_other += 1

        if l["type"] != 3:
            self_website[domain] = 1
            self_script[domain + l["hash"]] = 1
            self_unique[l["hash"]] = 1


tot = delete_self + delete_by_parent + delete_by_child + delete_by_other
print(f"Self deletion:{delete_self}, {delete_self/tot}")
print(f"Delete by ancestor:{delete_by_parent}, {delete_by_parent/tot}")
print(f"Delete by descendant:{delete_by_child}, {delete_by_child/tot}")
print(f"Not self deletion:{delete_by_other}, {delete_by_other/tot}")
print("Total:", tot)
print("Self deletion website:", len(self_website))
print("Self deletion script:", len(self_script))
print("Self deletion unique script:", len(self_unique))
