"""
data structure used for repo_sync.py

structure follows this format:
repo_data = {
    'c7': {                         
        'repository subject': {
            'abbreviated name of company/institution providing the repo': 'url'
        }
    }
}

multiple urls can be giving for one repository if desired to act as a backup in case one fails
"""

repo_data = {
    'c7': {
        'os': {
            'umd': 'https://mirror.umd.edu/centos/7/os/x86_64/'
        },
        'updates': {
            'umd': 'https://mirror.umd.edu/centos/7/updates/x86_64/'
        },
        'extras': {
            'umd': 'https://mirror.umd.edu/centos/7/extras/x86_64/'
        },
        'epel': {
            'umd': 'https://mirror.umd.edu/fedora/epel/7/x86_64/'
        },
        'salt_latest': {
            'salt': 'https://repo.saltstack.com/py3/redhat/7/x86_64/latest/'
        },
        'docker': {
            'docker': 'https://download.docker.com/linux/centos/7/x86_64/stable/'
        },
        'google_cloud_monitoring': {
            'google': 'https://packages.cloud.google.com/yum/repos/google-cloud-monitoring-el7-x86_64-all/'
        }
    },
    'c8': {
        'appstream': {
            'umd': 'https://mirror.umd.edu/centos/8/AppStream/x86_64/os/',
        },
        'baseos': {
            'umd': 'https://mirror.umd.edu/centos/8/BaseOS/x86_64/os/'
        },
        'extras': {
            'umd': 'https://mirror.umd.edu/centos/8/extras/x86_64/os/'
        },
        'powertools': {
            'umd': 'https://mirror.umd.edu/centos/8/PowerTools/x86_64/os/'
        },
        'epel_everything': {
            'umd': 'https://mirror.umd.edu/fedora/epel/8/Everything/x86_64/'
        },
        'salt_latest': {
            'salt': 'https://repo.saltstack.com/py3/redhat/8/x86_64/latest/'
        },
        'google_cloud_monitoring': {
            'google': 'https://packages.cloud.google.com/yum/repos/google-cloud-monitoring-el8-x86_64-all/'
        }
    }
}
