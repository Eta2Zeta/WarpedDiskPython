import numpy as np
import matplotlib.pyplot as plt
import os

def fitplotprof(bdir, eraseit):
    """
    Plots the pulse profiles for the disk models at different phi angles.
    
    Parameters:
        bdir (str): Base directory containing the diskphi data folders.
        eraseit (bool): If True, delete 'diskvf.idl' files after processing.
    """
    params_path = os.path.join(bdir,'par.npz')
    params = np.load(params_path)

    nang = params['nangtoview']
    ang = np.arange(nang) / nang
    offsets = np.zeros(nang, dtype=int)
    
    # Set plot margins and configurations
    fig, axs = plt.subplots(2, 4, figsize=(15, 8), sharex=True, sharey=True)
    
    for i in range(nang):
        phi_dir = f'diskphi_{ang[i]:.3f}'
        file_path = os.path.join(bdir, phi_dir, 'inprof.npz')
        
        # Print current action
        print(f'Plotting disk angle phi: {ang[i]:.3f}')
        print(f'Restoring {file_path}')
        
        # Restore data
        data = np.load(file_path)
        instar = data['instar']
        inrepx = data['inrepx']
        
        # Optional: remove diskvf.idl to save space
        if eraseit:
            idl_file_path = os.path.join(bdir, phi_dir, 'diskvf.idl')
            if os.path.exists(idl_file_path):
                os.remove(idl_file_path)
        
        # Calculate offsets for plotting
        offsets[i] = np.argmax(instar) - 7
        if offsets[i] < 0:
            offsets[i] += len(instar)
        
        # Determine the indices including the offset
        io = np.concatenate([np.arange(offsets[i], len(instar)), np.arange(offsets[i])])
        
        # Prepare data for plotting
        ystar = instar[io] / np.mean(instar)
        yrep = inrepx[io] / np.mean(inrepx)
        x = np.arange(len(ystar)) / len(ystar)
        
        # Plot
        ax = axs.flatten()[i]
        ax.plot(x, ystar, label='Normalized Star Intensity')
        ax.plot(x, yrep, linestyle='dashed', label='Reprocessed Intensity')
        ax.set_ylim([0.5, 2.0])
        ax.set_title(f'phi: {ang[i]:.3f}')
        
        if i == 0:
            ax.legend()
    
    plt.tight_layout()
    plt.show()
    plt.close()
    
    # Save the processed profiles to a .npz file
    np.savez(os.path.join(bdir, 'profs.npz'), x=x, ystars=ystar, yreps=yrep)

