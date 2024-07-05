import os
import pickle
from fit_spec import fit_spec

def fit_fitsp(topdir):
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

        # Calculate Tbb using fit_spec
        Tbb = fit_spec(dname)

        # Save Tbb to a file
        with open(os.path.join(dname, 'tbb.pkl'), 'wb') as f:
            pickle.dump(Tbb, f)

        print(f'Tbb saved to {os.path.join(dname, "tbb.pkl")}')
