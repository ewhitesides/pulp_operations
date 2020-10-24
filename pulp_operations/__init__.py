"""
init
"""

from pulp_operations.logger import logger
from pulp_operations.repository import get_repo, create_repo, delete_repo
from pulp_operations.repository import sync_repo, add_remove_file_repo
from pulp_operations.remote import get_remote, create_remote, delete_remote
from pulp_operations.publication import get_publication, create_publication
from pulp_operations.distribution import get_distribution, get_distribution_url
from pulp_operations.distribution import update_distribution, create_distribution
from pulp_operations.distribution import delete_distribution
from pulp_operations.file import get_sha256hash, get_rpm_properties
from pulp_operations.artifact import get_artifact, create_artifact
from pulp_operations.content import get_content_by_hash, get_content_by_properties, create_content

def start_sync (
    repo_name: str,
    remote_name: str,
    remote_url: str,
    signservice_name: str = None
    ):
    """
    Summary:
        syncs a repository to a remote. if syncing changes the repository,
        create the publication and attach/create/update the distribution
        if repository and/or remote doesn't exist, it will create it.

    Parameters:
        repo_name (str): the repository name to add the file to
        remote_name (str): the remote name
        remote_url (str): the url attached to the remote
        signing_service (str): the name of the signing service. default is None.

    Returns:
        None
    """
    #distribution names based on repo name
    dev_dist_name = f"{repo_name}-dev_dist"
    prod_dist_name = f"{repo_name}-prod_dist"

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
    repoversion_href = sync_repo(repository, remote)

    #if sync produced a new repoversion href
    if repoversion_href:

        #dev distribution attaches to latest publication version
        latest_publication_href = create_publication(repoversion_href)
        try:
            distribution = get_distribution(dev_dist_name)
            update_distribution(distribution, latest_publication_href)
        except IndexError:
            create_distribution(dev_dist_name, latest_publication_href)

        #prod distribution attaches to previous publication version
        previous_publication_href = get_publication(repoversion_href, 1)
        try:
            distribution = get_distribution(prod_dist_name)
            update_distribution(distribution, previous_publication_href)
        except IndexError:
            create_distribution(prod_dist_name, previous_publication_href)

def add_rpm(
    rpm_file: str,
    repo_name: str,
    dist_name: str,
    signservice_name: str = None
    ):
    """
    Summary:
        adds a rpm to a repository. if adding the file changes the repository,
        create the publication and attach/create/update the distribution
        if repository doesn't exist, it will create it.

    Parameters:
        rpm_file (str): the rpm file
        repo_name (str): the repository name to add the file to
        dist_name (str): the distribution name
        signing_service (str): the name of the signing service. default is None.

    Returns:
        None
    """
    #repository
    try:
        repository = get_repo(repo_name)
    except IndexError:
        repository = create_repo(repo_name, signservice_name)

    #get sha256 of file
    rpm_file_sha256 = get_sha256hash(rpm_file)

    #artifact
    try:
        artifact = get_artifact(rpm_file_sha256)
    except IndexError:
        artifact = create_artifact(rpm_file)

    #content
    try:
        content = get_content_by_hash(rpm_file_sha256)
    except IndexError:
        create_content(artifact, rpm_file)
        content = get_content_by_hash(rpm_file_sha256)

    #add content to repository
    repoversion_href = add_remove_file_repo('add', repository, content)

    #if adding file created a new repoversion href
    if repoversion_href:

        #publication
        publication_href = create_publication(repoversion_href)

        #distribution
        try:
            distribution = get_distribution(dist_name)
            update_distribution(distribution, publication_href)
        except IndexError:
            create_distribution(dist_name, publication_href)

def remove_rpm(rpm_file: str, repo_name: str, dist_name: str):
    """
    Summary:
        removes a rpm from a repository. if removing the file changes the repository,
        create the publication and attach/create/update the distribution

    Parameters:
        rpm_file (str): the rpm file
        repo_name (str): the repository name to add the file to
        dist_name (str): the distribution name

    Returns:
        None
    """
    #repository
    repository = get_repo(repo_name)

    #get properties from rpm_file name
    rpm_file_properties = get_rpm_properties(rpm_file)

    #find content by rpm_file
    content = get_content_by_properties(rpm_file_properties, repository)

    #remove content from repository
    repoversion_href = add_remove_file_repo('remove', repository, content)

    #if removing file created a new repoversion href
    if repoversion_href:

        #publication
        publication_href = create_publication(repoversion_href)

        #distribution
        try:
            distribution = get_distribution(dist_name)
            update_distribution(distribution, publication_href)
        except IndexError:
            create_distribution(dist_name, publication_href)

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
