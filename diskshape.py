import numpy as np

def diskshape(npoints, nprof, disk_parameters):
    """
    Calculate the shape of the disk and return the X, Y, and Z values.
    
    :param params: Array of parameters [rin, rout, tiltin, tiltout, phsoff]
    :param npoints: Number of points for the disk profile
    :param nprof: Number of profile points
    :return: ang, xv, yv, zv
    """
    
    # Parameters of the disk
    rin, rout, tiltin, tiltout, phsoff = disk_parameters

    # Offsets and amplitudes for the disk profile
    off = np.linspace(0, phsoff, nprof)
    amp = np.linspace(tiltin, tiltout, nprof)

    ang = np.zeros((npoints, nprof))
    xv = np.zeros((npoints, nprof))
    yv = np.zeros((npoints, nprof))
    zv = np.zeros((npoints, nprof))

    # Make the vector of radii
    rv = np.linspace(rin, rout, nprof)
    # rphys = rv * rinphys  #? This is used in disktemp and somehow commented out in the idl code, investigate later
    #? Seems like it converse the r (random unit) to r (physical unit)

    # Find the appropriate values of phase to use
    ph = np.linspace(0, 1, npoints, endpoint=False) + 0.0001  # Avoid division by zero
    
    # Fill in the angles of the profiles to plot
    for i in range(npoints):
        ang[i, :] = -amp * np.sin(2 * np.pi * ph[i] + off)

    # Make the x, y, and z profiles
    for i in range(npoints):
        xv[i, :] = rv * np.cos(2 * np.pi * ph[i]) * np.cos(ang[i, :])
        yv[i, :] = rv * np.sin(2 * np.pi * ph[i]) * np.cos(ang[i, :])
        zv[i, :] = rv * np.sin(ang[i, :])

    return ang, xv, yv, zv
