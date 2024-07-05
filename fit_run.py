import os
import glob
import subprocess
from disktempsave import disktempsave  # assuming disktempsave.py is the Python translation of the IDL disktempsave
from diskspecrest import diskspecrest  # assuming diskspecrest.py is the Python translation of the IDL diskspecrest
from fitplotprof import fitplotprof  # assuming fitplotprof.py is the Python translation of the IDL fitplotprof

def fit_run(topdir):
    """Create input files and process a set of simulated profiles for various configurations."""
    # List all directories that include 'obs' in their names
    dlist = [d for d in glob.glob(f"{topdir}/*obs*")]

    
    for i, directory in enumerate(dlist):
        # Process every 5th directory only
        if i % 5 != 0:
            continue
        
        print(f"Processing directory: {directory}")

        # Make the disk temperature files
        disktempsave(directory)

        # Plot and get the profiles
        diskspecrest(directory)

        # Remove the disk temperature files
        temp_files = glob.glob(f'{directory}/dtemp*.idl')
        for file in temp_files:
            os.remove(file)

        # Optionally, plot the results and erase files as needed
        fitplotprof(directory, eraseit='y')
