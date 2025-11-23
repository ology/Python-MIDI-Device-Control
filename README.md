# MIDI Device Control

Generically control MIDI devices with other MIDI devices!

### Example:
```python
from midi_device_control import Controller
device_file = 'some-controller-some-device.yaml'
c = Controller(device_file=device_file)
c.control()
```