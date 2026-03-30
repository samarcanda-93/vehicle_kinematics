from pathlib import Path

from vehicle_kinematics.models import GNSSDataRow


# TODO: Harden the parser
def parse_txt(ifile_path: Path) -> list[GNSSDataRow]:
    with ifile_path.open("r", encoding="utf-8") as ifile:
        parsed_data: list[GNSSDataRow] = []
        for line in ifile:
            time_s, x_mm, y_mm, roll_deg, pitch_deg = [
                float(data_val) for data_val in line.split(",")
            ]
            parsed_data.append(GNSSDataRow(time_s, x_mm, y_mm, roll_deg, pitch_deg))

        return parsed_data
