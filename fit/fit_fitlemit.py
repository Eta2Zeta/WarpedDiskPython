import os
import numpy as np
import pickle

def fit_fitlemit(topdir):
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

        print(f'i={i}, {dlist[i]}')

        # Plot and print the mean emitted luminosity
        chisqlim = 8.0

        try:
            with open(os.path.join(dname, 'lemit.pkl'), 'rb') as f:
                lemit_data = pickle.load(f)
            lemitv = lemit_data['lemitv']
            print(np.mean(lemitv) / 3.0)
        except FileNotFoundError:
            print(f'File not found: {os.path.join(dname, "lemit.pkl")}')
            continue
