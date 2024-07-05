import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.io import readsav

def fit_spec(bdir, num_profs=8, nspec=30):
    """
    Process spectral data for a given base directory and number of profiles.
    
    Args:
    bdir (str): Base directory containing the spectral data files.
    num_profs (int): Number of profile orientations to process.
    nspec (int): Number of spectral files per profile orientation.
    
    Returns:
    np.array: Array containing the peak energy values.
    """
    # Initialize array to hold peak energy values
    Tbb = np.zeros((num_profs, nspec))

    # Process each profile orientation
    for i in range(num_profs):
        ddir = f'diskphi_{i/num_profs:.3f}/'

        # Process each spectral file within this orientation
        for j in range(nspec):
            filename = f'{bdir}{ddir}spec_{j:03d}.idl'
            if os.path.exists(filename):
                data = readsav(filename)
                spec = data['spec']
                en = data['en']
                
                # Calculate the peak energy
                peak_index = np.argmax(spec)
                peak_energy = en[peak_index] / 2.8
                Tbb[i, j] = peak_energy

                # Plotting the spectrum
                if j == 0:
                    plt.loglog(en, spec, label=f'Profile {i}, Spec {j}', basex=10, basey=10)
                else:
                    plt.loglog(en, spec, basex=10, basey=10)

    # Show the plot
    plt.xlim([0.5, 10.])
    plt.xlabel('Energy (keV)')
    plt.ylabel('Spectrum')
    plt.legend()
    plt.show()

    return Tbb
