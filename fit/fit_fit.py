import os
import numpy as np
from fit_data import fit_data

def fit_fit(topdir):
    """
    Create input files for doing a set of simulated profiles for several disk and beam shapes.
    
    :param topdir: Top directory containing the data
    """
    # Get the list of directories
    dlist1 = os.listdir(topdir)
    dlist = [d for d in dlist1 if 'obs' in d]

    print(topdir)

    for i in range(len(dlist)):
        # Get the directory name
        dname = os.path.join(topdir, dlist[i], '')

        print(dlist[i])

        # Do the fits to the Chandra SMC X-1 data
        chisq = 0.0
        fit_data(dname, 'n', chisq)
        print(f'low chisq: {chisq}')

    print('Multiplot completed')

fit_fit("./test/")
