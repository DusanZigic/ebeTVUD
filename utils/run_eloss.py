#!/usr/bin/env python3

from sys import argv, exit
from os import path, listdir, mkdir, rename, remove
from subprocess import call
import json

if __name__ == "__main__":

	if (len(argv) != 3): exit()

	dreenadir  = path.abspath(argv[1])
	dssffssdir = path.join(dreenadir, 'DSSFFsEbEv6.0m')
	vndir      = path.join(dreenadir, 'Vnv4.0m')
	workdir    = path.abspath(argv[2])

	with open('params.json', 'r') as jsonf: params = json.load(jsonf)

	cent_lows  = [int(c.replace('%', '').split('-')[0]) for c in params['main']['centrality']]
	evid_low   = int(min(cent_lows)/100.0*params['trento']['mb_event_n'])
	cent_highs = [int(c.replace('%', '').split('-')[1]) for c in params['main']['centrality']]
	evid_high  = int(max(cent_highs)/100.0*params['trento']['mb_event_n'])

	runrecord   = open(path.abspath('runrecord.log'), 'w')
	errorrecord = open(path.abspath('errorrecord.log'), 'w')

	commandString  = 'export OMP_NUM_THREADS={0:d}; '.format(params['dreena']['THREAD_NUM'])
	commandString += './DREENAAEbE AverageEL --workdir={0:s} --c=dreena.conf --eventIDs={1:d}-{2:d} --pName=Bottom'.format(workdir, evid_low, evid_high)
	call(commandString, shell=True, cwd=dreenadir, stdout=runrecord, stderr=errorrecord)

	commandString  = 'export OMP_NUM_THREADS={0:d}; '.format(params['dreena']['THREAD_NUM'])
	commandString += './DREENAAEbE AverageEL --workdir={0:s} --c=dreena.conf --eventIDs={1:d}-{2:d} --pName=Charm'.format(workdir, evid_low, evid_high)
	call(commandString, shell=True, cwd=dreenadir, stdout=runrecord, stderr=errorrecord)

	commandString  = 'export OMP_NUM_THREADS={0:d}; '.format(params['dreena']['THREAD_NUM'])
	commandString += './DREENAAEbE AverageEL --workdir={0:s} --c=dreena.conf --eventIDs={1:d}-{2:d} --pName=LQuarks'.format(workdir, evid_low, evid_high)
	call(commandString, shell=True, cwd=dreenadir, stdout=runrecord, stderr=errorrecord)

	commandString  = 'export OMP_NUM_THREADS={0:d}; '.format(params['dreena']['THREAD_NUM'])
	commandString += './DREENAAEbE AverageEL --workdir={0:s} --c=dreena.conf --eventIDs={1:d}-{2:d} --pName=Gluon'.format(workdir, evid_low, evid_high)
	call(commandString, shell=True, cwd=dreenadir, stdout=runrecord, stderr=errorrecord)

	commandString  = 'export OMP_NUM_THREADS={0:d}; '.format(params['dreena']['THREAD_NUM'])
	commandString += './DSSFFsEbE --workdir={0:s} --c=dsssffs.conf --eventIDs={1:d}-{2:d}'.format(workdir, evid_low, evid_high)
	call(commandString, shell=True, cwd=dssffssdir, stdout=runrecord, stderr=errorrecord)

	if not path.exists(path.abspath('highpt')): mkdir(path.abspath('highpt'))

	methods = []
	for m in params['dreena']['methods']:
		if len(m.split('_')) == 1:
			methods.append([m.split('_')[0], 'off'])
		else:
			methods.append([m.split('_')[0], m.split('_')[1].replace('F', '')])

	for pName in ['b', 'c', 'ch']:
		for centrality in params['main']['centrality']:
			evid_low  = int(params['trento']['mb_event_n']*int(centrality.replace('%', '').split('-')[0])/100.0)
			evid_high = int(params['trento']['mb_event_n']*int(centrality.replace('%', '').split('-')[1])/100.0)
			commandString  = 'export OMP_NUM_THREADS={0:d}; '.format(params['dreena']['THREAD_NUM'])
			for mtd in methods:
				commandString += './VnEbE --workdir={0:s} --c=vn.conf --pName={1:s} --eventIDs={2:d}-{3:d} --centrality={4:s} --method={5:s} --filter={6:s}; '.format(workdir, pName, evid_low, evid_high, centrality, mtd[0], mtd[1])
			call(commandString, shell=True, cwd=vndir, stdout=runrecord, stderr=errorrecord)

	runrecord.close()
	errorrecord.close()