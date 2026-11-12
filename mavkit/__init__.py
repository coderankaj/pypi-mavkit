"""mavkit — MAVLink toolkit for gimbal, camera, and payload control."""

from mavkit.camera import Camera
from mavkit.connection import MavLink, Protocol, build_uri
from mavkit.gimbal import Attitude, H16Gimbal, ServoAxis

__version__ = "0.1.0"

__all__ = [
    "Attitude",
    "Camera",
    "H16Gimbal",
    "MavLink",
    "Protocol",
    "ServoAxis",
    "build_uri",
    "__version__",
]
