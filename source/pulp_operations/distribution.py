"""distribution functions"""

import logging
import pulpcore.client.pulp_rpm
from pulpcore.client.pulp_rpm.rest import ApiException
from pulp_operations.api_client_conf import rpm_configuration
from pulp_operations.task import wait_for_task_complete

# module logger - child of parent logger 'pulp_operations'
mlogger = logging.getLogger("pulp_operations.distribution")


def get_distribution_url(dist_name: str):
    """
    Summary:
        get distribution and log the associated url

    Parameters:
        dist_name (str): the name of the distribution

    Returns:
        None
    """

    distribution = get_distribution(dist_name)
    msg = f"{dist_name} url is {distribution.base_url}"
    mlogger.info(msg)


def get_distribution(dist_name: str):
    """
    Summary:
        gets an existing distribution by name

    Parameters:
        dist_name (str): the name of the distribution

    Returns:
        distribution response object
    """

    # Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        # Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.DistributionsRpmApi(api_client)

        try:
            distribution = api_instance.list(name=dist_name).results[0]
            msg = f"found {dist_name}"
            mlogger.info(msg)
            return distribution

        except ApiException as err:
            msg = f"Exception when calling DistributionsRpmApi->list: {err}"
            mlogger.error(msg)
            raise


def update_distribution(distribution, publication_href: str):
    """
    Summary:
        updates the properties of an existing distribution

    Parameters:
        distribution (distribution object): the distribution object
        publication_href (str): the href for the publication

    Returns:
        None
    """

    # Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        # Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.DistributionsRpmApi(api_client)

        try:
            # update distribution
            distribution_task = api_instance.update(
                rpm_rpm_distribution_href=distribution.pulp_href,
                rpm_rpm_distribution={
                    "name": distribution.name,
                    "publication": publication_href,
                    "base_path": distribution.name,  # was repository.name
                },
            )

            # wait for task to complete
            wait_for_task_complete(
                task_name="update distribution", task_href=distribution_task.task
            )

            # output
            msg = f"updated {distribution.name}"
            mlogger.info(msg)

            msg = f"{distribution.name} linked to publication {publication_href}"
            mlogger.debug(msg)

        except ApiException as err:
            msg = f"Exception when calling DistributionsRpmApi->update: {err}"
            mlogger.error(msg)
            raise


def create_distribution(dist_name: str, publication_href: str):
    """
    Summary:
        creates a distribution

    Parameters:
        dist_name (str): the name of the distribution
        publication_href (str): the href for the publication

    Returns:
        None
    """
    # Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        # Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.DistributionsRpmApi(api_client)

        try:
            # create distribution
            distribution_task = api_instance.create(
                rpm_rpm_distribution={
                    "name": dist_name,
                    "publication": publication_href,
                    "base_path": dist_name,  # was repository.name
                }
            )

            # wait for task to complete
            wait_for_task_complete(
                task_name="create distribution", task_href=distribution_task.task
            )

            # logging
            msg = f"created {dist_name}"
            mlogger.info(msg)

            msg = f"{dist_name} linked to publication {publication_href}"
            mlogger.debug(msg)

        except ApiException as err:
            msg = f"Exception when calling DistributionsRpmApi->create: {err}"
            mlogger.error(msg)
            raise


def list_distribution():
    """
    Summary:
        lists all distributions

    Parameters:
        none

    Returns:
        list of distributions
    """

    # Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        # Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.DistributionsRpmApi(api_client)

        try:
            output = api_instance.list()
            return output
        except ApiException as err:
            msg = f"Exception when calling DistributionsRpmApi->list: {err}"
            mlogger.error(msg)
            raise


def delete_distribution(distribution):
    """
    Summary:
        deletes an existing distribution

    Parameters:
        distribution: the distribution object

    Returns:
        None
    """

    # Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        # Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.DistributionsRpmApi(api_client)

        try:
            distribution_task = api_instance.delete(
                rpm_rpm_distribution_href=distribution.pulp_href
            )

            wait_for_task_complete(
                task_name="delete distribution", task_href=distribution_task.task
            )

            msg = f"deleted {distribution.name}"
            mlogger.info(msg)

        except ApiException as err:
            msg = f"Exception when calling DistributionsRpmApi->delete: {err}"
            mlogger.error(msg)
            raise
