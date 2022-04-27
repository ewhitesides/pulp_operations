"""
Summary:
    delete a rpm from a repository and update the distribution

Example:
    python3 delete_rpm.py --rpm_file='app.rpm' --repo_name='myrepo' --dist_name='myrepo-dist'
"""

import argparse
import urllib3
from pulp_operations.repository import get_repo, add_remove_file_repo
from pulp_operations.file import get_rpm_properties
from pulp_operations.content import get_content_by_properties
from pulp_operations import release

# disable ssl
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def delete_rpm(rpm_file: str, repo_name: str) -> None:
    """
    Summary:
        removes a rpm from a repository and updates the distribution

    Parameters:
        rpm_file (str): the rpm file
        repo_name (str): the repository name to add the file to

    Returns:
        None
    """

    # repository
    repository = get_repo(repo_name)

    # get properties from rpm_file name
    rpm_file_properties = get_rpm_properties(rpm_file)

    # find content by rpm_file
    content = get_content_by_properties(rpm_file_properties, repository)

    # remove content from repository
    add_remove_file_repo('remove', repository, content)


if __name__ == '__main__':

    # get arguments from cli
    parser = argparse.ArgumentParser()
    parser.add_argument('--rpm_file',  required=True, action='store')
    parser.add_argument('--repo_name', required=True, action='store')
    parser.add_argument('--dist_name', required=True, action='store')
    args = parser.parse_args()

    # delete the rpm
    delete_rpm(
        rpm_file=args.rpm_file,
        repo_name=args.repo_name
    )

    # update the distribution
    release(
        repo_name=args.repo_name,
        version_rollback=0,
        dist_name=args.dist_name
    )
