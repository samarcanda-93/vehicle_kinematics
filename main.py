from pathlib import Path

from vehicle_kinematics import parse, run_pipeline

if __name__ == "__main__":
    data_path = Path("data/input_coordinates.txt")
    data = parse(data_path)
    run_pipeline(data, h=1500.0)
