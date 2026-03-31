from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D

from vehicle_kinematics.models import GNSSDataRow, GNSSProjectedDataRow, VelocityDataRow


def _relative_time(time_s: list[float]) -> list[float]:
    """Return timestamps shifted"""
    if not time_s:
        return []

    t0 = time_s[0]
    return [t - t0 for t in time_s]


def plot_trajectory(
    raw_data: list[GNSSDataRow],
    projected_data: list[GNSSProjectedDataRow],
) -> plt.Figure:
    """Plot the trajectory of GNSS module and its projection. Color the GNSS path by
    elapsed time."""
    fig = plt.figure()
    for raw_row, projected_row in zip(raw_data, projected_data):
        plt.plot(
            [raw_row.x_mm, projected_row.x_mm],
            [raw_row.y_mm, projected_row.y_mm],
            "--",
            color="0.6",
            alpha=0.35,
            linewidth=1.0,
        )

    plt.plot(
        [row.x_mm for row in projected_data],
        [row.y_mm for row in projected_data],
        color="0.6",
        linewidth=1.5,
        label="Projection on moving plane",
    )

    x_raw = np.array([row.x_mm for row in raw_data], dtype=float)
    y_raw = np.array([row.y_mm for row in raw_data], dtype=float)
    time_s = np.array(_relative_time([row.time_s for row in raw_data]), dtype=float)

    if len(raw_data) >= 2:
        points = np.column_stack((x_raw, y_raw)).reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        line = LineCollection(segments, cmap="viridis", linewidth=2.5)
        line.set_array(time_s[:-1])
        plt.gca().add_collection(line)
        colorbar = plt.colorbar(line)
    else:
        scatter = plt.scatter(x_raw, y_raw, c=time_s, cmap="viridis", s=30)
        colorbar = plt.colorbar(scatter)

    plt.scatter(
        x_raw,
        y_raw,
        c=time_s,
        cmap="viridis",
        s=18,
        edgecolors="none",
        label="GNSS module position",
    )
    colorbar.set_label("time since first sample [s]")
    plt.title("2D Trajectory")
    plt.xlabel("x [mm]")
    plt.ylabel("y [mm]")
    plt.axis("equal")
    plt.grid(True)
    legend_handles = [
        Line2D([0], [0], color="0.6", linewidth=1.5),
        Line2D(
            [0],
            [0],
            color=plt.cm.viridis(0.55),
            linewidth=2.5,
            marker="o",
            markersize=5,
            markerfacecolor=plt.cm.viridis(0.55),
            markeredgewidth=0,
        ),
    ]
    plt.legend(
        legend_handles,
        ["Projection on moving plane", "GNSS module position"],
        loc="best",
    )
    plt.tight_layout()
    return fig


def plot_heading(velocity_data: list[VelocityDataRow]) -> plt.Figure:
    """Plot heading as a function of time."""
    fig = plt.figure()
    time_s = _relative_time([row.time_s for row in velocity_data])
    plt.plot(
        time_s,
        [row.heading_deg for row in velocity_data],
    )
    plt.title("Heading Over Time")
    plt.xlabel("time since first sample [s]")
    plt.ylabel("heading [deg]")
    plt.grid(True)
    plt.tight_layout()
    return fig


def plot_roll_pitch(raw_data: list[GNSSDataRow]) -> plt.Figure:
    """Plot roll and pitch over time."""
    fig = plt.figure()
    time_s = _relative_time([row.time_s for row in raw_data])
    plt.plot(time_s, [row.roll_deg for row in raw_data], label="Roll")
    plt.plot(time_s, [row.pitch_deg for row in raw_data], label="Pitch")
    plt.title("Roll and Pitch Over Time")
    plt.xlabel("time since first sample [s]")
    plt.ylabel("angle [deg]")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    return fig


def plot_velocity(velocity_data: list[VelocityDataRow]) -> plt.Figure:
    """Plot velocity components and speed over time."""
    fig = plt.figure()
    time_s = _relative_time([row.time_s for row in velocity_data])
    plt.plot(time_s, [row.vx_mm_s for row in velocity_data], label="vx")
    plt.plot(time_s, [row.vy_mm_s for row in velocity_data], label="vy")
    plt.plot(time_s, [row.speed_mm_s for row in velocity_data], label="speed")
    plt.title("Velocity and Speed Over Time")
    plt.xlabel("time since first sample [s]")
    plt.ylabel("velocity [mm/s]")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    return fig


