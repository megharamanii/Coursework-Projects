from pathlib import Path
from collections import defaultdict, deque


def process_file(file_path: Path):
    """Processes the input file and returns the simulation data, propagated data, alert data, and cancelled data"""
    simulation_data = 0
    propagated_data = defaultdict(list)
    alert_data = defaultdict(list)
    cancelled_data = defaultdict(list)

    seen_devices = set()

    with open(file_path, 'r') as sample_file:
        for line in sample_file:
            line = line.strip()

            if line.startswith("LENGTH"):
                simulation_data = int(line.split()[1])

            elif line.startswith("DEVICE"):
                device_id = int(line.split()[1])
                seen_devices.add(device_id)
                propagated_data[device_id] = []

            elif line.startswith("PROPAGATE"):
                _, source_device_id, to_device, delay = line.split()
                propagated_data[int(source_device_id)].append((int(to_device), int(delay)))

            elif line.startswith("ALERT"):
                _, device_id, alert_d, time = line.split()
                alert_data[int(time)].append((int(device_id), alert_d))

            elif line.startswith("CANCEL"):
                _, device_id, cancel_d, time = line.split()
                cancelled_data[int(time)].append((int(device_id), cancel_d))

        for device_id in seen_devices:
            if device_id not in propagated_data:
                propagated_data[device_id] = []
    return simulation_data, propagated_data, alert_data, cancelled_data


def sort_key(event):
    return event[0]

