from pathlib import Path

from vehicle_kinematics import run_pipeline

if __name__ == "__main__":
    # TODO: Add CLI file input. or scan all data.
    # TODO: Read data from vector.
    data_path = Path("data/input_coordinates.txt")
    parsed_data, projected_data, velocity_data = run_pipeline(data_path, h=1500.0)

    print(f"Parsed {len(parsed_data)} samples from {data_path}.")
    print(parsed_data[0])
    print(projected_data[0])
    print(velocity_data[0])

# TODO: Handle edge cases
