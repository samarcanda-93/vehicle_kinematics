from dataclasses import dataclass


@dataclass(frozen=True)
class GNSSDataRow:
    time_s: float
    x_mm: float
    y_mm: float
    roll_deg: float
    pitch_deg: float
