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
