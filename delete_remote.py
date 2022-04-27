"""
Summary:
    delete a remote

Example:
    python3 delete_remote.py --name "myremote"
"""

import argparse
import urllib3
import pulp_operations

# disable ssl
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def delete_remote(name: str) -> None:
    """
    Summary:
        delete a remote

    Parameters:
        name (str): the remote name

    Returns:
        None
    """

    # get the remote object
    remote = pulp_operations.remote.get_remote(name)

    # delete the remote object
    pulp_operations.remote.delete_remote(remote)


if __name__ == '__main__':
    # get arguments from cli
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True, action='store')
    args = parser.parse_args()

    # run
    delete_remote(name=args.name)
