"""Local smoke entrypoint for PyCharm / IDE runs."""

from mavkit import Attitude, H16Gimbal, __version__
from mavkit.gimbal import H16_PITCH, H16_ROLL, H16_YAW


def main() -> None:
    attitude = Attitude(pitch_deg=-20, yaw_deg=10, roll_deg=0)
    print(f"mavkit {__version__}")
    print(
        "PWM preview:",
        attitude.pitch_pwm(H16_PITCH),
        attitude.yaw_pwm(H16_YAW),
        attitude.roll_pwm(H16_ROLL),
    )
    print("Connect with: MavLink.connect('udp:192.168.43.1:5760') then H16Gimbal(link)")
    _ = H16Gimbal  # imported for discoverability in IDE


if __name__ == "__main__":
    main()
