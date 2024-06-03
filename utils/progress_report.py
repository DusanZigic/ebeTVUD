#!/usr/bin/env python3

from sys import argv, exit
from os import path, listdir
from os import walk as pwalk
from glob import glob

class progressReport:
	def __init__(self, work_dir):
		self.work_dir = work_dir

	def __progress_trento(self):
		jobN = len(glob(path.join(self.work_dir, "trentojob*")))
		total_events = 0
		total_events_done = 0
		print_total = False
		for jobID in range(jobN):
			job_dir = path.join(self.work_dir, f"trentojob{jobID:d}")
			with open(path.join(job_dir, "trento.conf")) as f:
				while True:
					line = f.readline().rstrip().split()
					if line[0] == "number-events":
						total_events_job = int(line[2])
						break
			total_events += total_events_job
			events_dir  = path.join(job_dir, "eventstemp")
			events_done = len(listdir(events_dir))
			total_events_done += events_done
			if events_done < total_events_job:
				print(f"{path.split(job_dir)[1]:>6s}: {events_done:5d}/{total_events_job:5d}")
				print_total = True
		if print_total:
			print('-'*25)
			print(f"{'total':>10s}: {total_events_done:5d}/{total_events:5d}")

		if not print_total:
			total_events_done = 0
			total_events = 0
			for jobID in range(jobN):
				job_dir = path.join(self.work_dir, f"trentojob{jobID:d}")
				with open(path.join(job_dir, "trento.conf")) as f:
					while True:
						line = f.readline().rstrip().split()
						if line[0] == "number-events":
							total_events_job = int(line[2])
							break
				total_events += total_events_job
				events_dir  = path.join(job_dir, "eventstemp")
				events_done = len([f for f in listdir(events_dir) if "bcp" in f])
				total_events_done += events_done
				if events_done < total_events_job:
					print(f"bcp{path.split(job_dir)[1]:>6s}: {events_done:5d}/{total_events_job:5d}")
					print_total = True
			if print_total:
				print('-'*28)
				print(f"{'total':>13s}: {total_events_done:5d}/{total_events:5d}")

		if "trentoic" in listdir(self.work_dir):
			trentoic_events = len(listdir(path.join(self.work_dir, "trentoic")))
			print(f"trentoic: {trentoic_events:5d}/{2*total_events:5d}")

	def __progress_hydro(self):
		jobN     = len([path.join(self.work_dir, f) for f in listdir(self.work_dir) if path.isdir(path.join(self.work_dir, f))])
		total_events = 0
		total_events_done = 0
		for jobID in range(jobN):
			job_dir = path.join(self.work_dir, f"job{jobID:d}")
			total_events_job = len([f for f in listdir(job_dir) if "event" in f])
			total_events += total_events_job
			events_done  = 0
			for root, dirs, files in pwalk(job_dir):
				if "eventdone.info" in files: events_done += 1
			total_events_done += events_done
			if events_done < total_events_job:
				print(f"{path.split(job_dir)[1]:>6s}: {events_done:3d}/{total_events_job:3d}")
		print('-'*18)
		print(f"{'total':>6s}: {total_events_done:3d}/{total_events:3d}")

	def __progress_eloss(self):
		total_events = len(listdir(path.join(self.work_dir, "elossjob", "bcp")))
		res_dir = path.join(self.work_dir, "elossjob", "results")
		for p in [["bottom", "b"], ["charm", "c"], ["lquarks", "db"], ["gluon", "g"], ["ch", "ch"]]:
			events_done = len(glob(path.join(res_dir, f"{p[1]:s}*.dat")))
			if events_done < total_events:
				print(f"{p[0]:>7s}: {events_done:4d}/{total_events:4d}")

	def progress_report(self):
		if not path.exists(self.work_dir):
			print("no work in progress")
			return

		if "trentojob0" in listdir(self.work_dir):
			self.__progress_trento()
			return

		if 'job0' in listdir(self.work_dir):
			self.__progress_hydro()
			return

		if 'elossjob' in listdir(self.work_dir):
			self.__progress_eloss()
			return