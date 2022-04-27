"""file functions"""

import hashlib


def get_sha256hash(input_file: str):
    """
    Summary:
        creates a sha256 hash for the given file

    Parameters:
        input_file (str): the input file

    Returns:
        the hash
    """

    with open(input_file, "rb") as file:
        file_bytes = file.read()  # read entire file as bytes
        output = hashlib.sha256(file_bytes).hexdigest()
        return output


def get_rpm_properties(input_file: str):
    """
    Summary:
        processes the structured name of the rpm file to get the
        arch, release, version, and name

    Parameters:
        input_file (str): the file

    Returns:
        dictionary containing arch, release, version, and name
    """

    # get properties from rpm_file name
    arch = input_file.rsplit(".", 2)[1]
    release = input_file.rsplit(".", 2)[0].rsplit("-", 1)[1]
    version = input_file.rsplit(".", 2)[0].rsplit("-", 1)[0].rsplit("-", 1)[1]
    name = input_file.rsplit(".", 2)[0].rsplit("-", 1)[0].rsplit("-", 1)[0]

    # put into dictionary
    output = {"arch": arch, "release": release, "version": version, "name": name}

    # output
    return output
