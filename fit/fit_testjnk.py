import numpy as np
import os
from scipy.io import readsav
from fit_data import fit_data

def fit_testjnk():
    """
    This function randomly selects a directory and performs disk temperature fitting.
    """
    # Define the top directory containing simulation data
    topdir = '/pool/zeus1/rhickox/beams/warpsx1_all/'

    # List all directories within the top directory
    dlist = os.listdir(topdir)

    print(topdir)

    # Seed the random number generator for reproducibility
    seed = 5
    np.random.seed(seed)

    # Randomly select an index for the directory list
    nlist = len(dlist)
    i = np.random.randint(nlist)

    # Optional: Fixed index to use while debugging or specific testing
    i = 89  # Fixed to a specific directory for demonstration

    print(f'i={i}')

    # Get the directory name
    dname = os.path.join(topdir, dlist[i])

    print(dlist[i])

    # Perform disk temperature fitting
    chisq = fit_data(dname, 'y', None)
    print(f'low chisq: {chisq}')

fit_testjnk()
