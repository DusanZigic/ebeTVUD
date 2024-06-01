#!/usr/bin/env python3

from os import path
from glob import glob
from subprocess import call, Popen, DEVNULL
from params import params

def submit_trento_jobs():
	for job_id in range(params['trento']['num_of_jobs']):
		job_dir = path.abspath('work/trentojob%d' % job_id)
		if params['main']['batch_system'] == 'slurm':
			call('sbatch jobscript.slurm', shell=True, cwd=job_dir, stdout=DEVNULL)
		else:
			Popen('bash jobscript.slurm', shell=True, cwd=job_dir, stdout=DEVNULL)

def submit_jobs():
	for job_id in range(params['main']['num_of_jobs']):
		job_dir = path.abspath('work/job{0:d}'.format(job_id))
		if params['main']['batch_system'] == 'slurm':
			call('sbatch jobscript.slurm', shell=True, cwd=job_dir, stdout=DEVNULL)
		else:
			Popen('bash jobscript.slurm', shell=True, cwd=job_dir, stdout=DEVNULL)

def submit_eloss_jobs():
	if params['main']['simulation'] != 'hybrid': return
	job_dir = path.abspath('work/elossjob')
	if params['main']['batch_system'] == 'slurm':
		call('sbatch jobscript.slurm', shell=True, cwd=job_dir, stdout=DEVNULL)
	else:
		Popen('bash jobscript.slurm', shell=True, cwd=job_dir, stdout=DEVNULL)