"""remote functions"""

import pulpcore.client.pulp_rpm
from pulpcore.client.pulp_rpm.rest import ApiException
from pulp_operations.api_client_conf import rpm_configuration

def get_remote(remote_name: str):
    """
    Summary:
        searches for existing remote by name

    Parameters:
        remote_name (str): the remote name

    Returns:
        remote response object
    """

    #Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        #Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.RemotesRpmApi(api_client)

        try:
            remote = api_instance.list(name=remote_name).results[0]
            print(f"remote: found {remote_name}")
            return remote

        except ApiException as err:
            print("Exception when calling RemotesRpmApi->list: %s\n" % err)
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
    #Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        #Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.RemotesRpmApi(api_client)

        try:
            remote = api_instance.create(
                rpm_rpm_remote = {
                    'name': remote_name,
                    'url': remote_url,
                    'policy': 'on_demand'
                }
            )
            print(f"remote: created {remote_name}")
            return remote

        except ApiException as err:
            print("Exception when calling RemotesRpmApi->create: %s\n" % err)
            raise
