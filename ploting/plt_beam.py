import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Add the parent directory to the system path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from beam import beam  # Now you can import the beam function

def plot_beam(nth, nphi, vth, vphi, nbeam):
    """
    Plot the beam pattern in 3D.
    """

    rv = 1  # Radius vector for plotting

    # Initialize vectors for plotting the beam pattern
    xv = np.zeros((nth, nphi))
    yv = np.zeros((nth, nphi))
    zv = np.zeros((nth, nphi))

    # Calculate the x, y, and z coordinates for plotting the beam pattern
    for i in range(nth):
        xv[i, :] = rv * np.cos(vphi) * np.cos(vth[i])
        yv[i, :] = rv * np.sin(vphi) * np.cos(vth[i])
        zv[i, :] = rv * np.sin(vth[i])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Normalize beam intensity for color mapping
    norm = plt.Normalize(nbeam.min(), nbeam.max())
    colors = plt.cm.viridis(norm(nbeam))

    # Plot the surface
    ax.plot_surface(xv, yv, zv, facecolors=colors, rstride=1, cstride=1, antialiased=False, shade=False)

    # Add a color bar
    mappable = plt.cm.ScalarMappable(cmap='viridis', norm=norm)
    mappable.set_array(nbeam)
    plt.colorbar(mappable, ax=ax, shrink=0.5, aspect=5)

    plt.show()

def main():
    # Parameters
    nth = 1000
    nphi = 1000
    long1 = 0
    lat1 = 0
    sigma1 = np.pi / 10
    th1 = 0
    norm1 = 1
    long2 = np.pi / 2
    lat2 = np.pi / 4
    sigma2 = np.pi / 10
    th2 = 0
    norm2 = 1
    floor = 0.1

    # Generate the beam
    vth, vphi, nbeam = beam(nth, nphi, long1, lat1, sigma1, th1, norm1, long2, lat2, sigma2, th2, norm2, floor)

    # Plot the beam
    plot_beam(nth, nphi, vth, vphi, nbeam)

if __name__ == "__main__":
    main()
