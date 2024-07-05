import numpy as np
import os
from dtmpspec import dtmpspec
from diskshape import diskshape
def diskspecrest(bdir):
    """
    Plot views of the heated accretion disk.
    """
    # Load parameters
    params_path = os.path.join(bdir, 'par.npz')
    params = np.load(params_path)


    nang = 8
    ang = np.arange(nang) / nang
    inp = ''
    paper = 'y'
    plot = 'n'
    fast = 'n'

    # Correction for actual viewing angles
    angc = 0.67 - ang

    strang = [f"{a:.3f}" for a in ang]

    # Observer elevation angle
    obselev = 0.0

    ntemps = 128


    # Load the beam parameters
    diskbeam_path = os.path.join(bdir, 'diskbeam.npz')
    diskbeam = np.load(diskbeam_path)
    thbeam = diskbeam['thbeam']

    # Figure out where the observer is looking on the beam
    thobsdiff = np.abs(thbeam - obselev)
    ithobs = np.argmin(thobsdiff)

    # Initialize Tmax and Tmin for colormap
    Tmax = 0.0
    Tmin = 1.0e20

    for k in range(ntemps):
        dtemp_path = os.path.join(bdir, f'dtemp_{k:03d}.npz')
        dtemp = np.load(dtemp_path)
        for key in dtemp.keys():
            print(f"{key}: {dtemp[key]}")
        T = dtemp['T']

        Tmin1 = np.min(T[T > 0])
        Tmax1 = np.max(T)

        if Tmax1 > Tmax:
            Tmax = Tmax1
        if Tmin1 < Tmin:
            Tmin = Tmin1

    # Plot the disk at various phi angles
    for i in range(nang):
        load_color_table(3)

        print(f'disk angle phi: {strang[i]}')

        # Create a directory to hold the plots and info
        diskphi_dir = os.path.join(bdir, f'diskphi_{strang[i]}')
        os.makedirs(diskphi_dir, exist_ok=True)

        inrep = np.zeros(ntemps)
        inrepx = np.zeros(ntemps)
        instar = np.zeros(ntemps)

        diskvf_path = os.path.join(diskphi_dir, 'diskvf.npz')

        for j in range(ntemps):
            dtemp_path = os.path.join(bdir, f'dtemp_{j:03d}.npz')
            dtemp = np.load(dtemp_path)
            T = dtemp['T']
            illum = dtemp['illum']
            phbeam = dtemp['phbeam']
            labs = dtemp['labs']
            side = dtemp['side']
            ph = dtemp['ph']


            plot = 'n'
            if j == 0:
                plot = 'y'

            print(f'   beam angle no. {j:03d}/{ntemps:03d}')

            # Find what the observer sees of the beam
            if angc[i] >= 0.0:
                beamoff = np.abs(phbeam - 2.0 * np.pi * angc[i])
            else:
                beamoff = np.abs(phbeam - (2.0 * np.pi + 2.0 * np.pi * angc[i]))

            irot = np.argmin(beamoff)
            instar[j] = 4.0 * np.pi * illum[ithobs, irot]

            if paper == 'y' and plot == 'y':
                psopen(os.path.join(diskphi_dir, f'frame_{j:03d}.eps'))

            # Check if the disk viewing information has already been saved
            rdiskf = os.path.exists(diskvf_path)

            if not rdiskf:
                diskv = 'y'
            else:
                diskv = 'n'

            # Calculate the observed view of the disk
            ang, xv, yv, zv = diskshape(params)  # Assuming the diskshape function is defined
            intot, intotx, en, spec = dtmpspec(xv, yv, zv, labs, T, Tmax, Tmin, side, ph, angc[i], obselev, fast, diskv, diskvf_path, plot)


            if paper == 'y' and plot == 'y':
                psclose()

            # Get the pulse profile information
            inrep[j] = intot
            inrepx[j] = intotx

            if fast != 'y':
                np.savez(os.path.join(diskphi_dir, f'spec_{j:03d}.npz'), en=en, spec=spec)

        # Save the profiles and the spectrum
        np.savez(os.path.join(diskphi_dir, 'inprof.npz'), inrep=inrep, inrepx=inrepx, instar=instar)

    angcinp = angc[i]

def load_color_table(index):
    """Placeholder function to load a color table."""
    print(f"Loading color table {index}")
    # Actual implementation needed to load color table

def psopen(filepath):
    """Placeholder function to open a PostScript file."""
    print(f"Opening PostScript file: {filepath}")
    # Actual implementation needed for creating a PostScript file

def psclose():
    """Placeholder function to close a PostScript file."""
    print("Closing PostScript file")
    # Actual implementation needed for closing a PostScript file

