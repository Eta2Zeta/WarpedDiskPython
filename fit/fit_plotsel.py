import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def scale_offs(xdata, p, xprof, prof, diffprof):
    """Scale and phase shift the calculated lightcurves to fit the observed data."""
    scale, offset = p
    interp_func = interp1d(xprof, prof, kind='linear', fill_value="extrapolate")
    interp_diff_func = interp1d(xprof, diffprof, kind='linear', fill_data="extrapolate")
    xpdata2 = (xdata + offset) % 1
    return 1 + scale * (interp_func(xpdata2) - np.mean(prof))

def fit_plotsel(bdir, chisqlim, print_output, double):
    """
    Fit and plot pulse profiles based on chi-square criteria.
    
    Parameters:
        bdir (str): Base directory containing the data.
        chisqlim (float): Chi-square limit for plotting.
        print_output (bool): Flag to indicate if output should be printed.
        double (bool): Flag to indicate if plots should be doubled.
    """
    # Load data
    with open(f'{b_path}/profs.pkl', 'rb') as file:
        profs_data = pickle.load(file)
    xprof = profs_data['x']
    ystars = profs_data['ystars']
    yreps = profs_data['yreps']

    # Load fits data
    with open(f'{b_path}/fits.pkl', 'rb') as file:
        fits_data = pickle.load(file)
    plnmv = fits_data['plnmv']
    bbnmv = fits_data['bbnmv']
    errplflv = fits_data['errplflv']
    errbbnmv = fits_data['errbbnmv']

    num_profs = ystars.shape[1]
    chisqbb = np.zeros((num_profs, nfits))
    chisqbbmin = np.zeros(nfits)

    # Evaluate chi-square values
    for i in range(num_profs):
        ddir = f'{bdir}/diskphi_{i/num_profs:.3f}'
        with open(f'{ddir}/fit_data.pkl', 'rb') as file:
            fit_data = pickle.load(file)
        chisqbb[i, :] = fit_data['fitsout'][7, :]

    chisqbbmin = np.min(chisqbb, axis=0)

    if np.sum(chisqbbmin < chisqlim) > 2:
        for i in range(num_profs):
            ddir = f'{bdir}/diskphi_{i/num_profs:.3f}'
            with open(f'{ddir}/fit_data.pkl', 'rb') as file:
                fit_data = pickle.load(file)
            for j in range(nfits):
                if chisqbb[i, j] < chisqlim:
                    print(f'Plotting {ddir} {fits_data["obsids"][j]} chi-square: {chisqbb[i, j]}')
                    prof = ystars[:, i]
                    diffprof = np.diff(np.append(prof[-1], prof))  # wrap-around diff
                    plflsc = plnmv[:, j] / np.mean(plnmv[:, j])
                    errplflsc = errplflv[:, j] / np.mean(plflv[:, j])
                    bbnmsc = bbnmv[:, j] / np.mean(bbnmv[:, j])
                    errbbnmsc = errbbnmv[:, j] / np.mean(bbnmv[:, j])
                    poutpl = fit_data['fitsout'][2:4, j]
                    poutbb = fit_data['fitsout'][5:7, j]

                    # Plot
                    plt.figure(figsize=(10, 5))
                    plt.errorbar(xdata, plflsc, yerr=errplflsc, fmt='o')
                    plt.plot(xprof, scale_offs(xprof, poutpl, xprof, prof, diffprof), 'r-', linewidth=4)
                    plt.errorbar(xdata, bbnmsc, yerr=errbbnmsc, fmt='o')
                    plt.plot(xprof, scale_offs(xprof, poutbb, xprof, prof, diffprof), 'g-', linewidth=4)
                    plt.title(f'Profile Fit: {ddir} {fits_data["obsids"][j]}')
                    plt.xlabel('Phase')
                    plt.ylabel('Normalized Intensity')
                    plt.show()

                    if print_output:
                        plt.savefig(f'{ddir}/fit_data_{fits_data["obsids"][j]}.pdf')
                        plt.close()

    if print_output:
        print("Finished plotting all selected profiles.")
