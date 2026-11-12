"""H-16 gimbal PWM mapping tests (no hardware required)."""

from mavkit.gimbal import Attitude, H16_PITCH, H16_ROLL, H16_YAW


def test_trim_is_center() -> None:
    attitude = Attitude()
    assert attitude.pitch_pwm(H16_PITCH) == 1500
    assert attitude.yaw_pwm(H16_YAW) == 1500
    assert attitude.roll_pwm(H16_ROLL) == 1500


def test_pitch_servo9_limits() -> None:
    assert H16_PITCH.servo == 9
    assert H16_PITCH.rc_channel == 11
    assert H16_PITCH.pwm_for_angle(-90) == 1000
    assert H16_PITCH.pwm_for_angle(90) == 1700


def test_yaw_servo10_rcin12() -> None:
    assert H16_YAW.servo == 10
    assert H16_YAW.rc_channel == 12
    assert H16_YAW.pwm_for_angle(-180) == 1100
    assert H16_YAW.pwm_for_angle(180) == 1900


def test_roll_servo11_rcin8() -> None:
    assert H16_ROLL.servo == 11
    assert H16_ROLL.rc_channel == 8
    assert H16_ROLL.pwm_for_angle(-180) == 1100
    assert H16_ROLL.pwm_for_angle(180) == 1900
