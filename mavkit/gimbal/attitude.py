"""Gimbal attitude command (degrees → PWM via axis map)."""

from __future__ import annotations

from dataclasses import dataclass

from mavkit.gimbal.axis import ServoAxis


@dataclass(slots=True)
class Attitude:
    """Requested gimbal attitude in degrees."""

    pitch_deg: float = 0.0
    yaw_deg: float = 0.0
    roll_deg: float = 0.0

    def pitch_pwm(self, axis: ServoAxis) -> int:
        return axis.pwm_for_angle(self.pitch_deg)

    def yaw_pwm(self, axis: ServoAxis) -> int:
        return axis.pwm_for_angle(self.yaw_deg)

    def roll_pwm(self, axis: ServoAxis) -> int:
        return axis.pwm_for_angle(self.roll_deg)
