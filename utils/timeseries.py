"""
timeseries.py

Utilities for creating time-series datasets from
multiple radiosonde launches.
"""

from utils.parser import (
    extract_launch_lines,
    create_dataframe
)

from utils.interpolation import (
    interpolate_profile
)


# ==========================================================
# Load All Interpolated Profiles
# ==========================================================

def load_interpolated_profiles(
    lines,
    launches,
    step=100
):
    """
    Read every radiosonde launch, interpolate it
    onto a standard height grid and return all
    profiles (raw + interpolated).

    Parameters
    ----------
    lines : list[str]
        Complete radiosonde text file.

    launches : list[dict]
        Metadata returned by extract_metadata().

    step : int
        Height interval (meters).

    Returns
    -------
    list[dict]
    """

    profiles = []
    skipped = 0

    total = len(launches)

    print("\nLoading All Profiles...\n")

    for i, launch in enumerate(launches):

        if i % 500 == 0:
            print(f"Processing {i}/{total}")

        try:

            # --------------------------------------
            # Read launch
            # --------------------------------------

            raw_data = extract_launch_lines(
                lines,
                launch["start_line"]
            )

            df = create_dataframe(raw_data)

            # --------------------------------------
            # Interpolate
            # --------------------------------------

            interpolated_df, height_grid = interpolate_profile(
                df,
                step=step
            )

            # --------------------------------------
            # Store profile (raw + interpolated)
            # --------------------------------------

            profiles.append(
                {
                    "station": launch["station"],
                    "station_number": launch["station_number"],
                    "launch": launch["launch"],
                    "raw": df,
                    "profile": interpolated_df
                }
            )

        except Exception:
            skipped += 1
            continue

    print("\n========================================")
    print(f"Total Launches   : {total}")
    print(f"Loaded Profiles  : {len(profiles)}")
    print(f"Skipped Profiles : {skipped}")
    print("========================================")

    return profiles


# ==========================================================
# Extract Time Series at One Height
# ==========================================================

def extract_variable_timeseries(
    profiles,
    height,
    variable
):
    """
    Extract one variable at a given height from
    every interpolated radiosonde profile.
    """

    import pandas as pd

    rows = []

    for profile in profiles:

        df = profile["profile"]

        row = df[df["HGHT"] == height]

        if row.empty:
            continue

        rows.append(
            {
                "Launch": profile["launch"],
                "Station": profile["station"],
                "Station_Number": profile["station_number"],
                "Height": height,
                variable: row.iloc[0][variable]
            }
        )

    ts = pd.DataFrame(rows)

    if not ts.empty:
        ts["Launch"] = pd.to_datetime(ts["Launch"])
        ts = ts.sort_values("Launch").reset_index(drop=True)

    return ts