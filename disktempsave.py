import numpy as np
import os
from beam import beam  # Import the beam function from the beam module
from disktemp import disktemp  # Import the disktemp function from the disktemp module

def disktempsave(bdir):
    """
    Calculate disk temperature profiles for a particular beam shape and save them in .npz files.
    """
    # Load parameters from the file
    params_path = os.path.join(bdir, 'par.npz')
    params_data = np.load(params_path)
    
    rin = params_data['rin']
    rout = params_data['rout']
    tiltin = params_data['tiltin']
    tiltout = params_data['tiltout']
    phsoff = params_data['phsoff']
    nphi = params_data['nphi']
    nth = params_data['nth']
    long1 = params_data['long1']
    lat1 = params_data['lat1']
    sigma1 = params_data['sigma1']
    th1 = params_data['th1']
    norm1 = params_data['norm1']
    long2 = params_data['long2']
    lat2 = params_data['lat2']
    sigma2 = params_data['sigma2']
    th2 = params_data['th2']
    norm2 = params_data['norm2']
    rinphys = params_data['rinphys']
    lum38 = params_data['lum38']

    # Beam rotation angles
    nang = 128
    istep = nphi / nang
    iang = (np.arange(nang) * istep).astype(int)
    
    params = [rin, rout, tiltin, tiltout, phsoff]
    
    instar = np.zeros(nang)  # Array to hold the pulse profiles

    # Generate the beam
    thbeam, phbeam, nbeam, xv2, yv2, zv2 = beam(nth, nphi, long1, lat1, sigma1, th1, norm1, long2, lat2, sigma2, th2, norm2, 0)
    
    # Save the beam parameters
    beam_params_path = os.path.join(bdir, 'diskbeam.npz')
    np.savez(beam_params_path, nth=nth, nphi=nphi, long1=long1, lat1=lat1, long2=long2, lat2=lat2,
             sigma1=sigma1, sigma2=sigma2, th1=th1, th2=th2, norm1=norm1, norm2=norm2, 
             thbeam=thbeam, phbeam=phbeam, nbeam=nbeam, params=params, rinphys=rinphys, lum38=lum38)
    
    # Array to hold the emitted luminosities
    lemitv = np.zeros(nang)
    
    j = 0
    while j < nang:
        ij = iang[j]
        nbeam2 = np.copy(nbeam)
        
        if ij != 0 and ij != nphi - 1:
            nbeam2[:, :nphi - ij] = nbeam[:, ij:]
            nbeam2[:, nphi - ij:] = nbeam[:, :ij]
        
        illum = nbeam2 * lum38

        # Create a disk and heat it with an isotropic X-ray source
        xv = np.zeros((params_data['npoints'], params_data['nprof']))
        yv = np.zeros((params_data['npoints'], params_data['nprof']))
        zv = np.zeros((params_data['npoints'], params_data['nprof']))
        T = np.zeros((params_data['npoints'], params_data['nprof']))
        side = np.zeros((params_data['npoints'], params_data['nprof']), dtype=int)
        lemit = 0.0
        
        side, T, sang, labs, lemit = disktemp(params_data['npoints'], params_data['nprof'], rinphys, thbeam, phbeam, illum, 
                 params_data['ph'], xv, yv, zv, T, side, lemit, params_data)
        

        dtemp_path = os.path.join(bdir, f'dtemp_{j:03d}.npz')
        np.savez(dtemp_path, ph=params_data['ph'], illum=illum, xv=xv, yv=yv, zv=zv, labs=labs, T=T, side=side, phbeam = phbeam)
        
        # Put the emitted luminosity in the vector
        lemitv[j] = lemit
        
        # print(f'phi={phbeam[iang[j]]}')
        
        j += 1
    
    # Save the absorbed luminosity
    lemit_path = os.path.join(bdir, 'lemit.npz')
    np.savez(lemit_path, lemitv=lemitv)
