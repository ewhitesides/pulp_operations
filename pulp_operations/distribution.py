"""distribution functions"""

import pulpcore.client.pulp_rpm
from pulpcore.client.pulp_rpm.rest import ApiException
from pulp_operations.api_client_conf import rpm_configuration
from pulp_operations.task import wait_for_task_complete

def get_distribution_info(dist_name: str):
    """
    Summary:
        prints some basic info about the distribution

    Parameters:
        dist_name (str): the name of the distribution

    Returns:
        None
    """

    distribution = get_distribution(dist_name=dist_name)
    dist_url = distribution.base_url
    print(f"repository: client file is {dist_url}config.repo")

def get_distribution(dist_name: str):
    """
    Summary:
        gets an existing distribution by name

    Parameters:
        dist_name (str): the name of the distribution

    Returns:
        distribution response object
    """

    #Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        #Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.DistributionsRpmApi(api_client)

        try:
            distribution = api_instance.list(name=dist_name).results[0]
            print(f"distribution: found {dist_name}")
            return distribution

        except ApiException as err:
            print("Exception when calling DistributionsRpmApi->list: %s\n" % err)
            raise

def update_distribution(distribution, repository, publication_href: str):
    """
    Summary:
        updates the properties of an existing distribution

    Parameters:
        distribution (distribution object): the distribution object
        repository (repository object): the repository object
        publication_href (str): the href for the publication

    Returns:
        None
    """

    #Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        #Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.DistributionsRpmApi(api_client)

        try:
            #update distribution
            distribution_task = api_instance.update(
                rpm_rpm_distribution_href=distribution.pulp_href,
                rpm_rpm_distribution={
                    'name': distribution.name,
                    'publication': publication_href,
                    'base_path': repository.name
                }
            )

            #wait for task to complete
            wait_for_task_complete(task_href=distribution_task.task)

            #status message
            print(f"distribution {distribution.name} updated")

        except ApiException as err:
            print("Exception when calling DistributionsRpmApi->update: %s\n" % err)
            raise

def create_distribution(dist_name: str, repository, publication_href: str):
    """
    Summary:
        creates a distribution

    Parameters:
        dist_name (str): the name of the distribution
        repository (repository object): the repository object
        publication_href (str): the href for the publication

    Returns:
        None
    """
    #Enter a context with an instance of the API client
    with pulpcore.client.pulp_rpm.ApiClient(rpm_configuration) as api_client:

        #Create an instance of the API class
        api_instance = pulpcore.client.pulp_rpm.DistributionsRpmApi(api_client)

        try:
            #create distribution
            distribution_task = api_instance.create(
                rpm_rpm_distribution={
                    'name': dist_name,
                    'publication': publication_href,
                    'base_path': repository.name
                }
            )

            #wait for task to complete
            wait_for_task_complete(task_href=distribution_task.task)

            #status message
            print(f"distribution {dist_name} created")

        except ApiException as err:
            print("Exception when calling DistributionsRpmApi->create: %s\n" % err)
            raise
