from __future__ import annotations

from typing import NamedTuple
from pathlib import Path
from .settings import load_config

Experiment = NamedTuple("Experiment", name=str, description=str, num_runs=int)

def create_new_experiment(form_data: dict):
    config = load_config()

    experiment_path = Path(config['Directories']['results_path']) / form_data['name']
    experiment_path.mkdir(parents=True, exist_ok=False)
    (experiment_path / 'description.txt').write_text(form_data['description'])

def get_experiments() -> list[Experiment]:
    experiment_table_items = [
        Experiment(
            name = "quad_scan_with_jitter",
            description = "Quadrupole scan where noise is added to position, angle, and momentum.",
            num_runs = 14,
        )
    ]

    return experiment_table_items