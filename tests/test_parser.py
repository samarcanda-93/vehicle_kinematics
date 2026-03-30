from pathlib import Path

from vehicle_kinematics.models import GNSSDataRow
from vehicle_kinematics.parser import parse_txt

# TODO: make path independent from where test is run. makefile? __file__?
test_data_path = Path("data/input_coordinates.txt")


def test_parser_txt():
    parsed_data = parse_txt(test_data_path)
    assert len(parsed_data) == 30
    assert isinstance(parsed_data[0], GNSSDataRow)

    first_row = parsed_data[0]
    assert first_row.time_s == 1621693264.0155628
    assert first_row.x_mm == 9521.0
    assert first_row.y_mm == -35074.0
    assert first_row.roll_deg == 3.92
    assert first_row.pitch_deg == -1.35
