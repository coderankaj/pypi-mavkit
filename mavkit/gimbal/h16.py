"""H-16 gimbal controller (SERVO9–11 / RCIN11, RCIN12, RCIN8)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from mavkit.gimbal.attitude import Attitude
from mavkit.gimbal.axis import ServoAxis
from mavkit.mav.rc import override_rc_channels
from mavkit.mav.servo import set_servo

if TYPE_CHECKING:
    from mavkit.connection import MavLink

# H-16 Vehicle Setup → Parameters (Servo9 / Servo10 / Servo11).
H16_PITCH = ServoAxis(
    name="pitch",
    servo=9,
    rc_channel=11,
    pwm_min=1000,
    pwm_max=1700,
    pwm_trim=1500,
    min_deg=-90.0,
    max_deg=90.0,
)
H16_YAW = ServoAxis(
    name="yaw",
    servo=10,
    rc_channel=12,
    pwm_min=1100,
    pwm_max=1900,
    pwm_trim=1500,
    min_deg=-180.0,
    max_deg=180.0,
)
H16_ROLL = ServoAxis(
    name="roll",
    servo=11,
    rc_channel=8,
    pwm_min=1100,
    pwm_max=1900,
    pwm_trim=1500,
    min_deg=-180.0,
    max_deg=180.0,
)


class H16Gimbal:
    """Move the H-16 gimbal using DO_SET_SERVO + RC override."""

    def __init__(
        self,
        link: MavLink,
        *,
        pitch: ServoAxis = H16_PITCH,
        yaw: ServoAxis = H16_YAW,
        roll: ServoAxis = H16_ROLL,
    ) -> None:
        self._link = link
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll

    def set_attitude(self, pitch_deg: float = 0.0, yaw_deg: float = 0.0, roll_deg: float = 0.0) -> str:
        """Slew to pitch / yaw / roll. Returns a short status string."""
        return self.send(Attitude(pitch_deg=pitch_deg, yaw_deg=yaw_deg, roll_deg=roll_deg))

    def center(self) -> str:
        """Return all axes to trim (0°)."""
        return self.set_attitude(0.0, 0.0, 0.0)

    def send(self, attitude: Attitude) -> str:
        """Send an attitude command over the open MAVLink link."""
        master = self._link.master
        pitch_pwm = attitude.pitch_pwm(self.pitch)
        yaw_pwm = attitude.yaw_pwm(self.yaw)
        roll_pwm = attitude.roll_pwm(self.roll)

        set_servo(master, self.pitch.servo, pitch_pwm)
        set_servo(master, self.yaw.servo, yaw_pwm)
        set_servo(master, self.roll.servo, roll_pwm)
        override_rc_channels(
            master,
            {
                self.roll.rc_channel: roll_pwm,
                self.pitch.rc_channel: pitch_pwm,
                self.yaw.rc_channel: yaw_pwm,
            },
        )

        return (
            f"H-16 gimbal SERVO{self.pitch.servo}/RCIN{self.pitch.rc_channel} pitch {pitch_pwm} µs · "
            f"SERVO{self.yaw.servo}/RCIN{self.yaw.rc_channel} yaw {yaw_pwm} µs · "
            f"SERVO{self.roll.servo}/RCIN{self.roll.rc_channel} roll {roll_pwm} µs"
        )
