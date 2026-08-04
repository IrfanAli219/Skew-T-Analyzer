# from utils.parser import (
#     read_file,
#     extract_metadata,
#     extract_launch_lines,
#     create_dataframe
# )
# from utils.qc import quality_control

# # ==========================================================
# # File Path
# # ==========================================================

# FILE_PATH = "/home/irfan/new/irfan laptop/Radiosonde_system/SkewT_Analyzer/input/Srinagar.txt"

# # ==========================================================
# # Read File
# # ==========================================================

# lines = read_file(FILE_PATH)

# # ==========================================================
# # Extract All Launch Metadata
# # ==========================================================

# launches = extract_metadata(lines)

# # ==========================================================
# # Extract First Launch Raw Data
# # ==========================================================

# raw_data = extract_launch_lines(
#     lines,
#     launches[0]["start_line"]
# )

# # ==========================================================
# # Convert Raw Data to DataFrame
# # ==========================================================

# df = create_dataframe(raw_data)

# # ==========================================================
# # Display Results
# # ==========================================================

# df = create_dataframe(raw_data)

# print(df)

# print("\nShape:", df.shape)

# print("Before QC")

# quality_control(df)

# print("After QC")


from utils.parser import (
    read_file,
    extract_metadata,
    extract_launch_lines,
    create_dataframe
)

FILE_PATH = "/home/irfan/new/irfan laptop/Radiosonde_system/SkewT_Analyzer/input/Srinagar.txt"

# --------------------------------------------------
# Read File
# --------------------------------------------------

lines = read_file(FILE_PATH)

# --------------------------------------------------
# Read Metadata
# --------------------------------------------------

launches = extract_metadata(lines)

# --------------------------------------------------
# Find Launch with Maximum Observations
# --------------------------------------------------

max_rows = 0
best_launch = None
bad_launches = []

for i, launch in enumerate(launches):

    raw_data = extract_launch_lines(
        lines,
        launch["start_line"]
    )

    try:

        df = create_dataframe(raw_data)

        rows = len(df)

        if rows > max_rows:

            max_rows = rows
            best_launch = launch

    except Exception as e:

        bad_launches.append((i, launch["launch"]))

        print("\n" + "=" * 70)
        print(f"Launch Index : {i}")
        print(launch)
        print(e)

        print("\nRaw Data")
        print("-" * 70)

        for line in raw_data:
            print(repr(line))

        break

print("\nMaximum Observation Launch")
print("-" * 40)
print(best_launch)
print(f"Total Levels : {max_rows}")

print(f"\nBad Launches : {len(bad_launches)}")