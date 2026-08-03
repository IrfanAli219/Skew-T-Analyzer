import pandas as pd


def quality_control(df: pd.DataFrame) -> None:
    """
    Perform quality control checks on a radiosonde profile.
    """

    print("\n" + "=" * 50)
    print("QUALITY CONTROL REPORT")
    print("=" * 50)

    # =====================================================
    # Basic Information
    # =====================================================

    print(f"Rows    : {len(df)}")
    print(f"Columns : {len(df.columns)}")

    # =====================================================
    # Missing Values
    # =====================================================

    print("\nMissing Values")

    missing = df.isna().sum()

    for column, count in missing.items():
        print(f"{column:5} : {count}")

    # =====================================================
    # Duplicate Pressure Levels
    # =====================================================

    duplicates = df["PRES"].duplicated().sum()

    print("\nDuplicate Pressure Levels")

    print(f"Count : {duplicates}")

    # =====================================================
    # Pressure Order
    # =====================================================

    decreasing = df["PRES"].is_monotonic_decreasing

    print("\nPressure Order")

    if decreasing:
        print("PASS")
    else:
        print("FAIL")

    # =====================================================
    # Meteorological Quality Checks
    # =====================================================

    print("\nMeteorological Checks")
    print("-"*50)

    check_pressure(df)

    check_temperature(df)

    check_dewpoint(df)

    check_relative_humidity(df)

    check_wind_speed(df)

    check_height(df)

    print("=" * 50)

def check_pressure(df):
    """
    Check whether all pressure values are physically valid.
    """

    invalid = df[df["PRES"] <= 0]

    if invalid.empty:
        print("Pressure Range : PASS")
    else:
        print("Pressure Range : FAIL")

        for index, row in invalid.iterrows():
            print(
                f"Row {index}: Invalid Pressure = {row['PRES']}"
            )


def check_temperature(df):
    """
    Check whether temperatures are within a realistic range.
    """

    invalid = df[
        (df["TEMP"] < -100) |
        (df["TEMP"] > 60)
    ]

    if invalid.empty:
        print("Temperature Range : PASS")
    else:
        print("Temperature Range : FAIL")

        for index, row in invalid.iterrows():
            print(
                f"Row {index}: TEMP = {row['TEMP']}"
            )


def check_dewpoint(df):
    """
    Dew point must not exceed air temperature.
    """

    valid = df.dropna(subset=["TEMP", "DWPT"])

    invalid = valid[
        valid["DWPT"] > valid["TEMP"]
    ]

    if invalid.empty:
        print("Dew Point : PASS")
    else:
        print("Dew Point : FAIL")

        for index, row in invalid.iterrows():
            print(
                f"Row {index}: "
                f"TEMP={row['TEMP']}  "
                f"DWPT={row['DWPT']}"
            )



def check_relative_humidity(df):
    """
    Relative humidity must be between 0 and 100.
    """

    valid = df.dropna(subset=["RELH"])

    invalid = valid[
        (valid["RELH"] < 0) |
        (valid["RELH"] > 100)
    ]

    if invalid.empty:
        print("Relative Humidity : PASS")
    else:
        print("Relative Humidity : FAIL")

        for index, row in invalid.iterrows():
            print(
                f"Row {index}: RH={row['RELH']}"
            )



def check_wind_speed(df):
    """
    Wind speed cannot be negative.
    """

    valid = df.dropna(subset=["SPED"])

    invalid = valid[
        valid["SPED"] < 0
    ]

    if invalid.empty:
        print("Wind Speed : PASS")
    else:
        print("Wind Speed : FAIL")

        for index, row in invalid.iterrows():
            print(
                f"Row {index}: SPED={row['SPED']}"
            )


def check_height(df):
    """
    Height should increase upward through the profile.
    """

    increasing = df["HGHT"].dropna().is_monotonic_increasing

    if increasing:
        print("Height Order : PASS")
    else:
        print("Height Order : FAIL")


