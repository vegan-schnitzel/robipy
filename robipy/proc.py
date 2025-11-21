"""
Mostly climate data processing.
"""

import numpy as np


def global_mean(data, lat):
    """
    Grid cells based on longitude and latitude are larger at the equator
    and smaller at the poles. Hence, when computing the meridional mean,
    I've got to add weights accordingly.

    Parameters
    ----------
    data : ndarray
    lat : ndarray
    """
    # zonal mean
    data_zm = np.mean(data, axis=2)
    # meridional mean
    w = np.cos(np.deg2rad(lat))
    data_gm = np.average(data_zm, weights=w, axis=1)
    return data_gm


def pa_to_hpa(ds, var='psl'):
    """
    Convert pressure from pascal to hectopascal.
    """
    #if ds[var].attrs['units'] == 'hPa':
    #    raise ValueError(f"Variable '{var}' already appears to be in hPa.")
    attrs = ds[var].attrs.copy()
    ds[var] = ds[var] / 100
    ds[var].attrs = attrs
    ds[var].attrs['units'] = 'hPa'
