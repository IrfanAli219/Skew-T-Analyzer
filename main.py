"""
main.py

SkewT-LogP Analyzer
Entry point — loads all profiles for a station once,
then provides an interactive menu for various analyses.
"""

from utils.parser import read_file, extract_metadata
from utils.timeseries import load_interpolated_profiles
from utils.plot_skewt import plot_skewt
from utils.plot_timeseries import plot_timeseries


# ==========================================================
# Helper - Find Profile By Launch Time
# ==========================================================

def find_profile(profiles, launch_time):
    """
    Find a stored profile matching an exact launch time.
    """

    for profile in profiles:

        if profile["launch"] == launch_time:
            return profile

    return None


# ==========================================================
# Helper - Format Launch Time Input
# ==========================================================

def format_launch_time(raw_input):
    """
    Convert '2026_07_30_00' style input into
    '2026-07-30 00:00:00' format used in the data.
    """

    raw_input = raw_input.strip().replace("_", "-")

    date_part = raw_input[:10]
    hour_part = raw_input[-2:]

    return f"{date_part} {hour_part}:00:00"


# ==========================================================
# Menu
# ==========================================================

def show_menu():

    print("\n" + "=" * 40)
    print("Radiosonde Analyzer")
    print("=" * 40)
    print("1. Skew-T Diagram")
    print("2. Temperature Time Series")
    print("3. Relative Humidity Time Series")
    print("4. Wind Speed Time Series")
    print("5. Pressure Time Series")
    print("6. Exit")

    return input("\nChoice : ").strip()


# ==========================================================
# Main
# ==========================================================

def main():

    # ------------------------------------------------------
    # User Input
    # ------------------------------------------------------

    station_name = input("Station Name : ").strip()
    station_number = input("Station Number : ").strip()

    # ------------------------------------------------------
    # File Path
    # ------------------------------------------------------

    FILE_PATH = (
        "/home/irfan/new/irfan laptop/"
        "Radiosonde_system/SkewT_Analyzer/input/"
        f"{station_name}.txt"
    )

    # ------------------------------------------------------
    # Read File
    # ------------------------------------------------------

    print("\nStep 1 : Reading File...")

    lines = read_file(FILE_PATH)

    print(f"Done. Total Lines : {len(lines)}")

    # ------------------------------------------------------
    # Extract Metadata
    # ------------------------------------------------------

    print("\nStep 2 : Extracting Metadata...")

    launches = extract_metadata(lines)

    launches = [
        launch for launch in launches
        if launch["station"] == station_name
        and launch["station_number"] == station_number
    ]

    print(f"Done. Total Launches : {len(launches)}")

    if not launches:
        print("\nNo Launches Found For This Station.")
        return

    # ------------------------------------------------------
    # Load + Interpolate ALL Profiles (One Time)
    # ------------------------------------------------------

    print("\nStep 3 : Loading & Interpolating All Profiles...")

    profiles = load_interpolated_profiles(lines, launches)

    if not profiles:
        print("\nNo Profiles Could Be Loaded.")
        return

    # ------------------------------------------------------
    # Menu Loop
    # ------------------------------------------------------

    while True:

        choice = show_menu()

        if choice == "1":

            launch_time = format_launch_time(
                input("\nLaunch Time (YYYY_MM_DD_HH) : ")
            )

            profile = find_profile(profiles, launch_time)

            if profile is None:
                print("\nLaunch Not Found.")
                continue

            plot_skewt(profile)

        elif choice == "2":
            plot_timeseries(profiles, "TEMP", "Temperature (\u00b0C)")

        elif choice == "3":
            plot_timeseries(profiles, "RELH", "Relative Humidity (%)")

        elif choice == "4":
            plot_timeseries(profiles, "SPED", "Wind Speed (m/s)")

        elif choice == "5":
            plot_timeseries(profiles, "PRES", "Pressure (hPa)")

        elif choice == "6":
            print("\nExiting...")
            break

        else:
            print("\nInvalid Choice.")


if __name__ == "__main__":
    main()