import unittest
from collections import defaultdict, deque
from unittest.mock import patch
from simulation import simulate


class TestSimulation(unittest.TestCase):
    def test_empty_data(self):
        """Test simulation with no alerts or cancellations."""
        simulation_data = 10  # Ensure that simulation length is defined, even for empty data
        propagated_data = defaultdict(list)
        alert_data = {}
        cancelled_data = {}
        with patch('builtins.print') as mocked_print:
            simulate(simulation_data, propagated_data, alert_data, cancelled_data)
            # If the simulate function prints an end message by default, expect it
            mocked_print.assert_called_with(f"@{simulation_data}: END")


    def test_only_alerts(self):
        """Test simulation with only alert events."""
        simulation_data = 5
        propagated_data = defaultdict(list, {1: [(2, 1)]})
        alert_data = {0: [(1, 'alert1')]}
        cancelled_data = {}
        expected_output = [
            "@0: #1 SENT ALERT TO #2: alert1",
            "@1: #2 RECEIVED ALERT FROM #1: alert1"
        ]
        with patch('builtins.print') as mocked_print:
            simulate(simulation_data, propagated_data, alert_data, cancelled_data)
            mocked_print.assert_has_calls([unittest.mock.call(line) for line in expected_output], any_order=True)


    def test_only_cancellations(self):
        """Test simulation with only cancellation events."""
        simulation_data = 5
        propagated_data = defaultdict(list, {1: [(2, 1)]})
        alert_data = {}
        cancelled_data = {0: [(1, 'cancel1')]}
        expected_output = [
            "@0: #1 SENT CANCELLATION TO #2: cancel1",
            "@1: #2 RECEIVED CANCELLATION FROM #1: cancel1"
        ]
        with patch('builtins.print') as mocked_print:
            simulate(simulation_data, propagated_data, alert_data, cancelled_data)
            mocked_print.assert_has_calls([unittest.mock.call(line) for line in expected_output], any_order=True)

    def test_alert_and_cancel_interaction(self):
        """Test simulation where alerts are followed by cancellations."""
        simulation_data = 10
        propagated_data = defaultdict(list, {1: [(2, 1)], 2: [(1, 1)]})
        alert_data = {0: [(1, 'alert1')]}
        cancelled_data = {2: [(2, 'cancel1')]}
        expected_output = [
            "@0: #1 SENT ALERT TO #2: alert1",
            "@1: #2 RECEIVED ALERT FROM #1: alert1",
            "@2: #2 SENT CANCELLATION TO #1: cancel1",
            "@3: #1 RECEIVED CANCELLATION FROM #2: cancel1"
        ]
        with patch('builtins.print') as mocked_print:
            simulate(simulation_data, propagated_data, alert_data, cancelled_data)
            mocked_print.assert_has_calls([unittest.mock.call(line) for line in expected_output], any_order=True)

    def test_simulation_end(self):
        """Test that the simulation stops at the defined simulation end time."""
        simulation_data = 3
        propagated_data = defaultdict(list, {1: [(2, 2)]})
        alert_data = {0: [(1, 'alert1')]}
        cancelled_data = {}
        expected_output = [
            "@0: #1 SENT ALERT TO #2: alert1"
        ]
        with patch('builtins.print') as mocked_print:
            simulate(simulation_data, propagated_data, alert_data, cancelled_data)
            mocked_print.assert_has_calls([unittest.mock.call(line) for line in expected_output], any_order=True)
            mocked_print.assert_called_with("@3: END")

if __name__ == "__main__":
    unittest.main()


