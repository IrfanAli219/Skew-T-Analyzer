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
    profiles.

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
            # Store profile
            # --------------------------------------

            profiles.append(
                {
                    "station": launch["station"],
                    "station_number": launch["station_number"],
                    "launch": launch["launch"],
                    "profile": interpolated_df
                }
            )

        except Exception:
            skipped +=1
            continue

    print("\n========================================")
    print(f"Total Launches   : {total}")
    print(f"Loaded Profiles  : {len(profiles)}")
    print(f"Skipped Profiles : {skipped}")
    print("========================================")

    return profiles