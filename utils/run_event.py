#!/usr/bin/env python3

from os import path, remove
from subprocess import call
import json

if __name__ == "__main__":

	with open("params.json", 'r') as jsonf: params = json.load(jsonf)

	cwdir = path.abspath("")

	runrecord   = open(path.join(cwdir, "runrecord.log"), 'w')
	errorrecord = open(path.join(cwdir, "errorrecord.log"), 'w')

	# freestream
	if params['freestream']['turn_on'] == 1:
		call("python3 streamIC.py", shell=True, cwd=cwdir, stdout=runrecord, stderr=errorrecord)
		all_files = ["sd.dat", "bcp.dat"]
		rm_files  = list(set(all_files) - set(params['trento']['save_files']))
		if params['main']['simulation'] == 'hybrid':
			rm_files = list(set(rm_files) - set(["bcp.dat"]))
		for aFile in rm_files:
			remove(path.join(cwdir, aFile))
		remove(path.join(cwdir, "streamIC.py"))

	# hydro
	call("./osu-hydro", shell=True, cwd=cwdir, stdout=runrecord, stderr=errorrecord)
	if params['freestream']['turn_on'] == 1:
		all_files = ["ed.dat", "u1.dat", "u2.dat", "pi11.dat", "pi12.dat", "pi22.dat"]
		rm_files  = list(set(all_files) - set(params['freestream']['save_files']))
		for aFile in rm_files:
			remove(path.join(cwdir, aFile))
	else:
		all_files = ["sd.dat", "bcp.dat"]
		rm_files  = list(set(all_files) - set(params['trento']['save_files']))
		if params['main']['simulation'] == "hybrid":
			rm_files = list(set(rm_files) - set(['bcp.dat']))
		for aFile in rm_files:
			remove(path.join(cwdir, aFile))
	remove(path.join(cwdir, "osu-hydro"))
	remove(path.join(cwdir, "osu-hydro.conf"))

	# particlization
	call("python3 sampleSurface.py", shell=True, cwd=cwdir, stdout=runrecord, stderr=errorrecord)
	all_files = ["Temp_evo.dat", "surface.dat", "eta_per_s_T.dat"]
	rm_files  = list(set(all_files) - set(params['hydro']['save_files']))
	if params['main']['simulation'] == "hybrid":
		rm_files = list(set(rm_files) - set(["Temp_evo.dat"]))
	for aFile in rm_files:
		remove(path.join(cwdir, aFile))
	remove(path.join(cwdir, "sampleSurface.py"))
	remove(path.join(cwdir, "eos.dat"))

	# afterburner
	call("./afterburner particles_in.dat particles_out.dat", shell=True, cwd=cwdir, stdout=runrecord, stderr=errorrecord)
	all_files = ["particles_in.dat"]
	rm_files  = list(set(all_files) - set(params['frzout']['save_files']))
	for aFile in rm_files:
		remove(path.join(cwdir, aFile))
	remove(path.join(cwdir, "afterburner"))
	remove(path.join(cwdir, "osc2u"))
	remove(path.join(cwdir, "urqmd"))
	remove(path.join(cwdir, "tables.dat"))
	remove(path.join(cwdir, "urqmd.conf"))
	remove(path.join(cwdir, "urqmd_input.dat"))

	# analysis
	call("python3 analyse.py", shell=True, cwd=cwdir, stdout=runrecord, stderr=errorrecord)
	call("python3 reference_flow.py qn.dat > intflows.dat", shell=True, cwd=cwdir, stdout=runrecord, stderr=errorrecord)
	all_files = ["particles_out.dat"]
	rm_files  = list(set(all_files) - set(params['urqmd']['save_files']))
	for aFile in rm_files: remove(path.join(cwdir, aFile))
	remove(path.join(cwdir, "analyse.py"))
	remove(path.join(cwdir, "reference_flow.py"))

	all_files = ["dndpt.dat", "identified.dat", "qn.dat", "intflows.dat"]
	rm_files  = list(set(all_files) - set(params['analysis']['save_files']))
	rm_files  = list(set(rm_files) - set(["identified.dat", "qn.dat"]))
	for aFile in rm_files:
		remove(path.join(cwdir, aFile))

	runrecord.close()
	errorrecord.close()

	with open(path.abspath("eventdone.info"), 'w') as f:
		f.write("event done\n")