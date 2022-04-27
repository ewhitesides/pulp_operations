"""
init
"""

from pulp_operations.repository import get_repo, get_repoversion, create_repo
from pulp_operations.repository import sync_repo
from pulp_operations.remote import get_remote, create_remote
from pulp_operations.publication import get_publication, create_publication
from pulp_operations.distribution import get_distribution, update_distribution, create_distribution

def sync(repo_name: str, remote_name: str, remote_url: str, signservice_name: str = None):
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

    #repository
    try:
        repository = get_repo(repo_name)
    except IndexError:
        repository = create_repo(repo_name, signservice_name)

    #remote
    try:
        remote = get_remote(remote_name)
    except IndexError:
        remote = create_remote(remote_name, remote_url)

    #sync
    sync_repo(repository, remote)

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

    #get repository latest version
    repository = get_repo(repo_name)
    repoversion_href = get_repoversion(repository.latest_version_href, version_rollback)

    #publication
    try:
        publication_href = get_publication(repoversion_href)
    except IndexError:
        publication_href = create_publication(repoversion_href)

    #distribution
    try:
        distribution = get_distribution(dist_name)
        update_distribution(distribution, publication_href)
    except IndexError:
        create_distribution(dist_name, publication_href)
