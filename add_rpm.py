"""
Summary:
    add all rpm files found in same path as this script and update the distribution
    if the repository specified does not exist, it is created as part of adding the rpm

Example:
    python3 add_rpm.py --repo_name='myrepo' --dist_name='myrepo-dist' --sign_service='sign-metadata'
"""

import pathlib
import argparse
import urllib3
from pulp_operations import release
from pulp_operations.repository import get_repo, create_repo, add_remove_file_repo
from pulp_operations.artifact import get_artifact, create_artifact
from pulp_operations.file import get_sha256hash
from pulp_operations.content import get_content_by_hash, create_content

# disable ssl
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def add_rpm(rpm_file: str, repo_name: str, signservice_name: str = None) -> None:
    """
    Summary:
        adds a rpm to a repository

    Parameters:
        rpm_file (str): the rpm file
        repo_name (str): the repository name to add the file to
        signing_service (str): the name of the signing service. default is None.

    Returns:
        None
    """

    # repository
    try:
        repository = get_repo(repo_name)
    except IndexError:
        repository = create_repo(repo_name, signservice_name)

    # get sha256 of file
    rpm_file_sha256 = get_sha256hash(rpm_file)

    # artifact
    try:
        artifact = get_artifact(rpm_file_sha256)
    except IndexError:
        artifact = create_artifact(rpm_file)

    # content
    try:
        content = get_content_by_hash(rpm_file_sha256)
    except IndexError:
        create_content(artifact, rpm_file)
        content = get_content_by_hash(rpm_file_sha256)

    # add content to repository
    add_remove_file_repo('add', repository, content)


if __name__ == '__main__':
    # get arguments from cli
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo_name', required=True, action='store')
    parser.add_argument('--dist_name', required=True, action='store')
    parser.add_argument('--sign_service', required=True, action='store')
    args = parser.parse_args()

    # run add_rpm function on each rpm file found in this directory
    for file in pathlib.Path('.').glob('*.rpm'):
        add_rpm(
            rpm_file=str(file),
            repo_name=args.repo_name,
            signservice_name=args.sign_service
        )

    # release updated version of the repository to the distribution
    release(
        repo_name=args.repo_name,
        version_rollback=0,
        dist_name=args.dist_name
    )
