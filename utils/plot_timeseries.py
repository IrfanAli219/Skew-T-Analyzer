"""
plot_timeseries.py

Plots a single-variable time series extracted from
all interpolated radiosonde profiles at one height,
along with a smooth polynomial trend line.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from utils.timeseries import extract_variable_timeseries


def plot_timeseries(profiles, variable, ylabel, output_dir="output/plots", trend_degree=3):
    """
    Ask the user for a height, extract the time series
    for `variable` at that height, print + plot it with
    a smooth trend line overlay.
    """

    height = int(input("\nHeight (m) : ").strip())

    ts = extract_variable_timeseries(profiles, height, variable)

    if ts.empty:
        print(f"\nNo Data Found For {variable} At {height} m.")
        return

    print("\nTime Series")
    print(ts.head())
    print("\nTotal Observations :", len(ts))

    # ------------------------------------------------------
    # Convert Launch Time to Numeric (for fitting)
    # ------------------------------------------------------

    x_numeric = ts["Launch"].map(pd.Timestamp.toordinal)

    # ------------------------------------------------------
    # Fit Smooth Polynomial Trend
    # ------------------------------------------------------

    coeffs = np.polyfit(x_numeric, ts[variable], trend_degree)
    trend = np.polyval(coeffs, x_numeric)

    # R-squared (goodness of fit)
    residuals = ts[variable] - trend
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((ts[variable] - ts[variable].mean()) ** 2)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0

    # ------------------------------------------------------
    # Plot
    # ------------------------------------------------------

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        ts["Launch"], ts[variable],
        color="black", linewidth=1, label="Observed"
    )

    ax.plot(
        ts["Launch"], trend,
        color="red", linewidth=2,
        label=f"Trend (R\u00b2 = {r_squared:.2f})"
    )

    ax.set_xlabel("Launch Time")
    ax.set_ylabel(ylabel)
    ax.set_title(f"{variable} Time Series at {height} m")

    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.autofmt_xdate()

    # ------------------------------------------------------
    # Save
    # ------------------------------------------------------

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{variable}_timeseries_{height}m.png"
    save_path = out_dir / filename

    fig.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print("\nTime Series Plot Saved Successfully")
    print(save_path)
    print(f"Trend R\u00b2 : {r_squared:.4f}")