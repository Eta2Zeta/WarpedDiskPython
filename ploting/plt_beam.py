import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Add the parent directory to the system path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from beam import beam_luminosity, Beam  # Now you can import the beam function

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

    # Set the aspect ratio to be equal
    ax.set_box_aspect([1, 1, 1])  # Aspect ratio is 1:1:1

    # Set the limits to ensure the sphere is not distorted
    max_range = np.array([xv.max()-xv.min(), yv.max()-yv.min(), zv.max()-zv.min()]).max() / 2.0
    mean_x = xv.mean()
    mean_y = yv.mean()
    mean_z = zv.mean()

    ax.set_xlim([mean_x - max_range, mean_x + max_range])
    ax.set_ylim([mean_y - max_range, mean_y + max_range])
    ax.set_zlim([mean_z - max_range, mean_z + max_range])

    # Add a color bar
    mappable = plt.cm.ScalarMappable(cmap='viridis', norm=norm)
    mappable.set_array(nbeam)
    plt.colorbar(mappable, ax=ax, shrink=0.5, aspect=5)

    plt.show()

def plot_beam_3D(nth, nphi, vth, vphi, nbeam):
    """
    Plot the beam pattern in 3D.
    """

    # Adjust the radius vector based on the beam intensity
    rv = 1 + nbeam  # Radius vector for plotting, adjusted by the beam intensity

    # Initialize vectors for plotting the beam pattern
    xv = np.zeros((nth, nphi))
    yv = np.zeros((nth, nphi))
    zv = np.zeros((nth, nphi))

    # Calculate the x, y, and z coordinates for plotting the beam pattern
    for i in range(nth):
        xv[i, :] = rv[i, :] * np.cos(vphi) * np.cos(vth[i])
        yv[i, :] = rv[i, :] * np.sin(vphi) * np.cos(vth[i])
        zv[i, :] = rv[i, :] * np.sin(vth[i])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Normalize beam intensity for color mapping
    norm = plt.Normalize(nbeam.min(), nbeam.max())
    colors = plt.cm.viridis(norm(nbeam))

    # Plot the surface
    ax.plot_surface(xv, yv, zv, facecolors=colors, rstride=1, cstride=1, antialiased=False, shade=False)

    # Set the aspect ratio to be equal
    ax.set_box_aspect([1, 1, 1])  # Aspect ratio is 1:1:1

    # Set the limits to ensure the sphere is not distorted
    max_range = np.array([xv.max()-xv.min(), yv.max()-yv.min(), zv.max()-zv.min()]).max() / 2.0
    mean_x = xv.mean()
    mean_y = yv.mean()
    mean_z = zv.mean()

    ax.set_xlim([mean_x - max_range, mean_x + max_range])
    ax.set_ylim([mean_y - max_range, mean_y + max_range])
    ax.set_zlim([mean_z - max_range, mean_z + max_range])

    # Add a color bar
    mappable = plt.cm.ScalarMappable(cmap='viridis', norm=norm)
    mappable.set_array(nbeam)
    plt.colorbar(mappable, ax=ax, shrink=0.5, aspect=5)

    plt.show()

def main():
    nth = 70
    nphi = 70
    beam_params = [
        {'long': 0.0, 'latdeg': 0.0, 'sigmadeg': 18.0, 'thdeg': 30.0, 'norm': 3.0},
        {'long': 180.0, 'latdeg': 60.0, 'sigmadeg': 12.0, 'thdeg': 0.0, 'norm': 3.0}
    ]
    
    # Convert degrees to radians
    for beam in beam_params:
        beam['lat'] = np.radians(beam['latdeg'])
        beam['sigma'] = np.radians(beam['sigmadeg'])
        beam['th'] = np.radians(beam['thdeg'])
    
    # Remove the degree keys
    for beam in beam_params:
        del beam['latdeg']
        del beam['sigmadeg']
        del beam['thdeg']

    # Create Beam objects
    beams = [Beam(**params) for params in beam_params]

    # Generate the beam
    vth, vphi, nbeam = beam_luminosity(nth, nphi, beams, floor=0.1)

    # Plot the beam
    plot_beam_3D(nth, nphi, vth, vphi, nbeam)

if __name__ == "__main__":
    main()
