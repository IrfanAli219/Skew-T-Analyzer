"""
interpolation.py

Interpolation of radiosonde profiles
onto a standard height grid.
"""

import numpy as np
import pandas as pd


# ==========================================================
# Create Height Grid
# ==========================================================

def create_height_grid(
    min_height,
    max_height,
    step=100
):
    """
    Create a regular height grid.
    """

    start = int(min_height)
    end = int(max_height)

    return np.arange(
        start,
        end + step,
        step
    )


# ==========================================================
# Interpolate Profile
# ==========================================================

def interpolate_profile(
    df,
    step=100,
    method="linear"
):
    """
    Interpolate one radiosonde profile onto a
    regular height grid.

    Parameters
    ----------
    df : pandas.DataFrame
        Radiosonde profile.

    step : int
        Height interval in meters.

    method : str
        Interpolation method.
        (Currently only 'linear' is supported.)

    Returns
    -------
    interpolated : pandas.DataFrame
        Interpolated profile.

    height_grid : numpy.ndarray
        Standard height grid.
    """

    # ------------------------------------------------------
    # Remove rows without height
    # ------------------------------------------------------

    df = df.dropna(
        subset=["HGHT"]
    ).copy()

    # ------------------------------------------------------
    # Sort by height
    # ------------------------------------------------------

    df = df.sort_values(
        "HGHT"
    )

    # ------------------------------------------------------
    # Remove duplicate heights
    # ------------------------------------------------------

    df = df.drop_duplicates(
        subset="HGHT",
        keep="first"
    )

    # ------------------------------------------------------
    # Create height grid
    # ------------------------------------------------------

    height_grid = create_height_grid(
        df["HGHT"].min(),
        df["HGHT"].max(),
        step
    )

    # ------------------------------------------------------
    # Output DataFrame
    # ------------------------------------------------------

    interpolated = pd.DataFrame()

    interpolated["HGHT"] = height_grid

    # ------------------------------------------------------
    # Variables to interpolate
    # ------------------------------------------------------

    variables = [
        "PRES",
        "TEMP",
        "DWPT",
        "RELH",
        "MIXR",
        "SPED",
        "THTA",
        "THTE",
        "THTV"
    ]

    # ------------------------------------------------------
    # Interpolate Variables
    # ------------------------------------------------------

    for variable in variables:

        valid = df[
            ["HGHT", variable]
        ].dropna()

        if len(valid) < 2:

            interpolated[variable] = np.nan
            continue

        if method == "linear":

            interpolated[variable] = np.interp(
                height_grid,
                valid["HGHT"],
                valid[variable]
            )

        else:

            raise ValueError(
                f"Interpolation method '{method}' is not supported."
            )

    # ------------------------------------------------------
    # Reset Index
    # ------------------------------------------------------

    interpolated.reset_index(
        drop=True,
        inplace=True
    )

    return interpolated, height_grid