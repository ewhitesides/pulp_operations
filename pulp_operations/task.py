"""task functions"""

import time
from timeit import default_timer as timer
import pulpcore.client.pulpcore
from pulpcore.client.pulpcore.rest import ApiException
from pulp_operations.api_client_conf import core_configuration

def get_task_created_resource (task_href: str):
    """
    Summary:
        get the created resource from the completed task

    Parameters:
        task_href (str): the href for the task

    Returns:
        if the task created a change, it will output a created resource href
    """

    #Enter a context with an instance of the API client
    with pulpcore.client.pulpcore.ApiClient(core_configuration) as api_client:

        #Create an instance of the API class
        api_instance = pulpcore.client.pulpcore.TasksApi(api_client)

        try:
            #get created resources
            created_resources = api_instance.read(task_href).created_resources

            #return the href from created_resources, if it exists
            if created_resources:
                return created_resources[0]

            #else return None
            return None

        except ApiException as err:
            print("Exception when calling TasksApi->read: %s\n" % err)
            raise

def wait_for_task_complete (task_href: str):
    """
    Summary:
        polls a task state and returns when the task is complete

    Parameters:
        task_href (str): the href for the task

    Returns:
        None
    """

    #Enter a context with an instance of the API client
    with pulpcore.client.pulpcore.ApiClient(core_configuration) as api_client:

        #Create an instance of the API class
        api_instance = pulpcore.client.pulpcore.TasksApi(api_client)

        #start time
        start = timer()

        #poll task until it is finished
        while True:

            try:
                #get state
                state = api_instance.read(task_href).state

                #state is completed
                if state in ['completed']:
                    return

                #state is failed/canceled
                if state in ['failed', 'canceled']:
                    class TaskStateException(Exception):
                        """custom exception to raise when task is failed/canceled"""
                    raise TaskStateException(f"task {task_href} is {state}")

                #state is something else
                end = timer()
                elapsed_seconds = int(end - start)
                print(f"waiting for task to complete. elapsed seconds: {elapsed_seconds}")
                time.sleep(5)

            except ApiException as err:
                print("Exception when calling TasksApi->read: %s\n" % err)
                raise
