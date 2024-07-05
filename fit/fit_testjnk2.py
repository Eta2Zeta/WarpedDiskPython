import os
from fit_data import fit_data  # Assuming fit_data is a Python module handling the data fitting
from fit_plotjnk import fit_plotjnk  # Assuming fit_plotjnk is another Python module for plotting

def fit_testjnk2():
    """
    This function iterates over directories within a specified top directory,
    performs data fitting, and then plots the results if the chi-squared limit condition is met.
    """
    # Define the top directory containing the simulation data
    topdir = '/pool/zeus1/rhickox/beams/warpsx1_all/'

    # List all directories within the top directory
    dlist = os.listdir(topdir)

    print(topdir)

    # Loop through each directory in the directory list
    for i, directory in enumerate(dlist):
        print(f'i={i}')
        dname = os.path.join(topdir, directory)  # Full path to the directory

        print(directory)

        # Perform data fitting; assume this function returns a chi-squared value
        chisq = fit_data(dname, 'n', None)  # 'n' could represent a plot flag
        print(f'low chisq: {chisq}')

        # Plot results if chi-squared is below a certain limit
        chisqlim = 2.5
        if chisq < chisqlim:
            fit_plotjnk(dname, chisqlim)

fit_testjnk2()
