"""
plot_skewt.py

Builds a Skew-T Log-P diagram for one radiosonde launch.
Uses the RAW (uninterpolated) profile so wind direction
data is available for the barbs.
"""

import matplotlib.pyplot as plt
from pathlib import Path

from metpy.plots import SkewT
from metpy.units import units
from metpy.calc import wind_components


STANDARD_LEVELS = [
    1000, 925, 850, 700, 500,
    400, 300, 250, 200, 150, 100
]


def plot_skewt(profile, output_dir="output/plots"):
    """
    Plot and save a Skew-T diagram for a single launch.

    Parameters
    ----------
    profile : dict
        One entry from the `profiles` list — must contain
        'station', 'launch', and 'raw' (DataFrame) keys.

    output_dir : str
        Folder to save the resulting PNG.
    """

    station = profile["station"]
    launch = profile["launch"]
    df = profile["raw"]

    # ------------------------------------------------------
    # Clean Data
    # ------------------------------------------------------

    data = df.dropna(subset=["PRES", "TEMP", "DWPT"])

    pressure = data["PRES"].values * units.hPa
    temperature = data["TEMP"].values
    dewpoint = data["DWPT"].values

    # ------------------------------------------------------
    # Create Figure
    # ------------------------------------------------------

    fig = plt.figure(figsize=(9, 9))
    skew = SkewT(fig)

    skew.ax.set_xlim(-55, 50)

    skew.plot(pressure, temperature, "r", linewidth=2, label="Temperature")
    skew.plot(pressure, dewpoint, "g", linewidth=2, label="Dew Point")

    skew.ax.set_title(f"{station}  |  {launch}")
    skew.ax.legend()

    # ------------------------------------------------------
    # Wind Barbs (Standard Pressure Levels)
    # ------------------------------------------------------

    wind_df = df.dropna(subset=["PRES", "DRCT", "SPED"]).copy()

    selected_rows = []

    for level in STANDARD_LEVELS:

        difference = (wind_df["PRES"] - level).abs()

        if difference.empty:
            continue

        idx = difference.idxmin()

        if abs(wind_df.loc[idx, "PRES"] - level) <= 25:
            selected_rows.append(idx)

    wind_df = wind_df.loc[selected_rows]

    if not wind_df.empty:

        wind_speed = wind_df["SPED"].values * units("m/s")
        wind_direction = wind_df["DRCT"].values * units.degree

        u, v = wind_components(wind_speed, wind_direction)

        skew.plot_barbs(
            wind_df["PRES"].values * units.hPa,
            u,
            v,
            xloc=1.1,
            length=6.5,
            linewidth=0.8
        )

    plt.subplots_adjust(right=0.70)

    # ------------------------------------------------------
    # Pressure Axis
    # ------------------------------------------------------

    skew.ax.set_ylim(1050, 100)
    skew.ax.set_yticks(STANDARD_LEVELS)

    # ------------------------------------------------------
    # Save
    # ------------------------------------------------------

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{station}_{launch.replace(':', '-')}.png"
    save_path = out_dir / filename

    plt.savefig(save_path, dpi=300, bbox_inches="tight", pad_inches=0.4)
    plt.close()

    print("\nDiagram Saved Successfully")
    print(save_path)