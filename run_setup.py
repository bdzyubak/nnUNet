import os
from utils.os_utilities import run_command, check_conda_installed


def main():
    check_conda_installed()

    env_name = 'nnunet'
    conda_create = 'conda create -n ' + env_name + ' -y'
    retcode, text = run_command(conda_create)

    setup_path = "pip install -e " + os.path.join(os.path.dirname(__file__), '.')

    conda_setup = 'conda run -n ' + env_name + ' ' + setup_path
    retcode, text = run_command(conda_setup)
    print(f'Conda environemnt ' + env_name + ' installed successfully.')


if __name__ == "__main__":
    main()
