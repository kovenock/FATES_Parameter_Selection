import numpy as np


def error_rate(model_ts, obs_ts, dg):
    """Calculate the error rate.
    
    Error rate is calculated as the percentage of model
    annual means that fall within the observed range.
    
    :param model_ts (numpy.ndarray): a 2-D array of annual mean 
        time series for a given variable indexed by (nens, nyrs)
    :param obs_ts (numpy.ndarray): a vector or 2-D array of the
        observed time series for the given variable 
        indexed as (years) or (sample_number, years)
    :param dg (float): a scalar specifying how much to extend
        the observed range in both directions as a fraction
        (e.g., 0.10 extends the observed range by 10% in
        both directions)
    :return error_rate: a vector containing the error rates 
        indexed by parameter set (nens)
    :rtype: numpy.ndarray
    """

    # Number of parameter sets
    nens = model_ts.shape[0]
    
    obs_min = np.nanmin(obs_ts)
    obs_max = np.nanmax(obs_ts)
    
    error_rate = np.zeros([nens])
    error_rate = (100 * np.nansum(np.where(
        (model_ts <= obs_min*(1-dg)) | (model_ts >= obs_max*(1+dg)), 1, 0), 1)
        /model_ts.shape[1])
    
    return error_rate


def nrmse(model_ts, obs_ts):
    """Calculate the normalized root mean square error (NRMSE).
    
    Note: When multiple observed time series are available, 
    this function calculates the NRMSE for each time series 
    and then selects the lowest of those NRMSE values.
    
    :param model_ts (numpy.ndarray): a 2-D array containing the 
        annual mean time series with shape (nens, nyrs)
    :param obs_ts (numpy.ndarray): a vector or 2-D array 
        containing the observed time series with shape (years) or 
        (sample_number, years)
    :return nrmse: a vector containing the normalized root mean 
        square error indexed by (nens)
    :rtype: numpy.ndarray
    """
    
    # Number of parameter sets
    nens = model_ts.shape[0]

    # If multiple observational time series exist, 
    # use the lowest NRMSE for each ensemble member
    try:
        if obs_ts.shape[1] > 0:
            # Number of observational time series
            nobs = obs_ts.shape[0]
            obs_min = np.nanmin(obs_ts, axis=1)
            obs_max = np.nanmax(obs_ts, axis=1)
            obs_mean = np.nanmean(obs_ts, axis=1)
            
            temp_nrmse = np.zeros([nobs, nens])
            for obsnum in range(nobs):
                temp_nrmse[obsnum, :] = (np.sqrt(np.nansum(
                    (model_ts[:, :]-obs_mean[obsnum])**2, axis=1) 
                    / model_ts.shape[1])
                    / (obs_max[obsnum]-obs_min[obsnum]))
                
            nrmse = np.nanmin(temp_nrmse, axis=0)

            temp_nrmse = None
        
    # Otherwise, simply calculate NRMSE
    except IndexError:
        obs_min = np.nanmin(obs_ts, axis=0)
        obs_max = np.nanmax(obs_ts, axis=0)
        obs_mean = np.nanmean(obs_ts, axis=0)    
        
        nrmse = (np.sqrt(np.nansum(
            (model_ts[:, :]-obs_mean)**2, axis=1)
            / model_ts.shape[1])
            / (obs_max-obs_min))

    return nrmse


def avg_nrmse(nrmse_array, weights):
    """Calculate the weighted average NRMSE.
 
     The weighted average normalized root mean square error 
     (NRMSE) is calculated as the weighted Euclidean distance
     between each individual variable's NRMSE.
 
    :param nrmse_array (numpy.ndarray): a 3-D array containing the 
        NRMSE for each individual variable with shape 
        (CO2levels, varlist, nens)
    :param weights (numpy.ndarray, list): the weights to be applied
        to each variable indexed by varlist
    :return avg_nrmse: a 2-D array containing weighted average
        NRMSE values for each parameter set with shape (CO2levels,
        nens)
    :rtype: numpy.ndarray
    """
    
    nvar = nrmse_array.shape[1]
    
    nrmse_sum_weighted_squares = np.zeros(
        [nrmse_array.shape[0],nrmse_array.shape[2]])
    for i in range(nvar):
        nrmse_sum_weighted_squares = (
            nrmse_sum_weighted_squares
            + weights[i]*np.square(nrmse_array[:, i, :]))
    
    avg_nrmse = np.sqrt(nrmse_sum_weighted_squares)
    return avg_nrmse