#!/usr/bin/env python3

from os import path
from subprocess import call, Popen, DEVNULL

class submitJobs:
	def __init__(self, params):
		self.params = params

	def submit_trento_jobs(self):
		for job_id in range(self.params['trento']['num_of_jobs']):
			job_dir = path.abspath(f"work/trentojob{job_id:d}")
			if self.params['main']['batch_system'] == "slurm":
				call("sbatch jobscript.slurm", shell=True, cwd=job_dir, stdout=DEVNULL)
			elif self.params['main']['batch_system'] == "local":
				Popen("bash jobscript.slurm", shell=True, cwd=job_dir, stdout=DEVNULL)

	def submit_jobs(self):
		for job_id in range(self.params['main']['num_of_jobs']):
			job_dir = path.abspath(f"work/job{job_id:d}")
			if self.params['main']['batch_system'] == "slurm":
				call("sbatch jobscript.slurm", shell=True, cwd=job_dir, stdout=DEVNULL)
			elif self.params['main']['batch_system'] == "local":
				Popen("bash jobscript.slurm", shell=True, cwd=job_dir, stdout=DEVNULL)

	def submit_eloss_jobs(self):
		if self.params['main']['simulation'] != "hybrid":
			return
		job_dir = path.abspath("work/elossjob")
		if self.params['main']['batch_system'] == "slurm":
			call("sbatch jobscript.slurm", shell=True, cwd=job_dir, stdout=DEVNULL)
		elif self.params['main']['batch_system'] == "local":
			Popen("bash jobscript.slurm", shell=True, cwd=job_dir, stdout=DEVNULL)