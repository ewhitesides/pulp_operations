# overview

this is a general demo of how to use the pulp 3 python client packages to build workflows.

it includes working examples of syncing a remote to a repository, and adding/removing rpms.

## example usage

```python
import urllib3
import pulp_operations

#disable ssl warnings for now
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#example of syncing to repository
pulp_operations.start_sync(
    repo_name='test-repo',
    remote_name='test-remote',
    remote_url='https://mirror.cs.uwp.edu/pub/centos/8/PowerTools/x86_64/os/',
    dist_name='test-dist'
)

#example of adding a rpm to a repository
pulp_operations.add_rpm(
    rpm_file='snake-server-0.11-0.20.el6.noarch.rpm',
    repo_name='test-repo',
    dist_name='test-dist'
)

#example of removing a rpm from a repository
pulp_operations.remove_rpm(
    rpm_file='snake-server-0.11-0.20.el6.noarch.rpm',
    repo_name='test-repo',
    dist_name='test-dist'
)

#example of syncing multiple remotes to one repository
pulp_operations.start_sync(
    repo_name='repo_centos8',
    remote_name='remote_centos8_base',
    remote_url='https://mirror.cs.uwp.edu/pub/centos/8/BaseOS/x86_64/os/',
    dist_name='dist_centos8'
)

pulp_operations.start_sync(
    repo_name='repo_centos8',
    remote_name='remote_centos8_powertools',
    remote_url='https://mirror.cs.uwp.edu/pub/centos/8/PowerTools/x86_64/os/',
    dist_name='dist_centos8'
)

#example of syncing/adding to a repository with signed repodata
pulp_operations.start_sync(
    repo_name='signtest-repo',
    remote_name='signtest-remote',
    remote_url='https://mirror.cs.uwp.edu/pub/centos/8/PowerTools/x86_64/os/',
    dist_name='signtest-dist',
    signservice_name='sign-metadata'
)

pulp_operations.add_rpm(
    rpm_file='snake-server-0.11-0.20.el6.noarch.rpm',
    repo_name='signtest-repo',
    dist_name='signtest-dist',
    signservice_name='sign-metadata'
)
```

## option 1 for development: python virtual environment

```bash
cd ~
git clone repository
pip3 install virtualenv
#vi .profile and add '$HOME/.local/bin' to PATH
. .profile
cd pulp_operations
virtualenv venv
source venv/bin/activate
pip install .

#install direnv, add .envrc with the following
export PULP_USER=admin
export PULP_PASS=<password from install.yml>
export PULP_SERVER=<server from install.yml>
```

## option 2 for development: container-based environment

```bash
#the following assumes your machine has docker desktop and vscode installed
cd ~
git clone repository
cd pulp_operations/.devcontainer

#add the following to devcontainer.env
PULP_USER=admin
PULP_PASS=<password from install.yml>
PULP_SERVER=<server from install.yml>

#launch in vscode as a container
#press F5 to run 'run.py' script
#go into code and press F9 to create a breakpoint
```
