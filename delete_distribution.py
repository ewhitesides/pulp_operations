"""
Summary:
    delete a distribution

Example:
    python3 delete_distribution.py --name "mydistribution"
"""

import argparse
import urllib3
import pulp_operations

#disable ssl
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def delete_distribution(name: str) -> None:
    """
    Summary:
        deletes a distribution

    Parameters:
        name (str): the distribution name

    Returns:
        None
    """

    #get the distribution object
    distribution = pulp_operations.distribution.get_distribution(name)

    #delete the distribution object
    pulp_operations.distribution.delete_distribution(distribution)

if __name__ == '__main__':
    #get arguments from cli
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True, action='store')
    args = parser.parse_args()

    #run
    delete_distribution(name=args.name)
