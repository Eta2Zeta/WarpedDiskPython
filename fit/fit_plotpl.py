import os
import numpy as np
import matplotlib.pyplot as plt
import pickle
from scipy.interpolate import interp1d

def fit_plotpl(bdir, chisqlim, print_output, double):
    """
    Test a lightcurve fitting algorithm.

    :param bdir: Base directory containing the data
    :param chisqlim: Chi-square limit for plotting
    :param print_output: Flag to indicate whether to print the output
    :param double: Flag to indicate whether to double the plots
    """

    def scale_offs(x, p):
        """
        Scale and offset function for fitting.
        """
        scale, offset = p
        f = interp1d(np.arange(len(x)), x, fill_value="extrapolate")
        return scale * f(x + offset)

    # Load the calculated pulse profiles
    with open(os.path.join(bdir, 'profs.pkl'), 'rb') as f:
        profs_data = pickle.load(f)
    
    xprof = profs_data['x']
    ystars = profs_data['ystars']
    yreps = profs_data['yreps']

    # Load the pulse profiles from the data
    with open(os.path.expanduser('~/softex/opthick/spec/fits/fits.pkl'), 'rb') as f:
        fits_data = pickle.load(f)

    plnmv = fits_data['plnmv']
    bbnmv = fits_data['bbnmv']
    errplflv = fits_data['errplflv']
    errbbnmv = fits_data['errbbnmv']

    ndata = plnmv.shape[0]
    xdata = np.arange(ndata) / float(ndata)
    nfits = plnmv.shape[1]
    num_profs = ystars.shape[1]

    # Initialize arrays
    fitsout = np.zeros((8, nfits))
    chisqbb = np.zeros((num_profs, nfits))
    chisqbbmin = np.zeros(nfits)

    # Calculate chi-square values for each profile
    for i in range(num_profs):
        ddir = f'diskphi_{i / float(num_profs):.3f}'
        with open(os.path.join(bdir, ddir, 'fit_data.pkl'), 'rb') as f:
            fit_data = pickle.load(f)
        chisqbb[i, :] = fit_data['fitsout'][7, :]

    for j in range(nfits):
        chisqbbmin[j] = np.min(chisqbb[:, j])

    if np.sum(chisqbbmin < chisqlim) > 2:
        if not double:
            plt.figure(figsize=(nfits * 3, (num_profs + 1) * 3))

        if print_output == 'y':
            plt.savefig(os.path.join(bdir, 'bbprofs.pdf'))

        for i in range(num_profs):
            ddir = f'diskphi_{i / float(num_profs):.3f}'
            with open(os.path.join(bdir, ddir, 'fit_data.pkl'), 'rb') as f:
                fit_data = pickle.load(f)

            for j in range(nfits):
                ystari = ystars[:, i]
                yrepi = yreps[:, i]

                print(f'plotting {ddir}{fits_data["obsids"][j]} chisq: {chisqbb[i, j]}')

                chisqpl = fit_data['fitsout'][4, j]
                poutpl = fit_data['fitsout'][2:4, j]
                poutbb = fit_data['fitsout'][5:7, j]

                prof = ystari
                diffprof = np.diff(np.concatenate(([prof[0]], prof)))

                plflsc = plnmv[:, j] / np.mean(plnmv[:, j])
                errplflsc = errplflv[:, j] / np.mean(plflv[:, j])
                bbnmsc = bbnmv[:, j] / np.mean(bbnmv[:, j])
                errbbnmsc = errbbnmv[:, j] / np.mean(bbnmv[:, j])

                plprof = scale_offs(xprof, poutpl)
                bbprof = scale_offs(xprof, poutbb)

                if double == 'y':
                    plt.figure(figsize=(6, 12))
                    plt.subplot(2, 1, 1)
                    plt.errorbar(xdata, plflsc, yerr=errplflsc, fmt='o')
                    plt.plot(xprof, plprof, linewidth=4)
                    plt.subplot(2, 1, 2)
                    plt.errorbar(xdata, bbnmsc, yerr=errbbnmsc, fmt='o')
                    plt.plot(xprof, bbprof, linewidth=4)
                    plt.savefig(os.path.join(bdir, ddir, f'fit_data_{fits_data["obsids"][j]}.pdf'))
                    plt.close()

                if i == 0 and j == 0 and not double:
                    plt.subplot(num_profs + 1, nfits, j + 1)
                    plt.errorbar(xdata, plflsc, yerr=errplflsc, fmt='o')
                    plt.plot(xprof, plprof, linewidth=4)
                    plt.title(bdir)
                else:
                    plt.subplot(num_profs + 1, nfits, i * nfits + j + 1)
                    plt.errorbar(xdata, plflsc, yerr=errplflsc, fmt='o')
                    plt.plot(xprof, plprof, linewidth=4)

                plt.subplot(num_profs + 1, nfits, (i + 1) * nfits + j + 1)
                plt.errorbar(xdata, bbnmsc, yerr=errbbnmsc, fmt='o')
                plt.plot(xprof, bbprof, linewidth=4)

        if print_output == 'y':
            plt.savefig(os.path.join(bdir, 'bbprofs.pdf'))
        plt.show()
