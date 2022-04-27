"""task functions"""

import time
from timeit import default_timer as timer
import logging
import pulpcore.client.pulpcore
from pulpcore.client.pulpcore.rest import ApiException
from pulp_operations.api_client_conf import core_configuration

# module logger - child of parent logger 'pulp_operations'
mlogger = logging.getLogger("pulp_operations.task")


def get_task_created_resource(task_href: str):
    """
    Summary:
        get the created resource from the completed task

    Parameters:
        task_href (str): the href for the task

    Returns:
        if the task created a change, it will output a created resource href
    """

    # Enter a context with an instance of the API client
    with pulpcore.client.pulpcore.ApiClient(core_configuration) as api_client:

        # Create an instance of the API class
        api_instance = pulpcore.client.pulpcore.TasksApi(api_client)

        try:
            # get created resources
            created_resources = api_instance.read(task_href).created_resources

            # return the href from created_resources, if it exists
            if created_resources:
                return created_resources[0]

            # else return None
            return None

        except ApiException as err:
            msg = f"Exception when calling TasksApi->read: {err}"
            mlogger.error(msg)
            raise


def wait_for_task_complete(task_name: str, task_href: str):
    """
    Summary:
        polls a task state and returns when the task is complete

    Parameters:
        task_name (str): the name of the task
        task_href (str): the href for the task

    Returns:
        None
    """

    # logging
    msg = f"waiting for '{task_name}' to complete"
    mlogger.info(msg)

    # Enter a context with an instance of the API client
    with pulpcore.client.pulpcore.ApiClient(core_configuration) as api_client:

        # Create an instance of the API class
        api_instance = pulpcore.client.pulpcore.TasksApi(api_client)

        # limit time in case we ever encounter a situation where task hangs indefinitely
        start = timer()
        elapsed_wait = 0
        max_wait = 3600  # 60 minutes

        # poll task until it is finished
        while elapsed_wait < max_wait:

            try:
                # get state
                state = api_instance.read(task_href).state

                # mark elapsed time
                end = timer()
                elapsed_wait = int(end - start)

                # state is completed
                if state in ["completed"]:
                    msg = f"{task_name} {state} in {elapsed_wait} seconds"
                    mlogger.info(msg)
                    return

                # state is failed/canceled
                if state in ["failed", "canceled"]:

                    class TaskStateException(Exception):
                        """custom exception"""

                    msg = f"{task_name} {state} in {elapsed_wait} seconds"
                    mlogger.error(msg)
                    raise TaskStateException(msg)

                # state is not completed/failed/canceled
                time.sleep(5)

            except ApiException as err:
                msg = f"Exception when calling TasksApi->read: {err}"
                mlogger.error(msg)
                raise
