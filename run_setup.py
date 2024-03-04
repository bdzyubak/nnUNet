import os
from pathlib import Path
from utils.os_utilities import run_command, check_conda_installed


def main():
    check_conda_installed()

    env_name = 'nnunet'
    command_conda_create = 'conda create -n ' + env_name + ' -y'
    retcode, text = run_command(command_conda_create)
    if retcode == 0:
        print(f'Conda environment {env_name} created successfully.')
    else:
        print(f'Conda environment {env_name} failed to be created. Check write permissions in conda install dir.')
        print(text)

    path_submodule_setup = "pip install -e " + os.path.join(os.path.dirname(__file__), '.')
    command_conda_setup = 'conda run -n ' + env_name + ' ' + path_submodule_setup
    retcode, text = run_command(command_conda_setup)
    if retcode == 0:
        print(f'Dependencies installed successfully.')
    else:
        print(f'Failed to install dependencies. {text}')

    # This is needed to run in command line; for Pycharm use Settings->Project->Project Structure and add the below
    # submodules as source folders
    path_source = Path(__file__).parents[1]
    for submodule in ['nnUnet', 'utils']:
        submodule_path = str(path_source / submodule)
        command_add_submodule_path = 'conda develop ' + submodule_path + ' -n ' + env_name
        retcode, text = run_command(command_add_submodule_path)
        print(f'Developed submodule path {submodule_path} to {env_name}')


if __name__ == "__main__":
    main()
