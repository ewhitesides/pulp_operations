"""
data structure used for repo_sync.py

multiple urls can be giving for one repository if desired to act as a backup in case one fails

#centos 8 stream repos can be found with queries like:
#curl 'http://mirrorlist.centos.org/?release=8-stream&arch=x86_64&repo=appstream'

#centos 8 stream uses epel next which is a supplement to epel
#https://docs.fedoraproject.org/en-US/epel/epel-about-next/#epel_next
"""

repo_data = {
    'c7': {
        'os': {
            'umd': 'https://mirror.umd.edu/centos/7/os/x86_64/',
            'prnc': 'https://mirror.math.princeton.edu/pub/centos/7/os/x86_64/',
            'ncsu': 'https://packages.oit.ncsu.edu/centos/7/os/x86_64/'
        },
        'updates': {
            'umd': 'https://mirror.umd.edu/centos/7/updates/x86_64/',
            'prnc': 'https://mirror.math.princeton.edu/pub/centos/7/updates/x86_64/',
            'ncsu': 'https://packages.oit.ncsu.edu/centos/7/updates/x86_64/'
        },
        'extras2': {
            'umd': 'https://mirror.umd.edu/centos/7/extras/x86_64/',
            'prnc': 'https://mirror.math.princeton.edu/pub/centos/7/extras/x86_64/',
            'ncsu': 'https://packages.oit.ncsu.edu/centos/7/extras/x86_64/'
        },
        'epel': {
            'umd': 'https://mirror.umd.edu/fedora/epel/7/x86_64/',
            'prnc': 'https://mirror.math.princeton.edu/pub/epel/7/x86_64/',
            'ncsu': 'https://packages.oit.ncsu.edu/epel/7/x86_64/'
        },
        'salt_latest': {
            'salt': 'https://repo.saltstack.com/py3/redhat/7/x86_64/latest/'
        },
        'docker': {
            'docker': 'https://download.docker.com/linux/centos/7/x86_64/stable/'
        },
        'google_cloud_monitoring2': {
            'google': 'https://packages.cloud.google.com/yum/repos/google-cloud-monitoring-el7-x86_64-all/'
        }
    },
    'c8s': { #centos8 stream
        'appstream': {
            'umd': 'https://mirror.umd.edu/centos/8-stream/AppStream/x86_64/os/',
            'prnc': 'https://mirror.math.princeton.edu/pub/centos/8-stream/AppStream/x86_64/os/',
            'ncsu': 'https://packages.oit.ncsu.edu/centos/8-stream/AppStream/x86_64/os/'
        },
        'baseos': {
            'umd': 'https://mirror.umd.edu/centos/8-stream/BaseOS/x86_64/os/',
            'prnc': 'https://mirror.math.princeton.edu/pub/centos/8-stream/BaseOS/x86_64/os/',
            'ncsu': 'https://packages.oit.ncsu.edu/centos/8-stream/BaseOS/x86_64/os/'
        },
        'extras': {
            'umd': 'https://mirror.umd.edu/centos/8-stream/extras/x86_64/os/',
            'prnc': 'https://mirror.math.princeton.edu/pub/centos/8-stream/extras/x86_64/os/',
            'ncsu': 'https://packages.oit.ncsu.edu/centos/8-stream/extras/x86_64/os/'
        },
        'powertools': {
            'umd': 'https://mirror.umd.edu/centos/8-stream/PowerTools/x86_64/os/',
            'prnc': 'https://mirror.math.princeton.edu/pub/centos/8-stream/PowerTools/x86_64/os/',
            'ncsu': 'https://packages.oit.ncsu.edu/centos/8-stream/PowerTools/x86_64/os/'
        },
        'epel_everything': {
            'umd': 'https://mirror.umd.edu/fedora/epel/8/Everything/x86_64/',
            'prnc': 'https://mirror.math.princeton.edu/pub/epel/8/Everything/x86_64/',
            'ncsu': 'https://packages.oit.ncsu.edu/epel/8/Everything/x86_64/'
        },
        'epel_everything_next': {
            'umd': 'https://mirror.umd.edu/fedora/epel/next/8/Everything/x86_64/',
            'prnc': 'https://mirror.math.princeton.edu/pub/epel/next/8/Everything/x86_64/',
            'ncsu': 'https://packages.oit.ncsu.edu/epel/next/8/Everything/x86_64/'
        },
        'salt_latest': {
            'salt': 'https://repo.saltstack.com/py3/redhat/8/x86_64/latest/'
        },
        'google_cloud_monitoring': {
            'google': 'https://packages.cloud.google.com/yum/repos/google-cloud-monitoring-el8-x86_64-all/'
        }
    },
    'rocky8': {
        'appstream': {
            'vblt': 'http://repo.accre.vanderbilt.edu/pub/rocky/8/AppStream/x86_64/os/',
            'nju': 'https://mirrors.nju.edu.cn/rocky/8/AppStream/x86_64/os/'
        },
        'baseos': {
            'vblt': 'http://repo.accre.vanderbilt.edu/pub/rocky/8/BaseOS/x86_64/os/',
            'nju': 'https://mirrors.nju.edu.cn/rocky/8/BaseOS/x86_64/os/'
        },
        'extras': {
            'vblt': 'http://repo.accre.vanderbilt.edu/pub/rocky/8/extras/x86_64/os/',
            'nju': 'https://mirrors.nju.edu.cn/rocky/8/extras/x86_64/os/'
        },
        'powertools': {
            'vblt': 'http://repo.accre.vanderbilt.edu/pub/rocky/8/PowerTools/x86_64/os/',
            'nju': 'https://mirrors.nju.edu.cn/rocky/8/PowerTools/x86_64/os/'
        },
        'epel_everything': {
            'umd': 'https://mirror.umd.edu/fedora/epel/8/Everything/x86_64/',
            'prnc': 'https://mirror.math.princeton.edu/pub/epel/8/Everything/x86_64/',
            'ncsu': 'https://packages.oit.ncsu.edu/epel/8/Everything/x86_64/'
        },
        'salt_latest': {
            'salt': 'https://repo.saltstack.com/py3/redhat/8/x86_64/latest/'
        },
        'google_cloud_monitoring': {
            'google': 'https://packages.cloud.google.com/yum/repos/google-cloud-monitoring-el8-x86_64-all/'
        }
    }
}
