from pathlib import Path

from vehicle_kinematics import run_pipeline

if __name__ == "__main__":
    # TODO: Add CLI file input. or scan all data.
    # TODO: Read data from vector.
    data_path = Path("data/input_coordinates.txt")
    run_pipeline(data_path, h=1500.0)

    # TODO: Add docstring to functions.
