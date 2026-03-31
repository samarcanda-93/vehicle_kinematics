import csv
from pathlib import Path

from vehicle_kinematics.kinematics import calc_GNSS_projection, calc_velocity
from vehicle_kinematics.models import GNSSDataRow, GNSSProjectedDataRow, VelocityDataRow
from vehicle_kinematics.parser import validate_gnss_data
from vehicle_kinematics.plotting import save_plots


def save_projection_csv(data: list[GNSSProjectedDataRow]) -> None:
    """Save projected GNSS positions to CSV file."""
    output_path = Path("output/GNSS_module_projection.csv")
    output_path.parent.mkdir(exist_ok=True)

    with output_path.open("w", encoding="utf-8", newline="") as ofile:
        writer = csv.writer(ofile)
        writer.writerow(["time_s", "x_mm", "y_mm"])
        for row in data:
            writer.writerow([row.time_s, row.x_mm, row.y_mm])


def save_heading_csv(data: list[VelocityDataRow]) -> None:
    """Save headings to the default output CSV file."""
    output_path = Path("output/vehicle_heading.csv")
    output_path.parent.mkdir(exist_ok=True)

    with output_path.open("w", encoding="utf-8", newline="") as ofile:
        writer = csv.writer(ofile)
        writer.writerow(["time_s", "heading_deg"])
        for row in data:
            writer.writerow([row.time_s, row.heading_deg])


def run_pipeline(data: list[GNSSDataRow], h: float = 1500.0) -> None:
    """Run the full processing pipeline from input samples."""
    validate_gnss_data(data)
    projected_data = calc_GNSS_projection(data, h)
    velocity_data = calc_velocity(projected_data)

    save_projection_csv(projected_data)
    save_heading_csv(velocity_data)
    save_plots(data, projected_data, velocity_data)
