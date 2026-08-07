"""
parser.py

Reads University of Wyoming radiosonde TXT files and extracts
all launches into a structured dictionary.
"""

from pathlib import Path
from typing import Dict, List
from io import StringIO

import pandas as pd


# ==========================================================
# Constants
# ==========================================================

COLUMNS = [
    "PRES",
    "HGHT",
    "TEMP",
    "DWPT",
    "RELH",
    "MIXR",
    "DRCT",
    "SPED",
    "THTA",
    "THTE",
    "THTV"
]

COLUMN_WIDTH = 7


# ==========================================================
# Read File
# ==========================================================

def read_file(file_path: str) -> List[str]:
    """
    Read a TXT file and return all lines.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(path, "r", encoding="utf-8") as file:
        return file.readlines()


# ==========================================================
# Extract Launch Metadata
# ==========================================================

def extract_metadata(lines: List[str]) -> List[Dict]:
    """
    Extract metadata for every launch present in the file.
    """

    launches = []

    for i, line in enumerate(lines):

        line = line.strip()

        if line.startswith("Station:"):

            launches.append(
                {
                    "station": line.split(":", 1)[1].strip(),
                    "station_number": lines[i + 1].split(":", 1)[1].strip(),
                    "launch": lines[i + 2].split(":", 1)[1].strip(),
                    "start_line": i,
                }
            )

    return launches


# ==========================================================
# Extract Raw Data Lines
# ==========================================================

def extract_launch_lines(
    lines: List[str],
    start_line: int
) -> List[str]:
    """
    Extract numerical data rows for one launch.
    """

    data_lines = []

    # Skip:
    # Station
    # Station Number
    # Launch
    # ==========================
    # Column Header

    index = start_line + 5

    while index < len(lines):

        line = lines[index].rstrip()

        if line == "":
            break

        data_lines.append(line)

        index += 1

    return data_lines


# ==========================================================
# Create DataFrame
# ==========================================================

def create_dataframe(data_lines: List[str]) -> pd.DataFrame:
    """
    Convert raw sounding data into a pandas DataFrame.
    """

    text = "\n".join(data_lines)

    colspecs = [
        (i * COLUMN_WIDTH, (i + 1) * COLUMN_WIDTH)
        for i in range(len(COLUMNS))
    ]

    df = pd.read_fwf(
        StringIO(text),
        colspecs=colspecs,
        names=COLUMNS,
        header=None,
    )

    df = df.apply(
        pd.to_numeric,
        errors="coerce"
    )

    df = df.dropna(subset=["PRES"])

    df = df.reset_index(drop=True)

    return df

def clean_dataframe(df):
    """
    Remove physically invalid rows so interpolation never
    sees corrupt values — enforces PRES > 0 and strictly
    increasing HGHT with strictly decreasing PRES.
    """

    df = df.dropna(subset=["PRES", "HGHT"]).copy()

    df = df[df["PRES"] > 0]

    df = df.sort_values("HGHT").reset_index(drop=True)

    # ------------------------------------------------------
    # Keep only rows where height increases AND
    # pressure decreases relative to the last kept row.
    # Any row violating this (corrupt reading) is dropped.
    # ------------------------------------------------------

    keep = [0]

    for i in range(1, len(df)):

        prev_idx = keep[-1]

        if (
            df.loc[i, "HGHT"] > df.loc[prev_idx, "HGHT"]
            and df.loc[i, "PRES"] < df.loc[prev_idx, "PRES"]
        ):
            keep.append(i)

    df = df.loc[keep].reset_index(drop=True)

    return df