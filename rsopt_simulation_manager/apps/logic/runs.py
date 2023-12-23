from __future__ import annotations
from typing import Optional, NamedTuple
from datetime import datetime
from .experiments import get_experiments


RUN_ID_DATETIME_FORMAT = "%Y-%m-%dT%H-%M-%S"

def run_simulation(form: dict):
    print(form)
class Run:
    def __init__(self, 
                 datetime: datetime,
                 experiment: str,
                ):
        self.datetime = datetime
        self.experiment = experiment

    def get_path(self) -> Path:
        config = load_config()
        return Path(config['Directories']['results_path']) / self.experiment / self.datetime.strftime(RUN_ID_DATETIME_FORMAT)

    def get_image_paths(self) -> list[Path]:
        image_paths = []
        for dirpath, dirnames, filenames in os_walk(self.get_path()):
            for filename in filenames:
                p = Path(dirpath) / filename
                if p.suffix in ['.png']:
                    # image_paths.append(p)
                    image_paths.append(url_for('.get_run_image', 
                                               run_id=self.datetime.strftime(RUN_ID_DATETIME_FORMAT),
                                               rel_image_path=p.relative_to(self.get_path()),
                                              )
                                      )

        return image_paths


    @property
    def description(self) -> str:
        try:
            return (self.get_path() / 'description.txt').read_text()
        except FileNotFoundError:
            return ""

    @description.setter
    def description(self, value: str):
        (self.get_path() / 'description.txt').write_text(value)

    @property
    def status(self) -> str:
        try:
            return (self.get_path() / 'status.txt').read_text()
        except FileNotFoundError:
            return ""

    @status.setter
    def status(self, value: str):
        (self.get_path() / 'status.txt').write_text(value)


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
