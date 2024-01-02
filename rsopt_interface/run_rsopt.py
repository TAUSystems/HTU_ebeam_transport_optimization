from __future__ import annotations

from pathlib import Path
from typing import Optional
import os
from shutil import move as shutil_move
import subprocess
from threading import Thread

def _rsopt_process(run_path: Path, rsopt_simulation_files_path: Path):
    # get list of all simulation files (as Path) in rsopt_simulation_files_path
    # to ignore these in copying everything else.
    simulation_files_folders = list(rsopt_simulation_files_path.iterdir())

    # run rsopt
    os.chdir(rsopt_simulation_files_path)
    subprocess.run(
        ['sh', './run.sh'], 
        cwd=rsopt_simulation_files_path
    )
    (run_path / 'status.txt').write_text('finished')

    # move output files
    (run_path / 'output').mkdir(parents=True, exist_ok=False)
    for p in rsopt_simulation_files_path.iterdir():
        if p not in simulation_files_folders:
            print(f"moving {p}")
            shutil_move(p, (run_path / 'output'))


def run_rsopt(run_path: Path, rsopt_simulation_files_path: Optional[Path] = None):
    """ Invoke rsopt 

    Runs the equivalent of calling `rsopt optimize configure configuration.yml`
    from the command line in the rsopt_simulation_files_path folder. Status will
    be written to run_path/status.txt and output to run_path/output

    Parameters
    ----------
    run_path : Path
        The path for this run's folder. status.txt and the output directory 
        will be placed in this folder
    rsopt_simulation_files_path : Path
        The path where simulation files, including configuration.yml, can be found.
        If not given, defaults to run_path/input

    """
    if rsopt_simulation_files_path is None:
        rsopt_simulation_files_path = run_path / 'input'

    th = Thread(target=_rsopt_process, args=(run_path, rsopt_simulation_files_path))
    th.start()    
    (run_path / 'status.txt').write_text('running')
