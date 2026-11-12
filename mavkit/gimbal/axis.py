"""One gimbal / servo axis and its angle → PWM mapping."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ServoAxis:
    """Servo + RCIN mapping for one axis (pitch, yaw, or roll)."""

    name: str
    servo: int
    rc_channel: int
    pwm_min: int
    pwm_max: int
    pwm_trim: int
    min_deg: float
    max_deg: float
    reversed: bool = False

    def pwm_for_angle(self, deg: float) -> int:
        """Convert degrees to PWM µs, clamped to this axis range."""
        angle = max(self.min_deg, min(self.max_deg, float(deg)))
        if self.reversed:
            angle = -angle
        if angle >= 0:
            span = self.max_deg if self.max_deg else 1.0
            pwm = self.pwm_trim + (self.pwm_max - self.pwm_trim) * (angle / span)
        else:
            span = abs(self.min_deg) if self.min_deg else 1.0
            pwm = self.pwm_trim + (self.pwm_trim - self.pwm_min) * (angle / span)
        return int(round(max(self.pwm_min, min(self.pwm_max, pwm))))
