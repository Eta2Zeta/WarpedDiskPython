import os
from fit_plot_double import fit_plot_double

def fit_fitpl(topdir):
    """
    Create input files for doing a set of simulated profiles for several disk and beam shapes.
    
    :param topdir: Top directory containing the data
    """
    # Get the list of directories
    dlist1 = os.listdir(topdir)
    dlist = [d for d in dlist1 if 'obs' in d]

    print(topdir)

    i = 0
    while True:
        # Read user input
        inp = input(f'run no {i}, press enter to continue (or q to quit, p to go back, or enter a specific index): ')

        if inp == '':
            i += 1
        elif inp == 'q':
            break
        elif inp == 'p':
            i -= 1
        else:
            try:
                i = int(inp)
            except ValueError:
                print("Invalid input. Please enter a valid index, 'q', or 'p'.")
                continue

        if i < 0 or i >= len(dlist):
            print("Index out of range. Please enter a valid index.")
            continue

        print(f'Input: {inp}')

        # Get the directory name
        dname = os.path.join(topdir, dlist[i], '')

        print(f'i={i}, {dlist[i]}')

        # Plot the results with a chi-square limit
        chisqlim = 8.0
        fit_plot_double(dname, dname, [1, 1, 1, 1, 1], chisqlim, 'n', 'n', 0.375)

