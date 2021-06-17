# README

## install in a virtual environment

```bash
#clone/pull repo
git clone git@github.com:ewhitesides/pulp_operations.git

#setup the virtual environment
pip3 install virtualenv
cd pulp_operations
virtualenv .venv
.venv/bin/pip install .

#add the following to pulp_operations/.env
PULP_USER=<user>
PULP_PASS=<password>
PULP_SERVER=<server>

#activate virtual environment with below command
source .venv/bin/activate
```

## production use notes

- use a virtual environment
- the file sync_repo.py runs all the necessary steps to sync repositories using data from repo_data.py
- the file distribute_repo.py runs all the necessary steps to distribute repositories using data from repo_data.py

```bash
#example one-off run
/root/pulp_operations_venv/bin/python /root/pulp_operations_code/sync_repo.py

#example cron entry to sync repos daily at 3:30am
30 3 * * * /root/pulp_operations_venv/bin/python /root/pulp_operations_code/sync_repo.py

#example cron entry to distribute repos biweekly sunday at 4:30am
30 4 * * 7 /root/pulp_operations_venv/bin/python /root/pulp_operations_code/distribute_repo.py
```

## debug/test

- edit debug_run.py script in root of pulp_operations
- press F9 to mark breakpoint in code
- press F5 to execute debug_run.py

## examples

### sync an external repository

```python
import urllib3
import pulp_operations

#disable ssl
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#sync

#if the repository or the remote specified does not exist, it is created as part
#of the sync operation. subsequent executions will just perform a sync.

#multiple remotes can be synced to one local repository by repeating the command with
#a different remote_name and remote_url.

#multiple remotes of the same content could be used as backup in case one fails.

#if the signservce_name parameter is not specified, the repository will be created without
#a signing service.

pulp_operations.sync(
    repo_name='my_pulp_repository',
    remote_name='centos8-powertools-uwp',
    remote_url='https://mirror.cs.uwp.edu/pub/centos/8/PowerTools/x86_64/os/',
    signservice_name='sign-metadata'
)

#release updated version of the repository to the distribution
pulp_operations.release(
    repo_name='my_pulp_repository',
    version_rollback=0,
    dist_name='latest'
)
```

### add a rpm to a repository

```bash
#copy rpm files to same folder level as add_rpms.py, 
#then run add_rpms.py
python add_rpms.py --repo_name signed-r8-myrepo
```

### remove a rpm from a repository

```python
import urllib3
import pulp_operations

#disable ssl
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#remove rpm from repository
pulp_operations.remove_rpm(
    rpm_file='snake-server-0.11-0.20.el6.noarch.rpm',
    repo_name='test-repo'
)

#release updated version of the repository to the distribution
pulp_operations.release(
    repo_name='my_pulp_repository',
    version_rollback=0,
    dist_name='latest'
)
```

### rolling back to the previous version of a repository

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

### example of processing several repositories using a dictionary data structure

```python
import urllib3
import pulp_operations

#disable ssl
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

repo_data = {
    'c7': {
        'os': {
            'umd': 'https://mirror.umd.edu/centos/7/os/x86_64',
            'uwp': 'https://mirror.cs.uwp.edu/pub/centos/7/os/x86_64'
        },
        'updates': {
            'umd': 'https://mirror.umd.edu/centos/7/updates/x86_64',
            'uwp': 'https://mirror.cs.uwp.edu/pub/centos/7/updates/x86_64'
        },
        'extras': {
            'umd': 'https://mirror.umd.edu/centos/7/extras/x86_64',
            'uwp': 'https://mirror.cs.uwp.edu/pub/centos/7/extras/x86_64'
        },
        'epel': {
            'umd': 'https://mirror.umd.edu/fedora/epel/7/x86_64/'
        },
        'salt_latest': {
            'salt': 'https://repo.saltstack.com/py3/redhat/7/x86_64/latest/'
        }
    },
    'c8': {
        'appstream': {
            'umd': 'https://mirror.umd.edu/centos/8/AppStream/x86_64/os/',
            'uwp': 'https://mirror.cs.uwp.edu/pub/centos/8/AppStream/x86_64/os/',
            'ncsu': 'https://packages.oit.ncsu.edu/centos/8/AppStream/x86_64/os/'
        },
        'baseos': {
            'umd': 'https://mirror.umd.edu/centos/8/BaseOS/x86_64/os/',
            'uwp': 'https://mirror.cs.uwp.edu/pub/centos/8/BaseOS/x86_64/os/'
        },
        'extras': {
            'umd': 'https://mirror.umd.edu/centos/8/extras/x86_64/os/',
            'uwp': 'https://mirror.cs.uwp.edu/pub/centos/8/extras/x86_64/os/'
        },
        'powertools': {
            'umd': 'https://mirror.umd.edu/centos/8/PowerTools/x86_64/os/',
            'uwp': 'https://mirror.cs.uwp.edu/pub/centos/8/PowerTools/x86_64/os/'
        },
        'epel_everything': {
            'umd': 'https://mirror.umd.edu/fedora/epel/8/Everything/x86_64/'
        },
        'salt_latest': {
            'salt': 'https://repo.saltstack.com/py3/redhat/8/x86_64/latest/'
        }
    }
}

#sync items from repo_data
SIGNSERVICE_NAME = 'sign-metadata'
for os in repo_data:
    for repo in repo_data[os]:
        for source_name, source_url in repo_data[os][repo].items():
            repo_name = f"signed-{os}-{repo}"
            remote_name = f"{os}-{repo}-{source_name}"
            remote_url = source_url
            pulp_operations.sync(repo_name, remote_name, remote_url, SIGNSERVICE_NAME)

#release latest version of the repo to distribution 'latest'
for os in repo_data:
    for repo in repo_data[os]:
        repo_name = f"signed-{os}-{repo}"
        dist_name = f"{repo_name}-latest"
        pulp_operations.release(repo_name, 0, dist_name)

#output distribution url info (optional)
for os in repo_data:
    for repo in repo_data[os]:
        repo_name = f"signed-{os}-{repo}"
        dist_name = f"{repo_name}-latest"
        pulp_operations.distribution.get_distribution_url(dist_name)
```

### other management commands

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
