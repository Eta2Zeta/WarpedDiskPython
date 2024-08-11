import numpy as np
import os
from beam import beam_luminosity, Beam
from disktemp import disktemp  # Import the disktemp function from the disktemp module
from ploting.plt_beam import plot_beam_3D
import time

def disktempsave(bdir):
    """
    Calculate disk temperature profiles for a particular beam shape and save them in .npz files.
    """
    print("Loading parameters from par.npz...")
    # Load parameters from the file
    params_path = os.path.join(bdir, 'par.npz')
    params_data = np.load(params_path)

    npoints = params_data['npoints']
    nprofs = params_data['nprof']
    
    # Extract parameters from the loaded data
    rin = params_data['rin']
    rout = params_data['rout']
    tiltin = params_data['tiltin']
    tiltout = params_data['tiltout']
    phsoff = params_data['phsoff']
    ph = params_data['ph']
    nphi_beam = params_data['nphi']
    nth_beam = params_data['nth']
    rinphys = params_data['rinphys']
    lum38 = params_data['lum38']
    nang = params_data['nang']

    disk_parameters = [rin,rout,tiltin,tiltout,phsoff]

    # Extract multiple beam parameters
    beams = []
    for key in params_data:
        if key.startswith('beam_'):
            idx = int(key.split('_')[1])
            if len(beams) < idx:
                beams.append({})
            param_type = key.split('_')[2]
            beams[idx - 1][param_type] = params_data[key]

    print("Generating the beam shape...")

    # Convert beam dictionaries to Beam objects
    beam_objects = [Beam(**beam) for beam in beams]

    # Generate the beam shape using the provided parameters
    thbeam, phbeam, nlum = beam_luminosity(nth_beam, nphi_beam, beam_objects, 0, 0)

    print("Saving beam parameters to diskbeam.npz...")
    # Save the beam parameters and generated beam shape to a file
    beam_params_path = os.path.join(bdir, 'diskbeam.npz')
    np.savez(beam_params_path, nth=nth_beam, nphi=nphi_beam, beams=beams, thbeam=thbeam, phbeam=phbeam, nlum=nlum, 
             rinphys=rinphys)
    
    # Initialize an array to hold the emitted luminosities for each angle
    lemitv = np.zeros(nang)

    print("Calculating disk temperature profiles for each angle...")
    # Calculate the step size for angles
    angle_step = 2 * np.pi / nang

    # Loop over each angle
    for ang in range(nang):
        print(f"Processing angle {ang + 1} of {nang}...")
        rotation_angle = ang * angle_step
        
        # Generate the beam shape with the correct rotation angle
        thbeam, phbeam, nlum_rotated = beam_luminosity(nth_beam, nphi_beam, beam_objects, 0.1, rotation_angle)

        # Calculate the illumination based on the rotated beam
        illum = nlum_rotated * lum38

        # Create a disk and heat it with an isotropic X-ray source
        xv = np.zeros((npoints, nprofs))
        yv = np.zeros((npoints, nprofs))
        zv = np.zeros((npoints, nprofs))
        T = np.zeros((npoints, nprofs))
        side = np.zeros((npoints, nprofs), dtype=int)
        lemit = 0.0
        
        # Calculate the disk temperature and other properties
        side, T, _, labs, lemit = disktemp(params_data['npoints'], params_data['nprof'], rinphys, thbeam, phbeam, illum, 
                ph, xv, yv, zv, T, side, lemit, disk_parameters)
        
        print(f"Saving disk temperature profile to dtemp_{ang:03d}.npz...")
        # Save the disk temperature profile and other properties to a file
        dtemp_path = os.path.join(bdir, f'dtemp_{ang:03d}.npz')
        np.savez(dtemp_path, ph=params_data['ph'], illum=illum, xv=xv, yv=yv, zv=zv, labs=labs, T=T, side=side, phbeam=phbeam)
        
        # Store the emitted luminosity for the current angle in the lemitv array
        lemitv[ang] = lemit
    
    print("Saving emitted luminosity vector to lemit.npz...")
    # Save the emitted luminosity vector to a file
    lemit_path = os.path.join(bdir, 'lemit.npz')
    np.savez(lemit_path, lemitv=lemitv)

    print("Disk temperature profiles calculation and saving completed.")
