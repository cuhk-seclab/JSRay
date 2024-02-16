import json

deletion_cnt = 0
deletion_website = 0
deletion_script = 0
deletion_unique = {}
with open("out.log", "r") as f:
    last_domain = ""
    website_script = {}
    for line in f.readlines():
        if line.strip() == "":
            continue
        l = json.loads(line)
        deletion_cnt += 1
        domain = l["domain"]

        if domain != last_domain:
            last_domain = domain
            deletion_website += 1
            deletion_script += len(website_script)
            website_script = {}

        website_script[l["hash"]] = 1
        deletion_unique[l["hash"]] = 1

    deletion_script += len(website_script)


print("Total deletion operation:", deletion_cnt)
print("Total deletion website:", deletion_website)
print("Total deletion scripts:", deletion_script)
print("Total unique deletion scripts:", len(deletion_unique))
