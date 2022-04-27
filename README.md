# README

## development setup

### setup with vscode devcontainer

```bash
#prerequisites
#ensure you have vscode and docker desktop installed on your machine
#in vscode, Ctrl-Shift-P and type "install devcontainer cli"

#clone/pull repo
git clone <url>

#add the following to .env at base of code folder
PULP_USER=<user>
PULP_PASS=<password>
PULP_SERVER=<server>
PULP_LOGPATH=/var/log/pulp_operations.log # or whatever path you'd like

#open directly into vscode as devcontainer
cd <code_folder>
devcontainer open .
```

### setup with local virtual environment
```bash
#clone/pull repo
git clone <url>

#setup the virtual environment
pip3 install virtualenv
cd pulp_operations
virtualenv .venv
.venv/bin/pip install .

#add the following to pulp_operations/.env
PULP_USER=<user>
PULP_PASS=<password>
PULP_SERVER=<server>
PULP_LOGPATH=/var/log/pulp_operations.log # or whatever path you'd like

#activate virtual environment with below command
source .venv/bin/activate
```

## Example of syncing/distributing a repo

### sync_repo.py

runs all the necessary steps to sync repositories using data from repo_data.py

### distribute_repo.py

runs all the necessary steps to distribute latest version of repositories using data from repo_data.py

### example cron to schedule sync_repo.py, distribute_repo.py

```bash
#sync repos daily at 3:30am
30 3 * * * /path/to/venv/bin/python /path/to/pulp_operations_code/sync_repo.py

#distribute repos biweekly sunday at 4:30am
30 4 * * 7 /path/to/venv/bin/python /path/to/pulp_operations/distribute_repo.py
```

## Additional scripts

the base path contains numerous scripts for basic operations

## Example of rolling back to the previous version of a repository

```python
import urllib3
import pulp_operations

#disable ssl
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

pulp_operations.release(
    repo_name='my_pulp_repository',
    version_rollback=1,
    dist_name='my_pulp_distribution'
)
```

## Other examples

```python
import urllib3
import pulp_operations

#disable ssl
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#general repository operations
pulp_operations.list_repository_names() #list all repository names
pulp_operations.repository.list_repo() #list all properties of all repositories
pulp_operations.remove_repository('test-repo')

#general remote operations
pulp_operations.remote.list_remote()
pulp_operations.remove_remote('test-remote')

#general publication operations
pulp_operations.publication.list_publication()

#general distribution operations
pulp_operations.list_distribution_names() #list all distribution names
pulp_operations.distribution.list_distribution() #list all properties of all distributions
pulp_operations.distribution.get_distribution_url('test-dist')
pulp_operations.remove_distribution('test-dist')
```

## finding repositories to sync from

### standard repos

find repos by going to mirrorlist.centos.org and filling in params
example: <http://mirrorlist.centos.org/?release=8&arch=x86_64&repo=AppStream>
note the structure of the url - some sites include a 'pub' or 'linux' directory
that prefixes the standardized format

### epel repos

for searching for epel, use the following, and view the contents of the downloaded metalink file
example: <https://mirrors.fedoraproject.org/metalink?repo=epel-modular-8&arch=x86_64>
example: <https://mirrors.fedoraproject.org/metalink?repo=epel-8&arch=x86_64&>

## reference links

<https://pulpcore-client.readthedocs.io/en/latest/>

<https://pulp-rpm.readthedocs.io/en/latest/>

<https://timber.io/blog/the-pythonic-guide-to-logging/>

<https://docs.python.org/3/howto/logging-cookbook.html#logging-cookbook>

<https://pulp-rpm.readthedocs.io/en/latest/workflows/metadata_signing.html>
