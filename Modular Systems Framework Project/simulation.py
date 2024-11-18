from collections import defaultdict, deque

def simulate(simulation_length, propagated_data, alert_data, cancelled_data):

    queue = deque()
    received_alerts = defaultdict(set)
    received_cancellations = defaultdict(set)


    for time, alerts in sorted(alert_data.items()):
        for device_id, alert in alerts:
            queue.append((time, "ALERT", device_id, alert, None))

    for time, cancellations in sorted(cancelled_data.items()):
        for device_id, cancel in cancellations:
            queue.append((time, "CANCEL", device_id, cancel, None))

    queue = deque(sorted(queue, key=lambda x: x[0]))

    while queue:
        event_time, event_type, device_id, message, source_id = queue.popleft()

        if event_time > simulation_length:
            continue

        if event_type == "ALERT":
            if message not in received_alerts[device_id]:
                received_alerts[device_id].add(message)
                if source_id is not None:
                    print(f"@{event_time}: #{device_id} RECEIVED ALERT FROM #{source_id}: {message}")
                for to_device, delay in propagated_data[device_id]:
                    send_time = event_time + delay
                    if send_time <= simulation_length and message not in received_alerts[to_device]:
                        queue.append((send_time, "ALERT", to_device, message, device_id))
                        print(f"@{event_time}: #{device_id} SENT ALERT TO #{to_device}: {message}")
            queue = deque(sorted(queue, key=lambda x: x[0]))

        elif event_type == "CANCEL":
            if message not in received_cancellations[device_id]:
                received_cancellations[device_id].add(message)
                if source_id is not None:
                    print(f"@{event_time}: #{device_id} RECEIVED CANCELLATION FROM #{source_id}: {message}")
                for to_device, delay in propagated_data[device_id]:
                    send_time = event_time + delay
                    if send_time <= simulation_length and message not in received_cancellations[to_device]:
                        queue.append((send_time, "CANCEL", to_device, message, device_id))
                        print(f"@{event_time}: #{device_id} SENT CANCELLATION TO #{to_device}: {message}")

    print(f"@{simulation_length}: END")

