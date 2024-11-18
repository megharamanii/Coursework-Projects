import unittest
from pathlib import Path
from process import process_file
import os

class TESTProcessFile(unittest.TestCase):
    def create_test_file(self, file_name, content):
        """Utility method to create a temporary file with the specified content."""
        path = Path(file_name)
        with open(path, 'w') as f:
            f.write(content)
        return path


    def test_valid_input_file(self):
        """Test with a valid input file."""
        file_content = """LENGTH 100
    DEVICE 1
    DEVICE 2
    PROPAGATE 1 2 5
    ALERT 1 alert1 10
    CANCEL 2 cancel1 20"""
        test_file = self.create_test_file("valid_input.txt", file_content)

        simulation_length, propagated, alerts, cancellations = process_file(test_file)

        self.assertEqual(simulation_length, 100)
        self.assertEqual(propagated, {1: [(2, 5)], 2: []})
        self.assertEqual(alerts, {10: [(1, 'alert1')]})
        self.assertEqual(cancellations, {20: [(2, 'cancel1')]})

        test_file.unlink()

    def test_empty_file(self):
        """Test with an empty file."""
        test_file = self.create_test_file("empty.txt", "")

        simulation_length, propagated, alerts, cancellations = process_file(test_file)

        self.assertEqual(simulation_length, 0)
        self.assertEqual(propagated, {})
        self.assertEqual(alerts, {})
        self.assertEqual(cancellations, {})

        test_file.unlink()

    def test_device_without_propagation_rules(self):
        """Test with a device that does not have any propagation rules."""
        file_content = """LENGTH 100
    DEVICE 1
    DEVICE 2
    PROPAGATE 2 3 5
    ALERT 1 alert1 10
    CANCEL 2 cancel1 20"""

        with open("temp_test_file.txt", "w") as temp_file:
            temp_file.write(file_content)

        _, propagated_data, _, _ = process_file("temp_test_file.txt")

        self.assertIn(1, propagated_data, "Device 1 should be in propagated_data.")
        self.assertEqual(propagated_data[1], [], "Device 1's propagation list should be empty.")

        try:
            os.remove("temp_test_file.txt")
        except OSError:
            pass

    def test_file_without_alerts(self):
        """Test with a file that does not contain any alerts."""
        file_content = """LENGTH 100
         DEVICE 1
         DEVICE 2
         PROPAGATE 1 2 5
         PROPAGATE 2 1 3
         CANCEL 1 cancel1 30"""

        with open("temp_test_file_no_alert.txt", "w") as temp_file:
            temp_file.write(file_content)

        simulation_length, propagated_data, alert_data, cancelled_data = process_file("temp_test_file_no_alert.txt")

        self.assertEqual(simulation_length, 100, "Simulation length should be 100.")
        self.assertIn(1, propagated_data, "Device 1 should be in propagated_data.")
        self.assertIn(2, propagated_data, "Device 2 should be in propagated_data.")
        self.assertEqual(propagated_data[1], [(2, 5)], "Propagation rules for Device 1 are incorrect.")
        self.assertEqual(propagated_data[2], [(1, 3)], "Propagation rules for Device 2 are incorrect.")
        self.assertEqual(alert_data, {}, "Alert data should be empty.")
        self.assertIn(30, cancelled_data, "Cancellation time 30 should be in cancelled_data.")
        self.assertEqual(cancelled_data[30], [(1, 'cancel1')], "Cancellation data is incorrect.")

        try:
            os.remove("temp_test_file_no_alert.txt")
        except OSError:
            pass
