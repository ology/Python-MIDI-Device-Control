import mido
import os
import re
import sys
import time
import yaml # pip install pyyaml

class Controller:
    def __init__(
        self,
        device_file=None,
        verbose=False,
    ):
        self.device_file = device_file
        with open(self.device_file, 'r') as f:
            self.data = yaml.safe_load(f)
            self.inport_name = self.data['controller']
            self.outport_name = self.data['device']
        self.inport = mido.open_input(self.inport_name)
        self.outport = mido.open_input(self.outport_name)
        self.verbose = verbose

    # https://mido.readthedocs.io/en/latest/message_types.html
    def send_to(self, mtype, patch=0, data=0, channel=0, velocity=100):
        if mtype == 'start' or mtype == 'stop':
            msg = mido.Message(mtype)
            if self.verbose:
                print(f"Out: {msg}")
            self.outport.send(msg)
        elif mtype == 'control_change':
            msg = mido.Message(mtype, control=patch, value=data, channel=channel)
            if self.verbose:
                print(f"Out: {msg}")
            self.outport.send(msg)
        elif mtype == 'pitchwheel':
            msg = mido.Message(mtype, pitch=data, channel=channel)
            if self.verbose:
                print(f"Out: {msg}")
            self.outport.send(msg)
        elif mtype == 'program_change':
            msg = mido.Message(mtype, program=patch, channel=channel)
            if self.verbose:
                print(f"Out: {msg}")
            self.outport.send(msg)
        else:
            msg = mido.Message('note_on', note=patch, velocity=velocity, channel=channel)
            if self.verbose:
                print(f"Out: {msg}")
            self.outport.send(msg)
            time.sleep(data)
            msg = mido.Message('note_off', note=patch, velocity=velocity, channel=channel)
            if self.verbose:
                print(f"Out: {msg}")
            self.outport.send(msg)

    # data arg keys: type (required), cmd (required), note, control, target, data
    def dispatch(self, msg, data):
        for m in data['messages']:
            if msg.type == m['type']:
                if m['type'] == 'note_on' and m['cmd'] == 'control_change' and msg.note == m['note']:
                    self.send_to(m['cmd'], patch=m['target'], data=m['data'])
                elif m['type'] == 'note_on' and msg.note == m['note']:
                    self.send_to(m['cmd'])
                elif m['type'] == 'control_change' and m['cmd'] == 'program_change' and msg.control == m['control']:
                    self.send_to('program_change', patch=msg.value)
                elif m['type'] == 'control_change' and msg.control == m['control'] and 'data' in m:
                    self.send_to('control_change', patch=m['target'], data=m['data'])
                elif m['type'] == 'control_change' and msg.control == m['control']:
                    self.send_to('control_change', patch=m['target'], data=msg.value)
                elif m['type'] == 'pitchwheel' and m['cmd'] == 'control_change':
                    scaled_result = self.scale_number(msg.pitch, -8192, 8192, 0, 127)
                    self.send_to('control_change', patch=m['target'], data=scaled_result)
                elif m['type'] == 'pitchwheel':
                    self.send_to('pitchwheel', data=msg.pitch)

    def _scale_number(value, original_min, original_max, target_min, target_max):
        """
        Scales a number from one range to another as an integer.
        Args:
            value: The number to be scaled.
            original_min: minimum value of the original range
            original_max: maximum value of the original range
            target_min: minimum value of the target range
            target_max: maximum value of the target range
        Returns:
            float: The integer scaled number in the target range
        """
        if original_max == original_min:
            # Handle the case where the original range is a single point
            return target_min  # Or raise an error, depending on desired behavior
        scaled_value = ((value - original_min) * (target_max - target_min)) / (original_max - original_min) + target_min
        return round(scaled_value)

    def control(self):
        with self.inport:
            print('Listening to:', self.inport.name)
            with self.outport:
                print('Sending to:', self.outport.name)
                for msg in self.inport:
                    if msg.type == 'clock':
                        continue
                    print(f"In: {msg}")
                    self.dispatch(msg, self.data)
