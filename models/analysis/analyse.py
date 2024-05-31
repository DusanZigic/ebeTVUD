#!/usr/bin/env python3

from itertools import chain, groupby, repeat
import numpy as np
from sys import argv
import json

with open('params.json', 'r') as jsonf: params = json.load(jsonf)

# species (name, ID) for identified particle observables
species = [
    ('pion', 211),
    ('kaon', 321),
    ('proton', 2212),
]

# fully specify numeric data types, including endianness and size, to
# ensure consistency across all machines
float_t = '<f8'
int_t = '<i8'
complex_t = '<c16'

# results "array" (one element)
# to be overwritten for each event
results = np.empty((), dtype=[
    ('nsamples', int_t),
    ('dNch_deta', float_t),
    ('dET_deta', float_t),
    ('dN_dy', [(s, float_t) for (s, _) in species]),
    ('mean_pT', [(s, float_t) for (s, _) in species]),
    ('dN_dpT', (float_t, 14)),
    ('flow', [('N', int_t), ('Qn', complex_t, 8)])
])

# UrQMD raw particle format
parts_dtype = [
    ('sample', int),
    ('ID', int),
    ('charge', int),
    ('pT', float),
    ('ET', float),
    ('mT', float),
    ('phi', float),
    ('y', float),
    ('eta', float)
]

results.fill(0)
nsamples = params['frzout']['maxsamples']
results['nsamples'] = nsamples

# read final particle data
with open('particles_out.dat', 'rb') as f:

    # partition UrQMD file into oversamples
    groups = groupby(f, key=lambda l: l.startswith(b'#'))
    samples = filter(lambda g: not g[0], groups)

    # iterate over particles and oversamples
    parts_iter = (
        tuple((nsample, *l.split()))
        for nsample, (header, sample) in enumerate(samples, start=1)
        for l in sample
    )

    parts = np.fromiter(parts_iter, dtype=parts_dtype)

    charged = (parts['charge'] != 0)
    abs_eta = np.fabs(parts['eta'])

    results['dNch_deta'] = np.count_nonzero(charged & (abs_eta < .5)) / nsamples
    
    ET_eta = .6
    results['dET_deta'] = parts['ET'][abs_eta < ET_eta].sum() / (2*ET_eta) / nsamples

    abs_ID = np.abs(parts['ID'])
    midrapidity = (np.fabs(parts['y']) < .5)

    pT = parts['pT']
    phi = parts['phi']

    for name, i in species:
        cut = (abs_ID == i) & midrapidity
        N = np.count_nonzero(cut)
        results['dN_dy'][name] = N / nsamples
        results['mean_pT'][name] = (0. if N == 0 else pT[cut].mean())

    with open("identified.dat", "w") as idf:
        for name, i in species:
            idf.write(name+" "+str(results['dN_dy'][name])+" "+str(results['mean_pT'][name])+'\n')

    dpt = 0.2
    for ipt in range(14):
        ptmin = 0.2 + ipt * dpt
        ptmax = ptmin + dpt
        pT_alice = pT[charged & (abs_eta < 0.8) & (ptmin < pT) & (pT < ptmax)]
        results['dN_dpT'][ipt] = pT_alice.size / nsamples

    np.savetxt("dndpt.dat", results['dN_dpT'], header=str(results['dNch_deta']))

    phi_alice = phi[charged & (abs_eta < .8) & (.2 < pT) & (pT < 5.)]
    results['flow']['N'] = phi_alice.size
    results['flow']['Qn'] = [
        np.exp(1j*n*phi_alice).sum()
        for n in range(1, results.dtype['flow']['Qn'].shape[0] + 1)
    ]
    with open("qn.dat", "w") as ff:
        ff.write(str(results['flow']['N']))
        ff.write('\n')
        for i in range(8):
            ff.write(str(i+1)+" ")
            ff.write(str(np.real(results['flow']['Qn'][i]))+" "+str(np.imag(results['flow']['Qn'][i])))
            ff.write('\n')
    

