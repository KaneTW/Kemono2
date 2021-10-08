"""
This modules holds various constants not related to environment variables.
Therefore no exported functions allowed.
"""

from pathlib import Path

project_path = Path(__file__, '..', '..').resolve()
test_path = project_path.joinpath('test')
client_files_folder = project_path.joinpath('dist')
templates_folder = client_files_folder.joinpath('pages')
