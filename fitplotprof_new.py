import os
import numpy as np
import matplotlib.pyplot as plt

def fitplotprof_new(bdir, eraseit):
    """
    Update Ryan's fitplotprof with newer plotting routines/larger plots.

    :param bdir: Base directory containing the data
    :param eraseit: Flag to indicate whether to erase diskvf.idl file
    """
    # Plot margins
    l = 0.13
    tb = 0.18
    r = 0.07

    # Setting values for loop
    nang = 8
    ang = np.arange(nang) / nang
    strang = [f"{a:.3f}" for a in ang]

    # This is the offset
    offs = np.zeros(nang, dtype=int)

    # This plots the disk at various phi angles
    for i in range(nang):
        a = i + 1
        shiftdown1 = 0.876 - a * 0.125
        shiftdown2 = 0.99 - a * 0.125

        # This is the angle that the DISK is rotated
        # print(f'plotting disk angle phi: {strang[i]}')
        # print(f'restoring {bdir}diskphi_{strang[i]}/inprof.pkl')
        
        inprof_data = np.load(os.path.join(bdir, f'diskphi_{strang[i]}', 'inprof.npz'))
        
        instar = inprof_data['instar']
        inrepx = inprof_data['inrepx']

        # This ERASES the diskvf.pkl file (to save space)
        if eraseit == 'y':
            os.remove(os.path.join(bdir, f'diskphi_{strang[i]}', 'diskvf.npz'))

        ntemps = len(instar)

        # Figure out the offset for the plot
        offsi = np.argmax(instar)
        offs[i] = offsi - 7
        if offs[i] < 0:
            print(f'going negative! {offs[i]}')
            offs[i] = ntemps + offs[i]

        ntemps = len(instar)

        if offs[i] == 0:
            io = np.arange(ntemps - offs[i])
        else:
            # These are the indices (including the offset)
            io = np.concatenate((np.arange(offs[i], ntemps), np.arange(offs[i])))

        # y range for all plots 
        yr = [0.0, 2.5]

        x = np.arange(ntemps) / ntemps
        x2 = np.concatenate((x, 1.0 + x))
        ystar = instar[io] / np.mean(instar)
        ystar2 = np.concatenate((ystar, ystar))
        yrep = inrepx[io] / np.mean(inrepx)
        yrep2 = np.concatenate((yrep, yrep))

        # Plotting with the plot function, all in current window
        plt.figure()
        plt.plot(x2, ystar2, label='Hard', color='blue')
        plt.plot(x2, yrep2, linestyle='dotted', label='Soft', color='red')
        plt.ylim(yr)
        plt.yticks([0, 1.25, 2.5])
        plt.xlabel('Phase')
        plt.ylabel('Relative intensity (hard solid, soft dotted)')
        plt.title(f'Disk angle phi: {strang[i]}')
        plt.legend()
        plt.savefig(os.path.join(bdir, f'plot_phi_{strang[i]}.png'))
        plt.close()

        # Make array to hold the stuff
        if i == 0:
            ystars = np.zeros((ntemps, nang))
            yreps = np.zeros((ntemps, nang))

        ystars[:, i] = ystar
        yreps[:, i] = yrep

    # Save the results
    # with open(os.path.join(bdir, 'profs.pkl'), 'wb') as f:
    #     pickle.dump({'x': x, 'ystars': ystars, 'yreps': yreps}, f)

if __name__ == "__main__":
    fitplotprof_new('/path/to/data', eraseit='y')
