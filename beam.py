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
    a = np.sin(delta_lat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(delta_lon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return c

class Beam:
    def __init__(self, long, lat, sigma, th, norm):
        self.original_long = long  # Store the original longitude
        self.long = long
        self.lat = lat
        self.sigma = sigma
        self.th = th
        self.norm = norm

    def reset_longitude(self):
        self.long = self.original_long  # Reset to the original longitude

    def update_longitude(self, star_rot_ang):
        self.long = (self.original_long + star_rot_ang) % (2 * np.pi)  # Rotate from the original longitude


def beam_luminosity(nth, nphi, beams, floor, star_rot_ang):
    """
    Generate a beam pattern with Gaussian profiles for multiple beams.
    :param nth: Number of theta divisions
    :param nphi: Number of phi divisions
    :param beams: List of Beam objects
    :param floor: Minimum value of the beam pattern
    :param star_rot_ang: Rotational angle to rotate the whole beam pattern by phi
    :return: Normalized luminosity pattern (nlum), theta (vth), and phi (vphi) coordinates
    """
    
    # Create theta and phi angle vectors
    vth = -np.pi / 2 + np.linspace(0, np.pi, nth)
    vphi = np.linspace(0, 2 * np.pi, nphi)

    # Apply rotation to the beam longitudes
    for beam in beams:
        beam.reset_longitude()  # Reset to original longitude before update
        beam.update_longitude(star_rot_ang)

    # Calculate the solid angle covered by each point
    thstep = np.pi / (nth - 1)
    phistep = 2 * np.pi / nphi
    sang = thstep * phistep * np.abs(np.cos(vth))

    # Initialize arrays for the beam pattern and distances
    beam_pattern = np.zeros((nth, nphi))

    # Calculate the spherical distances and beam patterns for each Beam object
    for beam in beams:
        sph_dist = np.zeros((nth, nphi))
        for i in range(nth):
            sph_dist[i, :] = sphdist(beam.long, beam.lat, vphi, vth[i])
        beam_contrib = beam.norm * np.exp(-((sph_dist - beam.th) ** 2) / (2 * beam.sigma ** 2))
        beam_pattern += beam_contrib

    # Add the floor value to the beam pattern
    beam_pattern += floor

    # Calculate the integral of the beam pattern for normalization
    beamint = 0
    for i in range(nth):
        beamint += np.sum(beam_pattern[i, :] * sang[i])

    # Normalize the beam pattern to create the luminosity pattern
    nlum = beam_pattern / beamint

    return vth, vphi, nlum
