from dataclasses import dataclass


@dataclass(frozen=True)
class GNSSDataRow:
    time_s: float
    x_mm: float
    y_mm: float
    roll_deg: float
    pitch_deg: float


@dataclass(frozen=True)
class GNSSProjectedDataRow:
    time_s: float
    x_mm: float
    y_mm: float


@dataclass(frozen=True)
class VelocityDataRow:
    time_s: float
    vx_mm_s: float
    vy_mm_s: float
    speed_mm_s: float
    heading_deg: float
