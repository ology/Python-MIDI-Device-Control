import sys
sys.path.append('./src')
from midi_device_control.midi_device_control import Controller
import unittest

class TestMIDIDeviceControl(unittest.TestCase):
    VERBOSE = False

    def test_attrs(self):
        obj = Controller(verbose=self.VERBOSE)
        # self.assertEqual(obj.octave, 1)
        # self.assertTrue(callable(obj.scale_fn))

if __name__ == '__main__':
    unittest.main()
