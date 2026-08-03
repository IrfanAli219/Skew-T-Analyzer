from utils.parser import (
    read_file,
    extract_metadata,
    extract_launch_lines,
    create_dataframe
)
from utils.qc import quality_control

# ==========================================================
# File Path
# ==========================================================

FILE_PATH = "/home/irfan/new/irfan laptop/Radiosonde_system/SkewT_Analyzer/input/Srinagar.txt"

# ==========================================================
# Read File
# ==========================================================

lines = read_file(FILE_PATH)

# ==========================================================
# Extract All Launch Metadata
# ==========================================================

launches = extract_metadata(lines)

# ==========================================================
# Extract First Launch Raw Data
# ==========================================================

raw_data = extract_launch_lines(
    lines,
    launches[0]["start_line"]
)

# ==========================================================
# Convert Raw Data to DataFrame
# ==========================================================

df = create_dataframe(raw_data)

# ==========================================================
# Display Results
# ==========================================================

df = create_dataframe(raw_data)

print(df)

print("\nShape:", df.shape)

print("Before QC")

quality_control(df)

print("After QC")