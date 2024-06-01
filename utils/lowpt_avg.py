#! /usr/bin/env python3

import sys
import math
import cmath

def calculate_mult(multfilelist, multfilepath):
    export_file = open(multfilepath, 'w')
    particles = []
    with open(multfilelist[0], 'r') as f:
        while True:
            line = f.readline().rstrip()
            if not line: break
            particles.append(line.split()[0])
    mults = [0.0]*len(particles)
    for aFile in multfilelist:
        with open(aFile, 'r') as f: lines = f.readlines()
        lines = [float(l.rstrip().split()[1]) for l in lines]
        for p, l in enumerate(lines): mults[p] += l
    mults = [m/len(multfilelist) for m in mults]
    mults = [[particles[p], m] for p,m in enumerate(mults)]
    
    for m in mults: print('{0:>6s} {1:10.5f}'.format(m[0], m[1]), file=export_file)

    export_file.close()

def calculate_vn(qnfilelist, flowfilepath):
    """
    Calculate 2- and 4-particle cumulant flow

    Based on
    A.~Bilandzic, R.~Snellings and S.~Voloshin,
    ``Flow analysis with cumulants: Direct calculations,''
    Phys. Rev. C 83, 044913 (2011)
    doi:10.1103/PhysRevC.83.044913
    [arXiv:1010.0233 [nucl-ex]].
    """

    export_file = open(flowfilepath, 'w')

    Q = {}
    dQ = {}
    for n in range(1, 9):
        Q[n] = None
        dQ[n] = []

    two_corr_norm = 0.0
    two_corr_sum_n2 = 0.0
    two_corr_sum_n3 = 0.0
    two_corr_sum_n4 = 0.0

    two_corr_single_event_n2 = []
    two_corr_single_event_n3 = []
    two_corr_single_event_n4 = []
    Wtwo_single_event = []

    two_diff_norm = {}
    two_diff_sum_n2 = {}
    two_diff_sum_n3 = {}
    two_diff_sum_n4 = {}
    two_diff_single_event_n2 = {}
    two_diff_single_event_n3 = {}
    two_diff_single_event_n4 = {}
    w_two_single_event = {}
    for ipt in range(14):
        two_diff_norm[ipt] = 0.0
        two_diff_sum_n2[ipt] = 0.0
        two_diff_sum_n3[ipt] = 0.0
        two_diff_sum_n4[ipt] = 0.0
        two_diff_single_event_n2[ipt] = []
        two_diff_single_event_n3[ipt] = []
        two_diff_single_event_n4[ipt] = []
        w_two_single_event[ipt] = []

    four_corr_norm = 0.0
    four_corr_sum_n2 = 0.0
    four_corr_sum_n3 = 0.0
    four_corr_sum_n4 = 0.0

    four_corr_single_event_n2 = []
    four_corr_single_event_n3 = []
    four_corr_single_event_n4 = []
    Wfour_single_event = []

    four_diff_norm = {}
    four_diff_sum_n2 = {}
    four_diff_sum_n3 = {}
    four_diff_sum_n4 = {}
    four_diff_single_event_n2 = {}
    four_diff_single_event_n3 = {}
    four_diff_single_event_n4 = {}
    w_four_single_event = {}
    for ipt in range(14):
        four_diff_norm[ipt] = 0.0
        four_diff_sum_n2[ipt] = 0.0
        four_diff_sum_n3[ipt] = 0.0
        four_diff_sum_n4[ipt] = 0.0
        four_diff_single_event_n2[ipt] = []
        four_diff_single_event_n3[ipt] = []
        four_diff_single_event_n4[ipt] = []
        w_four_single_event[ipt] = []

    Nevents = 0
    for arg in qnfilelist:
        M = 0
        dM = 0
        for n in range(1, 9):
            Q[n] = None
            dQ[n] = []
        with open(arg, "r") as qnfile:
            Nevents += 1
            for line in qnfile:
                data = line.split()
                if len(data) == 1:
                    try:
                        M = int(data[0])
                    except ValueError:
                        continue
                elif len(data) == 3:
                    try:
                        n = int(data[0])
                        qn_real = float(data[1])
                        qn_imag = float(data[2])
                        Q[n] = complex(qn_real, qn_imag)
                    except ValueError:
                        continue
                elif len(data) == 4:
                    try:
                        pt = float(data[0])
                        dM = int(data[1])
                        dqn_real = float(data[2])
                        dqn_imag = float(data[3])
                        dQ[n].append((dM, complex(dqn_real, dqn_imag)))
                    except ValueError:
                        continue


        # compute 2-particle and 4-particle correlations
        Q_2_2 = Q[2].real**2 + Q[2].imag**2
        Q_3_2 = Q[3].real**2 + Q[3].imag**2
        Q_4_2 = Q[4].real**2 + Q[4].imag**2
        Wtwo = M * (M - 1)
        two_corr_ev_n2 = (Q_2_2 - M) / Wtwo
        two_corr_ev_n3 = (Q_3_2 - M) / Wtwo
        two_corr_ev_n4 = (Q_4_2 - M) / Wtwo
        two_corr_norm += Wtwo
        two_corr_sum_n2 += two_corr_ev_n2 * Wtwo
        two_corr_sum_n3 += two_corr_ev_n3 * Wtwo
        two_corr_sum_n4 += two_corr_ev_n4 * Wtwo
        two_corr_single_event_n2.append(two_corr_ev_n2)
        two_corr_single_event_n3.append(two_corr_ev_n3)
        two_corr_single_event_n4.append(two_corr_ev_n4)
        Wtwo_single_event.append(Wtwo)

        Q_2_4 = Q_2_2 * Q_2_2
        Q_3_4 = Q_3_2 * Q_3_2
        Q_4_4 = Q_4_2 * Q_4_2
        Q_4_2 = Q[4].real**2 + Q[4].imag**2
        Q_6_2 = Q[6].real**2 + Q[6].imag**2
        Q_8_2 = Q[8].real**2 + Q[8].imag**2
        Re_Q4_cQ2_cQ2 = (Q[4] * Q[2].conjugate() * Q[2].conjugate()).real
        Re_Q6_cQ3_cQ3 = (Q[6] * Q[3].conjugate() * Q[3].conjugate()).real
        Re_Q8_cQ4_cQ4 = (Q[8] * Q[4].conjugate() * Q[4].conjugate()).real
        Wfour = M * (M - 1) * (M - 2) * (M - 3)
        four_corr_ev_n2 = (Q_2_4 + Q_4_2 - 2 * Re_Q4_cQ2_cQ2 - 2 * (2 * (M - 2) * Q_2_2 - M * (M - 3))) / Wfour
        four_corr_ev_n3 = (Q_3_4 + Q_6_2 - 2 * Re_Q6_cQ3_cQ3 - 2 * (2 * (M - 2) * Q_3_2 - M * (M - 3))) / Wfour
        four_corr_ev_n4 = (Q_4_4 + Q_8_2 - 2 * Re_Q8_cQ4_cQ4 - 2 * (2 * (M - 2) * Q_4_2 - M * (M - 3))) / Wfour
        four_corr_norm += Wfour
        four_corr_sum_n2 += four_corr_ev_n2 * Wfour
        four_corr_sum_n3 += four_corr_ev_n3 * Wfour
        four_corr_sum_n4 += four_corr_ev_n4 * Wfour
        four_corr_single_event_n2.append(four_corr_ev_n2)
        four_corr_single_event_n3.append(four_corr_ev_n3)
        four_corr_single_event_n4.append(four_corr_ev_n4)
        Wfour_single_event.append(Wfour)

        cQ_2 = Q[2].conjugate()
        cQ_3 = Q[3].conjugate()
        cQ_4 = Q[4].conjugate()
        cQ_6 = Q[6].conjugate()
        cQ_8 = Q[8].conjugate()
        for ipt in range(len(dQ[2])):
            mpt = dQ[2][ipt][0]   # Particle multiplicity is same for all n
            w_two = mpt * (M - 1)
            dQ_2 = dQ[2][ipt][1]
            dQ_3 = dQ[3][ipt][1]
            dQ_4 = dQ[4][ipt][1]
            dQ_6 = dQ[6][ipt][1]
            dQ_8 = dQ[8][ipt][1]
            if w_two > 0:
                two_diff_ev_n2 = ((dQ_2 * cQ_2).real - mpt) / w_two
                two_diff_ev_n3 = ((dQ_3 * cQ_3).real - mpt) / w_two
                two_diff_ev_n4 = ((dQ_4 * cQ_4).real - mpt) / w_two
            else:
                two_diff_ev_n2 = 0.0
                two_diff_ev_n3 = 0.0
                two_diff_ev_n4 = 0.0
            two_diff_norm[ipt] += w_two
            two_diff_sum_n2[ipt] += two_diff_ev_n2 * w_two
            two_diff_sum_n3[ipt] += two_diff_ev_n3 * w_two
            two_diff_sum_n4[ipt] += two_diff_ev_n4 * w_two
            two_diff_single_event_n2[ipt].append(two_diff_ev_n2)
            two_diff_single_event_n3[ipt].append(two_diff_ev_n3)
            two_diff_single_event_n4[ipt].append(two_diff_ev_n4)
            w_two_single_event[ipt].append(w_two)

            w_four = mpt * (M - 3) * (M - 2) * (M - 1)
            if w_four > 0:
                four_diff_ev_n2 = ((dQ_2 * Q[2] * cQ_2 * cQ_2
                                    - dQ_4 * cQ_2 * cQ_2
                                    - dQ_2 * Q[2] * cQ_4
                                    - 2 * M * dQ_2 * cQ_2
                                    + 7 * dQ_2 * cQ_2
                                    - Q[2] * dQ_2.conjugate()
                                    + dQ_4 * cQ_4
                                    + 2 * dQ_2 * cQ_2).real
                                   - 2 * mpt * Q_2_2 + 2 * mpt * M - 6 * mpt) / w_four

                four_diff_ev_n3 = ((dQ_3 * Q[3] * cQ_3 * cQ_3
                                    - dQ_6 * cQ_3 * cQ_3
                                    - dQ_3 * Q[3] * cQ_6
                                    - 2 * M * dQ_3 * cQ_3
                                    + 7 * dQ_3 * cQ_3
                                    - Q[3] * dQ_3.conjugate()
                                    + dQ_6 * cQ_6
                                    + 2 * dQ_3 * cQ_3).real
                                   - 2 * mpt * Q_3_2 + 2 * mpt * M - 6 * mpt) / w_four

                four_diff_ev_n4 = ((dQ_4 * Q[4] * cQ_4 * cQ_4
                                    - dQ_8 * cQ_4 * cQ_4
                                    - dQ_4 * Q[4] * cQ_8
                                    - 2 * M * dQ_4 * cQ_4
                                    + 7 * dQ_4 * cQ_4
                                    - Q[4] * dQ_4.conjugate()
                                    + dQ_8 * cQ_8
                                    + 2 * dQ_4 * cQ_4).real
                                   - 2 * mpt * Q_4_2 + 2 * mpt * M - 6 * mpt) / w_four
            else:
                four_diff_ev_n2 = 0.0
                four_diff_ev_n3 = 0.0
                four_diff_ev_n4 = 0.0

            four_diff_norm[ipt] += w_four
            four_diff_sum_n2[ipt] += four_diff_ev_n2 * w_four
            four_diff_sum_n3[ipt] += four_diff_ev_n3 * w_four
            four_diff_sum_n4[ipt] += four_diff_ev_n4 * w_four
            four_diff_single_event_n2[ipt].append(four_diff_ev_n2)
            four_diff_single_event_n3[ipt].append(four_diff_ev_n3)
            four_diff_single_event_n4[ipt].append(four_diff_ev_n4)
            w_four_single_event[ipt].append(w_four)

    # calculate the averages
    two_corr_avr_n2 = two_corr_sum_n2 / two_corr_norm
    four_corr_avr_n2 = four_corr_sum_n2 / four_corr_norm
    two_corr_avr_n3 = two_corr_sum_n3 / two_corr_norm
    four_corr_avr_n3 = four_corr_sum_n3 / four_corr_norm
    two_corr_avr_n4 = two_corr_sum_n4 / two_corr_norm
    four_corr_avr_n4 = four_corr_sum_n4 / four_corr_norm

    # Standard error of the weighted mean (bootstrap-verified result)
    # Gatz & Smith, Atmospheric Environment Volume 29, Issue 11, June 1995, Pages 1185-1193
    # First, compute weighted standard deviations of the averages
    wvar_twocorr_n2 = 0.0
    wvar_twocorr_n3 = 0.0
    wvar_twocorr_n4 = 0.0
    for i in range(Nevents):
        wvar_twocorr_n2 += (Wtwo_single_event[i]**2 * (two_corr_single_event_n2[i] - two_corr_avr_n2)**2)
        wvar_twocorr_n3 += (Wtwo_single_event[i]**2 *  (two_corr_single_event_n3[i] - two_corr_avr_n3)**2)
        wvar_twocorr_n4 += (Wtwo_single_event[i]**2 *  (two_corr_single_event_n4[i] - two_corr_avr_n4)**2)

    wvar_fourcorr_n2 = 0.0
    wvar_fourcorr_n3 = 0.0
    wvar_fourcorr_n4 = 0.0
    for i in range(Nevents):
        wvar_fourcorr_n2 += (Wfour_single_event[i]**2 * (four_corr_single_event_n2[i] - four_corr_avr_n2)**2)
        wvar_fourcorr_n3 += (Wfour_single_event[i]**2 * (four_corr_single_event_n3[i] - four_corr_avr_n3)**2)
        wvar_fourcorr_n4 += (Wfour_single_event[i]**2 * (four_corr_single_event_n4[i] - four_corr_avr_n4)**2)

    # the standard error of the weighted mean
    err_twocorr_n2 = math.sqrt(Nevents * wvar_twocorr_n2 / ((Nevents - 1) * two_corr_norm**2))
    err_twocorr_n3 = math.sqrt(Nevents * wvar_twocorr_n3 / ((Nevents - 1) * two_corr_norm**2))
    err_twocorr_n4 = math.sqrt(Nevents * wvar_twocorr_n4 / ((Nevents - 1) * two_corr_norm**2))
    err_fourcorr_n2 = math.sqrt(Nevents * wvar_fourcorr_n2 / ((Nevents - 1) * four_corr_norm**2))
    err_fourcorr_n3 = math.sqrt(Nevents * wvar_fourcorr_n3 / ((Nevents - 1) * four_corr_norm**2))
    err_fourcorr_n4 = math.sqrt(Nevents * wvar_fourcorr_n4 / ((Nevents - 1) * four_corr_norm**2))

    # The cumulants based on average correlations
    c22 = two_corr_avr_n2
    c24 = four_corr_avr_n2 - 2 * two_corr_avr_n2**2

    c32 = two_corr_avr_n3
    c34 = four_corr_avr_n3 - 2 * two_corr_avr_n3**2

    c42 = two_corr_avr_n4
    c44 = four_corr_avr_n4 - 2 * two_corr_avr_n4**2

    # Error propagation ignoring covariance
    c24err = math.sqrt(16 * two_corr_avr_n2**2 * err_twocorr_n2**2 + err_fourcorr_n2**2)
    c34err = math.sqrt(16 * two_corr_avr_n3**2 * err_twocorr_n3**2 + err_fourcorr_n3**2)
    c44err = math.sqrt(16 * two_corr_avr_n4**2 * err_twocorr_n4**2 + err_fourcorr_n4**2)

    # Finally, the harmonics
    try:
        v22 = math.sqrt(c22)
        # Propagated standard deviation
        v22err = err_twocorr_n2 / (2 * v22)
    except ValueError:
        v22 = -1.0
        v22err = -1.0

    try:
        v24 = (-c24)**0.25
        v24err = c24err / (4 * abs(c24)) * v24
    except ValueError:
        v24 = -1.0
        v24err = -1.0

    try:
        v32 = math.sqrt(c32)
        v32err = err_twocorr_n3 / (2 * v32)
    except ValueError:
        v32 = -1.0
        v32err = -1.0

    try:
        v34 = (-c34)**0.25
        v34err = c34err / (4 * abs(c34)) * v34
    except ValueError:
        v34 = -1.0
        v34err = -1.0

    try:
        v42 = math.sqrt(c42)
        v42err = err_twocorr_n4 / (2 * v42)
    except ValueError:
        v42 = -1.0
        v42err = -1.0

    try:
        v44 = (-c44)**0.25
        v44err = c44err / (4 * abs(c44)) * v44
    except ValueError:
        v44 = -1.0
        v44err = -1.0

    print("#Integrated flow:", file=export_file)
    print("#v2{{2}} {:.4f} {:.4f}".format(v22, v22err), file=export_file)
    print("#v2{{4}} {:.4f} {:.4f}".format(v24, v24err), file=export_file)
    print("#v3{{2}} {:.4f} {:.4f}".format(v32, v32err), file=export_file)
    print("#v3{{4}} {:.4f} {:.4f}".format(v34, v34err), file=export_file)
    print("#v4{{2}} {:.4f} {:.4f}".format(v42, v42err), file=export_file)
    print("#v4{{4}} {:.4f} {:.4f}".format(v44, v44err), file=export_file)

    print("#Differential flow:", file=export_file)
    print("#pT v2{{2}} err v2{{4}} err v3{{2}} err v3{{4}} err v4{{2}} err v4{{4}} err", file=export_file)
    for ipt in range(len(dQ[2])):

        if (two_diff_norm[ipt] < 2 or four_diff_norm[ipt] < 2):
            continue

        # calculate the averages
        two_dcorr_avr_n2 = two_diff_sum_n2[ipt] / two_diff_norm[ipt]
        four_dcorr_avr_n2 = four_diff_sum_n2[ipt] / four_diff_norm[ipt]
        two_dcorr_avr_n3 = two_diff_sum_n3[ipt] / two_diff_norm[ipt]
        four_dcorr_avr_n3 = four_diff_sum_n3[ipt] / four_diff_norm[ipt]
        two_dcorr_avr_n4 = two_diff_sum_n4[ipt] / two_diff_norm[ipt]
        four_dcorr_avr_n4 = four_diff_sum_n4[ipt] / four_diff_norm[ipt]

        # weighted standard deviations of the averages
        wvar_twodcorr_n2 = 0.0
        wvar_twodcorr_n3 = 0.0
        wvar_twodcorr_n4 = 0.0
        for i in range(Nevents):
            wvar_twodcorr_n2 += (w_two_single_event[ipt][i]**2
                                 * (two_diff_single_event_n2[ipt][i] - two_dcorr_avr_n2)**2)
            wvar_twodcorr_n3 += (w_two_single_event[ipt][i]**2
                                 *  (two_diff_single_event_n3[ipt][i] - two_dcorr_avr_n3)**2)
            wvar_twodcorr_n4 += (w_two_single_event[ipt][i]**2
                                 *  (two_diff_single_event_n4[ipt][i] - two_dcorr_avr_n4)**2)

        wvar_fourdcorr_n2 = 0.0
        wvar_fourdcorr_n3 = 0.0
        wvar_fourdcorr_n4 = 0.0
        for i in range(Nevents):
            wvar_fourdcorr_n2 += (w_four_single_event[ipt][i]**2
                                  * (four_diff_single_event_n2[ipt][i] - four_dcorr_avr_n2)**2)
            wvar_fourdcorr_n3 += (w_four_single_event[ipt][i]**2
                                  * (four_diff_single_event_n3[ipt][i] - four_dcorr_avr_n3)**2)
            wvar_fourdcorr_n4 += (w_four_single_event[ipt][i]**2
                                  * (four_diff_single_event_n4[ipt][i] - four_dcorr_avr_n4)**2)

        # the standard error of the weighted mean
        err_twodcorr_n2 = math.sqrt(Nevents * wvar_twodcorr_n2 / ((Nevents - 1) * two_diff_norm[ipt]**2))
        err_twodcorr_n3 = math.sqrt(Nevents * wvar_twodcorr_n3 / ((Nevents - 1) * two_diff_norm[ipt]**2))
        err_twodcorr_n4 = math.sqrt(Nevents * wvar_twodcorr_n4 / ((Nevents - 1) * two_diff_norm[ipt]**2))
        err_fourdcorr_n2 = math.sqrt(Nevents * wvar_fourdcorr_n2 / ((Nevents - 1) * four_diff_norm[ipt]**2))
        err_fourdcorr_n3 = math.sqrt(Nevents * wvar_fourdcorr_n3 / ((Nevents - 1) * four_diff_norm[ipt]**2))
        err_fourdcorr_n4 = math.sqrt(Nevents * wvar_fourdcorr_n4 / ((Nevents - 1) * four_diff_norm[ipt]**2))

        # The cumulants based on average correlations
        d22 = two_dcorr_avr_n2
        # note that the latter term is a product of differential and integrated
        d24 = four_dcorr_avr_n2 - 2 * two_dcorr_avr_n2 * two_corr_avr_n2

        d32 = two_dcorr_avr_n3
        d34 = four_dcorr_avr_n3 - 2 * two_dcorr_avr_n3 * two_corr_avr_n3

        d42 = two_dcorr_avr_n4
        d44 = four_dcorr_avr_n4 - 2 * two_dcorr_avr_n4 * two_corr_avr_n4

        # Error propagation ignoring covariance
        d24err = math.sqrt(4 * two_dcorr_avr_n2**2 * err_twocorr_n2**2
                           + 4 * two_corr_avr_n2**2 * err_twodcorr_n2**2
                           + err_fourdcorr_n2**2)
        d34err = math.sqrt(4 * two_dcorr_avr_n3**2 * err_twocorr_n3**2
                           + 4 * two_corr_avr_n3**2 * err_twodcorr_n3**2
                           + err_fourdcorr_n3**2)
        d44err = math.sqrt(4 * two_dcorr_avr_n4**2 * err_twocorr_n4**2
                           + 4 * two_corr_avr_n4**2 * err_twodcorr_n4**2
                           + err_fourdcorr_n4**2)

        # Finally, the harmonics
        try:
            v22 = d22 / math.sqrt(c22)
            # Propagated standard deviation
            v22err = math.sqrt(err_twodcorr_n2**2 / c22 + 0.25 * d22**2 * err_twocorr_n2**2 / c22**3)
        except ValueError:
            v22 = -1.0
            v22err = -1.0

        try:
            v24 = -d24 / (-c24)**0.75
            v24err = math.sqrt(d24err**2 / (-c24.real)**1.5 + 9.0/4.0 * d24**2 / (-c24.real)**3.5 * c24err**2)
        except (ValueError,TypeError):
            v24 = -1.0
            v24err = -1.0

        try:
            v32 = d32 / math.sqrt(c32)
            v32err = math.sqrt(err_twodcorr_n3**2 / c32 + 0.25 * d32**2 * err_twocorr_n3**2 / c32**3)
        except ValueError:
            v32 = -1.0
            v32err = -1.0

        try:
            v34 = -d34 / (-c34)**0.75
            v34err = math.sqrt(d34err**2 / (-c34.real)**1.5 + 9.0/4.0 * d34**2 / (-c34.real)**3.5 * c34err**2)
        except (ValueError,TypeError):
            v34 = -1.0
            v34err = -1.0

        try:
            v42 = d42 / math.sqrt(c42)
            v42err = math.sqrt(err_twodcorr_n4**2 / c42 + 0.25 * d42**2 * err_twocorr_n4**2 / c42**3)
        except ValueError:
            v42 = -1.0
            v42err = -1.0

        try:
            v44 = -d44 / (-c44)**0.75
            v44err = math.sqrt(d44err**2 / (-c44.real)**1.5 + 9.0/4.0 * d44**2 / (-c44.real)**3.5 * c44err**2)
        except (ValueError,TypeError):
            v44 = -1.0
            v44err = -1.0

        ptval = 0.3 + ipt * 0.2
        print("{:.3f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f}".format(ptval, v22, v22err, v24, v24err, v32, v32err, v34, v34err, v42, v42err, v44, v44err), file=export_file)

    export_file.close()