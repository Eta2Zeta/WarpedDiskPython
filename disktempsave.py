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
    
    # Extract parameters from the loaded data
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
    nang = params_data['nang']
    
    # Calculate the step size for angles and create an array of indices representing the beam rotation angles
    istep = nphi / nang
    iang = (np.arange(nang) * istep).astype(int)
    
    # Parameters for the beam function
    params = [rin, rout, tiltin, tiltout, phsoff]
    
    # Generate the beam shape using the provided parameters
    thbeam, phbeam, nbeam = beam(nth, nphi, long1, lat1, sigma1, th1, norm1, long2, lat2, sigma2, th2, norm2, 0)
    
    # Save the beam parameters and generated beam shape to a file
    beam_params_path = os.path.join(bdir, 'diskbeam.npz')
    np.savez(beam_params_path, nth=nth, nphi=nphi, long1=long1, lat1=lat1, long2=long2, lat2=lat2,
             sigma1=sigma1, sigma2=sigma2, th1=th1, th2=th2, norm1=norm1, norm2=norm2, 
             thbeam=thbeam, phbeam=phbeam, nbeam=nbeam, params=params, rinphys=rinphys, lum38=lum38)
    
    # Initialize an array to hold the emitted luminosities for each angle
    lemitv = np.zeros(nang)

    # Loop over each angle
    for j in range(nang):
        ij = iang[j]
        nbeam_copy = np.copy(nbeam)
        
        # Rotate the beam to the current angle ij
        if ij != 0 and ij != nphi - 1:
            nbeam_copy[:, :nphi - ij] = nbeam[:, ij:]
            nbeam_copy[:, nphi - ij:] = nbeam[:, :ij]
        
        # Calculate the illumination based on the rotated beam
        illum = nbeam_copy * lum38

        # Create a disk and heat it with an isotropic X-ray source
        xv = np.zeros((params_data['npoints'], params_data['nprof']))
        yv = np.zeros((params_data['npoints'], params_data['nprof']))
        zv = np.zeros((params_data['npoints'], params_data['nprof']))
        T = np.zeros((params_data['npoints'], params_data['nprof']))
        side = np.zeros((params_data['npoints'], params_data['nprof']), dtype=int)
        lemit = 0.0
        
        # Calculate the disk temperature and other properties
        side, T, _, labs, lemit = disktemp(params_data['npoints'], params_data['nprof'], rinphys, thbeam, phbeam, illum, 
                params_data['ph'], xv, yv, zv, T, side, lemit, params_data)
        
        # Save the disk temperature profile and other properties to a file
        dtemp_path = os.path.join(bdir, f'dtemp_{j:03d}.npz')
        np.savez(dtemp_path, ph=params_data['ph'], illum=illum, xv=xv, yv=yv, zv=zv, labs=labs, T=T, side=side, phbeam=phbeam)
        
        # Store the emitted luminosity for the current angle in the lemitv array
        lemitv[j] = lemit
    
    # Save the emitted luminosity vector to a file
    lemit_path = os.path.join(bdir, 'lemit.npz')
    np.savez(lemit_path, lemitv=lemitv)