import os
from fit_data import fit_data
from fit_plot import fit_plot

def fit_fitjnk(topdir):
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

        # Option to switch between plotting and fitting
        if False:  # Replace with actual condition if needed
            # Perform fits to the Chandra SMC X-1 data
            chisq = 0.0
            fit_data(dname, 'y', chisq)
            print(f'low chisq: {chisq}')
        else:
            # Plot the results with a chi-square limit
            chisqlim = 10.0
            fit_plot(dname, chisqlim, 'y', 'n')
