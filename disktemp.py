import numpy as np
from diskshape import diskshape

def cross_product(v1, v2):
    """Calculate the cross product of two vectors."""
    return np.array([
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0]
    ])



def disktemp(npoints, nprof, rinphys, thil, phil, illum, ph, xv, yv, zv, T, side, lemit, disk_parameters):
    """
    Calculate the temperature of the disk given an input radiation field.
    
    :param params: Parameters of the disk
    :param npoints: Number of points in the disk
    :param nprof: Number of profile points
    :param rinphys: Inner physical radius
    :param thil: Array of theta illumination
    :param phil: Array of phi illumination
    :param illum: Illumination array
    :param ph: Phi angles
    :param xv: X-coordinates of the disk
    :param yv: Y-coordinates of the disk
    :param zv: Z-coordinates of the disk
    :param labs: Luminosity absorbed
    :param T: Temperature array
    :param side: Side illumination array
    :param lemit: Emitted luminosity
    """

    # PHYSICAL CONSTANTS--------
    kpc242 = 9.523  # kpc^2 in 1E42
    k = 1.3807E-16  # Boltzmann constant in erg/K
    SBsigma = 5.6705E-5  # Stefan-Boltzmann constant in erg/(cm^2 K^4 s)
    
    # Arrays to store side illumination, temperature, solid angle, and energy absorbed
    side = np.zeros((npoints, nprof), dtype=int)
    sang = np.zeros((npoints, nprof))
    labs = np.zeros((npoints, nprof))

    # Calculate the shape of the disk
    ang, xv, yv, zv = diskshape(npoints, nprof, disk_parameters)

    # Assume constant steps in phi
    phistep = np.full(npoints, ph[1] - ph[0])

    # Calculate illumination array elements corresponding to disk points
    iphi = np.zeros(npoints, dtype=int)
    ith = np.zeros((npoints, nprof), dtype=int)
    illum2 = np.zeros((npoints, nprof))

    # Map disk points to illumination array indices
    for i in range(npoints):
        difphi = np.abs(2 * np.pi * ph[i] - phil)
        iphi[i] = np.argmin(difphi)

        for j in range(nprof):
            difth = np.abs(ang[i, j] - thil)
            ith[i, j] = np.argmin(difth)
            illum2[i, j] = illum[ith[i, j], iphi[i]]

    # Calculate the temperature profiles for each phi angle
    for i in range(npoints):
        p1 = ang[i, :]

        angin = p1[0]
        anghi = angin
        anglo = angin

        # Determine the bounds in phi of this particular piece of the disk
        inds = [i-1, i+1] if i not in [0, npoints-1] else ([npoints-1, 1] if i == 0 else [npoints-2, 0])

        for j in range(nprof):
            # Determine the bounds in angle of this piece of the disk
            jnds = [j-1, j+1] if j not in [0, nprof-1] else ([0, 1] if j == 0 else [nprof-2, nprof-1])

            # Determine if the disk is top-illuminated
            if p1[j] > anghi:
                anghi = p1[j]
                side[i, j] = 1

            # Determine if the disk is bottom-illuminated
            if ang[i, j] < anglo:
                anglo = p1[j]
                side[i, j] = -1

            # Calculate the solid angle from the central source
            sang[i, j] = np.abs((2 * np.pi * phistep[i]) * (ang[i, jnds[1]] - ang[i, jnds[0]]) / 2 * np.cos(ang[i, j]))

            # Calculate the temperature if the disk segment is illuminated
            if side[i, j] != 0:
                labs[i, j] = illum2[i, j] * sang[i, j]

                # Calculate vectors for the area estimation
                vec1 = np.array([xv[i, jnds[1]] - xv[i, jnds[0]], yv[i, jnds[1]] - yv[i, jnds[0]], zv[i, jnds[1]] - zv[i, jnds[0]]])
                vec2 = np.array([xv[inds[1], j] - xv[inds[0], j], yv[inds[1], j] - yv[inds[0], j], zv[inds[1], j] - zv[inds[0], j]])

                # Calculate the cross product to estimate the area
                orient = cross_product(vec1, vec2)
                area = rinphys**2 * np.sqrt(np.sum(orient**2))

                # Calculate the temperature using the Stefan-Boltzmann law
                T[i, j] = (1E38)**(1/4) * (labs[i, j] / (SBsigma * area))**(1/4)

    # Calculate the emitted radiation
    lemit = np.sum(labs[side != 0])

    return side, T, sang, labs, lemit
