"""
Support for Zwave roller shutter components.

For more details about this platform, please refer to the documentation
https://home-assistant.io/components/rollershutter.zwave/
"""

from homeassistant.components import zwave
from homeassistant.components.rollershutter import RollershutterDevice

COMMAND_CLASS_SWITCH_MULTILEVEL = 38  # 0x26
COMMAND_CLASS_SWITCH_BINARY = 37  # 0x25


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Find and return Z-Wave roller shutters."""
    if discovery_info is None or zwave.NETWORK is None:
        return

    node = zwave.NETWORK.nodes[discovery_info[zwave.ATTR_NODE_ID]]
    value = node.values[discovery_info[zwave.ATTR_VALUE_ID]]

    if value.command_class != zwave.COMMAND_CLASS_SWITCH_MULTILEVEL:
        return

    value.set_change_verified(False)
    add_devices([ZwaveRollershutter(value)])


class ZwaveRollershutter(zwave.ZWaveDeviceEntity, RollershutterDevice):
    """Representation of an Zwave roller shutter."""

    @property
    def should_poll(self):
        """No polling available in Zwave roller shutter."""
        return False

    @property
    def current_position(self):
        """Gives current position of Zwave roller shutter."""
        return None

    def move_up(self, **kwargs):
        """Move the roller shutter up."""
        for _, value in self._node.get_values(
                   class_id=COMMAND_CLASS_SWITCH_MULTILEVEL).values():
                if value.command_class == 38 and value.index == 1:
                    value.data = True

    def move_down(self, **kwargs):
        """Move the roller shutter down."""
        for _, value in self._node.get_values(
                   class_id=COMMAND_CLASS_SWITCH_MULTILEVEL).values():
                if value.command_class == 38 and value.index == 2:
                    value.data = True

    def stop(self, **kwargs):
        """Stop the roller shutter."""
        for _, value in self._node.get_values(
                   class_id=COMMAND_CLASS_SWITCH_BINARY).values():
                value.data = False
