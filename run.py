"""
high level script to call pulp_operations

standard repos
    find repos by going to mirrorlist.centos.org and filling in params
    example: http://mirrorlist.centos.org/?release=8&arch=x86_64&repo=AppStream
    note the structure of the url - some sites include a 'pub' or 'linux' directory that prefixes the standardized format

epel repos
    for searching for epel, use the following, and view the contents of the downloaded metalink file
    example: https://mirrors.fedoraproject.org/metalink?repo=epel-modular-8&arch=x86_64
    example: https://mirrors.fedoraproject.org/metalink?repo=epel-8&arch=x86_64&

"""
import urllib3
import pulp_operations

#disable ssl warnings for now
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

repo_config = {
    'c8_appstream': {
        'umd': 'https://mirror.umd.edu/centos/8/AppStream/x86_64/os/',
        'uwp': 'https://mirror.cs.uwp.edu/pub/centos/8/AppStream/x86_64/os/',
    },
    'c8_baseos': {
        'umd': 'https://mirror.umd.edu/centos/8/BaseOS/x86_64/os/',
        'uwp': 'https://mirror.cs.uwp.edu/pub/centos/8/BaseOS/x86_64/os/',
    },
    'c8_extras': {
        'umd': 'https://mirror.umd.edu/centos/8/extras/x86_64/os/',
        'uwp': 'https://mirror.cs.uwp.edu/pub/centos/8/extras/x86_64/os/',
    },
    'c8_powertools': {
        'umd': 'https://mirror.umd.edu/centos/8/PowerTools/x86_64/os/',
        'uwp': 'https://mirror.cs.uwp.edu/pub/centos/8/PowerTools/x86_64/os/',
    },
    'c8_epel_everything': {
        'umd': 'https://mirror.umd.edu/fedora/epel/8/Everything/x86_64/'
    },
    'c8_epel_modular': {
        'umd': 'https://mirror.umd.edu/fedora/epel/8/Modular/x86_64/'
    },
}

for repo in repo_config:
    for remote_name, remote_url in repo_config[repo].items():
        
        #unsigned
        pulp_operations.start_sync(
            repo_name=f"{repo}-repo",
            remote_name=f"{repo}-{remote_name}",
            remote_url=remote_url,
            dist_name=f"{repo}-dist"
        )

        #signed
        pulp_operations.start_sync(
            repo_name=f"signed-{repo}-repo",
            remote_name=f"{repo}-{remote_name}",
            remote_url=remote_url,
            dist_name=f"signed-{repo}-dist",
            signservice_name='sign-metadata'
        )
