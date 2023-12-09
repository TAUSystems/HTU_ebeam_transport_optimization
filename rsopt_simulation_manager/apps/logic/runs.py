from __future__ import annotations
from typing import Optional, NamedTuple
from datetime import datetime
from .experiments import get_experiments


Run = NamedTuple("Run", datetime=datetime, description=str, experiment=str, status=str)

def run_simulation(form: dict):
    print(form)

def get_runs(experiment_name: Optional[str] = None) -> list[Run]:
    def get_runs_for_experiment(experiment_name: str):
        if experiment_name == 'quad_scan_with_jitter':
            run_table_items = [
                Run(
                    datetime = datetime(2023, 12, 1, 18, 33, 12),
                    description = "start changed to xx",
                    experiment = "quad_scan_with_jitter",
                    status = "Success",
                )
            ]
        else:
            raise ValueError("No experiment with that name.")

        return run_table_items

    if experiment_name is None:
        return sum([get_runs_for_experiment(experiment.name) for experiment in get_experiments()], [])
    else:
        return get_runs_for_experiment(experiment_name)
