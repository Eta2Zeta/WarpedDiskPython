import numpy as np

def diskwarp(params, npoints, nprof, ph):
    """
    Calculate the shape of the disk and return the X, Y, and Z values.
    
    :param params: Parameters of the disk [rin, rout, tiltin, tiltout, phsoff]
    :param npoints: Number of points in the disk profile
    :param nprof: Number of profile points
    :param ph: Phi angles
    :return: ang, xv, yv, zv
    """
    
    # Number of inner points
    ninner = int(nprof)

    # Parameters of the disk
    rin = params[0]
    rout = params[1]
    tiltin = params[2]
    tiltout = params[3]
    phsoff = params[4]

    # Amplitudes for the disk profile
    amp = np.linspace(tiltin, tiltout, nprof)
    
    # Initialize arrays for angles and coordinates
    ang = np.zeros((npoints, nprof))
    xv = np.zeros((npoints, nprof))
    yv = np.zeros((npoints, nprof))
    zv = np.zeros((npoints, nprof))

    # Make the vector of radii
    rv = np.linspace(rin, rout, nprof)

    # Find the appropriate values of phase to use
    ph = np.linspace(0, 1, npoints, endpoint=False) + 0.0001

    out = tiltout * np.sin(2 * np.pi * ph)
    in_ = tiltin * np.sin(2 * np.pi * ph + phsoff)

    # Offsets for the inner points
    off = np.linspace(0, phsoff, ninner)
    iw = np.arange(ninner)
    if ninner < nprof:
        inw = ninner + np.arange(nprof - ninner)
    
    # Fill in the angles of the profiles to plot
    for i in range(npoints):
        ang[i, iw] = -amp * np.sin(2 * np.pi * ph[i] + off)
        if ninner < nprof:
            ang[i, inw] = np.arcsin(rv[ninner - 1] / rv[inw] * np.sin(ang[i, ninner - 1]))

    # Make the x, y, and z profiles
    for i in range(npoints):
        xv[i, :] = rv * np.cos(2 * np.pi * ph[i]) * np.cos(ang[i, :])
        yv[i, :] = rv * np.sin(2 * np.pi * ph[i]) * np.cos(ang[i, :])
        zv[i, :] = rv * np.sin(ang[i, :])

    return ang, xv, yv, zv

