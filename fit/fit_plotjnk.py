import os
import numpy as np
import matplotlib.pyplot as plt
import pickle
from scipy.interpolate import interp1d

def fit_plotjnk(bdir, chisqlim):
    """
    Test a lightcurve fitting algorithm.
    
    :param bdir: Base directory containing the data
    :param chisqlim: Chi-square limit for plotting
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
    fitsout = np.zeros((8, nfits))

    # Initial low chi-square value
    lowchisq = 100.0

    # Observational IDs
    obsidsh = ['X101', 'X201', 'C1024', 'C1025', 'C1026']

    # Array for chi-square values
    chisqbb = np.zeros((num_profs, nfits))
    chisqbbmin = np.zeros(nfits)

    # Calculate chi-square values for each profile
    for i in range(num_profs):
        ystari = ystars[:, i]
        yrepi = yreps[:, i]

        ddir = f'diskphi_{i / float(num_profs):.3f}'
        with open(os.path.join(bdir, ddir, 'fit_data.pkl'), 'rb') as f:
            fit_data = pickle.load(f)

        chisqbb[i, :] = fit_data['fitsout'][7, :]
        chisqpl = fit_data['fitsout'][4, :]

        # Print profiles with chi-square greater than the limit
        if max(chisqpl) > chisqlim:
            ii = np.argmax(chisqpl)
            print(f'{obsidsh[ii]}: {chisqpl[ii]}')

    for j in range(nfits):
        chisqbbmin[j] = np.min(chisqbb[:, j])

    if np.sum(chisqbbmin < chisqlim) > 2:
        for i in range(num_profs):
            ddir = f'diskphi_{i / float(num_profs):.3f}'

            for j in range(nfits):
                print(f'plotting {ddir}{obsidsh[j]} chisq: {chisqbb[i, j]}')
                chisqpl = fit_data['fitsout'][2, j]
                poutpl = fit_data['fitsout'][3:5, j]
                poutbb = fit_data['fitsout'][6:8, j]

                prof = ystari
                diffprof = np.diff(np.concatenate(([prof[0]], prof)))

                plflsc = plnmv[:, j] / np.mean(plnmv[:, j])
                errplflsc = errplflv[:, j] / np.mean(plflv[:, j])

                bbnmsc = bbnmv[:, j] / np.mean(bbnmv[:, j])
                errbbnmsc = errbbnmv[:, j] / np.mean(bbnmv[:, j])

                plprof = scale_offs(xprof, poutpl)
                bbprof = scale_offs(xprof, poutbb)

                plt.figure()
                plt.subplot(2, 1, 1)
                plt.errorbar(xdata, plflsc, yerr=errplflsc, fmt='o')
                plt.plot(xprof, plprof, color='black')
                plt.subplot(2, 1, 2)
                plt.errorbar(xdata, bbnmsc, yerr=errbbnmsc, fmt='o')
                plt.plot(xprof, bbprof, color='black')
                plt.savefig(os.path.join(bdir, ddir, f'fit_data{obsidsh[j]}.png'))
                plt.close()

def scale_offs(x, p):
    """
    Scale and offset function for fitting.
    """
    scale, offset = p
    return scale * interp1d(np.arange(len(x)), x, fill_value="extrapolate")(x + offset)
