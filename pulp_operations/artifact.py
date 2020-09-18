"""artifact functions"""

import pulpcore.client.pulpcore
from pulpcore.client.pulpcore.rest import ApiException
from pulp_operations.api_client_conf import core_configuration

def get_artifact(sha256hash: str):
    """
    Summary:
        searches for an existing artifact using rpm sha256 hash

    Parameters:
        sha256hash (str): the hash

    Returns:
        artifact response object
    """

    #Enter a context with an instance of the API client
    with pulpcore.client.pulpcore.ApiClient(core_configuration) as api_client:

        #Create an instance of the API class
        api_instance = pulpcore.client.pulpcore.ArtifactsApi(api_client)

        try:
            artifact = api_instance.list(sha256=sha256hash).results[0]
            print("artifact found")
            return artifact

        except ApiException as err:
            print("Exception when calling ArtifactsApi->list: %s\n" % err)
            raise

def create_artifact(rpm_file: str):
    """
    Summary:
        creates an artifact

    Parameters:
        rpm_file (str): the rpm file

    Returns:
        artifact response object
    """

    #Enter a context with an instance of the API client
    with pulpcore.client.pulpcore.ApiClient(core_configuration) as api_client:

        #Create an instance of the API class
        api_instance = pulpcore.client.pulpcore.ArtifactsApi(api_client)

        try:
            artifact = api_instance.create(file=rpm_file)
            print("artifact created")
            return artifact

        except ApiException as err:
            print("Exception when calling ArtifactsApi->create: %s\n" % err)
            raise
