#!/usr/bin/env python3

from os import path, mkdir, rename, listdir
from os import stat
from glob import glob
from re import findall
from time import sleep
from shutil import rmtree
import numpy as np
from struct import pack as spack

class collectData:
	def __init__(self, params):
		self.params = params

	def collect_trento_data(self):

		work_dir = path.abspath("work")
		job_dirs = glob(path.join(work_dir, "trentojob*"))
		job_dirs = sorted(job_dirs, key=lambda x: int(findall("\d+", path.split(x)[-1])[0]))

		while True:
			sleep(2)
			if all([path.exists(path.join(job_dir, "jobdone.info")) for job_dir in job_dirs]):
				break
		sleep(2)
		
		trento_events = np.empty((0, 6), float)
		for job_dir in job_dirs: trento_events = np.concatenate((trento_events, np.loadtxt(path.join(job_dir, "trento_events.dat"))), axis=0)
		sorted_index  = np.lexsort((trento_events[:,5], -trento_events[:,4], -trento_events[:,3], -trento_events[:,2]))
		trento_events = trento_events[sorted_index]
		trento_events = np.hstack((np.array(range(0, trento_events.shape[0]))[...,None], trento_events))
		format, header = "%6d %4d %6d %3d %3d %.5f %.5f", "id_sort job_id event_id npart ncoll TATB b"
		np.savetxt(path.join(work_dir, "trento_events.dat"), trento_events, fmt=format, header=header)

		dest_dir = path.join(work_dir, "trentoic")
		if not path.exists(dest_dir): mkdir(dest_dir)

		for tevent in trento_events:
			rename(path.join(work_dir, f"trentojob{tevent[1]:0.0f}", "eventstemp",    f"{tevent[2]:0.0f}.dat"), path.join(dest_dir,    f"{tevent[0]:0.0f}.dat"))
			rename(path.join(work_dir, f"trentojob{tevent[1]:0.0f}", "eventstemp", f"bcp{tevent[2]:0.0f}.dat"), path.join(dest_dir, f"bcp{tevent[0]:0.0f}.dat"))

		for job_id in range(len(job_dirs)):
			rmtree(path.join(work_dir, job_dirs[job_id]))

	def collect_data(self):

		work_dir = path.abspath("work")
		job_dirs = [path.join(work_dir, "job{0:d}".format(job_id)) for job_id in range(self.params['main']['num_of_jobs'])]

		while True:
			sleep(2)
			if all([path.exists(path.join(job_dir, "jobdone.info")) for job_dir in job_dirs]):
				break
		sleep(2)

		files_to_save = [f for f in listdir(path.join(work_dir, "job0", "event0")) if ".dat" in f]
		files_to_save = list(set(files_to_save) - set(["trentoid.dat"]))
		dest_dirs = {}
		for aFile in files_to_save:
			aDir = path.join(work_dir, aFile.replace(".dat", ""))
			if not path.exists(aDir): mkdir(aDir)
			dest_dirs[aFile] = aDir

		for job_dir in job_dirs:
			event_dirs = [path.join(job_dir, f) for f in listdir(job_dir) if "event" in f]
			for event_dir in event_dirs:
				if stat(path.join(event_dir, "errorrecord.log")).st_size != 0:
					continue
				trento_id = int(np.loadtxt(path.join(event_dir, "trentoid.dat"))[0])
				for aFile in files_to_save:
					rename(path.join(event_dir, aFile), path.join(dest_dirs[aFile], aFile.replace(".dat", f"{trento_id:d}.dat")))
			rmtree(job_dir)

		#averaging multiplicities and flows:
		from utils.lowpt_avg import lowpTAvg
		
		mult_dir = path.join(work_dir, "multiplicities")
		if not path.exists(mult_dir): mkdir(mult_dir)
		flow_dir = path.join(work_dir, "flows")
		if not path.exists(flow_dir): mkdir(flow_dir)

		for centrality in self.params['main']['centrality']:
			event_id_low   = int(centrality.replace('%', '').split('-')[0])
			event_id_low   = int(event_id_low/100.0*self.params['trento']['mb_event_n'])
			event_id_high  = int(centrality.replace('%', '').split('-')[1])
			event_id_high  = int(event_id_high/100.0*self.params['trento']['mb_event_n'])
			
			mult_file_list = [path.join(work_dir, "identified", "identified{0:d}.dat".format(eid)) for eid in range(event_id_low, event_id_high)]
			mult_file_path = path.join(mult_dir, "multiplicity{0:s}.dat".format(centrality.replace('-', '').replace('%', '')))

			qn_file_list   = [path.join(work_dir, "qn", "qn{0:d}.dat".format(eid)) for eid in range(event_id_low, event_id_high)]
			flow_file_path = path.join(flow_dir, "flows{0:s}.dat".format(centrality.replace('-', '').replace('%', '')))

			avg_lowpT = lowpTAvg(mult_file_list, mult_file_path, qn_file_list, flow_file_path)
			avg_lowpT.calculate_mult()
			avg_lowpT.calculate_vn()

		if "identified.dat" not in self.params['analysis']['save_files']:
			rmtree(path.join(work_dir, "identified"))
		if self.params['main']['simulation'] == 'hydro':
			if "qn.dat" not in self.params['analysis']['save_files']:
				rmtree(path.join(work_dir, "qn"))

	def collect_eloss_data(self):

		if self.params['main']['simulation'] != "hybrid":
			return

		work_dir = path.abspath("work")
		job_dir  = path.join(work_dir, "elossjob")

		while True:
			sleep(2)
			if path.exists(path.join(job_dir, "jobdone.info")):
				break
		sleep(2)
		
		if "dists" in self.params['dreena']['save_files']:
			res_dir   = path.join(job_dir, "results")
			eid_list  = [int(findall(r"\d+", f)[0]) for f in listdir(res_dir)]
			eid_list  = sorted(list(set(eid_list)))
			pCodeList = list(set(["".join(c for c in f.split('.')[0] if c.isalpha()) for f in listdir(res_dir)]))
			for pcode in pCodeList:
				dist_bin_file = open(path.join(job_dir, "highpt", f"{pcode:s}.dat"), 'wb')
				dist     = np.loadtxt(path.join(res_dir, f"{pcode:s}{eid_list[0]:d}.dat"))
				pTGrid   = np.unique(np.sort(dist[:, 0]))
				binout   = spack('i', int(pTGrid.size))
				dist_bin_file.write(binout)
				pTGrid   = [float(x) for x in pTGrid]
				binout   = spack('d'*len(pTGrid), *pTGrid)
				dist_bin_file.write(bytes(binout))
				phiGrid  = np.unique(np.sort(dist[:, 1]))
				binout   = spack('i', int(phiGrid.size))
				dist_bin_file.write(binout)
				phiGrid  = [float(x) for x in phiGrid]
				binout   = spack('d'*len(phiGrid), *phiGrid)
				dist_bin_file.write(bytes(binout))
				for eid in eid_list:
					binout   = spack('i', int(eid))
					dist_bin_file.write(binout)
					dist = np.loadtxt(path.join(res_dir, f"{pcode:s}{eid:d}.dat"))
					dist = [float(x) for x in dist[:, 2]]
					binout   = spack('d'*len(dist), *dist)
					dist_bin_file.write(bytes(binout))

		src_dir  = path.join(job_dir, "highpt")
		dest_dir = path.join(work_dir, "highpt")
		if not path.exists(dest_dir): mkdir(dest_dir)
		for aFile in listdir(src_dir): rename(path.join(src_dir, aFile), path.join(dest_dir, aFile))
		rmtree(job_dir)

		if "bcp.dat" not in self.params['trento']['save_files']:
			rmtree(path.join(job_dir, "bcp"))
		else:
			rename(path.join(job_dir, "bcp"), path.join(work_dir, "bcp"))
		if "Temp_evo.dat" not in self.params['hydro']['save_files']:
			rmtree(path.join(job_dir, "Temp_evo"))
		else:
			rename(path.join(job_dir, "Temp_evo"), path.join(work_dir, "Temp_evo"))
		if "qn.dat" not in self.params['analysis']['save_files']:
			rmtree(path.join(job_dir, "qn"))
		else:
			rename(path.join(job_dir, "qn"), path.join(work_dir, "qn"))

	def collect_all(self):

		run_id = len([f for f in listdir(path.abspath("")) if "analysis" in f])
		rename(path.abspath("work"), path.abspath(f"analysis{run_id:d}"))