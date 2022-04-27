"""
Summary:
    delete a repository

Example:
    python3 delete_repository.py --name "myrepo"
"""


import argparse
import urllib3
import pulp_operations

# disable ssl
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def delete_repository(name: str) -> None:
    """
    Summary:
        delete a repository

    Parameters:
        name (str): the repository name

    Returns:
        None
    """

    # get the repository object
    repository = pulp_operations.repository.get_repo(name)

    # delete the repository object
    pulp_operations.repository.delete_repo(repository)


if __name__ == '__main__':
    # get arguments from cli
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True, action='store')
    args = parser.parse_args()

    # run
    delete_repository(name=args.name)
