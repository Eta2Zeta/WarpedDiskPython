import numpy as np
import matplotlib.pyplot as plt
from scipy.io import readsav
from scale_offs import scale_offs


def fit_test(bdir):
    """
    Tests the fits output by fit_data function.
    """
    # Define constants and settings
    num_phis = 8
    num_obs = 5
    
    # Iterate over observation ids and disk angles
    for j in range(num_obs):
        for i in range(num_phis):
            print(f'i={i}, j={j}')
            
            ddir = f'diskphi_{i/8:.3f}'
            
            # Restore necessary files
            fits_data = readsav(f'{bdir}/{ddir}/fit_data.idl')
            profs = readsav(f'{bdir}/profs.idl')
            fits = readsav('~/softex/opthick/spec/fits/fits.idl')
            
            # Extract necessary data
            ystari = fits_data['ystars'][:, i]
            yrepi = fits_data['yreps'][:, i]
            chisqpl = fits_data['fitsout'][4, j]
            poutpl = fits_data['fitsout'][2:4, j]
            poutbb = fits_data['fitsout'][5:7, j]
            
            # Process pulse profiles
            plflsc = fits['plflv'][:, j] / np.mean(fits['plflv'][:, j])
            errplflsc = fits['errplflv'][:, j] / np.mean(fits['errplflv'][:, j])
            bbnmsc = fits['bbnmv'][:, j] / np.mean(fits['bbnmv'][:, j])
            
            # Apply scale and offset adjustments
            plprof = scale_offs(xprof, poutpl)
            bbprof = scale_offs(xprof, poutbb)
            
            # Prepare data for plotting
            xdata = np.arange(len(plflsc)) / len(plflsc)
            
            # Plotting
            plt.errorbar(xdata, plflsc, yerr=errplflsc, fmt='-', linestyle='None', label='PL Fit Error')
            plt.plot(xprof, plprof, label='PL Profile', linewidth=3)
            
            # Display results
            # print(f'Chi-squared for PL: {chisqpl}')
            # print(f'Max ystari index: {np.argmax(ystari)}')
            
            # Show plot
            plt.legend()
            plt.show()
            
            # Stop after each disk angle
            input("Press Enter to continue to the next angle...")

fit_test('/pool/zeus1/rhickox/beams/warpsx1_0223_all/001obs20tin10tout30tw090th00bm1_35bm2m10lng240/')
