import os
import numpy as np

def fit_inp(topdir='./test/'):
    """
    Create input files for doing a set of simulated profiles for several disk and beam shapes.
    """
    os.makedirs(topdir, exist_ok=True)

    fan = 'n'
    # Disk properties
    rin = 0.8
    rout = 1.0
    tiltindeg = [5.0]
    tiltoutdeg = [30.0]
    phsoffvdeg = [139.0]

    # Observation properties
    obselevdeg = [-5.0]

    # Beam properties based on the beam type (fan or pencil)
    if fan == 'y':
        # FAN BEAM properties
        sigma1 = np.pi / 3
        sigma2 = np.pi / 3
        long1 = 0.0
        long2vdeg = [130.0]
        thvdeg = [60.0]
        beamangdeg1 = [40.0]
        beamangdeg2 = [60.0]
    else:
        # PENCIL BEAM properties        
        sigma1 = np.pi / 10
        sigma2 = np.pi / 2
        long1 = 0.0
        long2vdeg = [180.0]
        thvdeg = [0.0]
        beamangdeg1 = [0.0]
        beamangdeg2 = [60.0]


    # Convert degrees to radians
    beamang1 = np.radians(beamangdeg1)
    beamang2 = np.radians(beamangdeg2)
    tiltinv = np.radians(tiltindeg)
    tiltoutv = np.radians(tiltoutdeg)
    phsoffv = np.radians(phsoffvdeg)
    obselevv = np.radians(obselevdeg)
    thv = np.radians(thvdeg)
    long2v = np.radians(long2vdeg)

    # More beam properties
    norm1 = 3.0
    norm2 = 3.0
    floor = 1.0

    # Disk angles
    npoints = 100
    nprof = 100
    nth = npoints
    nphi = npoints

    # Beam rotation angles
    nang = 128
    istep = nphi / nang
    iang = np.fix(np.arange(nang) * istep).astype(int)

    rinphys = 1e8 #The location of the magnetosphere is around 10^8 cm
    lum38 = 3.0 #The total hard emissino luminosity in 10^38 ergs s^{-1}
    icnt = 0

    # not sure what this is yet
    # Appropriate values of phase to use
    ph = np.linspace(0, 1, npoints, endpoint=False) + 0.0001

    for iobs in range(len(obselevv)):
        obselev = obselevv[iobs]

        # Converting the float into int first and then make it at least two digits for the file naming
        strobs = f'obs{int(obselevdeg[iobs]):+03d}'
        strobs = strobs.replace('+', '').replace('-', 'm')


        for itin in range(len(tiltinv)):
            tiltin = tiltinv[itin]
            strtin = f'tin{int(tiltindeg[itin]):02d}'

            for itout in range(len(tiltoutv)):
                tiltout = tiltoutv[itout]
                strtout = f'tout{int(tiltoutdeg[itout]):02d}'

                for ith in range(len(thv)):
                    th1 = thv[ith]
                    th2 = th1
                    strth = f'th{int(thvdeg[ith]):02d}'

                    for i in range(len(phsoffv)):
                        phsoff = phsoffv[i]

                        if phsoff < 0:
                            strphs = f'tw_m{abs(int(phsoffvdeg[i])):03d}'
                        else:
                            strphs = f'tw{int(phsoffvdeg[i]):03d}'

                        for ibm1 in range(len(beamang1)):
                            for ibm2 in range(len(beamang2)):
                                lat1 = beamang1[ibm1]
                                lat2 = beamang2[ibm2]

                                bm1str = 'm' if beamangdeg1[ibm1] < 0 else '_'
                                bm2str = 'm' if beamangdeg2[ibm2] < 0 else '_'
                                strbm = f'bm1{bm1str}{abs(int(beamangdeg1[ibm1])):02d}bm2{bm2str}{abs(int(beamangdeg2[ibm2])):02d}'

                                for ilng in range(len(long2v)):
                                    long2 = long2v[ilng]
                                    strlng = f'lng{int(long2vdeg[ilng]):03d}'

                                    dirname = f"{topdir}{icnt:03d}{strobs}{strtin}{strtout}{strphs}{strth}{strbm}{strlng}"
                                    os.makedirs(dirname, exist_ok=True)

                                    # Write parameters to a file
                                    with open(f"{dirname}/par.dat", 'w') as f:
                                        f.write(f'INPUT to warp disk shape: {dirname}\n')
                                        f.write(f'#UTC: {np.datetime64("now")}\n\n')
                                        f.write('DISK PARAMETERS:\n')
                                        f.write(f'rin={rin}\n')
                                        f.write(f'rout={rout}\n')
                                        f.write(f'tiltin={tiltin}\n')
                                        f.write(f'tiltout={tiltout}\n')
                                        f.write(f'phsoff={phsoffv[i]}\n')
                                        f.write(f'npoints={npoints}\n')
                                        f.write(f'nprof={nprof}\n')
                                        f.write(f'nth={nth}\n')
                                        f.write(f'nphi={nphi}\n')
                                        f.write(f'ph={ph}\n\n')
                                        f.write('BEAM PARAMETERS:\n')
                                        f.write(f'nang={nang}\n')
                                        f.write(f'long1={long1}\n')
                                        f.write(f'lat1={lat1}\n')
                                        f.write(f'long2={long2}\n')
                                        f.write(f'lat2={lat2}\n')
                                        f.write(f'sigma1={sigma1}\n')
                                        f.write(f'sigma2={sigma2}\n')
                                        f.write(f'th1={th1}\n')
                                        f.write(f'th2={-th2}\n')
                                        f.write(f'norm1={norm1}\n')
                                        f.write(f'norm2={norm2}\n')
                                        f.write(f'floor={floor}\n')
                                        f.write(f'rinphys={rinphys}\n')
                                        f.write(f'lum38={lum38}\n')
                                        f.write(f'obselev={obselev}\n')

                                    # Save parameters using numpy
                                    params = {
                                        'rin': rin, 'rout': rout, 'tiltin': tiltin, 'tiltout': tiltout, 'phsoff': phsoff,
                                        'npoints': npoints, 'nprof': nprof, 'nth': nth, 'nphi': nphi, 'nang': nang,
                                        'long1': long1, 'lat1': lat1, 'long2': long2, 'lat2': lat2, 'sigma1': sigma1,
                                        'sigma2': sigma2, 'th1': th1, 'th2': th2, 'norm1': norm1, 'norm2': norm2,
                                        'floor': floor, 'rinphys': rinphys, 'lum38': lum38, 'obselev': obselev, 'ph': ph
                                    }
                                    np.savez(f"{dirname}/par.npz", **params)

                                    icnt += 1

    # Write parameters for all runs to a file
    with open(f"{topdir}/par.dat", 'w') as f:
        f.write(f'INPUT to warp disk shape (multiple runs): {topdir}\n')
        f.write(f'#UTC: {np.datetime64("now")}\n\n')
        f.write('DISK PARAMETERS:\n')
        f.write(f'rin={rin}\n')
        f.write(f'rout={rout}\n')
        f.write(f'tiltin={tiltindeg}\n')
        f.write(f'tiltout={tiltoutdeg}\n')
        f.write(f'phsoff={phsoffvdeg}\n')
        f.write(f'npoints={npoints}\n')
        f.write(f'nprof={nprof}\n')
        f.write(f'nth={nth}\n')
        f.write(f'nphi={nphi}\n')
        f.write(f'ph={ph}\n\n')
        f.write(f'obselev={obselevdeg}\n')
        f.write('BEAM PARAMETERS:\n')
        f.write(f'nang={nang}\n')
        f.write(f'beam angles 1={beamangdeg1}\n')
        f.write(f'beam angles 2={beamangdeg2}\n')
        f.write(f'long1={long1}\n')
        f.write(f'long2={long2v}\n')
        f.write(f'sigma1={sigma1}\n')
        f.write(f'sigma2={sigma2}\n')
        f.write(f'th1={thvdeg}\n')
        f.write(f'th2={thvdeg}\n')
        f.write(f'norm1={norm1}\n')
        f.write(f'norm2={norm2}\n')
        f.write(f'floor={floor}\n')
        f.write(f'rinphys={rinphys}\n')
        f.write(f'lum38={lum38}\n')
        

