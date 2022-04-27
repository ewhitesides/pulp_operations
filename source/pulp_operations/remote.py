"""remote functions"""

import logging
import pulpcore.client.pulp_rpm
from pulpcore.client.pulp_rpm.rest import ApiException
from pulp_operations.api_client_conf import rpm_configuration
from pulp_operations.task import wait_for_task_complete

# module logger - child of parent logger 'pulp_operations'
mlogger = logging.getLogger("pulp_operations.remote")


def get_remote(remote_name: str):
    """
    Summary:
        searches for existing remote by name

    Parameters:
        remote_name (str): the remote name

    Returns:
        remote response object
    """

    # Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        # Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.RemotesRpmApi(api_client)

        try:
            remote = api_instance.list(name=remote_name).results[0]
            msg = f"found {remote_name}"
            mlogger.info(msg)
            return remote

        except ApiException as err:
            msg = f"Exception when calling RemotesRpmApi->list: {err}"
            mlogger.error(msg)
            raise


def create_remote(remote_name: str, remote_url: str):
    """
    Summary:
        creates a remote

    Parameters:
        remote_name (str): the remote name
        remote_url (str): the remote url

    Returns:
        remote response object
    """
    # Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        # Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.RemotesRpmApi(api_client)

        try:
            remote = api_instance.create(
                rpm_rpm_remote={
                    "name": remote_name,
                    "url": remote_url,
                    "policy": "on_demand",
                }
            )

            msg = f"created {remote_name}"
            mlogger.info(msg)

            return remote

        except ApiException as err:
            msg = f"Exception when calling RemotesRpmApi->create: {err}"
            mlogger.error(msg)
            raise


def list_remote():
    """
    Summary:
        lists all remotes

    Parameters:
        none

    Returns:
        list of remotes
    """

    # Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        # Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.RemotesRpmApi(api_client)

        try:
            output = api_instance.list()
            return output
        except ApiException as err:
            msg = f"Exception when calling RemotesRpmApi->list: {err}"
            mlogger.error(msg)
            raise


def delete_remote(remote):
    """
    Summary:
        deletes an existing remote

    Parameters:
        remote: the remote object

    Returns:
        None
    """

    # Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        # Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.RemotesRpmApi(api_client)

        try:
            remote_task = api_instance.delete(rpm_rpm_remote_href=remote.pulp_href)

            wait_for_task_complete(
                task_name="delete remote", task_href=remote_task.task
            )

            msg = f"deleted {remote.name}"
            mlogger.info(msg)

        except ApiException as err:
            msg = f"Exception when calling RemotesRpmApi->delete: {err}"
            mlogger.error(msg)
            raise
