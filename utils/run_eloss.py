#!/usr/bin/env python3

from sys import argv, exit
from os import path, mkdir
from subprocess import call
import json

if __name__ == "__main__":

	if (len(argv) != 3): exit()

	dreenadir  = path.abspath(argv[1])
	dssffssdir = path.join(dreenadir, "DSSFFsEbEv6.0m")
	vndir      = path.join(dreenadir, "Vnv4.0m")
	workdir    = path.abspath(argv[2])

	with open("params.json", 'r') as jsonf: params = json.load(jsonf)

	cent_lows  = [int(c.replace('%', '').split('-')[0]) for c in params['main']['centrality']]
	evid_low   = int(min(cent_lows)/100.0*params['trento']['mb_event_n'])
	cent_highs = [int(c.replace('%', '').split('-')[1]) for c in params['main']['centrality']]
	evid_high  = int(max(cent_highs)/100.0*params['trento']['mb_event_n'])

	runrecord   = open(path.abspath("runrecord.log"), 'w')
	errorrecord = open(path.abspath("errorrecord.log"), 'w')

	commandString  = f"export OMP_NUM_THREADS={params['dreena']['THREAD_NUM']:d}; "
	commandString += f"./ebeDREENA AverageEL --workDir={workdir} --config=dreena.conf --eventIDs={evid_low:d}-{evid_high:d} --pName=Bottom;"
	call(commandString, shell=True, cwd=dreenadir, stdout=runrecord, stderr=errorrecord)

	commandString  = f"export OMP_NUM_THREADS={params['dreena']['THREAD_NUM']:d}; "
	commandString += f"./ebeDREENA AverageEL --workDir={workdir} --config=dreena.conf --eventIDs={evid_low:d}-{evid_high:d} --pName=Charm;"
	call(commandString, shell=True, cwd=dreenadir, stdout=runrecord, stderr=errorrecord)

	commandString  = f"export OMP_NUM_THREADS={params['dreena']['THREAD_NUM']:d}; "
	commandString += f"./ebeDREENA AverageEL --workDir={workdir} --config=dreena.conf --eventIDs={evid_low:d}-{evid_high:d} --pName=LQuarks;"
	call(commandString, shell=True, cwd=dreenadir, stdout=runrecord, stderr=errorrecord)

	commandString  = f"export OMP_NUM_THREADS={params['dreena']['THREAD_NUM']:d}; "
	commandString += f"./ebeDREENA AverageEL --workDir={workdir} --config=dreena.conf --eventIDs={evid_low:d}-{evid_high:d} --pName=Gluon;"
	call(commandString, shell=True, cwd=dreenadir, stdout=runrecord, stderr=errorrecord)

	# commandString  = f"export OMP_NUM_THREADS={params['dreena']['THREAD_NUM']:d}; "
	# commandString += f"./DSSFFsEbE --workdir={workdir} --c=dsssffs.conf --eventIDs={evid_low:d}-{evid_high:d};"
	# call(commandString, shell=True, cwd=dssffssdir, stdout=runrecord, stderr=errorrecord)

	if not path.exists(path.abspath("highpt")):
		mkdir(path.abspath("highpt"))

	methods = []
	for m in params['dreena']['methods']:
		if len(m.split('_')) == 1:
			methods.append([m.split('_')[0], "off"])
		else:
			methods.append([m.split('_')[0], m.split('_')[1].replace("F", "")])

	# for pName in ["b", "c", "ch"]:
	for pName in ["b", "c"]:
		for centrality in params['main']['centrality']:
			evid_low  = int(params['trento']['mb_event_n']*int(centrality.replace('%', '').split('-')[0])/100.0)
			evid_high = int(params['trento']['mb_event_n']*int(centrality.replace('%', '').split('-')[1])/100.0)
			commandString = f"export OMP_NUM_THREADS={params['dreena']['THREAD_NUM']:d}; "
			for mtd in methods:
				commandString += f"./VnEbE --workdir={workdir} --c=vn.conf --pName={pName} --eventIDs={evid_low:d}-{evid_high:d} --centrality={centrality} --method={mtd[0]} --filter={mtd[1]}; "
			call(commandString, shell=True, cwd=vndir, stdout=runrecord, stderr=errorrecord)

	runrecord.close()
	errorrecord.close()