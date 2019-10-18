import netCDF4 as nc4
import numpy as np


def annual_mean_model(filepath, var, varfiletype, nyrs, conv_factor):
    """Calculate time series of model annual means for one variable.
    
    :param filepath (str): the file path and name for the data file
    :param var (str): the name of the variable to call from data file
    :param varfiletype (int): the model file type, where:
        0 - contains monthly averages for the entire ecosystem; and
        1 - contains annual mean values by tree size
    :param nyrs (int): the number of years to use in analysis
    :param conv_factor (int, float): the conversion factor for
        the variable given by var
    :return: a 2-D array containing the annual mean time series
        indexed by (parameter_set, nyrs)
    :rtype: numpy.ndarray
    """
    
    # If model output is stored as monthly ecosystem average,
    # calculate annual means.   
    if varfiletype == 0:
        
        # Load monthly time series
        if var != 'FLH':
            mthts_temp = nc4.Dataset(filepath).variables[var][:, :, 0]
        elif var == 'FLH':
            mthts_temp = (nc4.Dataset(filepath).variables['FCTR'][:, :, 0] 
                          + nc4.Dataset(filepath).variables['FGEV'][:, :, 0] 
                          + nc4.Dataset(filepath).variables['FCEV'][:, :, 0])
        
        # Calculate annual means for nyrs and convert units
        annmeants = (np.nanmean(np.reshape(
            (mthts_temp[:, int(-1*nyrs*12):]),
            (mthts_temp.shape[0], -1, 12)), 
            axis=2)) * conv_factor
        
        mthts_temp = None
        
    # If model output is stored as annual means by tree size,
    # sum across tree sizes.
    elif varfiletype == 1:
        
        # Calculate annual means for nyrs and convert units
        annmeants = np.squeeze(np.nansum((
            nc4.Dataset(filepath).variables[var + '_SCLS'][:, int(-1*nyrs):, :]),
            axis=2)) * conv_factor
    
    return annmeants


def annual_mean_fluxobs(mthts, startmth):
    """Calculate annual mean time series from monthly fluxtower estimates.
    
    :param mthts (numpy.ndarray): a 2-D array of fluxtower 
        observations with shape (years, months)
    :param startmth (int): the number of the start month
        for this annual mean time series calculation
        (e.g., 7 = start with July, 9 = start with Sept)
    :return: a vector containing the annual mean time series
    :rtype: numpy.ndarray
    """
    
    # Specify number of months to discard
    mthts_dif = np.reshape(mthts, (1, -1))[:, startmth-1 : startmth-1-12]
    
    # Calculate annual mean time series
    annmeants = np.nanmean(np.reshape(
        mthts_dif, (int(mthts_dif.shape[1] / 12), 12)), axis=1)
    
    return annmeants
