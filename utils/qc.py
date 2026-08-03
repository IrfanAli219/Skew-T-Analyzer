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

    check_wind_direction(df)

    check_theta(df)

    check_theta_e(df)

    check_theta_v(df)

    check_duplicate_heights(df)

    check_duplicate_rows(df)

    print("\nLevel-3 Scientific Checks")
    print("-" * 50)

    check_height_difference(df)
    check_pressure_step(df)
    check_temperature_gradient(df)
    check_dewpoint_depression(df)
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


def check_wind_direction(df: pd.DataFrame) -> None:
    """
    Check that wind direction is between 0 and 360 degrees.
    Missing values are ignored.
    """

    valid = df["DRCT"].dropna()

    invalid = valid[(valid < 0) | (valid > 360)]

    if len(invalid) == 0:
        print("Wind Direction        : PASS")
    else:
        print(f"Wind Direction        : FAIL ({len(invalid)} invalid values)")


def check_theta(df: pd.DataFrame) -> None:
    """
    Potential temperature must be positive.
    """

    valid = df["THTA"].dropna()

    invalid = valid[valid <= 0]

    if len(invalid) == 0:
        print("Potential Temperature : PASS")
    else:
        print(f"Potential Temperature : FAIL ({len(invalid)} invalid values)")


def check_theta_e(df: pd.DataFrame) -> None:
    """
    Equivalent potential temperature must be positive.
    """

    valid = df["THTE"].dropna()

    invalid = valid[valid <= 0]

    if len(invalid) == 0:
        print("Equivalent Theta-E    : PASS")
    else:
        print(f"Equivalent Theta-E    : FAIL ({len(invalid)} invalid values)")



def check_theta_v(df: pd.DataFrame) -> None:
    """
    Virtual potential temperature must be positive.
    """

    valid = df["THTV"].dropna()

    invalid = valid[valid <= 0]

    if len(invalid) == 0:
        print("Virtual Theta-V       : PASS")
    else:
        print(f"Virtual Theta-V       : FAIL ({len(invalid)} invalid values)")



def check_duplicate_heights(df: pd.DataFrame) -> None:
    """
    Check duplicate height levels.
    """

    duplicates = df["HGHT"].duplicated().sum()

    if duplicates == 0:
        print("Duplicate Heights     : PASS")
    else:
        print(f"Duplicate Heights     : FAIL ({duplicates} duplicates)")


def check_duplicate_rows(df: pd.DataFrame) -> None:
    """
    Check duplicate rows.
    """

    duplicates = df.duplicated().sum()

    if duplicates == 0:
        print("Duplicate Rows        : PASS")
    else:
        print(f"Duplicate Rows        : FAIL ({duplicates} duplicates)")



def check_height_difference(df: pd.DataFrame) -> None:
    """
    Check that height increases with altitude.
    """

    heights = df["HGHT"].dropna().reset_index(drop=True)

    invalid = 0

    for i in range(1, len(heights)):

        if heights.iloc[i] <= heights.iloc[i - 1]:
            invalid += 1

    if invalid == 0:
        print("Height Difference      : PASS")
    else:
        print(f"Height Difference      : FAIL ({invalid} invalid levels)")


def check_pressure_step(df: pd.DataFrame) -> None:
    """
    Check pressure decreases between adjacent levels.
    """

    pressure = df["PRES"].dropna().reset_index(drop=True)

    invalid = 0

    for i in range(1, len(pressure)):

        if pressure.iloc[i] >= pressure.iloc[i - 1]:
            invalid += 1

    if invalid == 0:
        print("Pressure Step          : PASS")
    else:
        print(f"Pressure Step          : FAIL ({invalid} invalid levels)")


def check_temperature_gradient(df: pd.DataFrame) -> None:
    """
    Check for unrealistic temperature changes
    between adjacent levels.
    """

    temp = df["TEMP"].dropna().reset_index(drop=True)

    invalid = 0

    for i in range(1, len(temp)):

        difference = abs(temp.iloc[i] - temp.iloc[i - 1])

        if difference > 30:
            invalid += 1

    if invalid == 0:
        print("Temperature Gradient   : PASS")
    else:
        print(f"Temperature Gradient   : WARNING ({invalid} large jumps)")


def check_dewpoint_depression(df: pd.DataFrame) -> None:
    """
    Check for unrealistic dew point depression.
    """

    valid = df[["TEMP", "DWPT"]].dropna()

    invalid = 0

    for _, row in valid.iterrows():

        depression = row["TEMP"] - row["DWPT"]

        if depression > 80:
            invalid += 1

    if invalid == 0:
        print("Dew Point Depression   : PASS")
    else:
        print(f"Dew Point Depression   : WARNING ({invalid} suspicious levels)")


