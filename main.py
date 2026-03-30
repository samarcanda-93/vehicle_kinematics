from pathlib import Path

from vehicle_kinematics.parser import parse_txt
from vehicle_kinematics.projection import calc_GNSS_projection

if __name__ == "__main__":
    # TODO: Add CLI file input. or scan all data/
    data_path = Path("data/input_coordinates.txt")
    parsed_data = parse_txt(data_path)

    print(f"Parsed {len(parsed_data)} samples form {data_path}.")
    print(parsed_data[0])

    projected_GNSS = calc_GNSS_projection(parsed_data, h=1500)
