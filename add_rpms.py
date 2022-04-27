"""
high level script to add rpms
"""
import urllib3
import pathlib
import argparse
import pulp_operations

# disable ssl
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# main
def main(repo_name: str):
    """
    add all rpm files found in same path as this script
    if the repository specified does not exist, it is created as part of adding the rpm
    """
    for rpm_file in pathlib.Path(".").glob("*.rpm"):
        pulp_operations.add_rpm(
            rpm_file=str(rpm_file),
            repo_name=repo_name,
            # signservice_name='sign-metadata' #optional
        )

    # release updated version of the repository to the distribution
    pulp_operations.release(
        repo_name=repo_name, version_rollback=0, dist_name=f"{repo_name}-dist"
    )


# if this file is called directly
if __name__ == "__main__":

    # get arguments from cli
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo_name", required=True, action="store")
    args = parser.parse_args()

    # run main func
    main(args.repo_name)
