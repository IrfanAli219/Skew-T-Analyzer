import matplotlib.pyplot as plt

from metpy.plots import SkewT
from metpy.units import units

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
bad_launches = []

for i, launch in enumerate(launches):

    # Progress every 500 launches
    if i % 500 == 0:
        print(f"Processing Launch {i}/{len(launches)}")

    try:

        raw_data = extract_launch_lines(
            lines,
            launch["start_line"]
        )

        df = create_dataframe(raw_data)

        rows = len(df)

        if rows > max_rows:

            max_rows = rows
            best_launch = launch

    except Exception as e:

        bad_launches.append((i, launch["launch"]))

        print("\n" + "=" * 70)
        print("ERROR FOUND")
        print("=" * 70)

        print(f"Launch Index : {i}")
        print(launch)

        print("\nException")
        print(e)

        print("\nRaw Data")
        print("-" * 70)

        for line in raw_data:
            print(repr(line))

        print("-" * 70)

        # Stop after first bad launch
        break

# ==========================================================
# Results
# ==========================================================

print("\n")
print("=" * 70)
print("RESULT")
print("=" * 70)

print("\nMaximum Observation Launch")
print(best_launch)

print(f"\nMaximum Levels : {max_rows}")

print(f"\nBad Launches : {len(bad_launches)}")