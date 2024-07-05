import numpy as np

def sphdist(lon1, lat1, lon2, lat2):
    """
    Calculate spherical distance between two points on a sphere.
    :param lon1: Longitude of the first point
    :param lat1: Latitude of the first point
    :param lon2: Longitude of the second point
    :param lat2: Latitude of the second point
    :return: Spherical distance
    """
    delta_lon = lon2 - lon1
    delta_lat = lat2 - lat1
    a = np.sin(delta_lat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(delta_lon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return c

def beam(nth, nphi, long1, lat1, sigma1, th1, norm1, long2, lat2, sigma2, th2, norm2, floor):
    """
    Generate a beam pattern with a Gaussian profile.
    :param nth: Number of theta divisions
    :param nphi: Number of phi divisions
    :param long1: Longitude of the first beam center
    :param lat1: Latitude of the first beam center
    :param sigma1: Standard deviation of the first Gaussian beam
    :param th1: Theta offset for the first beam
    :param norm1: Normalization factor for the first beam
    :param long2: Longitude of the second beam center
    :param lat2: Latitude of the second beam center
    :param sigma2: Standard deviation of the second Gaussian beam
    :param th2: Theta offset for the second beam
    :param norm2: Normalization factor for the second beam
    :param floor: Minimum value of the beam pattern
    :return: Normalized beam pattern, color scaled beam pattern, and transformed coordinates
    """
    ctop = 255  # Maximum value for color scaling

    # Create theta and phi angle vectors
    vth = -np.pi/2 + np.linspace(0, np.pi, nth)
    vphi = np.linspace(0, 2*np.pi, nphi) + 0.0001 * 2 * np.pi
    #? Why is it adding the 0.0001 * 2 * np.pi? 

    # Calculate the solid angle covered by each point
    thstep = np.pi / (nth - 1)
    phistep = 2 * np.pi / nphi
    sang = thstep * phistep * np.abs(np.cos(vth))
    #? I thought the solid angle was sin(theta) and not cos? 

    # Initialize arrays for the beam pattern and distances
    beam = np.zeros((nth, nphi))
    nbeam = np.zeros((nth, nphi))
    dist1 = np.zeros((nth, nphi))
    dist2 = np.zeros((nth, nphi))

    # Calculate the spherical distances for each theta and phi combination
    for i in range(nth):
        dist1[i, :] = sphdist(long1, lat1, vphi, vth[i])
        dist2[i, :] = sphdist(long2, lat2, vphi, vth[i])

    # Create the beam patterns with Gaussian profiles and sum them up
    beam1 = norm1 * np.exp(-((dist1 - th1) ** 2) / (2 * sigma1 ** 2))
    beam2 = norm2 * np.exp(-((dist2 - th2) ** 2) / (2 * sigma2 ** 2))
    beam = floor + beam1 + beam2

    # Calculate the integral of the beam pattern for normalization
    beamint = 0
    for i in range(nth):
        beamint += np.sum(beam[i, :] * sang[i])

    # Normalize the beam pattern
    nbeam = beam / beamint

    # Verify the normalization of the beam pattern
    nbeamint = 0
    for i in range(nth):
        nbeamint += np.sum(nbeam[i, :] * sang[i])

    # Scale the normalized beam pattern for plotting
    clrbeam = nbeam * ctop / np.max(nbeam)

    rv = 1  # Radius vector for plotting

    # Initialize vectors for plotting the beam pattern
    xv = np.copy(beam)
    yv = np.copy(beam)
    zv = np.copy(beam)

    # Calculate the x, y, and z coordinates for plotting the beam pattern
    for i in range(nth):
        xv[i, :] = rv * np.cos(vphi) * np.cos(vth[i])
        yv[i, :] = rv * np.sin(vphi) * np.cos(vth[i])
        zv[i, :] = rv * np.sin(vth[i])

    return vth, vphi, nbeam
