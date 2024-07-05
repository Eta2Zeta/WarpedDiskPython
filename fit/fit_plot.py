import os
import numpy as np
import matplotlib.pyplot as plt
import pickle
from scipy.interpolate import interp1d

def fit_plot(bdir, chisqlim, print_flag, double, phs0):
    """
    Test a lightcurve fitting algorithm.
    
    :param bdir: Base directory containing the data
    :param chisqlim: Chi-square limit for plotting
    :param print_flag: Flag to indicate whether to print the results
    :param double: Flag to indicate double plotting
    :param phs0: Phase offset
    """

    # Load the calculated pulse profiles
    with open(os.path.join(bdir, 'profs.pkl'), 'rb') as f:
        profs_data = pickle.load(f)

    # Load the pulse profiles from the data
    with open(os.path.expanduser('~/softex/opthick/spec/fits/fits.pkl'), 'rb') as f:
        fits_data = pickle.load(f)

    # Extract data from loaded profiles
    plnmv = fits_data['plnmv']
    bbnmv = fits_data['bbnmv']
    errplflv = fits_data['errplflv']
    errbbnmv = fits_data['errbbnmv']
    ystars = fits_data['ystars']
    yreps = fits_data['yreps']
    obsids = fits_data['obsids']

    # Get number of data points and create x-data for plotting
    ndata = plnmv.shape[0]
    xdata = np.arange(ndata) / float(ndata)

    # Number of fits
    nfits = plnmv.shape[1]

    # Initialize arrays
    num_profs = ystars.shape[1]
    fitsout = np.zeros((num_profs, nfits))

    # Initial low chi-square value
    lowchisq = 100.0

    # Observational IDs
    obsidsh = ['X101', 'X201', 'C1024', 'C1025', 'C1026']

    # Array for chi-square values
    chisqbb = np.zeros((num_profs, nfits))
    chisqbbmin = np.zeros(nfits)

    # Calculate chi-square values for each profile
    for i in range(num_profs):
        ddir = f'diskphi_{i / float(num_profs):.3f}'
        with open(os.path.join(bdir, ddir, 'fit_data.pkl'), 'rb') as f:
            fit_data = pickle.load(f)
        chisqbb[i, :] = fit_data['fitsout'][7, :]

    # Find minimum chi-square values for each fit
    for j in range(nfits):
        chisqbbmin[j] = np.min(chisqbb[:, j])

    if np.sum(chisqbbmin < chisqlim) > 2:
        if double != 'y':
            plt.figure(figsize=(10, 8))

        if print_flag == 'y':
            plt.savefig(os.path.join(bdir, 'bbprofs.png'))

        # Create phi values and sort them according to phase offset
        phis = np.arange(num_profs) / float(num_profs)
        phis2 = (2.0 + np.arange(num_profs) / float(num_profs) - phs0) % 1.0
        iord = np.argsort(phis2)

        for ii in range(num_profs + 1):
            inds = np.concatenate(([0], iord))
            i = inds[ii]

            strphi = f'{phis[i]:.3f}'
            strphi2 = f'{phis2[i]:.3f}'
            ddir = f'diskphi_{strphi}'

            with open(os.path.join(bdir, ddir, 'fit_data.pkl'), 'rb') as f:
                fit_data = pickle.load(f)

            ystari = ystars[:, i]
            yrepi = yreps[:, i]

            for jj in range(nfits):
                jnds = [2, 3, 4, 0, 1]
                j = jnds[jj]

                print(f'plotting {ddir}{obsidsh[j]} chisq: {chisqbb[i, j]}')

                chisqpl = fit_data['fitsout'][4, j]
                poutpl = fit_data['fitsout'][2:4, j]
                poutbb = fit_data['fitsout'][5:7, j]

                plflsc = plnmv[:, j] / np.mean(plnmv[:, j])
                errplflsc = errplflv[:, j] / np.mean(plflv[:, j])

                bbnmsc = bbnmv[:, j] / np.mean(bbnmv[:, j])
                errbbnmsc = errbbnmv[:, j] / np.mean(bbnmv[:, j])

                plprof = scale_offs(xprof, poutpl)
                bbprof = scale_offs(xprof, poutbb)

                if double == 'y':
                    plt.figure(figsize=(10, 8))
                    plt.subplot(2, 1, 1)
                    plt.errorbar(xdata, plflsc, yerr=errplflsc, fmt='o')
                    plt.plot(xprof, plprof, linewidth=4)

                titles = ['C102', 'C103', 'C104', 'X101', 'X201']
                if jj == 4:
                    syrg = [0.85, 1.15]
                    sytv = [0.9, 1.0, 1.1]
                else:
                    syrg = [0.65, 1.43]
                    sytv = [0.75, 1.0, 1.25]

                if ii == 0 and jj == 0 and double != 'y':
                    plt.subplot(num_profs + 1, nfits, 1 + ii * nfits + jj)
                    plt.errorbar(xdata, plflsc, yerr=errplflsc, fmt='o')
                    plt.plot(xprof, plprof, linewidth=4)
                    plt.title(f'!6{titles[jj]}')
                    plt.ylim(0.25, 1.75)
                    plt.yticks([0.5, 1.0, 1.5, 2.0])
                elif ii == 0 and double != 'y':
                    plt.subplot(num_profs + 1, nfits, 1 + ii * nfits + jj)
                    plt.errorbar(xdata, plflsc, yerr=errplflsc, fmt='o')
                    plt.plot(xprof, plprof, linewidth=4)
                    plt.title(f'!6{titles[jj]}')
                    plt.ylim(0.25, 1.75)
                    plt.yticks([0.5, 1.0, 1.5, 2.0])
                else:
                    plt.subplot(num_profs + 1, nfits, 1 + ii * nfits + jj)
                    plt.errorbar(xdata, bbnmsc, yerr=errbbnmsc, fmt='o')
                    plt.plot(xprof, bbprof, linewidth=4)
                    plt.ylim(syrg)
                    plt.yticks(sytv)
                    plt.xticks([0.5, 1.0, 1.5, 2.0])

                if jj == 0 and ii == 0:
                    plt.ylabel('Hard pulses')
                elif jj == 0 and ii != 0:
                    plt.ylabel(f'φ={strphi2}')

                if i == num_profs - 1 and jj == nfits // 2:
                    plt.xlabel('Pulse phase')

                if jj == 0 and i == num_profs // 2 - 2:
                    plt.ylabel('Relative intensity', rotation=90)

        if print_flag == 'y':
            plt.savefig(os.path.join(bdir, 'bbprofs.png'))
            os.system(f'lp {os.path.join(bdir, "bbprofs.png")}')

    plt.show()

def scale_offs(x, p):
    """
    Scale and offset function for fitting.
    """
    scale, offset = p
    return scale * interp1d(np.arange(len(x)), x, fill_value="extrapolate")(x + offset)
