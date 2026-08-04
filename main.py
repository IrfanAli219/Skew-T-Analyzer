import matplotlib.pyplot as plt

from metpy.plots import SkewT
from metpy.units import units
from pathlib import Path

from utils.parser import (
    read_file,
    extract_metadata,
    extract_launch_lines,
    create_dataframe
)


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

xmin = min(
    temperature.min(),
    dewpoint.min()
) - 10

xmax = max(
    temperature.max(),
    dewpoint.max()
) + 10

skew.ax.set_xlim(xmin, xmax)

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
# Save Figure
# ==========================================================

output_dir = Path("output/plots")
output_dir.mkdir(
    parents=True,
    exist_ok=True
)
pressure = df["PRES"].values

# Highest pressure (surface)
bottom = pressure.max()

# Lowest pressure (top of atmosphere)
top = pressure.min()

# Round to nearest 10 hPa
bottom = (bottom // 10 + 1) * 10
top = max(1, (top // 10) * 10)

skew.ax.set_ylim(bottom, top)
filename = (
    f"{selected_launch['station']}_"
    f"{selected_launch['launch'].replace(':', '-')}.png"
)

save_path = output_dir / filename

plt.savefig(
    save_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nDiagram Saved Successfully")
print(save_path)