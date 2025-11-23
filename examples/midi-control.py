try:
    import sys
    sys.path.append('./src')
    from midi_device_control.midi_device_control import Controller
except ImportError:
    from midi_device_control import Controller

if __name__ == "__main__":
    device_file = sys.argv[1] if len(sys.argv) > 1 else sys.argv[0]
    c = Controller(device_file=device_file)
    c.control()
