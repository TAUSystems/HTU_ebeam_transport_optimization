from __future__ import annotations
from typing import NamedTuple

Experiment = NamedTuple("Experiment", name=str, description=str, num_runs=int)

def create_new_experiment(form: dict):
    print(form)

def get_experiments() -> list[Experiment]:
    experiment_table_items = [
        Experiment(
            name = "quad_scan_with_jitter",
            description = "Quadrupole scan where noise is added to position, angle, and momentum.",
            num_runs = 14,
        )
    ]

    return experiment_table_items