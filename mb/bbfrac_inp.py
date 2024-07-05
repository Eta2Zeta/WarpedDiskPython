import numpy as np

def bbfrac_inp(logT, bbfracv, T):
    """
    We assume that logT is evenly spaced in log space.
    Perform (logarithmic) interpolation to find the blackbody fraction.
    """
    Tl = np.log10(T)

    nT = len(logT)
    Tfirst = logT[0]
    Tlast = logT[-1]

    igood = np.arange(4) + int(nT * (Tl - Tfirst) / (Tlast - Tfirst)) - 2

    # Do the (logarithmic) interpolation
    ilow = igood[logT[igood] < Tl]
    ihi = igood[logT[igood] >= Tl]

    lowT = logT[ilow[-1]]
    lowbbfr = bbfracv[ilow[-1]]
    hiT = logT[ihi[0]]
    hibbfr = bbfracv[ihi[0]]

    bbfracout = (hibbfr - lowbbfr) / (hiT - lowT) * (Tl - lowT) + lowbbfr

    return bbfracout
