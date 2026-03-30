import numpy as np

from vehicle_kinematics.models import GNSSDataRow
from vehicle_kinematics.projection import calc_GNSS_projection


def test_projection_zero_angles():
    data = [GNSSDataRow(0.0, 10.0, 20.0, 0.0, 0.0)]
    projected = calc_GNSS_projection(data, h=1500.0)

    np.testing.assert_allclose(projected, np.array([[10.0, 20.0]]))


def test_projection():
    data = [GNSSDataRow(0.0, 1000.0, 2000.0, 30.0, 0.0)]
    projected = calc_GNSS_projection(data, h=1500.0)

    np.testing.assert_allclose(
        projected, np.array([[1000.0, 2000.0 + 1500.0 * np.sin(np.deg2rad(30.0))]])
    )

    data = [
        GNSSDataRow(0.0, 0.0, 0.0, 0.0, 0.0),
        GNSSDataRow(1.0, 1.0, 2.0, 3.0, 4.0),
    ]
    projected = calc_GNSS_projection(data, h=1500.0)
    assert projected.shape == (2, 2)
