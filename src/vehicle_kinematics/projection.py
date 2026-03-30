import numpy as np

from vehicle_kinematics.models import GNSSDataRow


def calc_GNSS_projection(data: list[GNSSDataRow], h: float):
    xG = np.array([data_row.x_mm for data_row in data], dtype=float)
    yG = np.array([data_row.y_mm for data_row in data], dtype=float)
    roll_deg = np.array([data_row.roll_deg for data_row in data], dtype=float)
    pitch_deg = np.array([data_row.pitch_deg for data_row in data], dtype=float)

    roll_rad = np.deg2rad(roll_deg)
    pitch_rad = np.deg2rad(pitch_deg)

    xP = xG - h * np.sin(pitch_rad) * np.cos(roll_rad)
    yP = yG + h * np.sin(roll_rad)

    return np.column_stack((xP, yP))
