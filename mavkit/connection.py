"""MAVLink connection helper — TCP, UDP, and serial (cable)."""

from __future__ import annotations

from typing import Any, Literal

from pymavlink import mavutil

GCS_SYSTEM_ID = 255
GCS_COMPONENT_ID = mavutil.mavlink.MAV_COMP_ID_MISSIONPLANNER

Protocol = Literal["tcp", "udp", "udpout", "udpin", "serial"]


def build_uri(
    protocol: Protocol,
    *,
    host: str = "192.168.43.1",
    port: int = 5760,
    serial_port: str = "COM3",
    baud_rate: int = 57600,
) -> str:
    """Build a pymavlink connection URI.

    Protocols:
      tcp     — TCP client (common over ethernet cable / Wi‑Fi bridge)
      udp     — same as udpout (UDP client to host:port)
      udpout  — UDP client to host:port
      udpin   — UDP listen (GCS waits; default bind 0.0.0.0)
      serial  — USB/serial cable (COMx on Windows)
    """
    if protocol == "serial":
        return f"{serial_port}:{baud_rate}"
    if protocol == "udpin":
        bind_host = host if host else "0.0.0.0"
        return f"udpin:{bind_host}:{port}"
    if protocol in ("udp", "udpout"):
        return f"udpout:{host}:{port}"
    return f"tcp:{host}:{port}"


class MavLink:
    """Thin wrapper around a pymavlink connection."""

    def __init__(self, master: Any, *, uri: str = "") -> None:
        self._master = master
        self.uri = uri

    @classmethod
    def connect(
        cls,
        uri: str | None = None,
        *,
        protocol: Protocol | None = None,
        host: str = "192.168.43.1",
        port: int = 5760,
        serial_port: str = "COM3",
        baud_rate: int = 57600,
        heartbeat_timeout_s: float = 30.0,
        dialect: str = "ardupilotmega",
        source_system: int = GCS_SYSTEM_ID,
        source_component: int = GCS_COMPONENT_ID,
    ) -> MavLink:
        """Open a MAVLink link.

        Pass either a full ``uri`` or ``protocol`` + host/port/serial fields.

        Examples::

            MavLink.connect("tcp:192.168.43.1:5760")
            MavLink.connect(protocol="tcp", host="192.168.43.1", port=5760)
            MavLink.connect(protocol="udp", host="192.168.43.1", port=14550)
            MavLink.connect(protocol="udpin", port=14550)
            MavLink.connect(protocol="serial", serial_port="COM3", baud_rate=57600)
        """
        if uri is None:
            if protocol is None:
                raise ValueError("Pass uri=... or protocol='tcp'|'udp'|'udpin'|'serial'")
            uri = build_uri(
                protocol,
                host=host,
                port=port,
                serial_port=serial_port,
                baud_rate=baud_rate,
            )

        master = mavutil.mavlink_connection(
            uri,
            source_system=source_system,
            source_component=source_component,
            dialect=dialect,
        )
        master.wait_heartbeat(timeout=heartbeat_timeout_s)
        link = cls(master, uri=uri)
        link.send_gcs_heartbeat()
        return link

    @classmethod
    def connect_tcp(cls, host: str = "192.168.43.1", port: int = 5760, **kwargs: Any) -> MavLink:
        """Connect as TCP client — typical for ethernet-cable / network GCS links."""
        return cls.connect(protocol="tcp", host=host, port=port, **kwargs)

    @classmethod
    def connect_udp(cls, host: str = "192.168.43.1", port: int = 14550, **kwargs: Any) -> MavLink:
        """Connect as UDP client (udpout) to the vehicle / radio."""
        return cls.connect(protocol="udpout", host=host, port=port, **kwargs)

    @classmethod
    def connect_udp_listen(cls, port: int = 14550, host: str = "0.0.0.0", **kwargs: Any) -> MavLink:
        """Listen for UDP MAVLink (vehicle dials out to this GCS)."""
        return cls.connect(protocol="udpin", host=host, port=port, **kwargs)

    @classmethod
    def connect_serial(cls, serial_port: str = "COM3", baud_rate: int = 57600, **kwargs: Any) -> MavLink:
        """Connect over a USB/serial cable."""
        return cls.connect(protocol="serial", serial_port=serial_port, baud_rate=baud_rate, **kwargs)

    @property
    def master(self) -> Any:
        if self._master is None:
            raise ConnectionError("MAVLink is not connected")
        return self._master

    @property
    def is_connected(self) -> bool:
        return self._master is not None

    def send_gcs_heartbeat(self) -> None:
        """Identify this process as a ground control station."""
        self.master.mav.heartbeat_send(
            mavutil.mavlink.MAV_TYPE_GCS,
            mavutil.mavlink.MAV_AUTOPILOT_INVALID,
            0,
            0,
            mavutil.mavlink.MAV_STATE_ACTIVE,
        )

    def close(self) -> None:
        if self._master is None:
            return
        try:
            self._master.close()
        finally:
            self._master = None
