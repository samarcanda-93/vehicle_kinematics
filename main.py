from pathlib import Path

from vehicle_kinematics import (
    calc_GNSS_projection,
    calc_velocity,
    parse_txt,
    save_plots,
)

if __name__ == "__main__":
    # TODO: Add CLI file input. or scan all data/
    data_path = Path("data/input_coordinates.txt")
    parsed_data = parse_txt(data_path)

    print(f"Parsed {len(parsed_data)} samples from {data_path}.")
    print(parsed_data[0])

    projected_GNSS = calc_GNSS_projection(parsed_data, h=1500)
    print(projected_GNSS[0])

    velocities = calc_velocity(projected_GNSS)
    headings_deg = [velocity.heading_deg for velocity in velocities]
    print(velocities[0])
    print(headings_deg[0])

    save_plots(parsed_data, projected_GNSS, velocities)
