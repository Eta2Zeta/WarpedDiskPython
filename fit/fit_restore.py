import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pickle

def scale_offs(xdata, p, xprof, prof):
    """ Scale and offset function for fitting. """
    scale, offset = p
    shifted_xdata = (xdata + offset) % 1  # Wrap around at 1
    return 1 + scale * np.interp(shifted_xdata, xprof, prof - np.mean(prof))

def fit_data(bdir, plot, chisq):
    """ Fit lightcurve data from profiles restored from disk. """
    # Load profiles and fitting data
    with open(f'{bdir}/profs.pkl', 'rb') as file:
        data = pickle.load(file)
    xprof = data['xprof']
    ystars = data['ystars']
    yreps = data['yreps']

    # Parameters and arrays preparation
    nfits = len(data['fits'])
    num_profs = ystars.shape[1]
    fitsout = np.zeros((8, nfits))  # Placeholder for fit outputs

    # Loop over all profiles
    for i in range(num_profs):
        ddir = f'{bdir}/diskphi_{i/num_profs:.3f}'
        ystari = ystars[:, i]
        yrepi = yreps[:, i]
        prof = ystari
        diffprof = np.diff(np.append(prof[-1], prof))  # wrap-around diff

        # Loop over all fit sessions
        for j in range(nfits):
            plflsc = data['plflv'][:, j] / np.mean(data['plflv'][:, j])
            errplflsc = data['errplflv'][:, j] / np.mean(data['plflv'][:, j])
            bbnmsc = data['bbnmv'][:, j] / np.mean(data['bbnmv'][:, j])
            errbbnmsc = data['errbbnmv'][:, j] / np.mean(data['bbnmv'][:, j])

            # Initial parameter estimates
            p_initial = [(np.max(plflsc) - np.min(plflsc)) / 2, xprof[np.argmax(prof)]]
            
            # Fit using curve_fit from scipy.optimize
            popt_pl, pcov_pl = curve_fit(lambda x, scale, offs: scale_offs(x, [scale, offs], xprof, plflsc),
                                         xprof, plflsc, p0=p_initial, sigma=errplflsc, absolute_sigma=True)
            popt_bb, pcov_bb = curve_fit(lambda x, scale, offs: scale_offs(x, [scale, offs], xprof, bbnmsc),
                                         xprof, bbnmsc, p0=popt_pl, sigma=errbbnmsc, absolute_sigma=True)
            
            # Store results
            fitsout[:, j] = [p_initial[0], p_initial[1], popt_pl[0], popt_pl[1], np.nan, popt_bb[0], popt_bb[1], np.nan]

            # Optional plotting
            if plot:
                plt.figure()
                plt.errorbar(xprof, plflsc, yerr=errplflsc, label='PL Data', fmt='o')
                plt.plot(xprof, scale_offs(xprof, popt_pl, xprof, plflsc), label='PL Fit')
                plt.errorbar(xprof, bbnmsc, yerr=errbbnmsc, label='BB Data', fmt='o')
                plt.plot(xprof, scale_offs(xprof, popt_bb, xprof, bbnmsc), label='BB Fit')
                plt.legend()
                plt.title(f'Fits for {ddir}')
                plt.show()

    # Save fitted data
    with open(f'{bdir}/{ddir}/fit_data.pkl', 'wb') as f:
        pickle.dump(fitsout, f)

    # Return the minimum chi-square value as an example output
    return np.min(fitsout[7, :])
