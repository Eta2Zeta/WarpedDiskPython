import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_disk_with_illumination(npoints, nprof, xv, yv, zv, beam_illum_on_disk):
    """
    Plot the disk in 3D with colors corresponding to the illumination.

    :param npoints: Number of points for the disk profile
    :param nprof: Number of profile points
    :param disk_parameters: Array of parameters [rin, rout, tiltin, tiltout, phsoff]
    :param beam_illum_on_disk: 2D array of illumination values for the disk points
    """

    # Plotting the disk in 3D
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Normalize the illumination for coloring
    norm_illum = beam_illum_on_disk / np.max(beam_illum_on_disk)

    # Plot each profile line on the disk with color based on illumination
    for i in range(npoints):
        for j in range(nprof):
            ax.scatter(xv[i, j], yv[i, j], zv[i, j], color=plt.cm.viridis(norm_illum[i, j]), s=10)

    # Labels and showing the plot
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.set_title('3D Disk Shape with Illumination')
    plt.show()

# def plot_disk_with_illumination_surface(xv, yv, zv, beam_illum_on_disk):
#     """
#     Plot the disk in 3D as a surface with colors corresponding to the illumination.

#     :param npoints: Number of points for the disk profile
#     :param nprof: Number of profile points
#     :param xv: X-coordinates of the disk
#     :param yv: Y-coordinates of the disk
#     :param zv: Z-coordinates of the disk
#     :param beam_illum_on_disk: 2D array of illumination values for the disk points
#     """

#     # Normalize the illumination for coloring
#     norm_illum = beam_illum_on_disk / np.max(beam_illum_on_disk)

#     # Plotting the disk as a surface in 3D
#     fig = plt.figure(figsize=(10, 7))
#     ax = fig.add_subplot(111, projection='3d')

#     # Plot surface with color based on illumination
#     surf = ax.plot_surface(xv, yv, zv, facecolors=plt.cm.viridis(norm_illum), rstride=1, cstride=1, antialiased=False, shade=False)

#     # Set labels and show the plot
#     ax.set_xlabel('X axis')
#     ax.set_ylabel('Y axis')
#     ax.set_zlabel('Z axis')
#     ax.set_title('3D Disk Shape with Illumination as Surface')

#     # Adding a color bar to show the illumination scale
#     m = plt.cm.ScalarMappable(cmap=plt.cm.viridis)
#     m.set_array(norm_illum)
#     plt.colorbar(m, ax=ax, shrink=0.5, aspect=5)

#     plt.show()

def plot_disk_with_illumination_surface(xv, yv, zv, beam_illum_on_disk):
    """
    Plot the disk in 3D as a surface with colors corresponding to the illumination.

    :param xv: X-coordinates of the disk (nphi, nth)
    :param yv: Y-coordinates of the disk (nphi, nth)
    :param zv: Z-coordinates of the disk (nphi, nth)
    :param beam_illum_on_disk: 2D array of illumination values for the disk points (nphi, nth)
    """

    # Ensure the arrays are wrapped around by adding the first element at the end
    xv = np.append(xv, xv[0:1, :], axis=0)
    yv = np.append(yv, yv[0:1, :], axis=0)
    zv = np.append(zv, zv[0:1, :], axis=0)
    beam_illum_on_disk = np.append(beam_illum_on_disk, beam_illum_on_disk[0:1, :], axis=0)

    # Normalize the illumination for coloring
    norm_illum = beam_illum_on_disk / np.max(beam_illum_on_disk)

    # Plotting the disk as a surface in 3D
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Plot surface with color based on illumination
    surf = ax.plot_surface(xv, yv, zv, facecolors=plt.cm.viridis(norm_illum), rstride=1, cstride=1, antialiased=False, shade=False)

    # Set labels and show the plot
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.set_title('3D Disk Shape with Illumination as Surface')

    # Adding a color bar to show the illumination scale
    m = plt.cm.ScalarMappable(cmap=plt.cm.viridis)
    m.set_array(norm_illum)
    plt.colorbar(m, ax=ax, shrink=0.5, aspect=5)

    plt.show()
