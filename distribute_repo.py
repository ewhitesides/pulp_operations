"""
script to distribute repos from repo_data.py
"""

import urllib3
import pulp_operations
from repo_data import repo_data

# disable ssl warnings for now
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# release latest version of the repo to distribution 'latest'
for os in repo_data:
    for repo in repo_data[os]:
        repo_name = f"signed-{os}-{repo}"
        dist_name = f"{repo_name}-latest"
        pulp_operations.release(repo_name, 0, dist_name)

# output distribution url info (optional)
for os in repo_data:
    for repo in repo_data[os]:
        repo_name = f"signed-{os}-{repo}"
        dist_name = f"{repo_name}-latest"
        pulp_operations.distribution.get_distribution_url(dist_name)
