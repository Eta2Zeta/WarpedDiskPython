import os
from fit_plot_double import fit_plot_double

def fit_fitpldb(topdir):
    """
    Create input files for doing a set of simulated profiles for several disk and beam shapes.
    
    :param topdir: Top directory containing the data
    """
    # Get the list of directories
    dlist1 = os.listdir(topdir)
    dlist = [d for d in dlist1 if 'obs' in d]

    print(topdir)

    idirs = [1, 4]
    dname1, dname2 = '', ''

    for i in range(len(dlist)):
        # Get the directory name
        if i == idirs[0]:
            dname1 = os.path.join(topdir, dlist[i], '')
        if i == idirs[1]:
            dname2 = os.path.join(topdir, dlist[i], '')

        print(f'i={i}, {dlist[i]}')

    if dname1 and dname2:
        chisqlim = 8.0
        fit_plot_double(dname1, dname2, [1, 1, 1, 1, 2], chisqlim, 'n', 'n', 0.375)
    else:
        print('Required directories not found.')

