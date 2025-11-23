import os
import sys
try:
    import sys
    sys.path.append('./src')
    from midi_device_control.midi_device_control import Controller
except ImportError:
    from midi_device_control import Controller

if __name__ == "__main__":
    device_file = sys.argv[1] if len(sys.argv) > 1 else sys.argv[0]

    if not os.path.exists(device_file):
        print(device_file, 'does not exist')
        sys.exit()

    try:
        c = Controller(device_file=device_file)
        c.control()
    except KeyboardInterrupt:
        print('Stopping MIDI I/O.')
    except Exception as e:
        print(f"ERROR: {e}")