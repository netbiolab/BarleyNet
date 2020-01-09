#!/usr/bin/python3 -u

import sys

data = dict()
with open(sys.argv[1]) as TERM:
	for line in TERM:
		gene, gos = line.strip().split("\t")
		for go in gos.split(";"):
			if go not in data:
				data[go] = list()
			data[go].append(gene)

goterm = dict() # term id : [namespace, name]
current = ""
with open("go-basic.obo") as DATA:
	for line in DATA:
		if line.startswith("id: "):
			current = line.strip()[4:]
			goterm[current] = list()
		elif line.startswith("name: "):
			goterm[current].append(line.strip().split(": ")[1])
		elif line.startswith("namespace: "):
			goterm[current].insert(0, line.strip().split(": ")[1])
		elif line.startswith("alt_id: "):
			goterm[line.strip().split(": ")[1]] = goterm[current]
		else:
			continue

output = open(sys.argv[2], "w")

for go in data:
	print(go, goterm[go][1], len(data[go]), ",".join(data[go]), sep="\t", file=output)

output.close()
