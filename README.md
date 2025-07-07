# ebeTVUD

### Trento + Vishnu + Urqmd + Dreena  -  event-by-event

This is a package for full heavy-ion collision simulation performed on even-by-event fluctuating initial conditions. It contains [TRENTO](https://github.com/Duke-QCD/trento) initial conditions, [viscous hydrodynamics](https://github.com/jbernhard/osu-hydro) code, [UrQMD](https://github.com/jbernhard/urqmd-afterburner) afterburner and [ebeDREENA](https://github.com/DusanZigic/ebeDREENA) model for high-pT energy loss calculations, as well as [freestream](https://github.com/Duke-QCD/freestream) and [freezout](https://github.com/Duke-QCD/frzout) modules.

## <1> downloading, prerequisites and compilation

To download entire repository, with version 2.13 of Git and later, us ```--recurse-submodule``` flag when cloning:

```
git clone --recurse-submodule https://github.com/DusanZigic/ebeTVUD.git
```
Otherwise use ```--recursive``` flag:

```
git clone --recursive https://github.com/DusanZigic/ebeTVUD.git
```

Following modules, libraries and compilers are needed:
+ Python 3.5+ with the following modules: numpy, scipy, cython, and h5py
+ C, C++, and Fortran compilers
+ CMake 3.4+
+ Boost, HDF5 and GSL (Gnu Scientific Library) C++ libraries

When running the code, check for all prerequisites is performed, as well as check for all executables. If any of the prerequisites is
not found, executions is stoped and error message is printed. If executables are not found, they are automatically compiled. Output of
compilation is printed to ```compile.info``` file and if compilation is successful, this file is deleted and execution is continued - if not,
execution is stoped and compilation errors can be seen in this file.

## <2> running simulation and parameters

Entire simulation is ran through runHIC.py (run heavy-ion collision) with:
```
./runHIC.py
```
or with:
```
python3 runHIC.py
```

All the parameters are contained within python dictionary in ```params.py```. Details about all parameters and their values are commented in
this file. Different configuration files needed by other modules, e.g. osu-hydro.conf are automatically generated based on the values
from this dictionary.

Parameter values can be overwritten with command line arguments when executing:
```
./runHIC.py --paramName=paramValue
```
For example, default value of number of minimum bias TRENTO events is set to 10 000, through parameter ```mb_event_n```, but this value can bee changed to 100 000 with command line arguments like this:
```
./runHIC.py --mb_event_n=100000
```
Only parameter values that can not be overwritten with command line arguments are options which files to save after the calculation is done (see ```params.py``` for more info).

> [!TIP]
> To check progress, ```--progress``` flag can be used:
```
./runHIC.py --progress
```

When parameter values are overwritten, dictionary values are updated, and this updated dictionary will be saved as json file for record keeping after the calculation is finished.

Certain parameter values depend on other parameter values and if one is changed other one is automatically changed. For example, if freestreaming is turned on, hydro parameters that determine whether to read initial condition as energy or entropy density and wheter or not to read initial flow and viscous terms will be changed. Also, hydro's initial time, ```T0```, will be changed to the value of freestreaming time.

> [!NOTE]
> High-pT energy loss can be turned off by setting ```simulation``` parameter to hydro. In this scenaraio, only TRENTO, hydro, freezout and UrQMD, and freestream if it's turned on, parts of the simulation will be executed.

In [script used to freestream](https://github.com/DusanZigic/freestream/blob/34633c2795a2ce3548dda89730da2950b7e2e0d4/streamIC.py) intial conditions, TRENTO's grid parameters and freestreaming time are set to parameter dictionary value.  
In [script used for freezout](https://github.com/DusanZigic/frzout/blob/0c6d0fa0102714a606aea2b40ba764eacb69db9a/sampleSurface.py), ```Tswitch``` parameter is determined by hydro's decoupling energy parameter, ```Edec``` and equation of state (decoupling energy and/or equation of state can be changed and code would stil be consistent).  
Number of oversamples in [freezout](https://github.com/DusanZigic/frzout/blob/0c6d0fa0102714a606aea2b40ba764eacb69db9a/sampleSurface.py) and [analysys](https://github.com/DusanZigic/ebeTVUD/blob/main/utils/analyse.py) scripts is set to parameter dictionary value.

Cross-section as a TRENTO parameter is automatically determined based on the dictionary parameter value of collision energy - ecm, based on values from [TRENTO documentation page](http://qcd.phy.duke.edu/trento/usage.html).

> [!CAUTION]
> Intial pT distributions are not provided in this repository, however for heavy-flavour they can be downloaded from this [web interface](http://www.lpthe.jussieu.fr/~cacciari/fonll/fonllform.html) or you can use [this script](https://github.com/DusanZigic/heavyQuarkProduction) (see its README for more information).

## <3> outline of the algorithm

First, TRENTO is used to generate initial conditions. TRENTO parameter ```mb_event_n``` is used to determine number of minimum-bias events. If seed is set to pozitive integer, there is one job that runs TRENTO, otherwise there will be ```num_of_jobs``` TRENTO jobs in parallel. When all events are generated, they are sorted based on multiple keys: *npart* (participant number), *ncoll* (number of binary collisions), *TATB* (thickness functions) and *b* (impact parameter), respectively.

Based on centrality classes provided by the user, ```centrality``` parameter, number of events to be evolved is determined. These TRENTO initial condition events are then distributed into jobs. Number of jobs is determined by ```num_of_jobs``` parameter. If ```event_optimize``` parameter is set to 1, distribution of events into jobs is done so that calculation times per single job are as close as possible, i.e. to minimize overhead of some jobs finishing before others. Distribution of events per jobs is done based on participant number, with the assumption that calculation time will be proportional to it.

Evolution of these TRENTO initial condition is done for each job in parallel, event-by-event in each job. This includes freestreaming, if it is turned on, hydro, freezout and afterburner. Script that runs evolution for each event, deletes all unnecessary files while running different parts of the simulation to save storage space. Files that contain multiplicities and qn vectors for each event will be saved since they are needed for averaged multiplicities and integrated flows even if user does not want them saved. Once averaged multiplicities and integrated flows are calculated, multiplicity and qn vectors files are deleted. Same is true for other files, such as binary collision points and temperature evolution files, if simulation is set to hybrid, e.g. if high-pT energy loss is to be performed, these files are saved until energy loss calculation is done after which they are deleted.

After all events are evolved, integrated multiplicities and flows are calculated for centrality classes specified by the user.

If simulation is set to hybrid, single energy loss job is generated and ebeDREENA, a shared memory parallel code, performs energy loss calculation. After RAA(pT,phi) for single particles is generated, fragmentation functions calculate RAA(pT,phi) for charged hadrons, D and B mesons. Based on the centralities provided by the user, averaging over events is performed using methods specified by the user (dreena methods parameter).
> [!NOTE]
> Fragmentation functions are not provide in this repository, which means only bare quark and gluon RAA(pT,phi) will be calculated.

Once entire simulation has completed, data is moved into directory ```analysis[ID]``` in the same directory where runHIC.py is. *ID* in directory name will depend on how many directories with analysis in their name already exist. These can then be renamed by user so that they contain, as an example, parameter values in the name.

In case user changes code that needs to be recompiled, or copies whole package with executables to a different machine, there is a recompile
option - if recompile parameter is set to 1, all c/c++ and fortran codes will be recompiled.

---------------------------------------------------------------
for additional questions contact Zigic Dusan at zigic@ipb.ac.rs
