"""repository functions"""

import logging
import pathlib
import pulpcore.client.pulp_rpm
from pulpcore.client.pulp_rpm.rest import ApiException
from pulp_operations.api_client_conf import rpm_configuration
from pulp_operations.signing import get_signservice
from pulp_operations.task import wait_for_task_complete, get_task_created_resource

# module logger - child of parent logger 'pulp_operations'
mlogger = logging.getLogger("pulp_operations.repository")


# functions
def get_repo(repo_name: str):
    """
    Summary:
        searches for an existing repository by name

    Parameters:
        repo_name (str): the repository name

    Returns:
        repository response object
    """

    # Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        # Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.RepositoriesRpmApi(api_client)

        try:
            repository = api_instance.list(name=repo_name).results[0]
            msg = f"found {repo_name}"
            mlogger.info(msg)
            return repository

        except ApiException as err:
            msg = f"Exception when calling RepositoriesRpmApi->list: {err}"
            mlogger.error(msg)
            raise


def get_repoversion(latest_version_href: str, rollback: int = 0):
    """
    Summary:
        returns the repoversion_href for the latest_version minus rollback

        for example if a latest version is 7, and rollback is 1, it will
        return version 6

        if latest version minus rollback is less then or equal to 0, it will return version 1

    Parameters:
        latest_version_href (str): the latest version href of the repository
        rollback (int): number of versions to rollback to

    Returns:
        repoversion_href string
    """

    # use pathlib to split out latest version of the repo from the href
    pathed_latest_version_href = pathlib.Path(latest_version_href)
    version_index = int(pathed_latest_version_href.parts.index("versions")) + 1
    latest_version = pathed_latest_version_href.parts[version_index]

    # selected version of repository is latest version minus rollback.
    # publications can't be linked to anything less than 1.
    output_version = int(latest_version) - rollback
    if output_version <= 0:
        output_version = 1

    # build url with selected version
    output = latest_version_href.replace(
        f"/versions/{latest_version}/", f"/versions/{output_version}/"
    )

    msg = f"latest version: {latest_version_href}"
    mlogger.info(msg)

    msg = f"rollback value: {rollback}"
    mlogger.info(msg)

    msg = f"using version: {output}"
    mlogger.info(msg)

    # output
    return output


def create_repo(repo_name: str, signservice_name: str = None):
    """
    Summary:
        creates a repository

    Parameters:
        repo_name (str): the repository name

    Returns:
        repository response object
    """

    # Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        # Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.RepositoriesRpmApi(api_client)

        try:
            if signservice_name:
                signservice = get_signservice(signservice_name)
                repository = api_instance.create(
                    rpm_rpm_repository={
                        "name": repo_name,
                        "retain_package_versions": 10,  # default is 0 (unlimited)
                        "metadata_signing_service": signservice.pulp_href,
                    }
                )
            else:
                repository = api_instance.create(
                    rpm_rpm_repository={
                        "name": repo_name,
                        "retain_package_versions": 10,  # default is 0 (unlimited)
                    }
                )

            msg = f"created {repo_name}"
            mlogger.info(msg)

            return repository

        except ApiException as err:
            msg = f"Exception when calling RepositoriesRpmApi->create: {err}"
            mlogger.error(msg)
            raise


def sync_repo(repository, remote):
    """
    Summary:
        syncs a repository with remote

    Parameters:
        repository (repository object): repository object
        remote (remote object): remote object

    Returns:
        None
    """

    # Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        # Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.RepositoriesRpmApi(api_client)

        try:
            # sync url object
            sync_url_object = pulpcore.client.pulp_rpm.RpmRepositorySyncURL(
                remote=remote.pulp_href, optimize=True, mirror=False
            )

            # sync task
            sync_task = api_instance.sync(
                rpm_rpm_repository_href=repository.pulp_href,
                rpm_repository_sync_url=sync_url_object,
            )

            # wait for task to complete. if sync caused a change, it will create a repoversion_href
            wait_for_task_complete(task_name="sync", task_href=sync_task.task)
            repoversion_href = get_task_created_resource(task_href=sync_task.task)

            # logging
            if repoversion_href:
                msg = f"syncing {repository.name} to remote {remote.name} created a new version"
                mlogger.info(msg)
            else:
                msg = (
                    f"no change when syncing {repository.name} to remote {remote.name}"
                )
                mlogger.info(msg)

        except ApiException as err:
            msg = f"Exception when calling RepositoriesRpmApi->sync: {err}"
            mlogger.error(msg)
            raise


def add_remove_file_repo(action: str, repository, content):
    """
    Summary:
        adds or removes a rpm file from a repository

    Parameters:
        action (str): 'add' or 'remove'
        repository (repository object): the repository
        content (content object): the content

    Returns:
        None
    """

    # Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        # Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.RepositoriesRpmApi(api_client)

        try:
            # check action values
            valid_action_values = ["add", "remove"]
            if action not in valid_action_values:
                msg = f"action parameter value '{action}' is not valid"
                mlogger.error(msg)
                raise ValueError(msg)

            # add
            if action == "add":
                add_remove_content_object = (
                    pulpcore.client.pulp_rpm.RepositoryAddRemoveContent(
                        add_content_units=[content.pulp_href]
                    )
                )

            # remove
            else:
                add_remove_content_object = (
                    pulpcore.client.pulp_rpm.RepositoryAddRemoveContent(
                        remove_content_units=[content.pulp_href]
                    )
                )

            # task
            file_task = api_instance.modify(
                rpm_rpm_repository_href=repository.pulp_href,
                repository_add_remove_content=add_remove_content_object,
            )

            # wait for task to complete
            wait_for_task_complete(task_name=f"{action} rpm", task_href=file_task.task)
            repoversion_href = get_task_created_resource(task_href=file_task.task)

            # logging
            if repoversion_href:
                msg = f"{action} rpm to {repository.name} created a new version"
                mlogger.info(msg)
            else:
                msg = f"no change after rpm {action} on {repository.name}"
                mlogger.info(msg)

        except ApiException as err:
            msg = f"Exception when calling RepositoriesRpmApi->modify: {err}"
            mlogger.error(msg)
            raise


def list_repo():
    """
    Summary:
        lists all repos

    Parameters:
        none

    Returns:
        list of repos
    """

    # Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        # Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.RepositoriesRpmApi(api_client)

        try:
            output = api_instance.list()
            return output
        except ApiException as err:
            msg = f"Exception when calling RepositoriesRpmApi->list: {err}"
            mlogger.error(msg)
            raise


def delete_repo(repository):
    """
    Summary:
        deletes an existing repository

    Parameters:
        repository: the repository object

    Returns:
        None
    """

    # Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        # Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.RepositoriesRpmApi(api_client)

        try:
            repository_task = api_instance.delete(
                rpm_rpm_repository_href=repository.pulp_href
            )

            wait_for_task_complete(
                task_name="delete repository", task_href=repository_task.task
            )

            msg = f"deleted {repository.name}"
            mlogger.info(msg)

        except ApiException as err:
            msg = f"Exception when calling RepositoriesRpmApi->delete: {err}"
            mlogger.error(msg)
            raise
