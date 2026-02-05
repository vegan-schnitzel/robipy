"""
Mostly climate data processing.
"""

import numpy as np

month_to_season = {
    12: 'DJF', 1: 'DJF', 2: 'DJF',
    3: 'MAM', 4: 'MAM', 5: 'MAM',
    6: 'JJA', 7: 'JJA', 8: 'JJA',
    9: 'SON', 10: 'SON', 11: 'SON'
}


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


def add_season(df):
    """
    Adds season column to pandas dataframe based on month of date column.

    Parameters
    ----------
    df : DataFrame
    col_name : str, default="date"
        Name of date column.    
    """
    df.assign(season=df[col_name].dt.month.map(month_to_season))
    #todo
