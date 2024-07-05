import numpy as np
from scipy.interpolate import interp1d

def scale_offs(xdata, p, xprof, prof, diffprof):
    """
    Fit calculated lightcurves to observed data by scaling and phase shifting.

    Parameters:
    xdata : numpy.array
        The X data of the observed lightcurve.
    p : numpy.array
        Parameters for scaling (p[0]) and phase shifting (p[1]).
    xprof : numpy.array
        The X data of the calculated lightcurve profiles (should range from 0 to 1).
    prof : numpy.array
        The calculated lightcurve profiles corresponding to xprof.
    diffprof : numpy.array
        The derivative of prof, precomputed to speed up calculations.

    Returns:
    yout : numpy.array
        The scaled and shifted lightcurve to fit the observed data.
    """
    scale = p[0]
    offs = p[1]

    # Shift xdata with wrap-around using modulo to handle the periodic boundary condition
    xpdata2 = (xdata + offs) % 1.0

    # Create an interpolator for the profile
    interp_func = interp1d(xprof, prof, kind='linear', fill_value="extrapolate")
    interp_diff_func = interp1d(xprof, diffprof, kind='linear', fill_value="extrapolate")

    # Interpolate prof and diffprof at new phase-shifted x positions
    prof_interp = interp_func(xpdata2)
    diffprof_interp = interp_diff_func(xpdata2)

    # pstep is the step size in xprof, assumed to be uniformly spaced
    pstep = xprof[1] - xprof[0]

    # Calculate the offset within each step
    diffoff = (xpdata2 % pstep) / pstep

    # Interpolate to find the adjusted profile shape
    shape = prof_interp + diffprof_interp * diffoff

    # Scale and shift the shape to fit the observed data
    yout = 1.0 + scale * (shape - np.mean(shape))

    return yout
