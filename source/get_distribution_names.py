"""
Summary:
    get sorted list of distribution names

Example:
    python3 get_distribution_names.py
"""

import operator
import urllib3
import pulp_operations

# disable ssl
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# sort by name
sorted_results = sorted(
    pulp_operations.distribution.list_distribution().results,
    key=operator.attrgetter('name')
)

# output
for result in sorted_results:
    print(result.name)
