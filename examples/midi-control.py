import mido # also install python-rtmidi
import os
import re
import sys
import yaml # install pyyaml
try:
    import sys
    sys.path.append('./src')
    from midi_device_control.midi_device_control import Controller
except ImportError:
    from midi_device_control import Controller

if __name__ == "__main__":
    device_file = sys.argv[1] if len(sys.argv) > 1 else sys.argv[0]

    match = re.search(r'^(.+?)\.py$', device_file)
    if match:
        device_file = match.group(1)
        device_file = device_file + '.yaml'
    if not os.path.exists(device_file):
        print(device_file, 'does not exist')
        sys.exit()

    with open(device_file, 'r') as f:
        data = yaml.safe_load(f)
        in_port_name = data['controller']
        out_port_name = data['device']

    try:
        with mido.open_input(in_port_name) as inport:
            print('Listening to:', inport.name)
            with mido.open_output(out_port_name) as outport:
                c = Controller(outport=outport)
                print('Sending to:', c.outport.name)
                for msg in inport:
                    if msg.type == 'clock':
                        continue
                    print(f"In: {msg}")
                    c.dispatch(msg, data)
    except KeyboardInterrupt:
        print('Stopping MIDI I/O.')
    except Exception as e:
        print(f"ERROR: {e}")