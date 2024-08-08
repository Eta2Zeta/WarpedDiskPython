import numpy as np
import matplotlib.pyplot as plt

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

def sphdist(lon1, lat1, lon2, lat2):
    delta_lon = lon2 - lon1
    delta_lat = lat2 - lat1
    a = np.sin(delta_lat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(delta_lon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return c

def beam_luminosity(nth, nphi, beams, floor, star_rot_ang):
    vth = -np.pi / 2 + np.linspace(0, np.pi, nth)
    vphi = np.linspace(0, 2 * np.pi, nphi)

    for beam in beams:
        beam.reset_longitude()  # Reset to original longitude before update
        beam.update_longitude(star_rot_ang)

    thstep = np.pi / (nth - 1)
    phistep = 2 * np.pi / nphi
    sang = thstep * phistep * np.abs(np.cos(vth))

    beam_pattern = np.zeros((nth, nphi))

    for beam in beams:
        sph_dist = np.zeros((nth, nphi))
        for i in range(nth):
            sph_dist[i, :] = sphdist(beam.long, beam.lat, vphi, vth[i])
        beam_contrib = beam.norm * np.exp(-((sph_dist - beam.th) ** 2) / (2 * beam.sigma ** 2))
        beam_pattern += beam_contrib

    beam_pattern += floor

    beamint = 0
    for i in range(nth):
        beamint += np.sum(beam_pattern[i, :] * sang[i])

    nlum = beam_pattern / beamint

    return vth, vphi, nlum

def plot_beam_3D(nth, nphi, vth, vphi, nbeam):
    rv = 1 + nbeam

    xv = np.zeros((nth, nphi))
    yv = np.zeros((nth, nphi))
    zv = np.zeros((nth, nphi))

    for i in range(nth):
        xv[i, :] = rv[i, :] * np.cos(vphi) * np.cos(vth[i])
        yv[i, :] = rv[i, :] * np.sin(vphi) * np.cos(vth[i])
        zv[i, :] = rv[i, :] * np.sin(vth[i])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    norm = plt.Normalize(nbeam.min(), nbeam.max())
    colors = plt.cm.viridis(norm(nbeam))

    ax.plot_surface(xv, yv, zv, facecolors=colors, rstride=1, cstride=1, antialiased=False, shade=False)

    ax.set_box_aspect([1, 1, 1])

    max_range = np.array([xv.max() - xv.min(), yv.max() - yv.min(), zv.max() - zv.min()]).max() / 2.0
    mean_x = xv.mean()
    mean_y = yv.mean()
    mean_z = zv.mean()

    ax.set_xlim([mean_x - max_range, mean_x + max_range])
    ax.set_ylim([mean_y - max_range, mean_y + max_range])
    ax.set_zlim([mean_z - max_range, mean_z + max_range])

    mappable = plt.cm.ScalarMappable(cmap='viridis', norm=norm)
    mappable.set_array(nbeam)
    plt.colorbar(mappable, ax=ax, shrink=0.5, aspect=5)

    plt.show()

def main():
    nth = 100
    nphi = 100
    
    beam_params = [
        {'longdeg': 180.0, 'latdeg': 0.0, 'sigma': np.pi/10, 'thdeg': 0.0, 'norm': 3.0},
    ]
    
    for beam in beam_params:
        beam['long'] = np.radians(beam['longdeg'])
        beam['lat'] = np.radians(beam['latdeg'])
        beam['th'] = np.radians(beam['thdeg'])
    
    for beam in beam_params:
        del beam['longdeg']
        del beam['latdeg']
        del beam['thdeg']

    beams = [Beam(**params) for params in beam_params]
    
    nang = 10
    ang_step = 2 * np.pi / nang
    
    for ang in range(nang):
        angle = ang * ang_step
        vth, vphi, nbeam = beam_luminosity(nth, nphi, beams, floor=0.1, star_rot_ang=angle)
        plot_beam_3D(nth, nphi, vth, vphi, nbeam)

if __name__ == "__main__":
    main()
