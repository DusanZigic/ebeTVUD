#!/usr/bin/env python3

from sys import argv, exit
from os import path, listdir
from os import walk as pwalk
from glob import glob

def progresstrento():
	work_dir = path.abspath('work')
	jobN     = len(glob(path.join(work_dir, 'trentojob*')))
	total_events = 0
	total_events_done = 0
	print_total = False
	for jobID in range(jobN):
		job_dir = path.join(work_dir, 'trentojob{0:d}'.format(jobID))
		with open(path.join(job_dir, 'trento.conf')) as f:
			while True:
				line = f.readline().rstrip().split()
				if line[0] == 'number-events':
					total_events_job = int(line[2])
					break
		total_events += total_events_job
		events_dir  = path.join(job_dir, 'eventstemp')
		events_done = len(listdir(events_dir))
		total_events_done += events_done
		if events_done < total_events_job:
			print('{0:>6s}: {1:5d}/{2:5d}'.format(path.split(job_dir)[1], events_done, total_events_job))
			print_total = True
	if print_total:
		print('-'*25)
		print('{0:>10s}: {1:5d}/{2:5d}'.format('total', total_events_done, total_events))

	if not print_total:
		total_events_done = 0
		total_events = 0
		for jobID in range(jobN):
			job_dir = path.join(work_dir, 'trentojob{0:d}'.format(jobID))
			with open(path.join(job_dir, 'trento.conf')) as f:
				while True:
					line = f.readline().rstrip().split()
					if line[0] == 'number-events':
						total_events_job = int(line[2])
						break
			total_events += total_events_job
			events_dir  = path.join(job_dir, 'eventstemp')
			events_done = len([f for f in listdir(events_dir) if 'bcp' in f])
			total_events_done += events_done
			if events_done < total_events_job:
				print('bcp{0:>6s}: {1:5d}/{2:5d}'.format(path.split(job_dir)[1], events_done, total_events_job))
				print_total = True
		if print_total:
			print('-'*28)
			print('{0:>13s}: {1:5d}/{2:5d}'.format('total', total_events_done, total_events))

	if 'trentoic' in listdir(work_dir):
		trentoic_events = len(listdir(path.join(work_dir, 'trentoic')))
		print('trentoic: {0:5d}/{1:5d}'.format(trentoic_events, 2*total_events))

def progresshydro():
	work_dir = path.abspath('work')
	jobN     = len([path.join(work_dir, f) for f in listdir(work_dir) if path.isdir(path.join(work_dir, f))])
	total_events = 0
	total_events_done = 0
	for jobID in range(jobN):
		job_dir = path.join(work_dir, 'job{0:d}'.format(jobID))
		total_events_job = len([f for f in listdir(job_dir) if 'event' in f])
		total_events += total_events_job
		events_done  = 0
		for root, dirs, files in pwalk(job_dir):
			if 'eventdone.info' in files: events_done += 1
		total_events_done += events_done
		if events_done < total_events_job:
			print('{0:>6s}: {1:3d}/{2:3d}'.format(path.split(job_dir)[1], events_done, total_events_job))
	print('-'*18)
	print('{0:>6s}: {1:3d}/{2:3d}'.format('total', total_events_done, total_events))

def progresseloss():
	total_events = len(listdir(path.abspath('work/bcp')))
	res_dir = path.abspath('work/elossjob/results')
	for p in [['bottom', 'b'], ['charm', 'c'], ['lquarks', 'db'], ['gluon', 'g'], ['ch', 'ch']]:
		events_done = len(glob(path.join(res_dir, '{0:s}*.dat'.format(p[1]))))
		if events_done < total_events:
			print('{0:>7s}: {1:4d}/{2:4d}'.format(p[0], events_done, total_events))

if __name__ == '__main__':

	if not path.exists(path.abspath('work')):
		print('no work in progress')
		exit()

	if 'trentojob0' in listdir(path.abspath('work')):
		progresstrento()
		exit()

	if 'elossjob' in listdir(path.abspath('work')):
		progresseloss()
		exit()

	if 'job0' in listdir(path.abspath('work')):
		progresshydro()
		exit()