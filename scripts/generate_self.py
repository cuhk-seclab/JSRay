with open("out.log", "r") as f:
    with open("self.log", "w") as ff:
        for line in f.readlines():
            if line.strip() == "":
                continue
            if '"type": 3' not in line:
                ff.write(line.strip() + "\n")
