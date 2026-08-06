import matplotlib.pyplot as plt

from metpy.plots import SkewT
from metpy.units import units
from pathlib import Path
from metpy.calc import wind_components

from utils.parser import (
    read_file,
    extract_metadata,
    extract_launch_lines,
    create_dataframe
)
from utils.interpolation import create_height_grid
from utils.interpolation import interpolate_profile
from utils.timeseries import load_interpolated_profiles
from utils.timeseries import extract_variable_timeseries



# ==================================================
# User Input
# ==================================================

station_name = input("Station Name : ").strip()

station_number = input("Station Number : ").strip()

launch_time = input(
    "Launch Time (YYYY_MM_DD_HH) : "
).strip()

launch_time = launch_time.replace("_", "-")

date_part = launch_time[:10]
hour_part = launch_time[-2:]

launch_time = f"{date_part} {hour_part}:00:00"


# ==========================================================
# File Path
# ==========================================================

FILE_PATH = (
    "/home/irfan/new/irfan laptop/"
    "Radiosonde_system/SkewT_Analyzer/input/"
    f"{station_name}.txt"
)

# ==========================================================
# Read File
# ==========================================================

print("Step 1 : Reading File...")

lines = read_file(FILE_PATH)

print(f"Done. Total Lines : {len(lines)}")

# ==========================================================
# Read Metadata
# ==========================================================

print("\nStep 2 : Extracting Metadata...")

launches = extract_metadata(lines)

print("\nStep 6 : Loading All Profiles...")

profiles = load_interpolated_profiles(
    lines,
    launches
)

# ==========================================================
# Test Time Series Extraction
# ==========================================================

height = 5000
variable = "TEMP"

ts = extract_variable_timeseries(
    profiles,
    height,
    variable
)

print("\nTime Series")

print(ts.head())

print("\nTotal Observations :", len(ts))

print(f"\nProfiles Loaded : {len(profiles)}")

quit()

print(f"Done. Total Launches : {len(launches)}")

# ==========================================================
# Find Launch with Maximum Observations
# ==========================================================

print("\nStep 3 : Searching Maximum Profile...")


selected_launch = None

for launch in launches:

    if (
        launch["station"] == station_name
        and launch["station_number"] == station_number
        and launch["launch"] == launch_time
    ):

        selected_launch = launch
        break
if selected_launch is None:

    print("\nLaunch Not Found.")
    quit()

print("\nLaunch Found")
print(selected_launch)

print("\n" + "=" * 70)
print("SELECTED LAUNCH")
print("=" * 70)
print(selected_launch)

# ==========================================================
# Load Best Launch
# ==========================================================

print("\nStep 4 : Loading Best Launch...")

raw_data = extract_launch_lines(
    lines,
    selected_launch["start_line"]
)

df = create_dataframe(raw_data)

print("\nOriginal Profile")
print(df.head())

df = interpolate_profile(df)

print("\nInterpolated Profile")
print(df.head())

# ==========================================================
# Remove Missing Values
# ==========================================================

df = df.dropna(
    subset=[
        "PRES",
        "TEMP",
        "DWPT"
    ]
)

# ==========================================================
# Prepare Variables
# ==========================================================

pressure = df["PRES"].values * units.hPa
temperature = df["TEMP"].values * units.degC
dewpoint = df["DWPT"].values * units.degC

# ==========================================================
# Create Skew-T Diagram
# ==========================================================

print("\nStep 5 : Creating Skew-T Diagram...")

fig = plt.figure(figsize=(9, 9))

skew = SkewT(fig)
temperature = df["TEMP"].values
dewpoint = df["DWPT"].values

# Standard Skew-T Temperature Range
skew.ax.set_xlim(-55, 50)

skew.plot(
    pressure,
    temperature,
    "r",
    linewidth=2,
    label="Temperature"
)

skew.plot(
    pressure,
    dewpoint,
    "g",
    linewidth=2,
    label="Dew Point"
)

skew.ax.set_title(
    f'{selected_launch["station"]}  |  {selected_launch["launch"]}'
)

skew.ax.legend()

# ==========================================================
# Wind Barbs (Standard Pressure Levels)
# ==========================================================

standard_levels = [
    1000,
    925,
    850,
    700,
    500,
    400,
    300,
    250,
    200,
    150,
    100
]

wind_df = df.dropna(
    subset=["PRES", "DRCT", "SPED"]
).copy()

selected_rows = []

for level in standard_levels:

    difference = (wind_df["PRES"] - level).abs()

    if difference.empty:
        continue

    idx = difference.idxmin()

    if abs(wind_df.loc[idx, "PRES"] - level) <= 25:
        selected_rows.append(idx)

wind_df = wind_df.loc[selected_rows]

# ----------------------------------------------------------
# Convert wind speed & direction to U and V components
# ----------------------------------------------------------

wind_speed = wind_df["SPED"].values * units("m/s")
wind_direction = wind_df["DRCT"].values * units.degree

u, v = wind_components(
    wind_speed,
    wind_direction
)

# ----------------------------------------------------------
# Plot Wind Barbs
# ----------------------------------------------------------

skew.plot_barbs(
    wind_df["PRES"].values * units.hPa,
    u,
    v,
    xloc=1.1,      # aur right side le jao
    length=6.5,
    linewidth=0.8
)

plt.subplots_adjust(right=0.70)

# ==========================================================
# Save Figure
# ==========================================================

output_dir = Path("output/plots")
output_dir.mkdir(
    parents=True,
    exist_ok=True
)
pressure = df["PRES"].values

# ==========================================================
# Standard Pressure Range (1050 -> 100 hPa)
# ==========================================================

skew.ax.set_ylim(1050, 100)
skew.ax.set_yticks([
    1000,
    925,
    850,
    700,
    500,
    400,
    300,
    250,
    200,
    150,
    100
])
filename = (
    f"{selected_launch['station']}_"
    f"{selected_launch['launch'].replace(':', '-')}.png"
)

save_path = output_dir / filename

plt.savefig(
    save_path,
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.4
)

plt.close()

print("\nDiagram Saved Successfully")
print(save_path)