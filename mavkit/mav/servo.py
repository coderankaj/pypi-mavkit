"""Servo PWM helpers."""

from __future__ import annotations

from typing import Any

from pymavlink import mavutil


def set_servo(master: Any, servo_number: int, pwm: int) -> None:
    """Drive one ArduPilot servo output to a PWM value (µs)."""
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
        0,
        float(servo_number),
        float(pwm),
        0,
        0,
        0,
        0,
        0,
    )
