"""
configuration settings for api client
"""

import os
from dotenv import load_dotenv
import pulpcore.client.pulpcore
import pulpcore.client.pulp_rpm

#load in environment data
load_dotenv()
server = os.getenv('PULP_SERVER')
username = os.getenv('PULP_USER')
password = os.getenv('PULP_PASS')

#CORE - set config settings and instantiate pulp core api client
core_configuration = pulpcore.client.pulpcore.Configuration(
    host = f"https://{server}",
    username = username,
    password = password,
)
core_configuration.verify_ssl=False

#RPM - set config settings and instantiate pulp rpm api client
rpm_configuration = pulpcore.client.pulp_rpm.Configuration(
    host = f"https://{server}",
    username = username,
    password = password,
)
rpm_configuration.verify_ssl=False
