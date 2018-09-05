f = open("ps.out")
data = f.read().split("\n")

# exclui a ultima linha
data = data[:-1]

ppids = []

# test -------------------------

for row in data:
	ppid = int(row) 
	if ppid >= 2:
		ppids.append(ppid)

# dicionario
ppids_dic = {}

for ppid in ppids:
	if ppid in ppids_dic:
		ppids_dic[ppid] += 1
	else:
		ppids_dic[ppid] = 1

print(sorted(ppids_dic.items(), key =lambda pr: pr[1], reverse = True)[:3])

