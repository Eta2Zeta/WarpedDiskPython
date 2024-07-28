import numpy as np
import os
from scipy.interpolate import interp1d

def enstr(en):
    """
    Convert energy to string format.
    """
    if en < 10:
        return f"0{en:.2f}"
    else:
        return f"{en:.2f}"

def file_which(directory, filename):
    """
    Check if a file exists in the given directory.
    """
    return os.path.exists(os.path.join(directory, filename))

def listarr(start, stop, num):
    """
    Create an array with logarithmically spaced elements.
    """
    return np.logspace(start, stop, num)


def bbnorm(T, E):
    """
    Calculate the normalized blackbody spectrum.

    Parameters:
    T (float): Temperature in Kelvin.
    E (numpy array): Array of energies in ergs.

    Returns:
    numpy array: Normalized blackbody spectrum.
    """
    k = 1.3807e-16  # Boltzmann's constant in erg/K
    cbb = 3.824     # This is 1/h^3c^2 / 1E57
    
    # Calculate blackbody spectrum
    bbe = 1.e20 * (E**3) / (np.exp(E / (k * T)) - 1.)
    
    # Calculate the difference between consecutive elements of E
    Ebin = np.diff(E)
    
    # Integrate the blackbody spectrum
    bbint = np.sum(bbe[:-1] * Ebin)
    
    # Normalize the spectrum
    bbn = bbe / bbint


def bbfrac(enlo, enhi, T):
    """
    This takes an energy range enlo to enhi (in keV),
    a temperature (in K), and calculates the fraction of
    the total blackbody curve that is emitted in this energy range.
    RCH 8/9/04
    """
    # Convert energy to string format
    senlo = enstr(enlo)
    senhi = enstr(enhi)

    fname = f'bbf{senlo}_{senhi}.npz'
    ftop = '/home/rhickox/idl/xray/bbfrac/'

    # Check if the file exists
    r = file_which(ftop, fname)

    # If the file doesn't exist, perform the calculation
    if not r:
        print('Making grid for:')
        print(f'enlo: {senlo} keV')
        print(f'enhi: {senhi} keV')

        # Make the arrays for the temperature and energy
        keV = 1.6021E-9
        Tmin = 1.e4
        Tmax = 1.e8
        Tbins = 10000

        logT = listarr(np.log10(Tmin), np.log10(Tmax), Tbins)
        Tv = 10**logT

        enbins = 1000
        emin = 0.001
        emax = 100.0

        loge = listarr(np.log10(emin), np.log10(emax), enbins)
        en = 10**loge
        energ = en * keV

        endiff = np.diff(energ)

        ix = np.where((en >= enlo) & (en < enhi))[0]

        bbfracv = np.zeros(len(Tv))

        # Go through each temperature and do the calculation
        for i in range(len(Tv)):
            spec = bbnorm(Tv[i], energ)
            spectot = np.sum(spec[:-1] * endiff)
            specx = np.sum(spec[ix] * endiff[ix])
            bbfracv[i] = specx / spectot

        # Save the bb fraction vector (fracv)
        np.savez(os.path.join(ftop, fname), logT=logT, bbfracv=bbfracv)

    # Now restore the bbfracv file
    data = np.load(os.path.join(ftop, fname))
    logT = data['logT']
    bbfracv = data['bbfracv']

    # Do the (logarithmic) interpolation
    Tl = np.log10(T)
    ilow = np.where(logT < Tl)[0]
    ihi = np.where(logT >= Tl)[0]

    lowT = logT[ilow[-1]]
    lowbbfr = bbfracv[ilow[-1]]
    hiT = logT[ihi[0]]
    hibbfr = bbfracv[ihi[0]]

    bbfracout = (hibbfr - lowbbfr) / (hiT - lowT) * (Tl - lowT) + lowbbfr

    return bbfracout
