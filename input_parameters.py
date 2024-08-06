import os
import numpy as np

def input_parameters(topdir='./test/'):
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
        beam_params = [
            {'longdeg': 0.0, 'latdeg': 40.0, 'sigma': 60.0, 'thdeg': 60.0, 'norm': 3.0},
            {'longdeg': 130.0, 'latdeg': 60.0, 'sigma': 60.0, 'thdeg': 60.0, 'norm': 3.0}
        ]
    else:
        # PENCIL BEAM properties        
        beam_params = [
            {'longdeg': 0.0, 'latdeg': 0.0, 'sigma': np.pi / 10, 'thdeg': 0.0, 'norm': 3.0},
            {'longdeg': 180.0, 'latdeg': 60.0, 'sigma': np.pi / 2, 'thdeg': 0.0, 'norm': 3.0}
        ]

    # Convert degrees to radians
    for beam in beam_params:
        beam['long'] = np.radians(beam['longdeg'])
        beam['lat'] = np.radians(beam['latdeg'])
        beam['th'] = np.radians(beam['thdeg'])

    tiltinv = np.radians(tiltindeg)
    tiltoutv = np.radians(tiltoutdeg)
    phsoffv = np.radians(phsoffvdeg)
    obselevv = np.radians(obselevdeg)

    # More beam properties
    floor = 1.0

    # Disk angles
    npoints = 100
    nprof = 100
    nth = npoints
    nphi = npoints

    # Disk viewing angles
    nangtoview = 2

    # Beam rotation angles
    nang = 128
    istep = nphi / nang
    iang = np.fix(np.arange(nang) * istep).astype(int)

    rinphys = 1e8  # The location of the magnetosphere is around 10^8 cm
    lum38 = 3.0  # The total hard emission luminosity in 10^38 ergs s^{-1}
    icnt = 0

    # Appropriate values of phase to use
    ph = np.linspace(0, 1, npoints, endpoint=False) + 0.0001

    for iobs in range(len(obselevv)):
        obselev = obselevv[iobs]
        strobs = f'obs{int(obselevdeg[iobs]):+03d}'.replace('+', '').replace('-', 'm')

        for itin in range(len(tiltinv)):
            tiltin = tiltinv[itin]
            strtin = f'tin{int(tiltindeg[itin]):02d}'

            for itout in range(len(tiltoutv)):
                tiltout = tiltoutv[itout]
                strtout = f'tout{int(tiltoutdeg[itout]):02d}'

                for ith in range(len(beam_params)):
                    th = beam_params[ith]['th']
                    strth = f'th{int(np.degrees(th)):02d}'

                    for i in range(len(phsoffv)):
                        phsoff = phsoffv[i]

                        if phsoff < 0:
                            strphs = f'tw_m{abs(int(phsoffvdeg[i])):03d}'
                        else:
                            strphs = f'tw{int(phsoffvdeg[i]):03d}'

                        dirname = f"{topdir}{icnt:03d}{strobs}{strtin}{strtout}{strphs}{strth}"
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
                            for bidx, beam in enumerate(beam_params):
                                f.write(f'beam_{bidx+1}_long={beam["long"]}\n')
                                f.write(f'beam_{bidx+1}_lat={beam["lat"]}\n')
                                f.write(f'beam_{bidx+1}_sigma={beam["sigma"]}\n')
                                f.write(f'beam_{bidx+1}_th={beam["th"]}\n')
                                f.write(f'beam_{bidx+1}_norm={beam["norm"]}\n')
                            f.write(f'floor={floor}\n')
                            f.write(f'rinphys={rinphys}\n')
                            f.write(f'lum38={lum38}\n')
                            f.write(f'obselev={obselev}\n')
                            f.write(f'nangtoview={nangtoview}\n')  # Add this line to the .dat file

                        # Save parameters using numpy
                        params = {
                            'rin': rin, 'rout': rout, 'tiltin': tiltin, 'tiltout': tiltout, 'phsoff': phsoff,
                            'npoints': npoints, 'nprof': nprof, 'nth': nth, 'nphi': nphi, 'nang': nang,
                            'floor': floor, 'rinphys': rinphys, 'lum38': lum38, 'obselev': obselev, 'ph': ph,
                            'nangtoview': nangtoview  # Add this line to the .npz file
                        }
                        for bidx, beam in enumerate(beam_params):
                            params[f'beam_{bidx+1}_long'] = beam['long']
                            params[f'beam_{bidx+1}_lat'] = beam['lat']
                            params[f'beam_{bidx+1}_sigma'] = beam['sigma']
                            params[f'beam_{bidx+1}_th'] = beam['th']
                            params[f'beam_{bidx+1}_norm'] = beam['norm']

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
        for bidx, beam in enumerate(beam_params):
            f.write(f'beam_{bidx+1}_long={beam["long"]}\n')
            f.write(f'beam_{bidx+1}_lat={beam["lat"]}\n')
            f.write(f'beam_{bidx+1}_sigma={beam["sigma"]}\n')
            f.write(f'beam_{bidx+1}_th={beam["th"]}\n')
            f.write(f'beam_{bidx+1}_norm={beam["norm"]}\n')
        f.write(f'floor={floor}\n')
        f.write(f'rinphys={rinphys}\n')
        f.write(f'lum38={lum38}\n')
        f.write(f'nangtoview={nangtoview}\n')  # Add this line to the summary .dat file
