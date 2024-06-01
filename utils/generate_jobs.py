#!/usr/bin/env python3

from sys import argv, exit
from os import path, listdir, mkdir, rename
from shutil import copy, rmtree, copyfile
from glob import glob
import json
import numpy as np
from params import params

####################################################################################################################################################
#TRENTO JOBS:
####################################################################################
#function that generates trento conf file:
def gen_trento_conf(src_dir, jobid):

	cross_section = {
		200:  4.23,
		2760: 6.40,
		5020: 7.00,
		7000: 7.32,
	}

	event_n_per_job = [params['trento']['mb_event_n']//params['trento']['num_of_jobs']]*params['trento']['num_of_jobs']
	for i in range(params['trento']['mb_event_n']-sum(event_n_per_job)):
		event_n_per_job[i % params['trento']['num_of_jobs']] += 1
	event_n_per_job = event_n_per_job[jobid]

	with open(path.join(src_dir, 'trento.conf'), 'w') as f:
		f.write('projectile = {}\n'.format(params['trento']['projectile']))
		f.write('projectile = {}\n'.format(params['trento']['target']))
		
		f.write('number-events = %d\n' % event_n_per_job)
		
		f.write('grid-max = %f\n' % params['trento']['grid_max'])
		f.write('grid-step = %f\n' % params['trento']['grid_step'])
		
		f.write('cross-section = %f\n' % cross_section[params['trento']['ecm']])
		
		f.write('reduced-thickness = {:.6f}\n'.format(params['trento']['p']))
		f.write('normalization = %f\n' % params['trento']['norm'])
		f.write('fluctuation = %f\n' % params['trento']['k'])
		f.write('nucleon-width = %f\n' % params['trento']['w'])
		f.write('nucleon-min-dist = %f\n' % params['trento']['d'])
		
		f.write('ncoll = true\n')
		f.write('no-header = true\n')
		f.write('output = %s\n' % path.join(src_dir, 'eventstemp'))
		if params['trento']['trento_seed'] and params['trento']['trento_seed'] > 0:
			f.write('random-seed = %d\n' % params['trento']['trento_seed'])
####################################################################################
#function that generates slurm job scripts for trento jobs:
def gen_slurm_job_trento(src_dir, jobid):
	
	trento_src_dir  = path.abspath('models')
	trento_src_dir  = path.join(trento_src_dir, 'trento', 'build', 'src')

	event_n_per_job = [params['trento']['mb_event_n']//params['trento']['num_of_jobs']]*params['trento']['num_of_jobs']
	for i in range(params['trento']['mb_event_n']-sum(event_n_per_job)):
		event_n_per_job[i % params['trento']['num_of_jobs']] += 1
	event_n_per_job = event_n_per_job[jobid]

	with open(path.join(src_dir, 'jobscript.slurm'), 'w') as f:
		f.write('#!/bin/bash\n')
		f.write('#\n')
		f.write('#SBATCH --job-name=trento{0:d}\n'.format(jobid))
		f.write('#SBATCH --output=outputfile.txt\n')
		f.write('#\n')
		f.write('#SBATCH --ntasks=1\n')
		f.write('#SBATCH --cpus-per-task=1\n')
		f.write('#SBATCH --time={0:d}:00:00\n\n'.format(int(event_n_per_job*0.01)+1))
		f.write('(cd {0:s}\n'.format(trento_src_dir))
		f.write('	./trento -c {0:s} > {1:s}\n'.format(path.join(src_dir, 'trento.conf'), path.join(src_dir, 'trento_events.dat')))
		f.write(')\n\n')
		f.write('python3 gen_bcp.py\n\n')
		f.write('echo "job done" > jobdone.info')
####################################################################################
#function that generates trento jobs:
def gen_trento_jobs():
	
	work_dir = path.abspath('work')
	if path.exists(work_dir): rmtree(work_dir)
	mkdir(work_dir)

	#exporting parameters to json file:
	json_params = json.dumps(params, indent=4)
	with open(path.join(work_dir, 'params.json'), 'w') as f: f.write(json_params)

	for job_id in range(params['trento']['num_of_jobs']):
		
		job_dir = path.join(work_dir, 'trentojob%d' % job_id)
		if not path.exists(job_dir): mkdir(job_dir)

		copy(path.abspath('utils/gen_bcp.py'), job_dir)

		gen_trento_conf(job_dir, job_id)
		gen_slurm_job_trento(job_dir, job_id)
##################################################################################################################

####################################################################################################################################################
#FULL JOBS:
####################################################################################
#function that exports hydro parameters:
def gen_hydro_conf(src_dir):
	with open(path.join(src_dir, 'osu-hydro.conf'), 'w') as f:
		f.write('{0:.2f}\n'.format(params['hydro']['T0']))
		f.write('{0:d}\n'.format(params['hydro']['IEin']))
		f.write('{0:d}\n'.format(params['hydro']['InitialURead']))
		f.write('{0:d}\n\n'.format(params['hydro']['Initialpitensor']))

		f.write('{0:.3f}\n'.format(params['hydro']['DT']))
		f.write('{0:.2f}\n'.format(params['hydro']['DXY']))
		f.write('{0:d}\n\n'.format(params['hydro']['NLS']))

		f.write('{0:.3f}\n'.format(params['hydro']['Edec']))
		f.write('{0:d}\n'.format(params['hydro']['NDT']))
		f.write('{0:d}\n\n'.format(params['hydro']['NDXY']))

		f.write('{0:d}\n\n'.format(params['hydro']['ViscousEqsType']))

		f.write('{0:.3f}\n'.format(params['hydro']['VisT0']))
		f.write('{0:.2f}\n'.format(params['hydro']['VisHRG']))
		f.write('{0:.2f}\n'.format(params['hydro']['VisMin']))
		f.write('{0:.1f}\n'.format(params['hydro']['VisSlope']))
		f.write('{0:.1f}\n'.format(params['hydro']['VisCrv']))
		f.write('{0:.6f}\n\n'.format(params['hydro']['VisBeta']))

		f.write('{0:.3f}\n'.format(params['hydro']['VisBulkT0']))
		f.write('{0:.3f}\n'.format(params['hydro']['VisBulkMax']))
		f.write('{0:.3f}\n'.format(params['hydro']['VisBulkWidth']))
		f.write('{0:d}\n'.format(params['hydro']['IRelaxBulk']))
		f.write('{0:.1f}\n'.format(params['hydro']['BulkTau']))

####################################################################################
#function that generates job run script:
def gen_job_script(jobid, eventN):
	workdir = path.abspath('work')
	jobdir  = path.join(workdir, 'job{0:d}'.format(jobid))
	with open(path.join(jobdir, 'jobscript.slurm'), 'w') as f:
		f.write('#!/usr/bin/env bash\n')
		f.write('#\n')
		f.write('#SBATCH --job-name=job{0:d}\n'.format(jobid))
		f.write('#SBATCH --output=outputfile.txt\n')
		f.write('#\n')
		f.write('#SBATCH --ntasks=1\n')
		f.write('#SBATCH --cpus-per-task=1\n')
		f.write('#SBATCH --time={0:d}:00:00\n\n'.format(eventN*2))
		for event_id in range(eventN):
			f.write('(cd event{0:d}; python3 run_event.py;)\n'.format(event_id))
		f.write('\necho "job done" > jobdone.info')

####################################################################################
#function that generates full jobs:
def gen_jobs():

	work_dir = path.abspath('work')
	if not path.exists(work_dir):
		print('Error: no work directory. Aborting...')
		exit()

	mdl_dir   = path.abspath('models')
	utils_dir = path.abspath('utils')

	json_params = json.dumps(params, indent=4)

	trento_events = np.loadtxt(path.abspath('work/trento_events.dat'))
	cent_lows     = [int(c.replace('%', '').split('-')[0]) for c in params['main']['centrality']]
	evid_low      = int(min(cent_lows)/100.0*trento_events.shape[0])
	cent_highs    = [int(c.replace('%', '').split('-')[1]) for c in params['main']['centrality']]
	evid_high     = int(max(cent_highs)/100.0*trento_events.shape[0])
	trento_events = trento_events[evid_low:evid_high, :]

	from opt_sort_events import sort_events_opt
	opt_sorted_events = sort_events_opt(params['main']['num_of_jobs'], trento_events.shape[0])

	for job_id in range(params['main']['num_of_jobs']):
		
		job_dir = path.join(work_dir, 'job{0:d}'.format(job_id))
		if not path.exists(job_dir): mkdir(job_dir)

		for event_id in range(len(opt_sorted_events[job_id])):

			event_dir = path.join(job_dir, 'event{0:d}'.format(event_id))
			if not path.exists(event_dir): mkdir(event_dir)

			with open(path.join(event_dir, 'params.json'), 'w') as f: f.write(json_params)

			np.savetxt(path.join(event_dir, 'trentoid.dat'), [trento_events[opt_sorted_events[job_id][event_id]]], fmt='%6d %4d %6d %3d %3d %.5f %.5f',\
				header='id_sort job_id event_id npart ncoll TATB b')
			rename(path.join(work_dir, 'trentoic',    '{0:0.0f}.dat'.format(trento_events[opt_sorted_events[job_id][event_id],0])),\
					path.join(event_dir, 'sd.dat'))
			rename(path.join(work_dir, 'trentoic', 'bcp{0:0.0f}.dat'.format(trento_events[opt_sorted_events[job_id][event_id],0])),\
					path.join(event_dir, 'bcp.dat'))

			if params['freestream']['turn_on'] == 1: copy(path.join(mdl_dir, 'freestream', 'stream_ic.py'), event_dir)

			copy(path.join(mdl_dir, 'osu-hydro', 'build', 'hydro', 'bin', 'osu-hydro'), event_dir)
			copy(path.join(mdl_dir, 'osu-hydro', 'eos', 'eos.dat'), event_dir)
			gen_hydro_conf(event_dir)

			copy(path.join(mdl_dir, 'frzout', 'sample_surface.py'), event_dir)

			copy(path.join(mdl_dir, 'urqmd-afterburner', 'build', 'hadrontransport', 'bin', 'afterburner'), event_dir)
			copy(path.join(mdl_dir, 'urqmd-afterburner', 'build', 'hadrontransport', 'bin', 'osc2u'),       event_dir)
			copy(path.join(mdl_dir, 'urqmd-afterburner', 'build', 'hadrontransport', 'bin', 'urqmd'),       event_dir)

			copy(path.join(mdl_dir, 'analysis', 'analyse.py'),        event_dir)
			copy(path.join(mdl_dir, 'analysis', 'reference_flow.py'), event_dir)

			copy(path.join(utils_dir, 'run_event.py'), event_dir)

		gen_job_script(job_id, len(opt_sorted_events[job_id]))

	rmtree(path.join(work_dir, 'trentoic'))

####################################################################################################################################################
#ELOSS JOBS:
####################################################################################
#function that generates temperature grid parameters file:
def gen_temp_grids(srcdir):
	tau0     = params['hydro']['T0']
	tau_step = params['hydro']['DT']
	x_min    = 0.0 - params['hydro']['DXY']*params['hydro']['NLS']
	x_max    = 0.0 + params['hydro']['DXY']*params['hydro']['NLS']
	x_step   = 0.5
	y_min    = 0.0 - params['hydro']['DXY']*params['hydro']['NLS']
	y_max    = 0.0 + params['hydro']['DXY']*params['hydro']['NLS']
	y_step   = 0.5
	with open(path.join(srcdir, 'temp_grids.dat'), 'w') as f:
		f.write('#tau0 tau_step\n')
		f.write('{0:.3f} {1:.5f}\n'.format(tau0, tau_step))
		f.write('#x_min x_max x_step\n')
		f.write('{0:.2f} {1:.2f} {2:.5f}\n'.format(x_min, x_max, x_step))
		f.write('#y_min y_max y_step\n')
		f.write('{0:.2f} {1:.2f} {2:.5f}\n'.format(y_min, y_max, y_step))

####################################################################################
def gen_bcpp(srcdir):
	BCPP = {'PbPb':
			{'Bottom':  {'10-20%': '8%', '20-30%': '13%', '30-40%': '22%', '40-50%': '40%',},
			 'Charm':   {'10-20%': '8%', '20-30%': '13%', '30-40%': '22%', '40-50%': '40%',},
			 'LQuarks': {'10-20%': '5%', '20-30%': '8%',  '30-40%': '14%', '40-50%': '25%',},
			 'Gluon':   {'10-20%': '5%', '20-30%': '8%',  '30-40%': '14%', '40-50%': '25%',},},
		    'AuAu':
		    {'Bottom':  {'10-20%': '13%', '20-30%': '22%', '30-40%': '36%', '40-50%': '65%',},
			 'Charm':   {'10-20%': '12%', '20-30%': '20%', '30-40%': '34%', '40-50%': '60%',},
			 'LQuarks': {'10-20%': '10%', '20-30%': '17%', '30-40%': '28%', '40-50%': '50%',},
			 'Gluon':   {'10-20%': '10%', '20-30%': '17%', '30-40%': '28%', '40-50%': '50%',},},
			}
	collsys = params['trento']['projectile'] + params['trento']['target']
	eventN = params['trento']['mb_event_n']
	pNameList = sorted(list(BCPP[collsys].keys()))
	centList  = list(BCPP[collsys][pNameList[0]].keys())
	centList  = sorted(centList, key=lambda x: int(x.split('-')[0]))
	with open(path.join(srcdir, 'bcpp.dat'), 'w') as f:
		for pName in pNameList:
			f.write('#{0:s}\n'.format(pName))
			for cent in centList:
				eventIDs = [int(float(cent.replace('%', '').split('-')[0])/100*eventN),\
							int(float(cent.replace('%', '').split('-')[1])/100*eventN)]
				f.write('{0:>6d} {1:>6d} '.format(*eventIDs))
				f.write('{0:>7s}\n'.format(BCPP[collsys][pName][cent]))

####################################################################################
#function that exports hydro parameters:
def gen_eloss_conf(srcdir):
	with open(path.join(srcdir, 'dreena.conf'), 'w') as f:
		f.write('sNN = {0:d}GeV\n'.format(params['trento']['ecm']))
		f.write('xB = {0:.1f}\n'.format(params['dreena']['xB']))
		f.write('BCPSEED = {0:d}\n'.format(params['dreena']['BCPSEED']))
		f.write('phiGridN = {0:d}\n'.format(params['dreena']['phiGridN']))
		f.write('TIMESTEP = {0:.2f}\n'.format(params['dreena']['TIMESTEP']))
		f.write('TCRIT = {0:.3f}\n'.format(params['dreena']['TCRIT']))
	with open(path.join(srcdir, 'dsssffs.conf'), 'w') as f:
		f.write('sNN = {0:d}GeV\n'.format(params['trento']['ecm']))
	with open(path.join(srcdir, 'vn.conf'), 'w') as f:
		f.write('sNN = {0:d}GeV\n'.format(params['trento']['ecm']))
		f.write('eventN = {0:d}\n'.format(params['trento']['mb_event_n']))

####################################################################################
#function that generates eloss job script:
def gen_eloss_job_script(srcdir):
	dreenadir = path.abspath('models/dreena')
	workdir   = path.abspath('work')
	with open(path.join(srcdir, 'jobscript.slurm'), 'w') as f:
		f.write('#!/bin/bash\n')
		f.write('#\n')
		f.write('#SBATCH --job-name=eloss\n')
		f.write('#SBATCH --output=outputfile.txt\n')
		f.write('#\n')
		f.write('#SBATCH --ntasks=1\n')
		f.write('#SBATCH --cpus-per-task={0:d}\n'.format(params['dreena']['THREAD_NUM']))
		f.write('#SBATCH --time={0:d}:00:00\n\n'.format(int(200/params['dreena']['THREAD_NUM']*params['trento']['mb_event_n']/1000)))
		f.write('python3 run_eloss.py {0:s} {1:s}\n'.format(dreenadir, workdir))
		f.write('\necho "job done" > jobdone.info')

####################################################################################
#function that generates full jobs:
def gen_eloss_jobs():

	if params['main']['simulation'] != 'hybrid': return

	work_dir = path.abspath('work')
	if not path.exists(work_dir):
		print('Error: no work directory. Aborting...')
		exit()

	#creating job directory;
	job_dir = path.join(work_dir, 'elossjob')
	if path.exists(job_dir): rmtree(job_dir)
	mkdir(job_dir)

	#exporting parameters to json file:
	json_params = json.dumps(params, indent=4)
	with open(path.join(job_dir, 'params.json'), 'w') as f: f.write(json_params)

	#creating results directory;
	res_dir = path.join(job_dir, 'results')
	if not path.exists(res_dir): mkdir(res_dir)

	copy(path.abspath('utils/run_eloss.py'), job_dir)

	gen_temp_grids(path.join(work_dir, 'Temp_evo'))
	gen_bcpp(job_dir)
	gen_eloss_conf(job_dir)
	gen_eloss_job_script(job_dir)