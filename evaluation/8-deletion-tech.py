import json

e1sc = 0
e1sw = set()
e3sc = 0
e3sw = set()
e1dc = 0
e1dw = set()
e3dc = 0
e3dw = set()
a1sc = 0
a1sw = set()
a3sc = 0
a3sw = set()
a1dc = 0
a1dw = set()
a3dc = 0
a3dw = set()

with open("self.log", "r") as f:
    for line in f.readlines():
        if line.strip() == "":
            continue
        l = json.loads(line)
        domain = l["domain"]

        sd = "s" if l["static"] else "d"
        ea = "a" if l["attr"] else "e"
        ft = "3" if l["third"] else "1"

        ty = ea + ft + sd
        if ty == "e1s":
            e1sc += 1
            e1sw.add(domain)
        elif ty == "e3s":
            e3sc += 1
            e3sw.add(domain)
        elif ty == "e1d":
            e1dc += 1
            e1dw.add(domain)
        elif ty == "e3d":
            e3dc += 1
            e3dw.add(domain)
        elif ty == "a1s":
            a1sc += 1
            a1sw.add(domain)
        elif ty == "a3s":
            a3sc += 1
            a3sw.add(domain)
        elif ty == "a1d":
            a1dc += 1
            a1dw.add(domain)
        elif ty == "a3d":
            a3dc += 1
            a3dw.add(domain)
        else:
            assert 0

cases = 1596796
websites = 226854
e1sw = len(e1sw)
e3sw = len(e3sw)
e1dw = len(e1dw)
e3dw = len(e3dw)
a1sw = len(a1sw)
a3sw = len(a3sw)
a1dw = len(a1dw)
a3dw = len(a3dw)
print(f"{e1sc} & {e1sc*100/cases} & {e1sw} & {e1sw*100/websites}")
print(f"{e3sc} & {e3sc*100/cases} & {e3sw} & {e3sw*100/websites}")
print(f"{e1dc} & {e1dc*100/cases} & {e1dw} & {e1dw*100/websites}")
print(f"{e3dc} & {e3dc*100/cases} & {e3dw} & {e3dw*100/websites}")

print(f"{a1sc} & {a1sc*100/cases} & {a1sw} & {a1sw*100/websites}")
print(f"{a3sc} & {a3sc*100/cases} & {a3sw} & {a3sw*100/websites}")
print(f"{a1dc} & {a1dc*100/cases} & {a1dw} & {a1dw*100/websites}")
print(f"{a3dc} & {a3dc*100/cases} & {a3dw} & {a3dw*100/websites}")
