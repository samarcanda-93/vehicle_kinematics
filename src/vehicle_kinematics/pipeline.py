import csv
from pathlib import Path

from vehicle_kinematics.kinematics import calc_GNSS_projection, calc_velocity
from vehicle_kinematics.models import GNSSProjectedDataRow, VelocityDataRow
from vehicle_kinematics.parser import parse
from vehicle_kinematics.plotting import save_plots


def save_projection_csv(data: list[GNSSProjectedDataRow]) -> None:
    output_path = Path("output/GNSS_module_projection.csv")
    output_path.parent.mkdir(exist_ok=True)

    with output_path.open("w", encoding="utf-8", newline="") as ofile:
        writer = csv.writer(ofile)
        writer.writerow(["time_s", "x_mm", "y_mm"])
        for row in data:
            writer.writerow([row.time_s, row.x_mm, row.y_mm])


def save_heading_csv(data: list[VelocityDataRow]) -> None:
    output_path = Path("output/vehicle_heading.csv")
    output_path.parent.mkdir(exist_ok=True)

    with output_path.open("w", encoding="utf-8", newline="") as ofile:
        writer = csv.writer(ofile)
        writer.writerow(["time_s", "heading_deg"])
        for row in data:
            writer.writerow([row.time_s, row.heading_deg])


# TODO: Think about refactoring into a class.
def run_pipeline(data_path: Path, h: float = 1500.0) -> None:
    parsed_data = parse(data_path)
    projected_data = calc_GNSS_projection(parsed_data, h)
    velocity_data = calc_velocity(projected_data)

    save_projection_csv(projected_data)
    save_heading_csv(velocity_data)
    save_plots(parsed_data, projected_data, velocity_data)
