from subprocess import run
from pathlib import Path

from sequestrum import logging
from sequestrum import symlink
from sequestrum import directory

_HOME_PATH = str(Path.home()) + "/"


def _check_location(pkg_config, path, use_source=True, inverted=False):
    """
        Checks to see if link locations are clean
    """
    noerrors = True

    for link in pkg_config['links']:
        for key, value in link.items():
            dest_link = key if use_source else value
            dest_path = path + dest_link
            direction = "Source" if use_source else "Dest"
            pkg_name = pkg_config['pkgName']

            exists = symlink.source_exists(dest_path)

            if exists and not inverted:
                logging.error("{} file already exists: {}"
                              .format(direction, dest_path), pkg_name)
                noerrors = False
            elif not exists and inverted:
                logging.error("{} file dosen't exists: {}"
                              .format(direction, dest_path), pkg_name)
                noerrors = False

    return noerrors


def check_install_locations(pkg_config, inverted=False):
    """
        Checks to see if link locations are clean
    """
    return _check_location(pkg_config, _HOME_PATH, False, inverted)


def check_source_locations(pkg_config, dotfile_path, inverted=False):
    """
        Check to see if dotfile locations are clean
    """
    directory_path = dotfile_path + pkg_config['directoryName'] + "/"
    return _check_location(pkg_config, directory_path, True, not inverted)


def run_commands(pkg_config, after):
    commands = None

    # Use commandsBefore list when after is false
    if "commandsBefore" in pkg_config and not after:
        commands = pkg_config['commandsBefore']

    # Use commandsAfter list when after is true
    if "commandsAfter" in pkg_config and after:
        commands = pkg_config['commandsAfter']

    # Check if we have something todo
    if commands is None:
        return True

    for command in commands:
        parsed_command = command.split()

        try:
            runner = run(parsed_command)
        except Exception as error:
            logging.error(
                "Error occured during command \"{}\": {}"
                .format(command, error), pkg_config['pkgName'])
            return False
        else:
            logging.debug(
                "Command \"{}\" finished with exit code: {}"
                .format(command, runner.returncode), pkg_config['pkgName'])

    return True


def symlink_package(pkg_config, dotfile_path):
    """
        Symlink package to local system
    """
    # Grab dotfile package directory
    directory_path = dotfile_path + pkg_config['directoryName'] + "/"

    # Loop through files to link
    for link in pkg_config['links']:
        # Symlink files to local files
        for key, value in link.items():
            source_file = directory_path + key
            dest_file = _HOME_PATH + value
            pkg_name = pkg_config['pkgName']

            # Create base folder if it dosent exist
            if directory.create_parent_folder(dest_file, pkg_name):
                # Create symlink, if it fails return false
                if not symlink.create(source_file, dest_file, pkg_name):
                    return False
            else:
                return False

    return True


def install(pkg_config, dotfile_path):
    if not run_commands(pkg_config, after=False):
        logging.error(
            "Abort installation of package due to \"commandsBefore\" Errors",
            pkg_config['pkgName'])
        return False

    if not symlink_package(pkg_config, dotfile_path):
        logging.error(
            "Abort installation of package due to Symlink Errors",
            pkg_config['pkgName'])
        return False

    if not run_commands(pkg_config, after=True):
        logging.error(
            "Abort installation of package due to \"commandsAfter\" Errors",
            pkg_config['pkgName'])
        return False

    logging.info("Package was installed successfully",
                 pkg_config['pkgName'])
    return True


def uninstall(pkg_config):
    noerrors = True
    unlink_files = []
    pkg_name = pkg_config['pkgName']

    for link in pkg_config['links']:
        for _, value in link.items():
            symlink_file = _HOME_PATH + value

            if symlink_file not in unlink_files:
                unlink_files.append(symlink_file)

    for symlink_file in unlink_files:
        if directory.isfolder(symlink_file):
            if not directory.delete_folder(symlink_file, pkg_name):
                noerrors = False
        elif directory.isfile(symlink_file):
            if not directory.delete_file(symlink_file, pkg_name):
                noerrors = False

    return noerrors


