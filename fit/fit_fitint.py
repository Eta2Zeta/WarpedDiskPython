import numpy as np
import os
import matplotlib.pyplot as plt
from fit_intens import fit_intens

def fit_fitint(topdir):
    """
    Test variations in the BB intensity as a function of disk rotation phase and compare to what's observed.
    
    :param topdir: Top directory containing the data
    """
    # Load the pulse profiles (assuming you have a way to load these)
    with open(os.path.join(topdir, 'plnmv.pkl'), 'rb') as f:
        plnmv = pickle.load(f)

    with open(os.path.join(topdir, 'bbnmv.pkl'), 'rb') as f:
        bbnmv = pickle.load(f)
    
    nfits = len(plnmv[0, :])
    intrat = np.zeros(nfits)
    
    for j in range(nfits):
        intrat[j] = np.mean(bbnmv[:, j] / plnmv[:, j])
    
    intrat = intrat / np.mean(intrat)

    # Get the list of directories
    dlist1 = os.listdir(topdir)
    dlist = [d for d in dlist1 if 'obs' in d]


    for i in range(len(dlist)):
        # Get the directory name
        dname = os.path.join(topdir, dlist[i], '')

        print(dlist[i])

        # Calculate the intensity
        intout = fit_intens(dname)
        intoutm = intout / np.mean(intout)

        # Plot the results
        plt.figure()
        plt.plot(intrat, label='Observed')
        plt.plot(intoutm, linestyle='--', label='Simulated')
        plt.legend()
        plt.show()
