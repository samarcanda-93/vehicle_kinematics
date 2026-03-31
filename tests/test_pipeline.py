from vehicle_kinematics.models import GNSSDataRow
from vehicle_kinematics.pipeline import run_pipeline


def test_run_pipeline_accepts_structured_rows(monkeypatch):
    data = [
        GNSSDataRow(time_s=0.0, x_mm=0.0, y_mm=0.0, roll_deg=0.0, pitch_deg=0.0),
        GNSSDataRow(time_s=1.0, x_mm=10.0, y_mm=5.0, roll_deg=1.0, pitch_deg=2.0),
    ]
    outputs = {}

    def save_projection_csv(projected_data):
        outputs["projected"] = projected_data

    def save_heading_csv(velocity_data):
        outputs["velocity"] = velocity_data

    def save_plots(raw_data, projected_data, velocity_data):
        outputs["raw_data"] = raw_data
        outputs["projected_data"] = projected_data
        outputs["velocity_data"] = velocity_data

    monkeypatch.setattr(
        "vehicle_kinematics.pipeline.save_projection_csv", save_projection_csv
    )
    monkeypatch.setattr(
        "vehicle_kinematics.pipeline.save_heading_csv", save_heading_csv
    )
    monkeypatch.setattr("vehicle_kinematics.pipeline.save_plots", save_plots)

    run_pipeline(data, h=1500.0)

    assert outputs["raw_data"] == data
    assert len(outputs["projected"]) == len(data)
    assert len(outputs["velocity"]) == len(data)
    assert outputs["projected_data"] == outputs["projected"]
    assert outputs["velocity_data"] == outputs["velocity"]
