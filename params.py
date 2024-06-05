params = {
	#############################################################################################################
	#simulation, run and path parameters:
	'main': {
			'simulation':      'hybrid',															   # simulation type;
																									   # possible options: hydro, hybrid (hydro+dreena)

			'centrality':      ['10-20%', '10-30%', '20-30%', '20-40%', '30-40%', '30-50%', '40-50%'], # centralities

			'num_of_jobs':     100,																	   # number of jobs to be created
		    'batch_system':	   'slurm',																   # batch system options: local, slurm
			'event_optimize':  1,																	   # optimize event spliting per jobs; 1 - on, 0 - off

			'recompile':       0, 																	   # option to recompile executables: 0 - do not recompile, 1 - recompile
									   																   # could be used when trento, hydro, urqmd, dreena or dss codes are modified
	},

	#############################################################################################################
	#trento parameters:
	'trento': {
			'mb_event_n':  10000,			   # number of minimum bias events (not recomended to go below 10k)

			'projectile': 'Pb',				   # projectile and target options: p, d, Cu, Cu2, Xe, Xe2, Au, Au2, Pb, U, U2, U3
			'target':	  'Pb',				   # for more details see: http://qcd.phy.duke.edu/trento/
			'ecm':		   5020,			   # collision energy in GeV; trento parameter is nucleon-nucleon cross section,
											   # which is correlated to ecm (see http://qcd.phy.duke.edu/trento/)
			'p':		   0.0,				   # reduced thickness parameter p
			'k':		   1.19,			   # gamma distribution shape parameter for nucleon fluctuations
			'w':		   0.500,			   # Gaussian nucleon width in fm
			'd':		   0.500,			   # minimum nucleon-nucleon distance (fm) for Woods-Saxon nuclei (spherical and deformed)
			'norm': 	   90.00,			   # overall normalization factor

			'grid_max':	   20.05,   		   # x and y maximum of the grid in fm
			'grid_step':   0.1,	   			   # size of grid cell in fm
								   			   # TRENTO grid must be the same as the hydro grid
			'trento_seed': 1,	   			   # random seed for TRENTO event generator; if set to positive integer number of TRENTO jobs is set to 1
								   			   # and each TRENTO run will produce same events
			'save_files':  [],	               # chose which files to save;
									           # options:  sd.dat - entropy density,
									           #		  bcp.dat - binary collisions
	},

	#############################################################################################################
	#freestram parameters:
	'freestream': {
			'turn_on': 			 0, # turn freestream on or off: 1 - on, 0 - off
			'tau_freestream': 1.16, # freestreaming time in fm
									# if freestream is turned on, hydro T0 parameter is automaticaly updated to
									# tau_freestream value - there is no need to manually change T0 below
			'save_files': [],		# chose which files to save;
									# options: ed.dat - the energy density profile
									# 		   u1.dat - initial flow in x-direction at each grid point
									# 		   u2.dat - initial flow in y-direction
									# 		 pi11.dat - pi_xx component of the shear stress tensor at each grid point
									# 		 pi12.dat - pi_xy component of the shear stress tensor
									# 		 pi22.dat - pi_yy component of the shear stress tensor
	},

	#############################################################################################################
	#osu-hydro parameters:
	'hydro': {
			'T0':              1.0,      		 # initial time [fm]
			'IEin':            1,        		 # read initial condition as energy (0) or entropy (1) density
			'InitialURead':    0,        		 # read initial flow and viscous terms if not 0
			'Initialpitensor': 0,        		 # initialize shear tensor with zeros (0) or by Navier-Stokes (1)

			'DT':              0.025,    		 # timestep [fm]
			'DXY':             0.10,     		 # spatial step [fm]
			'NLS':             200,      		 # lattice size from origin (total size = 2*LS + 1)

			'Edec':            0.265,    		 # decoupling energy density [GeV/fm^3]
			'NDT':             1,        		 # freeze-out step in tau direction
			'NDXY':            1,        		 # freeze-out step in x, y directions

			'ViscousEqsType':  2,        		 # old Israel-Stewart (1) or updated 14-moment expansion (2)

			'VisT0':           0.154,    		 # temperature of minimum eta/s [GeV]
			'VisHRG':          0.15,     		 # constant eta/s below T0
			'VisMin':          0.15,     		 # eta/s at T0
			'VisSlope':        0.00,      		 # slope of (eta/s)(T) above T0 [GeV^-1]
			'VisCrv':          0.00,      		 # curvature of (eta/s)(T) above T0 (see readme)
			'VisBeta':         0.833333, 		 # shear relaxation time tau_pi = 6*VisBeta*eta/(sT)

			'VisBulkT0':       0.183,    		 # peak location of Cauchy (zeta/s)(T) [GeV]
			'VisBulkMax':      0.030,    		 # maximum value of zeta/s (at T0)
			'VisBulkWidth':    0.022,    		 # width of (zeta/s)(T) [GeV]
			'IRelaxBulk':      4,        		 # bulk relaxation time: critical slowing down (0), constant (1), 1.5/(2*pi*T) (2), ?? (3), 14-moment result (4)
			'BulkTau':         5.0,      		 # constant bulk relaxation time for IRelaxBulk == 1

			'save_files': 	   [], 				 # chose which files to save;
										 		 # options: Temp_evo.dat    - temperature evolution file
										 		 # 		    surface.dat     - freezout surface
										 		 # 		    eta_per_s_T.dat - eta/s as a function of temperature

	},

	#############################################################################################################
	#freez-out parameters:
	'frzout': {
			'maxsamples': 10, # number of separate particle ensembles from the freeze-out surface (so-called “oversampling”)

			'save_files': [], # chose which files to save;
							  # options: particles_in.dat - particle list produced by cooper-frye
	},

	#############################################################################################################
	#urqmd parameters:
	'urqmd': {

			'save_files': [], # chose which files to save;
							  # options: particles_out.dat - particle list produced by urqmd
	},

	#############################################################################################################
	#analysis parameters:
	'analysis': {

			'save_files': ['qn.dat'], 				# chose which files to save;
							  		  				# options:      dndpt.dat - pT spectrum of charged hadrons at mid(pseudo)rapidity |eta|<0.5
							  		  				#          identified.dat - multiplicities and mean transverse momenta of pions, kaons and
                                                    #							protons at 'id_cuts' (see bellow)
							  		  				#	  	           qn.dat - flow vectors of charged particles at 'vn_cuts' (see bellow) for
                                                    #							harmonics n=1 to 8
							  		  				#            intflows.dat - integrated flows calculated from qn
			'id_cuts': [[-0.5, 0.5], [0.0, 'inf']], # y and pT cuts for identified multiplicities and mean pT
												    # standard values:  ALICE: |y|<0.5, 0.0<pT<inf, 1910.07678
												   	#				   PHENIX: |y|<0.5, 0.0<pT<inf, nucl-ex/0307022
			'vn_cuts': [[-0.8, 0.8], [0.2, 5.0]],   # eta and pT cuts for integrated v_n
													# standard values: ALICE: |eta|<0.8, 0.20<pT<5.0, 1602.01119
													#				    STAR: |eta|<1.3, 0.15<pT<2.0, nucl-ex/0409033
	},

	#############################################################################################################
	#dreena parameters:
	'dreena': {
			'particles':					  '', # chose which particles to calculate;
							      				  # options: ch (charged hadrons), d (d meson), b (b meson); if left empty, all particles will be calculated
			'xB':		      				 0.6, # chromo-magnetic to chromo-electric mass ratio
			
			'BCPP':	       				  'auto', # percentage of binary collisions to be used as jet's initial positions (to be continued...)
			'BCPSEED':						   1, # seed for random generator that selects jet's initial positions from binary collisions;
            									  # value 0 means no seed is set
			'phiGridN':						  25, # number of phi angles
			
			'methods':	  ['SP', 'EP', 'C_F234'], # v_n averaging methods
			'save_files':       ['avg', 'dists'], # chose which files to save;
								   				  # options:   avg - R_AA(pT) and v_n(pT) averaged over events
								   				  # 		    dists - R_AA(pT,phi) distributions for each event in binary format

			'THREAD_NUM':					 112, # number of threads for energy loss calculation (if 0, num_of_jobs parameter will be used)

			'TIMESTEP':						 0.1, # jet's timestep
			'TCRIT':					   0.155, # critical temperature - below TCRIT jet's energy loss stops
	},
}
