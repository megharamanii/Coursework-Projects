from pathlib import Path
from simulation import*
from process import*


def _read_input_file_path() -> Path:
    """Reads the input file path from the standard input"""
    return Path(input())


def main() -> None:
    """Runs the simulation program in its entirety"""
    input_file_path = _read_input_file_path()

    if not input_file_path.exists():
        print("FILE NOT FOUND")
        return

    simulation_data, propagated_data, alert_data, cancelled_data = process_file(input_file_path)
    simulate(simulation_data, propagated_data, alert_data, cancelled_data)


if __name__ == '__main__':
    main()
