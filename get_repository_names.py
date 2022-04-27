"""
Summary:
    get sorted list of repository names

Example:
    python3 get_repository_names.py
"""

import operator
import urllib3
from dotenv import load_dotenv
import pulp_operations

#disable ssl
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#load in environment data
load_dotenv()

#sort by name
sorted_results=sorted(
    pulp_operations.repository.list_repo().results,
    key=operator.attrgetter('name')
)

#output
for result in sorted_results:
    print(result.name)
