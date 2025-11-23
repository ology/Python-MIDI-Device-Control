# MIDI Device Control

Generically control MIDI devices with other MIDI devices!

## DESCRIPTION

This package sports a single method: `control()` which allows MIDI control of a device with a controller, as defined in a `YAML` configuration file.

### Configuration YAML

The configuration file has four parts: The required MIDI `controller` and MIDI `device` to be controlled, an optional `description`, and a required list of `messages`. Each message can have differring keys depending on what is being controlled. These keys are as follows:

`type` (required) can either be `note_on`, `note_off`, `control_change`, `program_change`, or `pitchwheel`.

`cmd` (required) can be any of the above `type`s.

`note` is the MIDI note number (e.g. middle c = 60) that is sensed by the controller.

`control` is the MIDI CC# control change number that is sensed by the controller.

`target` is the MIDI CC# control change number that is changed on the controlled MIDI device.

`data` is the value to be changed given the above `target`.

```yaml
controller: 'Arturia Keyboard'
device: 'Yamaha DX7'
description: 'MIDI control test!'
messages:
    - type: note_on # what type of message is sensed
        note: 60 # middle c does the controlling here
        cmd: control_change # the message type that is sent
        target: 14 # what parameter is to be controlled
    - type: control_change
        control: 1 # the modwheel does the controlling here
        cmd: control_change
        target: 15
    - type: pitchwheel
        cmd: control_change
        target: 16
```

## Example:
```python
from midi_device_control import Controller
device_file = 'some-controller-some-device.yaml'
c = Controller(device_file=device_file)
c.control()
```