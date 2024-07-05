# I accidentally translated this again so this is an alternative

import numpy as np

def scale_offs(xdata, p, xprof, prof, diffprof):
    """
    This function adjusts a calculated lightcurve to fit an observed lightcurve by applying scaling and phase shifting.
    
    Parameters:
    xdata (np.array): The observed data's x-values.
    p (list): Parameters for scaling and phase shifting. p[0] is scale, p[1] is offset.
    xprof (np.array): The x-values of the profile to be adjusted.
    prof (np.array): The profile values to be adjusted.
    diffprof (np.array): The differential of the profile, precomputed for speed.

    Returns:
    np.array: The adjusted profile values.
    """
    scale = p[0]
    offs = p[1]

    # Normalize the profile x-values from 0 to 1
    nprof = len(xprof)
    pstep = 1.0 / nprof

    # Adjust xdata by the offset and wrap around using modulo to stay within the profile's x-range
    xpdata2 = (xdata + offs) % 1.0

    # Determine the indices of the profile that correspond to the adjusted xdata
    iprofoff = np.floor(xpdata2 / pstep).astype(int)

    # Calculate the difference from the exact location in xprof
    diffoff = xpdata2 - xprof[iprofoff]

    # Interpolate the profile values at the shifted locations
    shape = prof[iprofoff] + diffprof[iprofoff] * diffoff / pstep

    # Apply scaling to the shifted and interpolated profile
    yout = 1 + scale * (shape - np.mean(shape))
    
    return yout
