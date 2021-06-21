"""
script to sync repos from repo_data.py
"""

import urllib3
import pulp_operations
from repo_data import repo_data

#disable ssl warnings for now
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#sync items from repo_data
for os in repo_data:
    for repo in repo_data[os]:
        for source_name, source_url in repo_data[os][repo].items():
            
            #try syncing
            repo_name = f"{os}-{repo}"
            remote_name = f"{os}-{repo}-{source_name}"
            remote_url = source_url
            pulp_operations.sync(repo_name, remote_name, remote_url)

            #if particular source fails, continue to next one
            except Exception:
                continue

#optional example for use with a configured signing service
# SIGNSERVICE_NAME = 'sign-metadata'
# for os in repo_data:
#     for repo in repo_data[os]:
#         for source_name, source_url in repo_data[os][repo].items():
            
#             #try syncing
#             repo_name = f"{os}-{repo}"
#             remote_name = f"{os}-{repo}-{source_name}"
#             remote_url = source_url
#             pulp_operations.sync(repo_name, remote_name, remote_url, SIGNSERVICE_NAME)
            
#             #if particular source fails, continue to next one
#             except Exception:
#                 continue
