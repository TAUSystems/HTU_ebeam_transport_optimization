from __future__ import annotations

from flask import url_for

from typing import Optional, Union
from datetime import datetime
from pathlib import Path
from os import walk as os_walk
import re
from typing import Generator
from shutil import copytree
from .settings import load_config

from rsopt_interface.run_rsopt import run_rsopt

RUN_ID_DATETIME_FORMAT = "%Y-%m-%dT%H-%M-%S"

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


def get_run(run_id: Union[str, datetime]) -> Run:
    if isinstance(run_id, datetime):
        run_datetime = run_id.strftime(RUN_ID_DATETIME_FORMAT)
    elif isinstance(run_id, str):
        run_datetime = run_id
    
    for run_folder in run_folder_generator():
        if run_folder.name == run_datetime:
            break
    
    else:
        raise ValueError(f"No run found with run id {run_id}")

    return Run(datetime.strptime(run_folder.name, RUN_ID_DATETIME_FORMAT), 
               run_folder.parent.name
              )

def run_simulation(form_data: dict):
    run = Run(datetime.now(), form_data['experiment_name'])

    # create directory and store description and status
    run_path = run.get_path()
    run_path.mkdir(parents=False, exist_ok=False)

    (run_path / 'description.txt').write_text(form_data['description'])
    (run_path / 'status.txt').write_text("starting")

    # copy files from simulation files folder
    config = load_config()
    copytree(
        Path(config['Directories']['rsopt_simulation_files_path']), 
        run_path / 'input'
    )
    
    # start the simulation
    (run_path / 'status.txt').write_text("running")
    
    run_rsopt(
        run_path,
        run_path / 'input', 
    )



def run_folder_generator(experiment_name: Optional[str] = None) -> Generator[Path, None, None]:
    config = load_config()

    def experiment_run_folder_generator(experiment_name: str):
        experiment_path = Path(config['Directories']['results_path']) / experiment_name

        datetime_regex = re.compile("\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}")
        for p in experiment_path.iterdir():
            if p.is_dir() and datetime_regex.match(p.name):
                yield p
    
    if experiment_name is not None:
        yield from experiment_run_folder_generator(experiment_name)

    else:
        for p in Path(config['Directories']['results_path']).iterdir():
            if p.is_dir():
                yield from experiment_run_folder_generator(p.name)


def get_runs(experiment_name: Optional[str] = None) -> list[Run]:

    runs = []
    
    for run_folder in run_folder_generator(experiment_name):
        dt = datetime.strptime(run_folder.name, RUN_ID_DATETIME_FORMAT)
        experiment = run_folder.parent.name

        runs.append(
            Run(
                datetime = dt,
                experiment = experiment,
            )
        )

    return runs
