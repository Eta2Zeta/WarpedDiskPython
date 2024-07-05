import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pickle

def fit_data(bdir, plot_flag, chisq):
    """
    Test a lightcurve fitting algorithm.
    
    :param bdir: Directory containing the data
    :param plot_flag: Flag to indicate whether to plot the results
    :param chisq: Chi-square value
    """
    quiet = 1
    
    # Load the calculated pulse profiles
    with open(f"{bdir}/profs.npz", 'rb') as f:
        profs_data = np.load(f)

    # Load the pulse profiles from the data
    with open("~/softex/opthick/spec/fits/fits.pkl", 'rb') as f:
        fits_data = np.load(f)
    
    plnmv = fits_data['plnmv']
    xdata = np.linspace(0, 1, len(plnmv[:, 0]))

    nfits = len(plnmv[0, :])

    # Get some profiles (to test, for now)
    xprof = profs_data['x']
    ystars = profs_data['ystars']
    yreps = profs_data['yreps']
    plflv = profs_data['plflv']
    errplflv = profs_data['errplflv']
    bbnmv = profs_data['bbnmv']
    errbbnmv = profs_data['errbbnmv']
    obsids = profs_data['obsids']

    num_profs = len(ystars[0, :])

    fitsout = np.zeros((num_profs, nfits, 7))

    # Get a starting value for the low chisq to come out
    lowchisq = 100.0

    def scale_offs(x, scale, offset):
        """
        Function to scale and offset the profile.
        """
        return scale * np.interp((x + offset) % 1, xprof, prof)

    # Loop over disk precession angles
    for i in range(num_profs):
        ystari = ystars[:, 0]
        yrepi = yreps[:, i]

        p = np.zeros(2)

        # Directory for the disk orientation
        ddir = f'diskphi_{i/float(num_profs):.3f}'

        # Loop over observed pulse profiles
        for j in range(nfits):
            prof = ystari
            diffprof = np.diff(np.concatenate(([prof[-1]], prof)))

            # Make the scaled PL and BB pulse profiles
            plflsc = plflv[:, j] / np.mean(plflv[:, j])
            errplflsc = errplflv[:, j] / np.mean(plflv[:, j])

            bbnmsc = bbnmv[:, j] / np.mean(bbnmv[:, j])
            errbbnmsc = errbbnmv[:, j] / np.mean(bbnmv[:, j])

            p[0] = (np.max(plflsc) - np.min(plflsc)) / 2.0

            iprofmax = np.argmax(prof)
            iplflmax = np.argmax(plflsc)

            offstart = xprof[iprofmax] - xdata[iplflmax]
            if offstart < 0:
                offstart = 1.0 + offstart

            p[1] = offstart

            bounds = ([max(p[0] - 0.2, 0), 0], [p[0] + 0.2, 1])

            # Fit the PL profile
            poutpl, _ = curve_fit(scale_offs, xdata, plflsc, p0=p, bounds=bounds)
            plprof = scale_offs(xprof, *poutpl)
            chisqpl = np.sum(((plflsc - scale_offs(xdata, *poutpl)) / errplflsc) ** 2)
            dofpl = len(xdata) - len(poutpl)

            # Fit the BB profile
            p[1] = poutpl[1]
            bounds = ([max(p[0] - 0.2, 0), poutpl[1]], [p[0] + 0.2, poutpl[1]])
            poutbb, _ = curve_fit(scale_offs, xdata, bbnmsc, p0=p, bounds=bounds)
            bbprof = scale_offs(xprof, *poutbb)
            chisqbb = np.sum(((bbnmsc - scale_offs(xdata, *poutbb)) / errbbnmsc) ** 2)
            dofbb = len(xdata) - len(poutbb)

            if plot_flag == 'y':
                plt.figure()
                plt.subplot(211)
                plt.errorbar(xdata, plflsc, yerr=errplflsc, fmt='o')
                plt.plot(xprof, plprof, linestyle='--')
                plt.subplot(212)
                plt.errorbar(xdata, bbnmsc, yerr=errbbnmsc, fmt='o')
                plt.plot(xprof, bbprof, linestyle='--')
                plt.show()

            fitsout[i, j, :] = [p[0], poutpl[0], poutpl[1], chisqpl / dofpl, poutbb[0], poutbb[1], chisqbb / dofbb]

        with open(f"{bdir}/{ddir}/fit_data.pkl", 'wb') as f:
            pickle.dump({'fitsout': fitsout, 'obsids': obsids}, f)

        chisqmin = np.min(fitsout[:, :, 3])
        if chisqmin < lowchisq:
            lowchisq = chisqmin

    chisq = lowchisq

