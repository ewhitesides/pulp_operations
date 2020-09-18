"""signing functions"""

import pulpcore.client.pulpcore
from pulpcore.client.pulpcore.rest import ApiException
from pulp_operations.api_client_conf import core_configuration

def get_signservice(signservice_name: str):
    """
    Summary:
        searches for an existing signing service by name

    Parameters:
        signservice_name (str): the signing service name

    Returns:
        signing service response object
    """

    #Enter a context with an instance of the API client
    with pulpcore.client.pulpcore.ApiClient(core_configuration) as api_client:

        #Create an instance of the API class
        api_instance = pulpcore.client.pulpcore.SigningServicesApi(api_client)

        try:
            sign_service = api_instance.list(name=signservice_name).results[0]
            print(f"sign service: found {signservice_name}")
            return sign_service

        except ApiException as err:
            print("Exception when calling SigningServicesApi->list: %s\n" % err)
            raise
