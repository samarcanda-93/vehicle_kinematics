from pathlib import Path

from vehicle_kinematics import parse, run_pipeline

if __name__ == "__main__":
    data_path = Path("data/input_coordinates.txt")
    run_pipeline(parse(data_path), h=1500.0)
