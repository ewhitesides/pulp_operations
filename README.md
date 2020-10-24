# reference info

## example commands

```python
import pulp_operations

#optionally disable ssl warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#syncing to repository
#'start_sync' creates a '{repo_name}-dev_dist' and a '{repo_name}-prod_dist' distribution
#dev_dist reflects the latest version of the repository
#prod_dist reflects the previous version of the repository
#this allows test/dev servers to receive the latest updates first for testing
pulp_operations.start_sync(
    repo_name='test-repo',
    remote_name='test-remote',
    remote_url='https://mirror.cs.uwp.edu/pub/centos/8/PowerTools/x86_64/os/',
)

#adding a rpm to a repository
pulp_operations.add_rpm(
    rpm_file='snake-0.11-0.20.el6.noarch.rpm',
    repo_name='test-repo',
    dist_name='test-dist'
)

#removing a rpm from a repository
pulp_operations.remove_rpm(
    rpm_file='snake-server-0.11-0.20.el6.noarch.rpm',
    repo_name='test-repo',
    dist_name='test-dist'
)

#syncing multiple remotes to one repository
#useful for either merging multiple remotes into one single repository
#or you can use multiple of the same remote as backup if one fails
pulp_operations.start_sync(
    repo_name='repo_centos8',
    remote_name='remote_centos8_base',
    remote_url='https://mirror.cs.uwp.edu/pub/centos/8/BaseOS/x86_64/os/',
)

pulp_operations.start_sync(
    repo_name='repo_centos8',
    remote_name='remote_centos8_powertools',
    remote_url='https://mirror.cs.uwp.edu/pub/centos/8/PowerTools/x86_64/os/',
)

#syncing/adding to a repository with signed repodata
#signing service requires preparation on server before use
pulp_operations.start_sync(
    repo_name='signtest-repo',
    remote_name='signtest-remote',
    remote_url='https://mirror.cs.uwp.edu/pub/centos/8/PowerTools/x86_64/os/',
    signservice_name='sign-metadata'
)

#adding to a repository with signed repodata
pulp_operations.add_rpm(
    rpm_file='snake-server-0.11-0.20.el6.noarch.rpm',
    repo_name='signtest-repo',
    dist_name='signtest-dist',
    signservice_name='sign-metadata'
)

#adding all rpms that match pattern in directory to a repository
import pathlib
for rpm_file in pathlib.Path('.').glob('*.rpm'):
    pulp_operations.add_rpm(
        rpm_file=str(rpm_file),
        repo_name='signtest-repo',
        dist_name='signetest-dist',
        signservice_name='sign-metadata'
    )

#examples of processing entire groups of repositories using a dictionary data structure

#CentOS 7
config_centos_7 = {
    'c7_os': {
        'umd': 'https://mirror.umd.edu/centos/7/os/x86_64',
        'uwp': 'https://mirror.cs.uwp.edu/pub/centos/7/os/x86_64'
    },
    'c7_updates': {
        'umd': 'https://mirror.umd.edu/centos/7/updates/x86_64',
        'uwp': 'https://mirror.cs.uwp.edu/pub/centos/7/updates/x86_64'
    },
    'c7_extras': {
        'umd': 'https://mirror.umd.edu/centos/7/extras/x86_64',
        'uwp': 'https://mirror.cs.uwp.edu/pub/centos/7/extras/x86_64'
    },
    'c7_epel': {
        'umd': 'https://mirror.umd.edu/fedora/epel/7/x86_64/'
    }
}
for repo in config_centos_7:
    for remote_name, remote_url in config_centos_7[repo].items():
        pulp_operations.start_sync(
            repo_name=f"signed-{repo}",
            remote_name=f"{repo}-{remote_name}",
            remote_url=remote_url,
            signservice_name='sign-metadata'
        )

#CentOS 8
config_centos_8 = {
    'c8_appstream': {
        'umd': 'https://mirror.umd.edu/centos/8/AppStream/x86_64/os/',
        'uwp': 'https://mirror.cs.uwp.edu/pub/centos/8/AppStream/x86_64/os/'
    },
    'c8_baseos': {
        'umd': 'https://mirror.umd.edu/centos/8/BaseOS/x86_64/os/',
        'uwp': 'https://mirror.cs.uwp.edu/pub/centos/8/BaseOS/x86_64/os/'
    },
    'c8_extras': {
        'umd': 'https://mirror.umd.edu/centos/8/extras/x86_64/os/',
        'uwp': 'https://mirror.cs.uwp.edu/pub/centos/8/extras/x86_64/os/'
    },
    'c8_powertools': {
        'umd': 'https://mirror.umd.edu/centos/8/PowerTools/x86_64/os/',
        'uwp': 'https://mirror.cs.uwp.edu/pub/centos/8/PowerTools/x86_64/os/'
    },
    'c8_epel_everything': {
        'umd': 'https://mirror.umd.edu/fedora/epel/8/Everything/x86_64/'
    }
}
for repo in config_centos_8:
    for remote_name, remote_url in config_centos_8[repo].items():
        pulp_operations.start_sync(
            repo_name=f"signed-{repo}",
            remote_name=f"{repo}-{remote_name}",
            remote_url=remote_url,
            signservice_name='sign-metadata'
        )

#general repository operations
pulp_operations.repository.list_repo()
pulp_operations.remove_repository('test-repo')

#general remote operations
pulp_operations.remote.list_remote()
pulp_operations.remove_remote('test-remote')

#general publication operations
pulp_operations.publication.list_publication()

#general distribution operations
pulp_operations.distribution.list_distribution()
pulp_operations.distribution.get_distribution_url('test-dist')
pulp_operations.remove_distribution('test-dist')
```

## logging

pulp_operations logs to /var/log/pulp_operations.log at DEBUG level, and to console at INFO level

a new log file will be created once a day, and will automatically prune after 30 log files.

## development: container-based environment

```bash
#the following assumes your machine has docker desktop and vscode installed
cd ~
git clone <repo>
cd pulp_operations/.devcontainer

#add the following to devcontainer.env
PULP_USER=admin
PULP_PASS=<password from install.yml>
PULP_SERVER=<server from install.yml>

#launch in vscode as a container
#press F5 to run 'run_examples.py' script
#go into code and press F9 to create a breakpoint
```