def backup(pkg_config, backup_path):
    noerrors = True
    pkg_name = pkg_config['pkgName']

    for link in pkg_config['links']:
        for key, value in link.items():
            source_file = _HOME_PATH + value
            dest_file = backup_path + key

            if directory.isfile(source_file):
                if not directory.copy_file(source_file, dest_file, pkg_name):
                    noerrors = False
            else:
                if not directory.copy_folder(source_file, dest_file, pkg_name):
                    noerrors = False

    return noerrors


def setup(pkg_key, config, dotfile_path):
    """
        Setup package directory on dotfile
    """
    # Make a path for the new directory path using the name specified in the
    # config then make the folder using the path.
    pkg_config = config['options'][pkg_key]
    pkg_name = pkg_config['pkgName']
    pkg_path = dotfile_path + pkg_config['directoryName'] + "/"
    directory.create_folder(pkg_path, pkg_name)

    for link in pkg_config['links']:
        for key, value in link.items():
            source_file = _HOME_PATH + value
            dest_file = pkg_path + key

            if directory.isfolder(source_file):
                directory.copy_folder(source_file, dest_file, pkg_name)
                directory.delete_folder(source_file, pkg_name)
            elif directory.isfile(source_file):
                directory.copy_file(source_file, dest_file, pkg_name)
                directory.delete_file(source_file, pkg_name)

    return True


def refresh(pkg_config, dotfile_path):
    """
        Refresh package directory on dotfile
    """
    # Grab dotfile package directory
    directory_path = dotfile_path + pkg_config['directoryName'] + "/"
    pkg_name = pkg_config['pkgName']
    links_setup = []
    links_install = []

    for link in pkg_config['links']:
        for key, value in link.items():
            source_file = directory_path + key
            dest_file = _HOME_PATH + value

            exists_source = symlink.source_exists(source_file)
            exists_dest = symlink.source_exists(dest_file, False)

            if exists_dest and symlink.is_link(dest_file):
                if symlink.get_dest(dest_file) != source_file:
                    logging.warn(
                        "Link  \"{}\" exist but is invalid, ignoring"
                        .format(dest_file), pkg_name)
                continue

            if exists_source and symlink.is_link(source_file):
                logging.warn(
                    "File  \"{}\" is a symlink and will be ignored"
                    .format(source_file), pkg_name)
                continue

            # Check if we have already a file
            # inside $HOME directory
            if exists_dest and not exists_source:
                links_setup.append((key, value))
            elif exists_source and not exists_dest:
                links_install.append((key, value))
            elif exists_dest and exists_source:
                logging.warn(
                    "File for link  \"{}\" exist in both locations, ignoring"
                    .format(dest_file), pkg_name)

    # If both lists are empty, we just return since nothing todo
    if (len(links_setup) + len(links_install)) == 0:
        logging.debug("Files are up-to-date. No refresh needed", pkg_name)
        return True

    # First run setup
    for key, value in links_setup:
        source_file = directory_path + key
        dest_file = _HOME_PATH + value

        if directory.isfolder(dest_file):
            directory.create_parent_folder(source_file, pkg_name)
            directory.copy_folder(dest_file, source_file, pkg_name)
            directory.delete_folder(dest_file, pkg_name)
        elif directory.isfile(dest_file):
            directory.create_parent_folder(source_file, pkg_name)
            directory.copy_file(dest_file, source_file, pkg_name)
            directory.delete_file(dest_file, pkg_name)

        # Everything okay, lets add to install
        links_install.append((key, value))

    for key, value in links_install:
        source_file = directory_path + key
        dest_file = _HOME_PATH + value

        # Create base folder if it dosent exist
        if directory.create_parent_folder(dest_file, pkg_name):
            # Create symlink, if it fails return false
            if not symlink.create(source_file, dest_file, pkg_name):
                return False
        else:
            return False

    logging.info("Refresh of package was successfull.", pkg_name)
    return True
