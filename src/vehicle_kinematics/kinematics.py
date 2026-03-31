import numpy as np

from vehicle_kinematics.models import (
    GNSSDataRow,
    GNSSProjectedDataRow,
    VelocityDataRow,
)


def calc_GNSS_projection(
    data: list[GNSSDataRow], h: float
) -> list[GNSSProjectedDataRow]:
    """Project the GNSS module position onto the vehicle plane."""
    xG = np.array([data_row.x_mm for data_row in data], dtype=float)
    yG = np.array([data_row.y_mm for data_row in data], dtype=float)
    roll_deg = np.array([data_row.roll_deg for data_row in data], dtype=float)
    pitch_deg = np.array([data_row.pitch_deg for data_row in data], dtype=float)

    roll_rad = np.deg2rad(roll_deg)
    pitch_rad = np.deg2rad(pitch_deg)

    xP = xG - h * np.sin(pitch_rad) * np.cos(roll_rad)
    yP = yG + h * np.sin(roll_rad)

    return [
        GNSSProjectedDataRow(time_s=float(row.time_s), x_mm=float(xp), y_mm=float(yp))
        for row, xp, yp in zip(data, xP, yP)
    ]


def calc_velocity(data: list[GNSSProjectedDataRow]) -> list[VelocityDataRow]:
    """Calculate velocity vector and heading from projected GNSS positions."""
    if not data:
        return []

    if len(data) == 1:
        row = data[0]
        return [
            VelocityDataRow(
                time_s=float(row.time_s),
                vx_mm_s=0.0,
                vy_mm_s=0.0,
                speed_mm_s=0.0,
                heading_deg=0.0,
            )
        ]

    x = np.array([data_row.x_mm for data_row in data], dtype=float)
    y = np.array([data_row.y_mm for data_row in data], dtype=float)
    time = np.array([data_row.time_s for data_row in data], dtype=float)

    # calculate time derivatives
    v_x = np.gradient(x, time)
    v_y = np.gradient(y, time)
    # norm is the forward speed
    speed = np.sqrt(v_x * v_x + v_y * v_y)
    # arctan2 is defined on all quadrants
    heading = np.arctan2(v_y, v_x)

    return [
        VelocityDataRow(
            time_s=float(t),
            vx_mm_s=float(vx),
            vy_mm_s=float(vy),
            speed_mm_s=float(sp),
            heading_deg=float(head),
        )
        for t, vx, vy, sp, head in zip(time, v_x, v_y, speed, np.rad2deg(heading))
    ]
