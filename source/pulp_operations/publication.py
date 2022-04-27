"""publication functions"""

import logging
import pulpcore.client.pulp_rpm
from pulpcore.client.pulp_rpm.rest import ApiException
from pulp_operations.api_client_conf import rpm_configuration
from pulp_operations.task import wait_for_task_complete, get_task_created_resource

# module logger - child of parent logger 'pulp_operations'
mlogger = logging.getLogger("pulp_operations.publication")


def get_publication(repoversion_href: str):
    """
    Summary:
        gets a publication href for a repoversion_href

    Parameters:
        repoversion_href (str): repoversion href

    Returns:
        publication href
    """

    # enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        # Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.PublicationsRpmApi(api_client)

        try:
            # get publication associated with the repository version
            publication_href = (
                api_instance.list(repository_version=repoversion_href)
                .results[0]
                .pulp_href
            )

            # logging
            msg = f"found {publication_href}"
            mlogger.info(msg)

            # output
            return publication_href

        # if ApiException body matches 'not found' treat it like an IndexError
        except ApiException as err:
            if "not found" in err.body:
                raise IndexError(err) from err
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

    # Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        # Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.PublicationsRpmApi(api_client)

        try:
            # Create new publication. This links to latest repo version by default.
            publication_task = api_instance.create(
                rpm_rpm_publication={
                    "repository_version": repoversion_href,
                    # 'metadata_checksum_type': 'sha256', #sha256 is default
                    # 'package_checksum_type': 'sha256' #sha256 is default
                }
            )

            # wait for task to complete. output publication href
            wait_for_task_complete(
                task_name="create publication", task_href=publication_task.task
            )
            publication_href = get_task_created_resource(
                task_href=publication_task.task
            )

            # logging
            msg = f"created {publication_href}"
            mlogger.info(msg)

            # output
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

    # Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        # Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.PublicationsRpmApi(api_client)

        try:
            output = api_instance.list()
            return output
        except ApiException as err:
            msg = f"Exception when calling PublicationsRpmApi->list: {err}"
            mlogger.error(msg)
            raise
