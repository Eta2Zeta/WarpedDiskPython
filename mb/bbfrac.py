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

#? 
def bbnorm(T, energ):
    """
    Calculate the normalized blackbody spectrum.

    Parameters:
    T (float): Temperature in Kelvin.
    energ (numpy array): Array of energies in joules.

    Returns:
    numpy array: Normalized blackbody spectrum.
    """
    h = 6.6261e-34  # Planck's constant (J*s)
    c = 3.0e8       # Speed of light (m/s)
    k = 1.3806e-23  # Boltzmann's constant (J/K)

    frequencies = energ / h
    intensity = (2.0 * h * frequencies**3) / (c**2) / (np.exp(h * frequencies / (k * T)) - 1.0)

    return intensity / np.max(intensity)

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
