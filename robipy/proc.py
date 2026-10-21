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


def add_season(df, col_name):
    """
    Adds season column to pandas dataframe based on month of date column.

    Parameters
    ----------
    df : DataFrame
    col_name : str, default="date"
        Name of date column.
    """
    df.assign(season=df[col_name].dt.month.map(month_to_season))


def calc_change(df, rename_prefix):
    """
    Computes historical and future climatology per model & member.
    Pretty hard-coded for "potential drivers" analysis of Beaufort high.
    Remember to choose `.query("variable == 'bhi'")` if df is BH index.

    Parameters
    ----------
    df : DataFrame
    rename_prefix : str

    Returns
    -------
    DataFrame
    """
    df_cc = (
        df
        # add shortcut for bhi as df contains three variables: bhx, arctic, bhi
        .pipe(lambda d: d.query("variable == 'bhi'") if rename_prefix == "bhi" else d)
        .query("processing == 'raw'")
        .assign(cold_season=lambda d: d.date.dt.year)
    )
    # define climatologies
    hist = df_cc["cold_season"].between(1985, 2014)
    fut = df_cc["cold_season"].between(2070, 2099)
    # compute mean per model and member
    clim_hist = df_cc[hist].groupby(['model', 'member'], as_index=False)['value'].mean()
    clim_fut = df_cc[fut].groupby(['model', 'member'], as_index=False)['value'].mean()
    # calculate climate change signal
    clim = (
        clim_hist
        .merge(clim_fut, on=["model", "member"], suffixes=("_hist", "_fut"))
        .assign(value_cc=lambda d: d.value_fut - d.value_hist)
    )
    # rename columns from generic "value"
    clim.columns = [
        c.replace("value_", f"{rename_prefix}_") if c.startswith("value_") else c
        for c in clim.columns
    ]
    return clim


def calc_corr(df_bhi, df_other):
    """
    Compute Pearson correlation between BH index and other variable.

    Parameters
    ----------
    df_bhi
        Time series of BH index
    df_other
        Time series of related variable
    other_col_name
        Column name of related variable

    Returns
    -------
    DataFrame
    """
    return (
        df_bhi
        # helper column for merge
        .assign(cold_season=lambda d: d.date.dt.year)
        .query("variable == 'bhi' and processing == 'notrend'")
        .drop(columns=["variable"])
        # add potential driver
        .merge(
            df_other.assign(cold_season=lambda d: d.date.dt.year),
            on=["model", "member", "cold_season", "processing"]
        )
        .drop(columns=["cold_season"])
        # compute Pearson correlation and clean dataframe
        .groupby(["model", "member"])
        .corr(numeric_only=True)
        .iloc[0::2, -1]
        .rename("corr")
        .droplevel(level=2)
        .reset_index()
    )
