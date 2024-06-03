#!/usr/bin/env python3

from sys import  exit
from os import path, mkdir, rename
from shutil import copy, rmtree
import json
import numpy as np

class generateJobs():
	def __init__(self, params):
		self.params = params
	
	def __gen_trento_conf(self, src_dir, jobid):

		cross_section = {
			200:  4.23,
			2760: 6.40,
			5020: 7.00,
			7000: 7.32,
		}

		event_n_per_job = [self.params['trento']['mb_event_n']//self.params['trento']['num_of_jobs']]*self.params['trento']['num_of_jobs']
		for i in range(self.params['trento']['mb_event_n']-sum(event_n_per_job)):
			event_n_per_job[i % self.params['trento']['num_of_jobs']] += 1
		event_n_per_job = event_n_per_job[jobid]

		with open(path.join(src_dir, 'trento.conf'), 'w') as f:
			f.write(f"projectile = {self.params['trento']['projectile']}\n")
			f.write(f"projectile = {self.params['trento']['target']}\n")
			
			f.write(f"number-events = {event_n_per_job:d}\n")
			
			f.write(f"grid-max = {self.params['trento']['grid_max']:.6f}\n")
			f.write(f"grid-step = {self.params['trento']['grid_step']:.6f}\n")
			
			f.write(f"cross-section = {cross_section[self.params['trento']['ecm']]:.6f}\n")
			
			f.write(f"reduced-thickness = {self.params['trento']['p']:.6f}\n")
			f.write(f"normalization = {self.params['trento']['norm']:.6f}\n")
			f.write(f"fluctuation = {self.params['trento']['k']:.6f}\n")
			f.write(f"nucleon-width = {self.params['trento']['w']:.6f}\n")
			f.write(f"nucleon-min-dist = {self.params['trento']['d']:.6f}\n")
			
			f.write("ncoll = true\n")
			f.write("no-header = true\n")
			f.write(f"output = {path.join(src_dir, 'eventstemp')}\n")
			if self.params['trento']['trento_seed'] and self.params['trento']['trento_seed'] > 0:
				f.write(f"random-seed = {self.params['trento']['trento_seed']:d}\n")

	def __gen_slurm_job_trento(self, src_dir, jobid):
		
		trento_src_dir  = path.abspath("models")
		trento_src_dir  = path.join(trento_src_dir, "trento", "build", "src")

		event_n_per_job = [self.params['trento']['mb_event_n']//self.params['trento']['num_of_jobs']]*self.params['trento']['num_of_jobs']
		for i in range(self.params['trento']['mb_event_n']-sum(event_n_per_job)):
			event_n_per_job[i % self.params['trento']['num_of_jobs']] += 1
		event_n_per_job = event_n_per_job[jobid]

		eventTiming = int(event_n_per_job*0.01)+1

		with open(path.join(src_dir, "jobscript.slurm"), 'w') as f:
			f.write("#!/bin/bash\n")
			f.write("#\n")
			f.write(f"#SBATCH --job-name=trento{jobid:d}\n")
			f.write("#SBATCH --output=outputfile.txt\n")
			f.write("#\n")
			f.write("#SBATCH --ntasks=1\n")
			f.write("#SBATCH --cpus-per-task=1\n")
			f.write(f"#SBATCH --time={eventTiming:d}:00:00\n\n")
			f.write(f"(cd {trento_src_dir}\n")
			f.write(f"	./trento -c {path.join(src_dir, 'trento.conf')} > {path.join(src_dir, 'trento_events.dat')}\n")
			f.write(")\n\n")
			f.write("python3 gen_bcp.py\n\n")
			f.write("echo 'job done' > jobdone.info")

	def gen_trento_jobs(self):
		
		work_dir = path.abspath('work')
		if path.exists(work_dir): rmtree(work_dir)
		mkdir(work_dir)

		#exporting parameters to json file:
		json_params = json.dumps(self.params, indent=4)
		with open(path.join(work_dir, "params.json"), 'w') as f: f.write(json_params)

		for job_id in range(self.params['trento']['num_of_jobs']):
			
			job_dir = path.join(work_dir, f"trentojob{job_id:d}")
			if not path.exists(job_dir): mkdir(job_dir)

			copy(path.abspath("utils/gen_bcp.py"), job_dir)

			self.__gen_trento_conf(job_dir, job_id)
			self.__gen_slurm_job_trento(job_dir, job_id)

	def __gen_hydro_conf(self, src_dir):
		with open(path.join(src_dir, "osu-hydro.conf"), 'w') as f:
			f.write(f"{self.params['hydro']['T0']:.6f}\n")
			f.write(f"{self.params['hydro']['IEin']:d}\n")
			f.write(f"{self.params['hydro']['InitialURead']:d}\n")
			f.write(f"{self.params['hydro']['Initialpitensor']:d}\n\n")

			f.write(f"{self.params['hydro']['DT']:.6f}\n")
			f.write(f"{self.params['hydro']['DXY']:.6f}\n")
			f.write(f"{self.params['hydro']['NLS']:d}\n\n")

			f.write(f"{self.params['hydro']['Edec']:.6f}\n")
			f.write(f"{self.params['hydro']['NDT']:d}\n")
			f.write(f"{self.params['hydro']['NDXY']:d}\n\n")

			f.write(f"{self.params['hydro']['ViscousEqsType']:d}\n\n")

			f.write(f"{self.params['hydro']['VisT0']:.6f}\n")
			f.write(f"{self.params['hydro']['VisHRG']:.6f}\n")
			f.write(f"{self.params['hydro']['VisMin']:.6f}\n")
			f.write(f"{self.params['hydro']['VisSlope']:.6f}\n")
			f.write(f"{self.params['hydro']['VisCrv']:.6f}\n")
			f.write(f"{self.params['hydro']['VisBeta']:.6f}\n\n")

			f.write(f"{self.params['hydro']['VisBulkT0']:.6f}\n")
			f.write(f"{self.params['hydro']['VisBulkMax']:.6f}\n")
			f.write(f"{self.params['hydro']['VisBulkWidth']:.6f}\n")
			f.write(f"{self.params['hydro']['IRelaxBulk']:d}\n")
			f.write(f"{self.params['hydro']['BulkTau']:.6f}\n")

	def __gen_job_script(self, jobid, eventN):
		workdir = path.abspath("work")
		jobdir  = path.join(workdir, f"job{jobid:d}")
		with open(path.join(jobdir, "jobscript.slurm"), 'w') as f:
			f.write("#!/usr/bin/env bash\n")
			f.write("#\n")
			f.write(f"#SBATCH --job-name=job{jobid:d}\n")
			f.write("#SBATCH --output=outputfile.txt\n")
			f.write("#\n")
			f.write("#SBATCH --ntasks=1\n")
			f.write("#SBATCH --cpus-per-task=1\n")
			f.write(f"#SBATCH --time={eventN*2:d}:00:00\n\n")
			for event_id in range(eventN):
				f.write(f"(cd event{event_id:d}; python3 run_event.py;)\n")
			f.write("\n")
			f.write("echo 'job done' > jobdone.info")

	def gen_jobs(self):

		work_dir = path.abspath("work")
		if not path.exists(work_dir):
			print("Error: unable to find work directory. Aborting...")
			exit()

		mdl_dir   = path.abspath("models")
		utils_dir = path.abspath("utils")

		json_params = json.dumps(self.params, indent=4)

		trento_events = np.loadtxt(path.abspath("work/trento_events.dat"))
		cent_lows     = [int(c.replace('%', '').split('-')[0]) for c in self.params['main']['centrality']]
		evid_low      = int(min(cent_lows)/100.0*trento_events.shape[0])
		cent_highs    = [int(c.replace('%', '').split('-')[1]) for c in self.params['main']['centrality']]
		evid_high     = int(max(cent_highs)/100.0*trento_events.shape[0])
		trento_events = trento_events[evid_low:evid_high, :]

		from utils.opt_sort_events import optEventSort
		osevents = optEventSort(self.params['main']['num_of_jobs'], trento_events.shape[0])
		opt_sorted_events = osevents.sort_events_opt()

		for job_id in range(self.params['main']['num_of_jobs']):
			
			job_dir = path.join(work_dir, f"job{job_id:d}")
			if not path.exists(job_dir): mkdir(job_dir)

			for event_id in range(len(opt_sorted_events[job_id])):

				event_dir = path.join(job_dir, f"event{event_id:d}")
				if not path.exists(event_dir): mkdir(event_dir)

				with open(path.join(event_dir, "params.json"), 'w') as f: f.write(json_params)

				np.savetxt(path.join(event_dir, "trentoid.dat"), [trento_events[opt_sorted_events[job_id][event_id]]], fmt="%6d %4d %6d %3d %3d %.5f %.5f",\
					header="id_sort job_id event_id npart ncoll TATB b")
				rename(path.join(work_dir, "trentoic", f"{trento_events[opt_sorted_events[job_id][event_id],0]:0.0f}.dat"), path.join(event_dir, "sd.dat"))
				rename(path.join(work_dir, "trentoic", f"bcp{trento_events[opt_sorted_events[job_id][event_id],0]:0.0f}.dat"), path.join(event_dir, "bcp.dat"))

				if self.params['freestream']['turn_on'] == 1:
					copy(path.join(mdl_dir, "freestream", "streamIC.py"), event_dir)

				copy(path.join(mdl_dir, "osu-hydro", "build", "hydro", "bin", "osu-hydro"), event_dir)
				copy(path.join(mdl_dir, "osu-hydro", "eos", "eos.dat"), event_dir)
				self.__gen_hydro_conf(event_dir)

				copy(path.join(mdl_dir, "frzout", "sampleSurface.py"), event_dir)

				copy(path.join(mdl_dir, "urqmd-afterburner", "build", "hadrontransport", "bin", "afterburner"), event_dir)
				copy(path.join(mdl_dir, "urqmd-afterburner", "build", "hadrontransport", "bin", "osc2u"),       event_dir)
				copy(path.join(mdl_dir, "urqmd-afterburner", "build", "hadrontransport", "bin", "urqmd"),       event_dir)

				copy(path.join(utils_dir, "analyse.py"),        event_dir)
				copy(path.join(utils_dir, "reference_flow.py"), event_dir)

				copy(path.join(utils_dir, "run_event.py"), event_dir)

			self.__gen_job_script(job_id, len(opt_sorted_events[job_id]))

		rmtree(path.join(work_dir, "trentoic"))

	def __gen_temp_grids(self, srcdir):
		tau0     = self.params['hydro']['T0']
		tau_step = self.params['hydro']['DT']
		x_min    = 0.0 - self.params['hydro']['DXY']*self.params['hydro']['NLS']
		x_max    = 0.0 + self.params['hydro']['DXY']*self.params['hydro']['NLS']
		x_step   = 0.5
		y_min    = 0.0 - self.params['hydro']['DXY']*self.params['hydro']['NLS']
		y_max    = 0.0 + self.params['hydro']['DXY']*self.params['hydro']['NLS']
		y_step   = 0.5
		with open(path.join(srcdir, "temp_grids.dat"), 'w') as f:
			f.write("#tau0 tau_step\n")
			f.write(f"{tau0:.6f} {tau_step:.6f}\n")
			f.write("#x_min x_max x_step\n")
			f.write(f"{x_min:.6f} {x_max:.6f} {x_step:.6f}\n")
			f.write("#y_min y_max y_step\n")
			f.write(f"{y_min:.6f} {y_max:.6f} {y_step:.6f}\n")

	def __gen_bcpp(self, srcdir):
		BCPP = {"PbPb":
				{"Bottom":  {"10-20%": "8%", "20-30%": "13%", "30-40%": "22%", "40-50%": "40%",},
				"Charm":   {"10-20%": "8%", "20-30%": "13%", "30-40%": "22%", "40-50%": "40%",},
				"LQuarks": {"10-20%": "5%", "20-30%": "8%",  "30-40%": "14%", "40-50%": "25%",},
				"Gluon":   {"10-20%": "5%", "20-30%": "8%",  "30-40%": "14%", "40-50%": "25%",},},
				"AuAu":
				{"Bottom":  {"10-20%": "13%", "20-30%": "22%", "30-40%": "36%", "40-50%": "65%",},
				"Charm":   {"10-20%": "12%", "20-30%": "20%", "30-40%": "34%", "40-50%": "60%",},
				"LQuarks": {"10-20%": "10%", "20-30%": "17%", "30-40%": "28%", "40-50%": "50%",},
				"Gluon":   {"10-20%": "10%", "20-30%": "17%", "30-40%": "28%", "40-50%": "50%",},},
				}
		collsys = self.params['trento']['projectile'] + self.params['trento']['target']
		eventN = self.params['trento']['mb_event_n']
		pNameList = sorted(list(BCPP[collsys].keys()))
		centList  = list(BCPP[collsys][pNameList[0]].keys())
		centList  = sorted(centList, key=lambda x: int(x.split('-')[0]))
		with open(path.join(srcdir, "bcpp.dat"), 'w') as f:
			for pName in pNameList:
				f.write(f"#{pName:s}\n")
				for cent in centList:
					eventIDs = [int(float(cent.replace('%', '').split('-')[0])/100*eventN),\
								int(float(cent.replace('%', '').split('-')[1])/100*eventN)]
					f.write(f"{eventIDs[0]:>6d} {eventIDs[1]:>6d} ")
					f.write(f"{BCPP[collsys][pName][cent]:>7s}\n")

	def __gen_eloss_conf(self, srcdir):
		with open(path.join(srcdir, "dreena.conf"), 'w') as f:
			f.write(f"modelDir = {path.abspath('models/ebetvuddreena')}\n")
			f.write(f"sNN = {self.params['trento']['ecm']:d}GeV\n")
			f.write(f"xB = {self.params['dreena']['xB']:.6f}\n")
			f.write(f"BCPSEED = {self.params['dreena']['BCPSEED']:d}\n")
			f.write(f"phiGridN = {self.params['dreena']['phiGridN']:d}\n")
			f.write(f"TIMESTEP = {self.params['dreena']['TIMESTEP']:.6f}\n")
			f.write(f"TCRIT = {self.params['dreena']['TCRIT']:.6f}\n")
		if path.exists(path.abspath("models/DSSFFs")):
			with open(path.join(srcdir, "dsssffs.conf"), 'w') as f:
				f.write(f"modelDir = {path.abspath('models/DSSFFs')}\n")
				f.write(f"sNN = {self.params['trento']['ecm']:d}GeV\n")
		if path.exists(path.abspath("models/ebeVn")):
			with open(path.join(srcdir, "vn.conf"), 'w') as f:
				f.write(f"modelDir = {path.abspath('models/ebeVn')}\n")
				f.write(f"sNN = {self.params['trento']['ecm']:d}GeV\n")
				f.write(f"eventN = {self.params['trento']['mb_event_n']:d}\n")

	def __gen_eloss_job_script(self, srcdir):
		dreenaTiming = int(200/self.params['dreena']['THREAD_NUM']*self.params['trento']['mb_event_n']/1000)
		with open(path.join(srcdir, "jobscript.slurm"), 'w') as f:
			f.write("#!/bin/bash\n")
			f.write("#\n")
			f.write("#SBATCH --job-name=eloss\n")
			f.write("#SBATCH --output=outputfile.txt\n")
			f.write("#\n")
			f.write("#SBATCH --ntasks=1\n")
			f.write(f"#SBATCH --cpus-per-task={self.params['dreena']['THREAD_NUM']:d}\n")
			f.write(f"#SBATCH --time={dreenaTiming:d}:00:00\n\n")
			f.write(f"python3 run_eloss.py\n")
			f.write("echo 'job done' > jobdone.info")

	def gen_eloss_jobs(self):

		if self.params['main']['simulation'] != 'hybrid':
			return

		work_dir = path.abspath("work")
		if not path.exists(work_dir):
			print("Error: unable to find work directory. Aborting...")
			exit()

		#creating job directory;
		job_dir = path.join(work_dir, "elossjob")
		if path.exists(job_dir): rmtree(job_dir)
		mkdir(job_dir)

		#exporting parameters to json file:
		json_params = json.dumps(self.params, indent=4)
		with open(path.join(job_dir, "params.json"), 'w') as f: f.write(json_params)

		#creating results directory;
		res_dir = path.join(job_dir, "results")
		if not path.exists(res_dir): mkdir(res_dir)

		copy(path.abspath("utils/run_eloss.py"), job_dir)
		copy(path.abspath("models/ebetvuddreena/ebeDREENA"), job_dir)
		if path.exists(path.abspath("models/DSSFFs")):
			copy(path.abspath("models/DSSFFs/DSSFFs"), job_dir)
		if path.exists(path.abspath("models/ebeVn")):
			copy(path.abspath("models/ebeVn/ebeVn"), job_dir)

		rename(path.join(work_dir, "Temp_evo"), path.join(job_dir, "Temp_evo"))
		rename(path.join(work_dir, 		"bcp"), path.join(job_dir, 		"bcp"))
		rename(path.join(work_dir, 		 "qn"), path.join(job_dir, 		 "qn"))

		self.__gen_temp_grids(path.join(job_dir, "Temp_evo"))
		self.__gen_bcpp(job_dir)
		self.__gen_eloss_conf(job_dir)
		self.__gen_eloss_job_script(job_dir)