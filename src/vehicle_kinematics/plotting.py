from pathlib import Path

import matplotlib.pyplot as plt

from vehicle_kinematics.models import GNSSDataRow, GNSSProjectedDataRow, VelocityDataRow


def plot_trajectory(
    raw_data: list[GNSSDataRow],
    projected_data: list[GNSSProjectedDataRow],
) -> plt.Figure:
    fig = plt.figure()
    plt.plot(
        [row.x_mm for row in raw_data],
        [row.y_mm for row in raw_data],
        label="GNSS module position",
    )
    plt.plot(
        [row.x_mm for row in projected_data],
        [row.y_mm for row in projected_data],
        label="Projection of GNSS module on moving plane",
    )
    plt.title("2D Trajectory")
    plt.xlabel("x [mm]")
    plt.ylabel("y [mm]")
    plt.axis("equal")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    return fig


def plot_heading(velocity_data: list[VelocityDataRow]) -> plt.Figure:
    fig = plt.figure()
    plt.plot(
        [row.time_s for row in velocity_data],
        [row.heading_deg for row in velocity_data],
    )
    plt.title("Heading Over Time")
    plt.xlabel("time [s]")
    plt.ylabel("heading [deg]")
    plt.grid(True)
    plt.tight_layout()
    return fig


def plot_roll_pitch(raw_data: list[GNSSDataRow]) -> plt.Figure:
    fig = plt.figure()
    time_s = [row.time_s for row in raw_data]
    plt.plot(time_s, [row.roll_deg for row in raw_data], label="Roll")
    plt.plot(time_s, [row.pitch_deg for row in raw_data], label="Pitch")
    plt.title("Roll and Pitch Over Time")
    plt.xlabel("time [s]")
    plt.ylabel("angle [deg]")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    return fig


def plot_velocity(velocity_data: list[VelocityDataRow]) -> plt.Figure:
    fig = plt.figure()
    time_s = [row.time_s for row in velocity_data]
    plt.plot(time_s, [row.vx_mm_s for row in velocity_data], label="vx")
    plt.plot(time_s, [row.vy_mm_s for row in velocity_data], label="vy")
    plt.plot(time_s, [row.speed_mm_s for row in velocity_data], label="speed")
    plt.title("Velocity and Speed Over Time")
    plt.xlabel("time [s]")
    plt.ylabel("velocity [mm/s]")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    return fig


def save_plots(
    raw_data: list[GNSSDataRow],
    projected_data: list[GNSSProjectedDataRow],
    velocity_data: list[VelocityDataRow],
) -> None:
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    plot_trajectory(raw_data, projected_data).savefig(output_dir / "trajectory.png")
    plot_heading(velocity_data).savefig(output_dir / "heading.png")
    plot_roll_pitch(raw_data).savefig(output_dir / "roll_pitch.png")
    plot_velocity(velocity_data).savefig(output_dir / "velocity.png")
    plt.close("all")
