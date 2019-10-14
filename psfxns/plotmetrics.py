import matplotlib.pyplot as plt
import numpy as np


def heatmap_subplot(heatdata, CO2indx, minval, maxval, plotnum, metriclabel,
                   highperform_num):
    """Create a heatmap of performance metric values.

    :param heatdata (numpy.ndarray): 3-D array containing a performance 
        metric values indexed by (CO2levels, varlist, nens)
    :param CO2indx (int): index for background carbon dioxide level,
        where 0 = 367 ppm, 1 = 400ppm
    :param minval (int, float): minimum value for heatmap colorbar
    :param maxval(int, float): maximum value for heatmap colorbar
    :param plotnum (int): subplot number
    :param metriclabel (str): label for performance metric
    :param highperform_num (numpy.ndarray): vector of numbers
        corresponding to high-performing parameter sets
    :return: heatmap subplot for one performance metric
    """
    
    # Number of parameter sets
    nens = np.size(heatdata,2)
    
    #Subplot indexing paramter
    i = 2
    
    # Figure labels
    heat_var_labels = ["LAI", "AGB", "BA",
                   "GPP", "LH", "SH",
                   "Av$_{E}$", "Av$_{S}$", "Av$_{C}$"]
    ens10label = [str(int(x)) for x in highperform_num]
    highperform_indx = (highperform_num - 1)
    ens = np.array(range(25, nens, 25))
    enslist = [str(x) for x in ens]
    
    # Plot highest-performing parameter sets
    ax1 = plt.subplot(3, i, plotnum)
    im1 = ax1.imshow(
        heatdata[CO2indx, :, highperform_indx],
        vmin=minval, vmax=maxval,
        cmap='viridis_r', aspect='auto')

    ax1.set_xticks(np.arange(len(heat_var_labels)))
    ax1.xaxis.tick_top()
    ax1.set_xticklabels(heat_var_labels)
    ax1.xaxis.set_label_position('top')

    ax1.set_ylabel('High Performing Parameter Sets (#)')
    ax1.set_yticks(np.arange(len(ens10label)))
    ax1.set_yticklabels(ens10label)

    # Plot all parameter sets
    ax2 = plt.subplot(3, i, (i+plotnum, i*2+plotnum))
    im2 = ax2.imshow(
        np.transpose(heatdata[CO2indx, :, :]),
        vmin=minval, vmax=maxval,
        cmap='viridis_r', aspect='auto')
    
    # Colorbar
    cbar = ax1.figure.colorbar(
        im2, ax=ax2, orientation='horizontal', 
        pad=0.025)
    # Labels
    cbar.ax.set_xlabel(metriclabel, fontsize=16, 
                       fontweight='bold')
    ax2.set_xticks([]) # hide xticks/labels
    ax2.set_ylabel('All Parameter Sets (#)')
    ax2.set_yticks(ens)
    ax2.set_yticklabels(enslist)