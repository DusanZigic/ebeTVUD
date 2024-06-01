#!/usr/bin/env python3

from params import params
from utils.prerequisites import prerequisites
from utils.update_parameters import update_params
from utils.generate_jobs import generateJobs
from utils.submit_jobs import submitJobs
from utils.collect_data import collectData

if __name__ == '__main__':

	# updating parameters:
	update_params()

	cp = prerequisites(params)
	gj = generateJobs(params)
	sj = submitJobs(params)
	cd = collectData(params)
	
	# checking prerequisites and executiables and recompile:
	cp.check_prerequisites()
	cp.check_execs()
	cp.recompile()


	# trento:
	gj.gen_trento_jobs()
	sj.submit_trento_jobs()
	cd.collect_trento_data()

	# freestream+hydro+frzout+urqmd:
	gj.gen_jobs()
	sj.submit_jobs()
	cd.collect_data()

	# dreena:
	gj.gen_eloss_jobs()
	sj.submit_eloss_jobs()
	cd.collect_eloss_data()

	# collect all model predictions:
	cd.collect_all()