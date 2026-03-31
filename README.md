# Vehicle Kinematics

**Author:** G. Accorto

---

The program takes the measurements of a GNSS module mounted on top of a rigid post,
attached to a moving vehicle (represented by a 2D plane). It calculates the projection of its coordinates onto the moving plane and the vehicle heading over time. The input consists of timestamped GNSS
2D coordinates, roll, and pitch in the world frame. The output includes visualization plots, together with the calculated quantities.

## Assumptions

- `x_mm`, `y_mm` are the GNSS module position in a fixed 2D world frame.
- The vehicle body can be approximated locally as a rigid moving plane. This is valid for low enough values of the post height.
- The GNSS module is at constant height `h = 1500 mm` above the moving plane, and the post remains perpendicular to the moving plane at each time.
- Positive roll (rotation around the longitudinal axis) means the right side of the vehicle is lower than the left side, while positive pitch (rotation around the lateral axis) means the front of the vehicle is lower than the rear.
- Motion is smooth, so that heading can be calculated from neighboring data. In fact, heading is calculated from the vehicle velocity vector, and it represents the motion direction.
- A moving right-handed frame of reference is defined at the base of the post, with the x-axis aligned with the instantaneous heading (velocity vector, direction of motion). All rotations follow the right hand rule.
- Data is assumed to imply roll first, then pitch. In this frame of reference and with these assumptions, the vehicle yaw is constantly zero.

- The parser expects five comma-separated fields: `time_s`, `x_mm`, `y_mm`, `roll_deg`, `pitch_deg`.
- A file header is optional. If present, it must contain all the expected field names. Fields columns can be shuffled, as long as a header labels them properly.

## Implementation

The main algorithm can be split in two steps:

1. Parse a CSV file containing the GNSS module data into records.
2. Project the GNSS module position onto the moving plane and use the result to calculate velocity vector and heading.

The geometric derivation and the rotation/sign conventions used by the implementation
are explained in detail in [docs/rotation_convention.pdf](docs/rotation_convention.pdf).

The implementation is split into modules:

- `models.py`: data containers
- `parser.py`: input parsing and validation that timestamps are strictly increasing
- `kinematics.py`: kinematics calculations
- `plotting.py`: plots
- `pipeline.py`: algorithm orchestration and output production
- `main.py`: simple client that feeds data/input_coordinates.txt to the pipeline

# TODO: comment the oo design

The `main.py` script produces:

- `output/GNSS_module_projection.csv`
- `output/vehicle_heading.csv`
- `output/trajectory.png`
- `output/heading.png`
- `output/roll_pitch.png`
- `output/velocity.png`

## Testing

A `pytest` suite includes both unit-tests and an e2e test, located in `test/`.

## Requirements

- Python 3.10 or newer

### Dependencies:

- `numpy`
- `matplotlib`
- `pytest`

Create a local virtual environment at `.venv/` and install the
dependencies before running the program or the tests.

## Build and Run

### Build and run the program

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python main.py
```

### Build and run tests

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python -m pytest tests
```
