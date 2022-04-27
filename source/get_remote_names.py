"""
Summary:
    get sorted list of remote names

Example:
    python3 get_remote_names.py
"""

import operator
import urllib3
import pulp_operations

# disable ssl
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# sort by name
sorted_results = sorted(
    pulp_operations.remote.list_remote().results,
    key=operator.attrgetter('name')
)

# output
for result in sorted_results:
    print(result.name)
