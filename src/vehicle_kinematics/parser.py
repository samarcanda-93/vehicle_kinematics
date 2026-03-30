from pathlib import Path

from vehicle_kinematics.models import GNSSDataRow

DEFAULT_HEADER = ("time_s", "x_mm", "y_mm", "roll_deg", "pitch_deg")


def validate_gnss_data(data: list[GNSSDataRow]) -> None:
    """Verify that time is strictly growing"""
    if any(curr.time_s <= prev.time_s for prev, curr in zip(data, data[1:])):
        raise ValueError("time_s values must be strictly increasing")


def parse(ifile_path: Path) -> list[GNSSDataRow]:
    """Parse GNSS rows from a CSV-like file with optional header columns.
    If no header is present, defaults to DEFAULT_HEADER. Otherwise read the header and
    dispatch data to the correct field. Header entries are limited to those of
    DEFAULT_HEADER, but can be scrambled. A header is only allowed on the first line."""
    with ifile_path.open("r", encoding="utf-8") as ifile:
        parsed_data: list[GNSSDataRow] = []
        header = DEFAULT_HEADER
        for line_no, line in enumerate(ifile):
            fields = [field.strip() for field in line.split(",")]

            match fields:
                case [col_1, col_2, col_3, col_4, col_5] if (
                    set(fields) == set(DEFAULT_HEADER) and line_no == 0
                ):
                    new_header = (col_1, col_2, col_3, col_4, col_5)
                    header = new_header
                    continue
                case [val_1, val_2, val_3, val_4, val_5]:
                    values = (val_1, val_2, val_3, val_4, val_5)
                    column_data = {key: value for key, value in zip(header, values)}
                    try:
                        parsed_data.append(
                            GNSSDataRow(
                                float(column_data["time_s"]),
                                float(column_data["x_mm"]),
                                float(column_data["y_mm"]),
                                float(column_data["roll_deg"]),
                                float(column_data["pitch_deg"]),
                            )
                        )
                    except ValueError as e:
                        raise ValueError(
                            f"Non-numeric value at line {line_no + 1}"
                        ) from e
                case _:
                    raise ValueError(
                        f"Expected 5 values, got {len(fields)} at line {line_no + 1}"
                    )

        if not parsed_data:
            raise ValueError("No data rows found")

        validate_gnss_data(parsed_data)
        return parsed_data
