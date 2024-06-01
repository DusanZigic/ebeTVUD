#!/usr/bin/env python3

from os import path
import argparse
from params import params

###################################################################################################################################
#updating dictionary parameters:
def update_params():

	parser = argparse.ArgumentParser()

	#############################################################################################################
	#simulation parameters:
	parser.add_argument('--simulation',     type=str)

	parser.add_argument('--centrality',     type=str)
	
	parser.add_argument('--num_of_jobs',    type=int)
	parser.add_argument('--batch_system',   type=str)
	parser.add_argument('--event_optimize', type=int)
	
	parser.add_argument('--recompile', 	    type=int)

	#############################################################################################################
	#TRENTO parameters:
	parser.add_argument('--mb_event_n',  type=int)

	parser.add_argument('--projectile',	 type=str)
	parser.add_argument('--target', 	 type=str)
	parser.add_argument('--ecm', 		 type=int)

	parser.add_argument('--p',           type=float)
	parser.add_argument('--k',           type=float)
	parser.add_argument('--w',           type=float)
	parser.add_argument('--d',           type=float)
	parser.add_argument('--norm',        type=float)

	parser.add_argument('--grid_max',    type=float)
	parser.add_argument('--grid_step',   type=float)

	parser.add_argument('--trento_seed', type=int)

	#############################################################################################################
	#freestream parameters:
	parser.add_argument('--freestream_on', 	type=int)
	parser.add_argument('--tau_freestream', type=float)
	
	#############################################################################################################
	#osu-hydro parameters:
	parser.add_argument('--T0', 			 type=float)
	parser.add_argument('--IEin',            type=int)
	parser.add_argument('--InitialURead',    type=int)
	parser.add_argument('--Initialpitensor', type=int)

	parser.add_argument('--DT',              type=float)
	parser.add_argument('--DXY',             type=float)
	parser.add_argument('--NLS',             type=int)

	parser.add_argument('--Edec',            type=float)
	parser.add_argument('--NDT',             type=int)
	parser.add_argument('--NDXY',            type=int)

	parser.add_argument('--ViscousEqsType',  type=int)

	parser.add_argument('--VisT0',           type=float)
	parser.add_argument('--VisHRG',          type=float)
	parser.add_argument('--VisMin',          type=float)
	parser.add_argument('--VisSlope',        type=float)
	parser.add_argument('--VisCrv',          type=float)
	parser.add_argument('--VisBeta',         type=float)

	parser.add_argument('--VisBulkT0',       type=float)
	parser.add_argument('--VisBulkMax',      type=float)
	parser.add_argument('--VisBulkWidth',    type=float)
	parser.add_argument('--IRelaxBulk',      type=int)
	parser.add_argument('--BulkTau',         type=float)

	#############################################################################################################
	#ebeDREENA parameters:
	parser.add_argument('--xB', 	    type=float)
	
	parser.add_argument('--BCPP',       type=str)
	parser.add_argument('--BCPSEED',    type=int)
	parser.add_argument('--phiGridN',   type=int)

	parser.add_argument('--methods',    type=str)

	parser.add_argument('--THREAD_NUM', type=int)

	parser.add_argument('--TIMESTEP',   type=float)
	parser.add_argument('--TCRIT',      type=float)

	#############################################################################################################
	args = parser.parse_args()

	#############################################################################################################
	#main parameters:
	if args.simulation     is not None: params['main']['simulation']     = args.simulation

	if args.centrality     is not None: params['main']['centrality']     = args.centrality.split(',')
	
	if args.num_of_jobs    is not None: params['main']['num_of_jobs']    = args.num_of_jobs
	if args.batch_system   is not None: params['main']['batch_system']   = args.batch_system
	if args.event_optimize is not None: params['main']['event_optimize'] = args.event_optimize

	if args.recompile      is not None: params['main']['recompile']      = args.recompile

	#############################################################################################################
	#TRENTO parameters:
	if args.mb_event_n  is not None: params['trento']['mb_event_n']  = args.mb_event_n

	if args.projectile  is not None: params['trento']['projectile']  = args.projectile
	if args.target      is not None: params['trento']['target']      = args.target
	if args.ecm         is not None: params['trento']['ecm']         = args.ecm

	if args.p           is not None: params['trento']['p']           = args.p
	if args.k           is not None: params['trento']['k']           = args.k
	if args.w           is not None: params['trento']['w']           = args.w
	if args.d           is not None: params['trento']['d']           = args.d
	if args.norm        is not None: params['trento']['norm']        = args.norm

	if args.grid_max    is not None: params['trento']['grid_max']    = args.grid_max
	if args.grid_step   is not None: params['trento']['grid_step']   = args.grid_step

	if args.trento_seed is not None: params['trento']['trento_seed'] = args.trento_seed

	#############################################################################################################
	#freestream parameters:
	if args.freestream_on  is not None: params['freestream']['turn_on']        = args.freestream_on
	if args.tau_freestream is not None: params['freestream']['tau_freestream'] = args.tau_freestream
	
	#############################################################################################################
	#osu-hydro parameters:
	if args.T0              is not None: params['hydro']['T0']              = args.T0
	if args.IEin            is not None: params['hydro']['IEin']            = args.IEin
	if args.InitialURead    is not None: params['hydro']['InitialURead']    = args.InitialURead
	if args.Initialpitensor is not None: params['hydro']['Initialpitensor'] = args.Initialpitensor

	if args.DT              is not None: params['hydro']['DT']              = args.DT
	if args.DXY             is not None: params['hydro']['DXY']             = args.DXY
	if args.NLS             is not None: params['hydro']['NLS']             = args.NLS

	if args.Edec            is not None: params['hydro']['Edec']            = args.Edec
	if args.NDT             is not None: params['hydro']['NDT']             = args.NDT
	if args.NDXY            is not None: params['hydro']['NDXY']            = args.NDXY

	if args.ViscousEqsType  is not None: params['hydro']['ViscousEqsType']  = args.ViscousEqsType

	if args.VisT0           is not None: params['hydro']['VisT0']           = args.VisT0
	if args.VisHRG          is not None: params['hydro']['VisHRG']          = args.VisHRG
	if args.VisMin          is not None: params['hydro']['VisMin']          = args.VisMin
	if args.VisSlope        is not None: params['hydro']['VisSlope']        = args.VisSlope
	if args.VisCrv          is not None: params['hydro']['VisCrv']          = args.VisCrv
	if args.VisBeta         is not None: params['hydro']['VisBeta']         = args.VisBeta

	if args.VisBulkT0       is not None: params['hydro']['VisBulkT0']       = args.VisBulkT0
	if args.VisBulkMax      is not None: params['hydro']['VisBulkMax']      = args.VisBulkMax
	if args.VisBulkWidth    is not None: params['hydro']['VisBulkWidth']    = args.VisBulkWidth
	if args.IRelaxBulk      is not None: params['hydro']['IRelaxBulk']      = args.IRelaxBulk
	if args.BulkTau         is not None: params['hydro']['BulkTau']         = args.BulkTau

	#############################################################################################################
	#dreena parameters:
	if args.xB 		   is not None: params['dreena']['xB'] 		   = args.xB
	if args.BCPP       is not None: params['dreena']['BCPP']       = args.BCPP
	if args.BCPSEED    is not None: params['dreena']['BCPSEED']    = args.BCPSEED
	if args.phiGridN   is not None: params['dreena']['phiGridN']   = args.phiGridN

	if args.methods    is not None: params['dreena']['methods']    = args.methods.split('')

	if args.THREAD_NUM is not None: params['dreena']['THREAD_NUM'] = args.THREAD_NUM

	if args.TIMESTEP   is not None: params['dreena']['TIMESTEP']   = args.TIMESTEP
	if args.TCRIT      is not None: params['dreena']['TCRIT']      = args.TCRIT

	#############################################################################################################
	#setting parameters that depend on other dictionary values:

	######################################################################################
	#trento
	if params['trento']['trento_seed'] > 0:
		params['trento']['num_of_jobs'] = 1                             #setting number of trento jobs to 1
	else:
		params['trento']['num_of_jobs'] = params['main']['num_of_jobs'] #setting number of trento jobs to num_of_jobs

	######################################################################################
	#freestreaming
	if params['freestream']['turn_on'] == 1:
		params['hydro']['T0'] =  params['freestream']['tau_freestream']   #setting hydro termalization time to freestream time
		params['hydro']['IEin'] = 0										  #setting read initial condition parameter as energy						
		params['hydro']['InitialURead'] = 1								  #setting read initial flow and viscous terms parameter to true
	if params['freestream']['turn_on'] == 0:
		params['hydro']['IEin'] = 1										  #setting read initial condition parameter as entropy
		params['hydro']['InitialURead'] = 0 						      #setting read initial flow and viscous terms parameter to false

	######################################################################################
	#analysis
	if not isinstance(params['analysis']['save_files'], list):				  #checking if analysis save_files parameter is a list
		params['analysis']['save_files'] = [params['analysis']['save_files']]

	######################################################################################
	#dreena
	if params['dreena']['THREAD_NUM'] == 0:							    #setting eloss NUM_THREADS to num_of_jobs if provided value is 0
		params['dreena']['THREAD_NUM'] = params['main']['num_of_jobs']

	##########################################################################################################
	#checking if provided save files parameters are valid:

	#trento files:
	trento_save_files = ['sd.dat', 'bcp.dat']
	for fs in params['trento']['save_files']:
		if fs not in trento_save_files:
			print('Error: provided trento file to save, {0:s}, not valid. Aborting...'.format(fs))
			return False

	#freestream files:
	freestream_save_files = ['ed.dat', 'u1.dat', 'u2.dat', 'pi11.dat', 'pi12.dat', 'pi22.dat']
	for fs in params['freestream']['save_files']:
		if fs not in freestream_save_files:
			print('Error: provided freestream file to save, {0:s}, not valid. Aborting...'.format(fs))
			return False

	#osu-hydro files:
	osuhydro_save_files = ['Temp_evo.dat', 'surface.dat']
	for fs in params['hydro']['save_files']:
		if fs not in osuhydro_save_files:
			print('Error: provided hydro file to save, {0:s}, not valid. Aborting...'.format(fs))
			return False

	#frzout files:
	frzout_save_files = ['particles_in.dat']
	for fs in params['frzout']['save_files']:
		if fs not in frzout_save_files:
			print('Error: provided freezout file to save, {0:s}, not valid. Aborting...'.format(fs))
			return False

	#urqmd files:
	urqmd_save_files = ['particles_out.dat']
	for fs in params['urqmd']['save_files']:
		if fs not in urqmd_save_files:
			print('Error: provided urqmd file to save, {0:s}, not valid. Aborting...'.format(fs))
			return False

	#analysis files:
	analysis_save_files = ['dndpt.dat', 'identified.dat', 'qn.dat', 'intflows.dat', 'Qn.dat']
	for fs in params['analysis']['save_files']:
		if fs not in analysis_save_files:
			print('Error: provided analysis file to save, {0:s}, not valid. Aborting...'.format(fs))
			return False

	#eloss files:
	eloss_save_files = ['avg', 'dists']
	for fs in params['dreena']['save_files']:
		if fs not in eloss_save_files:
			print('Error: provided dreena file to save, {0:s}, not valid. Aborting...'.format(fs))
			return False	

	##########################################################################################################

	return True
###################################################################################################################################