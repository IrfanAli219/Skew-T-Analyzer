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

# ==========================================================
# File Path
# ==========================================================

FILE_PATH = "/home/irfan/new/irfan laptop/Radiosonde_system/SkewT_Analyzer/input/Srinagar.txt"

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

max_rows = 0
best_launch = None

for i, launch in enumerate(launches):

    if i % 500 == 0:
        print(f"Processing Launch {i}/{len(launches)}")

    raw_data = extract_launch_lines(
        lines,
        launch["start_line"]
    )

    df = create_dataframe(raw_data)

    rows = len(df)

    if rows > max_rows:
        max_rows = rows
        best_launch = launch

print("\n" + "=" * 70)
print("RESULT")
print("=" * 70)

print("\nMaximum Observation Launch")
print(best_launch)

print(f"\nMaximum Levels : {max_rows}")

# ==========================================================
# Load Best Launch
# ==========================================================

print("\nStep 4 : Loading Best Launch...")

raw_data = extract_launch_lines(
    lines,
    best_launch["start_line"]
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
skew.ax.set_xlim(-50, 60)

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
    f'{best_launch["station"]}  |  {best_launch["launch"]}'
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

filename = (
    f"{best_launch['station']}_"
    f"{best_launch['launch'].replace(':', '-')}.png"
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