def save_trajectory_gif(
    raw_data: list[GNSSDataRow],
    projected_data: list[GNSSProjectedDataRow],
    output_path: Path,
) -> None:
    """Save a simple GIF showing the GNSS point and its projection over time."""
    fig = plt.figure()
    ax = plt.gca()

    x_raw = np.array([row.x_mm for row in raw_data], dtype=float)
    y_raw = np.array([row.y_mm for row in raw_data], dtype=float)
    x_projected = np.array([row.x_mm for row in projected_data], dtype=float)
    y_projected = np.array([row.y_mm for row in projected_data], dtype=float)
    time_s = np.array(_relative_time([row.time_s for row in raw_data]), dtype=float)

    ax.plot(
        x_projected,
        y_projected,
        color="0.8",
        linewidth=1.5,
        label="Projection on moving plane",
    )

    trajectory_line = LineCollection([], colors="tab:blue", linewidth=2.5)
    ax.add_collection(trajectory_line)

    gnss_point = ax.scatter([], [], color="tab:blue", s=40)
    projected_point, = ax.plot([], [], "o", color="0.45", markersize=5)
    connector_line, = ax.plot([], [], "--", color="0.6", alpha=0.35, linewidth=1.0)
    stopwatch_text = ax.text(
        0.02,
        0.98,
        "",
        transform=ax.transAxes,
        va="top",
        ha="left",
        bbox={"boxstyle": "round", "facecolor": "white", "alpha": 0.85, "edgecolor": "0.7"},
    )

    ax.set_title("2D Trajectory")
    ax.set_xlabel("x [mm]")
    ax.set_ylabel("y [mm]")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True)
    legend_handles = [
        Line2D([0], [0], color="0.8", linewidth=1.5),
        Line2D(
            [0],
            [0],
            color="tab:blue",
            linewidth=2.5,
            marker="o",
            markersize=5,
            markerfacecolor="tab:blue",
            markeredgewidth=0,
        ),
    ]
    ax.legend(
        legend_handles,
        ["Projection on moving plane", "GNSS module position"],
        loc="best",
    )

    x_all = np.concatenate([x_raw, x_projected])
    y_all = np.concatenate([y_raw, y_projected])
    x_pad = max(1.0, 0.05 * (x_all.max() - x_all.min()))
    y_pad = max(1.0, 0.05 * (y_all.max() - y_all.min()))
    ax.set_xlim(x_all.min() - x_pad, x_all.max() + x_pad)
    ax.set_ylim(y_all.min() - y_pad, y_all.max() + y_pad)
    fig.tight_layout()

    def update(frame_idx: int):
        if frame_idx >= 1:
            points = np.column_stack((x_raw[: frame_idx + 1], y_raw[: frame_idx + 1])).reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)
            trajectory_line.set_segments(segments)
        else:
            trajectory_line.set_segments([])

        gnss_point.set_offsets(np.array([[x_raw[frame_idx], y_raw[frame_idx]]]))
        projected_point.set_data([x_projected[frame_idx]], [y_projected[frame_idx]])
        connector_line.set_data(
            [x_raw[frame_idx], x_projected[frame_idx]],
            [y_raw[frame_idx], y_projected[frame_idx]],
        )
        stopwatch_text.set_text(f"t = {time_s[frame_idx]:.2f} s")
        return trajectory_line, gnss_point, projected_point, connector_line, stopwatch_text

    animation = FuncAnimation(
        fig,
        update,
        frames=len(raw_data),
        interval=250,
        blit=False,
        repeat=True,
    )
    animation.save(output_path, writer=PillowWriter(fps=4))
    plt.close(fig)


def save_plots(
    raw_data: list[GNSSDataRow],
    projected_data: list[GNSSProjectedDataRow],
    velocity_data: list[VelocityDataRow],
) -> None:
    """Generate and save all output plots to the ``output/`` directory."""
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    plot_trajectory(raw_data, projected_data).savefig(
        output_dir / "trajectory.png", dpi=300
    )
    plot_heading(velocity_data).savefig(output_dir / "heading.png", dpi=300)
    plot_roll_pitch(raw_data).savefig(output_dir / "roll_pitch.png", dpi=300)
    plot_velocity(velocity_data).savefig(output_dir / "velocity.png", dpi=300)
    save_trajectory_gif(raw_data, projected_data, output_dir / "trajectory.gif")
    plt.close("all")
