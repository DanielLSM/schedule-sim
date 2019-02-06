import pathlib
from pathlib import Path

ENVS_DIR = Path(__file__).resolve().parent

parameteres_default_file = ENVS_DIR / 'config' / 'task_day_custom.yaml'

render_file = ENVS_DIR / 'config' / 'render_options.yaml'

#TODO: one day we should make a function to search for yamls with rglob
TEMPLATES_DIR = [_ for _ in ENVS_DIR.rglob('*.yaml')]

# render_file = pathlib.Path('config/render_options.yaml').absolute()
