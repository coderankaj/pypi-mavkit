"""RC channel override helpers."""

from __future__ import annotations

from typing import Any, Mapping

# UINT16_MAX — leave that RC channel unchanged.
RC_LEAVE_ALONE = 65535


def override_rc_channels(master: Any, channel_pwm: Mapping[int, int], *, total_channels: int = 18) -> None:
    """Override selected RCIN channels.

    ``channel_pwm`` keys are 1-based RCIN numbers (for example ``{8: 1500, 11: 1400}``).
    Unlisted channels are left alone.
    """
    channels = [RC_LEAVE_ALONE] * total_channels
    for rc_channel, pwm in channel_pwm.items():
        if rc_channel < 1 or rc_channel > total_channels:
            raise ValueError(f"RC channel out of range: {rc_channel}")
        channels[rc_channel - 1] = int(pwm)

    try:
        master.mav.rc_channels_override_send(
            master.target_system,
            master.target_component,
            *channels,
        )
    except TypeError:
        # Older pymavlink builds only accept the first 8 channels.
        master.mav.rc_channels_override_send(
            master.target_system,
            master.target_component,
            *channels[:8],
        )
