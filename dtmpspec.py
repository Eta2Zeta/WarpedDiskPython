import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import matplotlib.cm as cm
from scipy.constants import k
from maskit import maskit
from bbfrac import *
from ploting.plot import plot1D

def cross_product(v1, v2):
    """Calculate the cross product of two vectors."""
    return np.array([
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0]
    ])


def dtmpspec(xv, yv, zv, labs, T, Tmax, Tmin, side, ph, phio, obselev, fast, diskv, diskvf, plot):
    """
    Take a disk with a given temperature profile and calculate the emission seen by the observer.
    RCH 7/04
    """

    # This is the new phi array, rotated by phio
    phf = ph - phio

    # Make the new X, Y vectors
    xvf = np.copy(xv)
    yvf = np.copy(yv)
    xv2 = np.copy(xv)
    zv2 = np.copy(zv)

    # Get the number of angles and profiles
    nang = xv.shape[0]
    nprof = xv.shape[1]

    # Array to hold the observed flux from each part of the disk
    intens = np.zeros((nang, nprof))

    # Array to hold the energy and spectral info
    # We will define the energies in keV, but will use erg in the calculation (in bbnorm)
    enbins = 1000
    emin = 0.001 
    emax = 100.0
    keV = 1.6021E-9

    Tclrmin = 100.0
    Tclrmax = 255.0
    clrdisk = 'k'

    for i in range(nang):
        # Rotate with respect to phi
        xvf[i, :] = xv[i, :] * np.cos(2.0 * np.pi * phf[i]) / np.cos(2.0 * np.pi * ph[i])
        yvf[i, :] = yv[i, :] * np.sin(2.0 * np.pi * phf[i]) / np.sin(2.0 * np.pi * ph[i])

        # Change the elevation angle
        xv2[i, :] = xvf[i, :] * np.cos(-obselev) - zv[i, :] * np.sin(-obselev)
        yv2 = yvf
        zv2[i, :] = zv[i, :] * np.cos(-obselev) + xvf[i, :] * np.sin(-obselev)

    xin = xv2[:, 0]
    xout = xv2[:, -1]
    yin = yv2[:, 0]
    yout = yv2[:, -1]
    zin = zv2[:, 0]
    zout = zv2[:, -1]

    # Find which parts are in the back or the front
    ibk = np.where(xout <= 0.0)[0]
    ifr = np.where(xout >= 0.0)[0]


    '''Colors'''
    Tclr = (T - Tmin) * (Tclrmax - Tclrmin) / (Tmax - Tmin) + Tclrmin

    # Normalize Tclr to the range [0, 1]
    norm = Normalize(vmin=Tclrmin, vmax=Tclrmax)
    cmap = plt.get_cmap('viridis')  


    if diskv == 'y':
        top = np.zeros((nang, nprof), dtype=int)

        for i in range(nang):
            # Handling edge cases for the first and last elements
            inds = [i-1, i+1] if i not in [0, nang-1] else ([nang-1, 1] if i == 0 else [nang-2, 0])

            for j in range(nprof):
                # Finding the bounds in angle of this piece of the disk
                jnds = [j-1, j+1] if j not in [0, nprof-1] else ([0, 1] if j == 0 else [nprof-2, nprof-1])

                vec1 = np.array([xv2[i, jnds[1]] - xv2[i, jnds[0]], yv2[i, jnds[1]] - yv2[i, jnds[0]], zv2[i, jnds[1]] - zv2[i, jnds[0]]])
                vec2 = np.array([xv2[inds[1], j] - xv2[inds[0], j], yv2[inds[1], j] - yv2[inds[0], j], zv2[inds[1], j] - zv2[inds[0], j]])

                orient = cross_product(vec1, vec2)
                top[i, j] = int(orient[0] / abs(orient[0]))

                # This is the fractional component of the area pointed toward us
                fsee = abs(orient[0]) / np.sqrt(np.sum(orient**2))

                if fsee < 0.1:
                    top[i, j] = 0

        # Whether we can see the illuminated side
        see = top * side

        # Placeholder for maskit function to be implemented
        iplot = maskit(nprof, nang, xv2, yv2, zv2)

        # Save the results of the visibility analysis
        np.savez(diskvf, iplot=iplot, see=see, fsee=fsee)
    else:
        # Load the results of the visibility analysis
        data = np.load(diskvf)
        iplot = data['iplot']
        see = data['see']
        fsee = data['fsee']

    # Get the intensity
    intens = fsee * labs

    # Find the total reprocessed intensity 
    # By summing all the points that you can see and if (iplot = True)
    intot = np.sum(intens[iplot + see == 2])

    # Define the intotx variable
    intotx = 0.0

    if fast == 'y':
        bbfracgrid_path = './mb/bbfrac/bbf00.60_10.00.npz'
        bbfracgrid = np.load(bbfracgrid_path)
        logT = bbfracgrid['logT']
        bbfracv = bbfracgrid['bbfracv']

        for i in range(nang):
            for j in range(nprof):
                if iplot[i, j] + see[i, j] == 2:
                    intotx += intens[i, j] * bbfrac_inp(logT, bbfracv, T[i, j])

    else:
        # Slow version, saves all the spectra
        
        #Create an array of energies that is linear in log space
        en = np.logspace(np.log10(emin), np.log10(emax), enbins) 

        energ = en * keV
        spec = np.zeros(enbins)

        for i in range(nang):
            for j in range(nprof):
                intens[i, j] = fsee * labs[i, j]
                if iplot[i, j] + see[i, j] == 2:
                    # For each point in an angle and profile, calculate the blackbody spectrum there
                    bb = bbnorm(T[i, j], energ)
                    # The spectrum at the point is equal to the intensity modeled by this blackbody spectrum there
                    spec += intens[i, j] * bb

        xlo = 0.3
        xhi = 0.7
        endiff = np.diff(en)
        spectot = np.sum(spec[:-1] * endiff)
        ix = np.where((en >= xlo) & (en < xhi))[0]
        specx = np.sum(spec[ix] * endiff[ix])

        intotx = intot * specx / spectot

    # Plot the disk if desired
    if plot == 'y':
        plt.plot(yv2[0, [0, 1]], zv2[0, [0, 1]], linestyle='-', color=clrdisk)
        for i in range(len(phf)):
            interval = 5
            if i % interval == 0:
                plt.plot(yv2[i, :], zv2[i, :], linestyle='-', color=clrdisk)

            if xout[i] > 0:
                ls = '-'
            else:
                ls = '--'

            for j in range(nprof - 1):
                if iplot[i, j] == 1 and see[i, j] == 1 and T[i, j] >= 0:
                    color = cmap(norm(Tclr[i, j]))  # Convert Tclr to an RGB color
                    plt.plot(yv2[i, [j, j+1]], zv2[i, [j, j+1]], linestyle=ls, color=color)

        # Some werid bug that I don't know how to fix yet
        # Fix the front and back indices so the rings come out OK
        # The problemm is that np.where(np.diff(ifr) != 1) is an empty arra because ifr 
        # array is all just one apart form each other
        # icutf = np.where(np.diff(ifr) != 1)[0][0]
        # if icutf >= 0:
        #     ifr = np.concatenate((ifr[(icutf+1):], ifr[:icutf+1]))
        if yout[ifr[-1]] == yout[ifr[0]]:
            ifr = ifr[:-1]

        
        # icutb = np.where(np.diff(ibk) != 1)[0][0]
        # if icutb >= 0:
        #     ibk = np.concatenate((ibk[(icutb+1):], ibk[:icutb+1]))
        if yout[ibk[-1]] == yout[ibk[0]]:
            ibk = ibk[:-1]
        
        # Calculate differences and find indices where differences are not 1
        icutf_indices = np.where(np.diff(ifr) != 1)[0]
        if icutf_indices.size > 0:
            icutf = icutf_indices[0]
            ifr = np.concatenate((ifr[(icutf+1):], ifr[:icutf+1]))
            if yout[ifr[-1]] == yout[ifr[0]]:
                ifr = ifr[:-1]

        icutb_indices = np.where(np.diff(ibk) != 1)[0]
        if icutb_indices.size > 0:
            icutb = icutb_indices[0]
            ibk = np.concatenate((ibk[(icutb+1):], ibk[:icutb+1]))
            if yout[ibk[-1]] == yout[ibk[0]]:
                ibk = ibk[:-1]


        # Plot the inner and outer rings
        plt.plot(yin[ifr], zin[ifr], color=clrdisk)
        plt.plot(yin[ibk], zin[ibk], linestyle='--', color=clrdisk)
        plt.plot(yout[ifr], zout[ifr], color=clrdisk)
        plt.plot(yout[ibk], zout[ibk], linestyle='--', color=clrdisk)

        # Plot the star
        plt.plot(0, 0, 'o', color='black')
        plt.show()
        plt.close()

    return intot, intotx, en, spec