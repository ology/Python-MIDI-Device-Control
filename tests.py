import sys
sys.path.append('./src')
from midi_device_control.midi_device_control import Controller
import unittest

class TestMIDIDeviceControl(unittest.TestCase):
    VERBOSE = False

    def test_control(self):
        pass
        # c = Controller(device_file='./examples/test.yaml', verbose=self.VERBOSE)
        # self.assertFalse(c.verbose)

if __name__ == '__main__':
    unittest.main()
