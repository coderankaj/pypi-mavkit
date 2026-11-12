# mavkit

MAVLink toolkit for **gimbal**, **camera**, and other **payload** controls.

Built for ArduPilot / Skydroid H-16 style setups. Uses [`pymavlink`](https://github.com/ArduPilot/pymavlink) under the hood.

## Install

```bash
pip install -e .
```

## Quick start

```python
from mavkit import MavLink, H16Gimbal

# Ethernet cable / network — TCP (most common for H-16 style links)
link = MavLink.connect_tcp("192.168.43.1", 5760)

# Or UDP client
# link = MavLink.connect_udp("192.168.43.1", 14550)

# Or UDP listen (vehicle connects to this PC)
# link = MavLink.connect_udp_listen(14550)

# Or USB/serial cable
# link = MavLink.connect_serial("COM3", 57600)

gimbal = H16Gimbal(link)
gimbal.set_attitude(pitch_deg=-20, yaw_deg=10, roll_deg=0)
gimbal.center()
link.close()
```

### Connection options

| Method | When to use |
|---|---|
| `connect_tcp(host, port)` | Ethernet cable or Wi‑Fi bridge (TCP) |
| `connect_udp(host, port)` | UDP client to vehicle/radio |
| `connect_udp_listen(port)` | GCS listens; vehicle sends UDP in |
| `connect_serial(port, baud)` | USB/serial cable (`COM3`, etc.) |
| `connect("tcp:host:port")` | Any raw pymavlink URI |

## Package layout

| Module | Role |
|---|---|
| `mavkit.connection` | Open / close MAVLink link |
| `mavkit.gimbal` | H-16 GMC attitude → servo PWM + RC override |
| `mavkit.mav` | Low-level servo / RC helpers |
| `mavkit.camera` | Camera control placeholders (extend next) |

## License

MIT
