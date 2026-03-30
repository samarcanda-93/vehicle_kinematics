import numpy as np

from vehicle_kinematics.kinematics import calc_velocity
from vehicle_kinematics.models import GNSSProjectedDataRow, VelocityDataRow


def test_calc_velocity_empty_input():
    assert calc_velocity([]) == []


def test_calc_velocity_single_sample_returns_zero_velocity():
    data = [GNSSProjectedDataRow(time_s=1.0, x_mm=5.0, y_mm=-3.0)]

    velocity = calc_velocity(data)

    assert velocity == [
        VelocityDataRow(
            time_s=1.0,
            vx_mm_s=0.0,
            vy_mm_s=0.0,
            speed_mm_s=0.0,
            heading_deg=0.0,
        )
    ]


def test_calc_velocity_straight_line_along_x():
    data = [
        GNSSProjectedDataRow(time_s=0.0, x_mm=0.0, y_mm=0.0),
        GNSSProjectedDataRow(time_s=1.0, x_mm=10.0, y_mm=0.0),
        GNSSProjectedDataRow(time_s=2.0, x_mm=20.0, y_mm=0.0),
    ]

    velocity = calc_velocity(data)

    assert len(velocity) == 3
    assert all(isinstance(row, VelocityDataRow) for row in velocity)
    np.testing.assert_allclose([row.vx_mm_s for row in velocity], [10.0, 10.0, 10.0])
    np.testing.assert_allclose([row.vy_mm_s for row in velocity], [0.0, 0.0, 0.0])
    np.testing.assert_allclose([row.speed_mm_s for row in velocity], [10.0, 10.0, 10.0])
    np.testing.assert_allclose([row.heading_deg for row in velocity], [0.0, 0.0, 0.0])


def test_calc_velocity_diagonal_motion_has_45_degree_heading():
    data = [
        GNSSProjectedDataRow(time_s=0.0, x_mm=0.0, y_mm=0.0),
        GNSSProjectedDataRow(time_s=1.0, x_mm=10.0, y_mm=10.0),
        GNSSProjectedDataRow(time_s=2.0, x_mm=20.0, y_mm=20.0),
    ]

    velocity = calc_velocity(data)

    np.testing.assert_allclose(
        [row.heading_deg for row in velocity],
        [45.0, 45.0, 45.0],
    )
    np.testing.assert_allclose(
        [row.speed_mm_s for row in velocity],
        [np.sqrt(200.0), np.sqrt(200.0), np.sqrt(200.0)],
    )


def test_calc_velocity_preserves_sample_times():
    data = [
        GNSSProjectedDataRow(time_s=1.5, x_mm=0.0, y_mm=0.0),
        GNSSProjectedDataRow(time_s=2.0, x_mm=5.0, y_mm=0.0),
        GNSSProjectedDataRow(time_s=3.0, x_mm=15.0, y_mm=0.0),
    ]

    velocity = calc_velocity(data)

    assert [row.time_s for row in velocity] == [1.5, 2.0, 3.0]
