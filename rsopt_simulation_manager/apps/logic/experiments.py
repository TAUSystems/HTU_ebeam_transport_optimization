from __future__ import annotations

from typing import NamedTuple
from pathlib import Path
from .settings import load_config
from .runs import run_folder_generator

Experiment = NamedTuple("Experiment", name=str, description=str, num_runs=int)

def create_new_experiment(form_data: dict):
    config = load_config()

    experiment_path = Path(config['Directories']['results_path']) / form_data['name']
    experiment_path.mkdir(parents=True, exist_ok=False)
    (experiment_path / 'description.txt').write_text(form_data['description'])

def get_experiments() -> list[Experiment]:
    config = load_config()

    experiments = []    

    for p in Path(config['Directories']['results_path']).iterdir():
        if not p.is_dir():
            continue

        experiment_name = p.name
        experiment_path = Path(config['Directories']['results_path']) / experiment_name

        try:
            description = (experiment_path / 'description.txt').read_text()
        except FileNotFoundError:
            description = ""

        experiments.append(
            Experiment(
                name = experiment_name,
                description = description,
                num_runs = sum(1 for _ in run_folder_generator(experiment_name)),
            )
        )

    return experiments
