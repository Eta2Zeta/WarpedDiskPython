import os
import numpy as np
import pickle

def fit_intens(bdir):
    """
    Find how the intensity of the blackbody component varies as a function of disk phase.
    
    :param bdir: Base directory containing the data
    :return: Array of intensity values for different disk phases
    """
    num_profs = 8
    intout = np.zeros(num_profs)

    for i in range(num_profs):
        # Construct the disk orientation directory name
        ddir = f'diskphi_{i / float(num_profs):.3f}'

        # Load the data
        try:
            with open(os.path.join(bdir, ddir, 'inprof.pkl'), 'rb') as f:
                inprof_data = pickle.load(f)
            intout[i] = np.mean(inprof_data['inrepx'])
        except FileNotFoundError:
            print(f'File not found: {os.path.join(bdir, ddir, "inprof.pkl")}')
            intout[i] = np.nan  # Assign NaN if the file is not found to avoid skewing the mean

    return intout
