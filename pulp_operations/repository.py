"""repository functions"""

import pulpcore.client.pulp_rpm
from pulpcore.client.pulp_rpm.rest import ApiException
from pulp_operations.api_client_conf import rpm_configuration
from pulp_operations.signing import get_signservice
from pulp_operations.task import wait_for_task_complete, get_task_created_resource

def get_repo(repo_name: str):
    """
    Summary:
        searches for an existing repository by name

    Parameters:
        repo_name (str): the repository name

    Returns:
        repository response object
    """

    #Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        #Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.RepositoriesRpmApi(api_client)

        try:
            repository = api_instance.list(name=repo_name).results[0]
            print(f"repository: found {repo_name}")
            return repository

        except ApiException as err:
            print("Exception when calling RepositoriesRpmApi->list: %s\n" % err)
            raise

def create_repo(repo_name: str, signservice_name: str = None):
    """
    Summary:
        creates a repository

    Parameters:
        repo_name (str): the repository name

    Returns:
        repository response object
    """

    #Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        #Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.RepositoriesRpmApi(api_client)

        try:
            if signservice_name:
                signservice = get_signservice(signservice_name)
                repository = api_instance.create(
                    rpm_rpm_repository = {
                        'name': repo_name,
                        'retain_package_versions': 10, #default is 0 (unlimited)
                        'metadata_signing_service': signservice.pulp_href
                    }
                )
            else:
                repository = api_instance.create(
                    rpm_rpm_repository = {
                        'name': repo_name,
                        'retain_package_versions': 10, #default is 0 (unlimited)
                    }
                )
            print(f"repository: created {repo_name}")
            return repository

        except ApiException as err:
            print("Exception when calling RepositoriesRpmApi->create: %s\n" % err)
            raise

def sync_repo(repository, remote):
    """
    Summary:
        syncs a repository with remote

    Parameters:
        repository (repository object): repository object
        remote (remote object): remote object

    Returns:
        if the sync changes the repository, it will
        output a new repoversion href
    """

    #Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        #Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.RepositoriesRpmApi(api_client)

        try:
            #sync url object
            sync_url_object = pulpcore.client.pulp_rpm.RpmRepositorySyncURL(
                remote=remote.pulp_href,
                optimize=True,
                mirror=False
            )

            #sync task
            sync_task = api_instance.sync(
                rpm_rpm_repository_href = repository.pulp_href,
                rpm_repository_sync_url = sync_url_object
            )

            #wait for task to complete. if sync caused a change, it will create a repoversion_href
            wait_for_task_complete(task_href=sync_task.task)
            repoversion_href = get_task_created_resource(task_href=sync_task.task)

            #status message
            if repoversion_href:
                print(f"updates found when syncing {repository.name} to {remote.name}")
            else:
                print(f"no updates found when syncing {repository.name} to {remote.name}")

            #output
            return repoversion_href

        except ApiException as err:
            print("Exception when calling RepositoriesRpmApi->sync: %s\n" % err)
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
        if adding or remove a file changes the repository, it will
        output a new repoversion href
    """

    #Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        #Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.RepositoriesRpmApi(api_client)

        try:
            #check action values
            valid_action_values = ['add', 'remove']
            if action not in valid_action_values:
                raise ValueError(f"action {action} is not valid")

            #add
            if action == 'add':
                add_remove_content_object = pulpcore.client.pulp_rpm.RepositoryAddRemoveContent(
                    add_content_units = [content.pulp_href]
                )

            #remove
            else:
                add_remove_content_object = pulpcore.client.pulp_rpm.RepositoryAddRemoveContent(
                    remove_content_units = [content.pulp_href]
                )

            #task
            file_task = api_instance.modify(
                rpm_rpm_repository_href = repository.pulp_href,
                repository_add_remove_content = add_remove_content_object
            )

            #wait for task to complete
            wait_for_task_complete(task_href=file_task.task)
            repoversion_href = get_task_created_resource(task_href=file_task.task)

            #status message
            if repoversion_href:
                print(f"{repository.name} has been changed")
            else:
                print(f"{repository.name} has not changed")

            #output
            return repoversion_href

        except ApiException as err:
            print("Exception when calling RepositoriesRpmApi->modify: %s\n" % err)
            raise
