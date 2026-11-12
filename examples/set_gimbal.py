"""Example: connect and center the H-16 gimbal.

Usage:
  python examples/set_gimbal.py udp:192.168.43.1:5760
"""

from __future__ import annotations

import sys

from mavkit import H16Gimbal, MavLink


def main() -> int:
    uri = sys.argv[1] if len(sys.argv) > 1 else "udp:192.168.43.1:5760"
    link = MavLink.connect(uri)
    try:
        gimbal = H16Gimbal(link)
        print(gimbal.center())
        print(gimbal.set_attitude(pitch_deg=-20, yaw_deg=0, roll_deg=0))
    finally:
        link.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
