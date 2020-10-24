"""content functions"""

import logging
import pulpcore.client.pulp_rpm
from pulpcore.client.pulp_rpm.rest import ApiException
from pulp_operations.api_client_conf import rpm_configuration
from pulp_operations.task import wait_for_task_complete

#module logger - child of parent logger 'pulp_operations'
mlogger = logging.getLogger('pulp_operations.content')

def get_content_by_properties(rpm_properties, repository):
    """
    Summary:
        searches for content in existing repository

    Parameters:
        rpm_properties (dictionary): dictionary of properties
        repository (repository object): the repository object

    Returns:
        content response object
    """

    #Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        #Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.ContentPackagesApi(api_client)

        try:
            content_search = api_instance.list(
                arch = rpm_properties['arch'],
                release = rpm_properties['release'],
                version = rpm_properties['version'],
                name = rpm_properties['name'],
                repository_version = repository.latest_version_href
            )
            content = content_search.results[0]

            msg = "found by properties"
            mlogger.info(msg)

            return content

        except ApiException as err:
            msg = f"Exception when calling ContentPackagesApi->list: {err}"
            mlogger.error(msg)
            raise

def get_content_by_hash(sha256hash: str):
    """
    Summary:
        searches for content using rpm sha256 hash

    Parameters:
        sha256hash (str): the hash
    Returns:
        content response object
    """

    #Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        #Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.ContentPackagesApi(api_client)

        try:
            content = api_instance.list(sha256=sha256hash).results[0]

            msg = "found by hash"
            mlogger.info(msg)

            return content

        except ApiException as err:
            msg = f"Exception when calling ContentPackagesApi->list: {err}"
            mlogger.error(msg)
            raise

def create_content(artifact, rpm_file):
    """
    Summary:
        creates content using artifact and rpm_file

    Parameters:
        artifact (artifact object): artifact object
        rpm_file (str): the rpm file

    Returns:
        None
    """

    #Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        #Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.ContentPackagesApi(api_client)

        try:
            content_task = api_instance.create(
                artifact = artifact.pulp_href,
                relative_path=rpm_file
            )

            #wait for task to complete
            wait_for_task_complete(
                task_name='create content',
                task_href=content_task.task
            )

            #logging
            msg = "created"
            mlogger.info(msg)

        except ApiException as err:
            msg = f"Exception when calling ContentPackagesApi->create: {err}"
            mlogger.error(msg)
            raise
