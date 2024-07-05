import numpy as np

def maskit(nprof, nang, xv2, yv2, zv2):
    """
    Masks out the parts of the disk that cannot be seen.

    Args:
    nprof (int): Number of profile points.
    nang (int): Number of angular points.
    xv2, yv2, zv2 (numpy.array): Coordinates of points on the disk.

    Returns:
    numpy.array: Mask array indicating visible (1) or occluded (0) status for each point.
    """
    # Initialize the mask and visibility arrays
    bdone = np.zeros((nang, nprof), dtype=int)
    iplot = np.ones((nang, nprof), dtype=int)

    # Iterate over all profiles and angles
    for j1 in range(nprof):
        for i1 in range(nang):
            ii = i1 + nang * j1
            ix = ii % nang  # Adjusted index for x
            jx = ii // nang  # Adjusted index for y

            if bdone[ix, jx] == 1:
                continue  # Skip already processed points

            iplot[ix, jx] = 1  # Mark as visible

            # Determine neighbors to consider for occlusion
            ixnds = [ix - 1 if ix > 0 else nang - 1, (ix + 1) % nang]
            jxnds = [jx - 1 if jx > 0 else nprof - 1, (jx + 1) % nprof]

            # Calculate center points for visibility determination
            cy = (yv2[ixnds, jx] + yv2[ix, jx]) / 2
            cz = (zv2[ixnds, jx] + zv2[ix, jx]) / 2

            # Find the points that are within the visible region defined by cy, cz
            visible = np.where((bdone == 0) & 
                               (yv2 >= np.min(cy)) & (yv2 <= np.max(cy)) &
                               (zv2 >= np.min(cz)) & (zv2 <= np.max(cz)))

            if visible[0].size > 0:
                # Further refine visibility based on more detailed criteria if needed
                bdone[visible] = 1  # Mark these points as processed
                iplot[visible] = 0  # Mark these points as not visible

    # Final pass to clean up any solitary visible points
    for i2 in range(nang):
        for j2 in range(1, nprof - 1):
            if iplot[i2, j2 - 1] + iplot[i2, j2 + 1] == 0:
                iplot[i2, j2] = 0  # Mask solitary points

    return iplot
