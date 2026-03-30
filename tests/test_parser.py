from pathlib import Path

import pytest

from vehicle_kinematics.models import GNSSDataRow
from vehicle_kinematics.parser import parse, validate_gnss_data

# TODO: make path independent from where test is run. makefile? __file__?
test_data_path = Path("data/input_coordinates.txt")


def test_parser_txt():
    parsed_data = parse(test_data_path)
    assert len(parsed_data) == 30
    assert isinstance(parsed_data[0], GNSSDataRow)

    first_row = parsed_data[0]
    assert first_row.time_s == 1621693264.0155628
    assert first_row.x_mm == 9521.0
    assert first_row.y_mm == -35074.0
    assert first_row.roll_deg == 3.92
    assert first_row.pitch_deg == -1.35


def test_validate_gnss_data_rejects_non_increasing_timestamps():
    data = [
        GNSSDataRow(0.0, 0.0, 0.0, 0.0, 0.0),
        GNSSDataRow(0.0, 1.0, 1.0, 0.0, 0.0),
        GNSSDataRow(1.0, 2.0, 2.0, 0.0, 0.0),
    ]

    with pytest.raises(ValueError, match="strictly increasing"):
        validate_gnss_data(data)


def test_parser_rejects_wrong_number_of_fields(tmp_path: Path):
    bad_data_path = tmp_path / "bad_input.txt"
    bad_data_path.write_text("1.0,2.0,3.0,4.0\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Expected 5 values, got 4"):
        parse(bad_data_path)


def test_parser_rejects_non_numeric_values(tmp_path: Path):
    bad_data_path = tmp_path / "bad_input.txt"
    bad_data_path.write_text("1.0,2.0,three,4.0,5.0\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Non-numeric value"):
        parse(bad_data_path)


def test_parser_accepts_expected_header(tmp_path: Path):
    data_path = tmp_path / "input_with_header.txt"
    data_path.write_text(
        "time_s,x_mm,y_mm,roll_deg,pitch_deg\n1.0,2.0,3.0,4.0,5.0\n",
        encoding="utf-8",
    )

    parsed_data = parse(data_path)

    assert parsed_data == [GNSSDataRow(1.0, 2.0, 3.0, 4.0, 5.0)]


def test_parser_accepts_reordered_header(tmp_path: Path):
    data_path = tmp_path / "input_with_reordered_header.txt"
    data_path.write_text(
        "x_mm,time_s,y_mm,roll_deg,pitch_deg\n2.0,1.0,3.0,4.0,5.0\n",
        encoding="utf-8",
    )

    parsed_data = parse(data_path)

    assert parsed_data == [GNSSDataRow(1.0, 2.0, 3.0, 4.0, 5.0)]


def test_parser_rejects_header_after_data(tmp_path: Path):
    data_path = tmp_path / "input_with_header_after_data.txt"
    data_path.write_text(
        "1.0,2.0,3.0,4.0,5.0\nx_mm,time_s,y_mm,roll_deg,pitch_deg\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Unexpected header at line 2"):
        parse(data_path)


def test_parser_rejects_repeated_header_after_header(tmp_path: Path):
    data_path = tmp_path / "input_with_repeated_header.txt"
    data_path.write_text(
        "time_s,x_mm,y_mm,roll_deg,pitch_deg\n"
        "1.0,2.0,3.0,4.0,5.0\n"
        "time_s,x_mm,y_mm,roll_deg,pitch_deg\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Unexpected header at line 3"):
        parse(data_path)


def test_parser_rejects_header_without_data(tmp_path: Path):
    data_path = tmp_path / "header_only.txt"
    data_path.write_text(
        "time_s,x_mm,y_mm,roll_deg,pitch_deg\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="No data rows found"):
        parse(data_path)
