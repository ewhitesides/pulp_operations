"""publication functions"""

import pulpcore.client.pulp_rpm
from pulpcore.client.pulp_rpm.rest import ApiException
from pulp_operations.api_client_conf import rpm_configuration
from pulp_operations.task import wait_for_task_complete, get_task_created_resource

def create_publication(repository):
    """
    Summary:
        creates a new publication

    Parameters:
        repository (repository object): the repository object

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
                    'repository': repository.pulp_href,
                    #'metadata_checksum_type': 'sha256', #sha256 is default
                    #'package_checksum_type': 'sha256' #sha256 is default
                }
            )

            #wait for task to complete. output publication href
            wait_for_task_complete(task_href=publication_task.task)
            publication_href = get_task_created_resource(task_href=publication_task.task)

            #status message
            print("new publication created")

            #output
            return publication_href

        except ApiException as err:
            print("Exception when calling PublicationsRpmApi->create: %s\n" % err)
            raise
