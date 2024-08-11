import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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
    tilt_angles = np.linspace(tiltin, tiltout, nprof)

    ang = np.zeros((npoints, nprof))
    xv = np.zeros((npoints, nprof))
    yv = np.zeros((npoints, nprof))
    zv = np.zeros((npoints, nprof))

    # Make the vector of radii
    rv = np.linspace(rin, rout, nprof)

    # Find the appropriate values of phase to use
    ph = np.linspace(0, 1, npoints, endpoint=False) + 0.0001  # Avoid division by zero
    
    # Fill in the angles of the profiles to plot
    for i in range(npoints):
        ang[i, :] = -tilt_angles * np.sin(2 * np.pi * ph[i] + off)

    # Make the x, y, and z profiles
    for i in range(npoints):
        xv[i, :] = rv * np.cos(2 * np.pi * ph[i]) * np.cos(ang[i, :])
        yv[i, :] = rv * np.sin(2 * np.pi * ph[i]) * np.cos(ang[i, :])
        zv[i, :] = rv * np.sin(ang[i, :])

    return ang, xv, yv, zv

def plot_disk():
    # Parameters for the disk
    npoints = 100  # Number of points for the disk profile
    nprof = 50     # Number of profile points
    disk_parameters = [1.0, 5.0, 0.1, 0.3, np.pi / 4]  # [rin, rout, tiltin, tiltout, phsoff]

    # Get the disk shape
    ang, xv, yv, zv = diskshape(npoints, nprof, disk_parameters)

    # Plotting the disk in 3D
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Plot each profile line on the disk
    for i in range(npoints):
        ax.plot(xv[i, :], yv[i, :], zv[i, :], color='b', alpha=0.7)

    # Labels and showing the plot
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.set_title('3D Disk Shape')
    plt.show()