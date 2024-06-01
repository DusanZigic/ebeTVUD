#!/usr/bin/env python3

import sys
from os import path
from params import params

from subprocess import call

if __name__ == '__main__':

	sys.path.insert(1, path.abspath('utils'))
	import check_prerequisites as cp
	from update_parameters import update_params
	import generate_jobs as gj
	import submit_jobs as sj
	import collect_data as cd

	#####################################################################
	#updating parameters:
	if not update_params(): sys.exit()

	#####################################################################
	#checking prerequisites and executiables and recompile:
	if not cp.check_prerequisites(): sys.exit()
	if not cp.check_execs():		 sys.exit()
	if not cp.recompile():			 sys.exit()

	#####################################################################
	#running trento:
	gj.gen_trento_jobs()
	sj.submit_trento_jobs()
	cd.collect_trento_data()

	#####################################################################
	gj.gen_jobs()
	sj.submit_jobs()
	cd.collect_data()

	#####################################################################
	gj.gen_eloss_jobs()
	sj.submit_eloss_jobs()
	cd.collect_eloss_data()

	#####################################################################
	#collect all model predictions:
	cd.collect_all()