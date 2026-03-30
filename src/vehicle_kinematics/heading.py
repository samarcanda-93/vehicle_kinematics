import numpy as np

from vehicle_kinematics.models import GNSSProjectedDataRow, VelocityDataRow


def calc_velocity(data: list[GNSSProjectedDataRow]):
    x = np.array([data_row.x_mm for data_row in data], dtype=float)
    y = np.array([data_row.y_mm for data_row in data], dtype=float)
    time = np.array([data_row.time_s for data_row in data], dtype=float)

    v_x = np.gradient(x, time)
    v_y = np.gradient(y, time)
    speed = np.sqrt(v_x * v_x + v_y * v_y)
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
