"""publication functions"""

import logging
import pathlib
import pulpcore.client.pulp_rpm
from pulpcore.client.pulp_rpm.rest import ApiException
from pulp_operations.api_client_conf import rpm_configuration
from pulp_operations.task import wait_for_task_complete, get_task_created_resource

#module logger - child of parent logger 'pulp_operations'
mlogger = logging.getLogger('pulp_operations.publication')

def get_publication(repoversion_href, rollback: int = 0):
    """
    Summary:
        gets a publication href for a repo version minus rollback.

        for example if a repo is at version 7, and rollback is 1, it will
        return the publication associated with version 6.

        if repo version minus rollback equates to <=0, it will return version 1.

    Parameters:
        repoversion_href (str): repoversion href

        rollback (int): number of versions to rollback from current version of repository

    Returns:
        publication href
    """

    #use pathlib to split out latest version of the repo from the href
    pathed_repoversion_href = pathlib.Path(repoversion_href)
    version_index = int(pathed_repoversion_href.parts.index('versions')) + 1
    repo_latest_version = pathed_repoversion_href.parts[version_index]

    #selected version of repository is latest version minus rollback.
    #publications can't be linked to anything less than 1.
    repo_selected_version = int(repo_latest_version) - rollback
    if repo_selected_version <= 0:
        repo_selected_version = 1

    #build url with selected version
    repo_selected_version_href = repoversion_href.replace(
        f'/versions/{repo_latest_version}/',
        f'/versions/{repo_selected_version}/'
    )

    #enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        #Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.PublicationsRpmApi(api_client)

        try:
            #get publication associated with the repository version
            publication_href = api_instance.list(
                repository_version = repo_selected_version_href
            ).results[0].pulp_href

            #logging
            msg = f"found {publication_href}"
            mlogger.info(msg)

            msg = f"publication {publication_href} links repoversion {repo_selected_version_href}"
            mlogger.debug(msg)

            #output
            return publication_href

        except ApiException as err:
            msg = f"Exception when calling PublicationsRpmApi->list: {err}"
            mlogger.error(msg)
            raise

def create_publication(repoversion_href: str):
    """
    Summary:
        creates a new publication

    Parameters:
        repoversion_href (str): repoversion href

    Returns:
        the publication href
    """

    #Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        #Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.PublicationsRpmApi(api_client)

        try:
            #Create new publication. This links to latest repo version by default.
            publication_task = api_instance.create(
                rpm_rpm_publication = {
                    'repository_version': repoversion_href,
                    #'metadata_checksum_type': 'sha256', #sha256 is default
                    #'package_checksum_type': 'sha256' #sha256 is default
                }
            )

            #wait for task to complete. output publication href
            wait_for_task_complete(
                task_name='create publication',
                task_href=publication_task.task
            )
            publication_href = get_task_created_resource(task_href=publication_task.task)

            #logging
            msg = f"created {publication_href}"
            mlogger.info(msg)

            msg = f"publication {publication_href} links repoversion {repoversion_href}"
            mlogger.debug(msg)

            #output
            return publication_href

        except ApiException as err:
            msg = f"Exception when calling PublicationsRpmApi->create: {err}"
            mlogger.error(msg)
            raise

def list_publication():
    """
    Summary:
        lists all publications

    Parameters:
        none

    Returns:
        list of publications
    """

    #Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        #Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.PublicationsRpmApi(api_client)

        try:
            output = api_instance.list()
            return output
        except ApiException as err:
            msg = f"Exception when calling PublicationsRpmApi->list: {err}"
            mlogger.error(msg)
            raise
