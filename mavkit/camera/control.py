"""Camera helpers.

This is a starter surface. Wire your camera MAVLink messages / vendor commands here.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pymavlink import mavutil

if TYPE_CHECKING:
    from mavkit.connection import MavLink


class Camera:
    """Basic MAVLink camera command helper.

    Uses standard ``MAV_CMD_IMAGE_START_CAPTURE`` / ``MAV_CMD_VIDEO_START_CAPTURE``
    when the autopilot / companion supports them. Extend this class for vendor-specific cameras.
    """

    def __init__(self, link: MavLink, *, camera_id: int = 0) -> None:
        self._link = link
        self.camera_id = camera_id

    def take_photo(self) -> str:
        """Request a single still image capture."""
        self._command_long(
            mavutil.mavlink.MAV_CMD_IMAGE_START_CAPTURE,
            param1=float(self.camera_id),
            param2=0.0,  # interval
            param3=1.0,  # count
        )
        return f"camera {self.camera_id}: image capture requested"

    def start_video(self) -> str:
        """Request video start."""
        self._command_long(
            mavutil.mavlink.MAV_CMD_VIDEO_START_CAPTURE,
            param1=float(self.camera_id),
            param2=0.0,  # status frequency
        )
        return f"camera {self.camera_id}: video start requested"

    def stop_video(self) -> str:
        """Request video stop."""
        self._command_long(
            mavutil.mavlink.MAV_CMD_VIDEO_STOP_CAPTURE,
            param1=float(self.camera_id),
        )
        return f"camera {self.camera_id}: video stop requested"

    def _command_long(self, command: int, **params: float) -> None:
        master: Any = self._link.master
        master.mav.command_long_send(
            master.target_system,
            master.target_component,
            command,
            0,
            float(params.get("param1", 0.0)),
            float(params.get("param2", 0.0)),
            float(params.get("param3", 0.0)),
            float(params.get("param4", 0.0)),
            float(params.get("param5", 0.0)),
            float(params.get("param6", 0.0)),
            float(params.get("param7", 0.0)),
        )
