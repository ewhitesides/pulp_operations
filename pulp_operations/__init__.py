"""
init
"""

from pulp_operations.repository import (
    get_repo,
    get_repoversion,
    create_repo,
    list_repo,
    delete_repo,
)
from pulp_operations.repository import sync_repo, add_remove_file_repo
from pulp_operations.remote import get_remote, create_remote, delete_remote
from pulp_operations.publication import get_publication, create_publication
from pulp_operations.distribution import get_distribution
from pulp_operations.distribution import (
    update_distribution,
    create_distribution,
    list_distribution,
)
from pulp_operations.distribution import delete_distribution
from pulp_operations.file import get_sha256hash, get_rpm_properties
from pulp_operations.artifact import get_artifact, create_artifact
from pulp_operations.content import (
    get_content_by_hash,
    get_content_by_properties,
    create_content,
)


def sync(
    repo_name: str, remote_name: str, remote_url: str, signservice_name: str = None
):
    """
    Summary:
        syncs a repository with a remote

    Parameters:
        repo_name (str): the repository name to add the file to
        remote_name (str): the remote name
        remote_url (str): the url attached to the remote
        signing_service (str): the name of the signing service. default is None.

    Returns:
        None
    """

    # repository
    try:
        repository = get_repo(repo_name)
    except IndexError:
        repository = create_repo(repo_name, signservice_name)

    # remote
    try:
        remote = get_remote(remote_name)
    except IndexError:
        remote = create_remote(remote_name, remote_url)

    # sync
    sync_repo(repository, remote)


def add_rpm(rpm_file: str, repo_name: str, signservice_name: str = None):
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
    add_remove_file_repo("add", repository, content)


def remove_rpm(rpm_file: str, repo_name: str):
    """
    Summary:
        removes a rpm from a repository

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
    add_remove_file_repo("remove", repository, content)


def release(repo_name: str, version_rollback: int, dist_name: str):
    """
    Summary:
        select a version of the repository and create a publication for it.
        the publication is then linked to the distribution.

        the rollback parameter determines how many versions behind the latest version
        of the repository that you want to present to the publication and distribution

    Parameters:
        repo_name (str): the repository name
        version_rollback (int): number of versions to rollback to
        dist_name (str): the name of the distribution to attach to

    Returns:
        None
    """

    # get repository latest version
    repository = get_repo(repo_name)
    repoversion_href = get_repoversion(repository.latest_version_href, version_rollback)

    # publication
    try:
        publication_href = get_publication(repoversion_href)
    except IndexError:
        publication_href = create_publication(repoversion_href)

    # distribution
    try:
        distribution = get_distribution(dist_name)
        update_distribution(distribution, publication_href)
    except IndexError:
        create_distribution(dist_name, publication_href)


def list_repository_names():
    """
    Summary:
        list the names of all repositories
    """

    results = list_repo().to_dict()["results"]
    for result in results:
        print(result["name"])


def remove_repository(repo_name: str):
    """
    Summary:
        deletes a repository

    Parameters:
        repo_name (str): the repository name

    Returns:
        None
    """
    repository = get_repo(repo_name)
    delete_repo(repository)


def remove_remote(remote_name: str):
    """
    Summary:
        deletes a remote

    Parameters:
        remote_name (str): the remote name

    Returns:
        None
    """
    remote = get_remote(remote_name)
    delete_remote(remote)


def list_distribution_names():
    """
    Summary:
        list the names of all distributions
    """

    results = list_distribution().to_dict()["results"]
    for result in results:
        print(result["name"])


def remove_distribution(dist_name: str):
    """
    Summary:
        deletes a distribution

    Parameters:
        dist_name (str): the distribution name

    Returns:
        None
    """

    distribution = get_distribution(dist_name)
    delete_distribution(distribution)
