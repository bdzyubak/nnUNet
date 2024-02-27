import os
from utils.os_utilities import check_conda_installed


def main():
    check_conda_installed()

    env_name = 'nnunet'
    conda_create = 'conda create -n ' + env_name + ' -y'
    os.system(conda_create)

    setup_path = os.path.join(os.path.dirname(__file__), 'setup.py .')
    conda_setup = 'conda run -n ' + env_name + ' ' + setup_path
    os.system(conda_setup)
    print(f'Conda environemnt ' + env_name + ' installed successfully.')


if __name__ == "__main__":
    main()
