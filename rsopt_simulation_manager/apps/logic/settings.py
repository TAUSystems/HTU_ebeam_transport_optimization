from __future__ import annotations

from platformdirs import user_data_dir
from pathlib import Path
from configparser import ConfigParser

def config_path() -> Path:
    return Path(user_data_dir(appname="rsopt_simulation_manager", appauthor="TAUSystems")) / "config.ini"


def save_config(form_data: dict):
    cp = ConfigParser()
    cp['Directories'] = {
        'rsopt_simulation_files_path': form_data['rsopt_simulation_files_path'],
        'results_path': form_data['results_path'],
    }
    
    config_path().parent.mkdir(parents=True, exist_ok=True)

    with config_path().open('w') as f:
        cp.write(f)

def load_config() -> dict[str, dict[str, str]]:
    cp = ConfigParser()

    try:
        cp.read(config_path())
        return {section_name: dict(cp.items(section_name)) for section_name in cp.sections()}

    except:
        return {'Directories': {
            'rsopt_simulation_files_path': "",
            'results_path': "",
        }}
