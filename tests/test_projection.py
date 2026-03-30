import numpy as np

from vehicle_kinematics.models import GNSSDataRow, GNSSProjectedDataRow
from vehicle_kinematics.kinematics import calc_GNSS_projection


def test_projection_zero_angles():
    data = [GNSSDataRow(0.0, 10.0, 20.0, 0.0, 0.0)]
    projected = calc_GNSS_projection(data, h=1500.0)

    assert len(projected) == 1
    assert projected[0] == GNSSProjectedDataRow(time_s=0.0, x_mm=10.0, y_mm=20.0)


def test_projection():
    data = [GNSSDataRow(0.0, 1000.0, 2000.0, 30.0, 0.0)]
    projected = calc_GNSS_projection(data, h=1500.0)

    assert len(projected) == 1
    assert projected[0] == GNSSProjectedDataRow(
        time_s=0.0,
        x_mm=1000.0,
        y_mm=2000.0 + 1500.0 * np.sin(np.deg2rad(30.0)),
    )

    data = [
        GNSSDataRow(0.0, 0.0, 0.0, 0.0, 0.0),
        GNSSDataRow(1.0, 1.0, 2.0, 3.0, 4.0),
    ]
    projected = calc_GNSS_projection(data, h=1500.0)
    assert len(projected) == 2
    assert all(isinstance(row, GNSSProjectedDataRow) for row in projected)
