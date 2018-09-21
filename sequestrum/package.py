from subprocess import run
from pathlib import Path

from sequestrum import logging
from sequestrum import symlink
from sequestrum import directory

homePath = str(Path.home()) + "/"


def _check_location(pkgConfig, path, useSource=True, inverted=False):
    """
        Checks to see if link locations are clean
    """

    noErrors = True

    for link in pkgConfig['links']:
        for key, value in link.items():
            destLink = key if useSource else value
            direction = "Source" if useSource else "Dest"
            destPath = path + destLink
            pkgName = pkgConfig['pkgName']

            exists = symlink.source_exists(destPath)

            if symlink.source_exists(destPath) and not inverted:
                logging.error("{} file already exists: {}"
                              .format(direction, destPath), pkgName)
                noErrors = False
            elif not exists and inverted:
                logging.error("{} file dosen't exists: {}"
                              .format(direction, destPath), pkgName)
                noErrors = False

    return noErrors


def check_install_locations(pkgConfig, inverted=False):
    """
        Checks to see if link locations are clean
    """

    return _check_location(pkgConfig, homePath, False, inverted)


def check_source_locations(pkgConfig, dotfilePath, inverted=False):
    """
        Check to see if dotfile locations are clean
    """
    directoryPath = dotfilePath + pkgConfig['directoryName'] + "/"
    return _check_location(pkgConfig, directoryPath, True, not inverted)


def run_commands(pkgConfig, after):

    unparsedCommands = None

    # Use commandsBefore list when after is false
    if "commandsBefore" in pkgConfig and not after:
        unparsedCommands = pkgConfig['commandsBefore']

    # Use commandsAfter list when after is true
    if "commandsAfter" in pkgConfig and after:
        unparsedCommands = pkgConfig['commandsAfter']

    # Check if we have something todo
    if unparsedCommands is None:
        return True

    for command in unparsedCommands:
        parsedCommand = command.split()

        try:
            runner = run(parsedCommand)
        except Exception as error:
            logging.error(
                "Error occured during command \"{}\": {}"
                .format(command, error), pkgConfig['pkgName'])
            return False
        else:
            logging.debug(
                "Command \"{}\" finished with exit code: {}"
                .format(command, runner.returncode), pkgConfig['pkgName'])

    return True


def symlink_package(pkgConfig, dotfilePath):
    """
        Symlink package to local system
    """
    # Grab dotfile package directory
    directoryPath = dotfilePath + pkgConfig['directoryName'] + "/"

    # Loop through files to link
    for link in pkgConfig['links']:
        # Symlink files to local files
        for key, value in link.items():
            sourceFile = directoryPath + key
            destFile = homePath + value
            pkgName = pkgConfig['pkgName']

            # Create base folder if it dosent exist
            if directory.create_parent_folder(destFile, pkgName):
                # Create symlink, if it fails return false
                if not symlink.create(sourceFile, destFile, pkgName):
                    return False
            else:
                return False

    return True


def install(pkgConfig, dotfilePath):
    if not run_commands(pkgConfig, after=False):
        logging.error(
            "Abort installation of package due to \"commandsBefore\" Errors",
            pkgConfig['pkgName'])
        return False

    if not symlink_package(pkgConfig, dotfilePath):
        logging.error(
            "Abort installation of package due to Symlink Errors",
            pkgConfig['pkgName'])
        return False

    if not run_commands(pkgConfig, after=True):
        logging.error(
            "Abort installation of package due to \"commandsAfter\" Errors",
            pkgConfig['pkgName'])
        return False

    logging.info("Package was installed successfully",
                 pkgConfig['pkgName'])
    return True


def uninstall(pkgConfig):

    noErrors = True
    filesToUnlink = []
    pkgName = pkgConfig['pkgName']

    for link in pkgConfig['links']:
        for _, value in link.items():
            symlinkFile = homePath + value

            if symlinkFile not in filesToUnlink:
                filesToUnlink.append(symlinkFile)

    for symlinkFile in filesToUnlink:
        if directory.isfolder(symlinkFile):
            if not directory.delete_folder(symlinkFile, pkgName):
                noErrors = False
        elif directory.isfile(symlinkFile):
            if not directory.delete_file(symlinkFile, pkgName):
                noErrors = False

    return noErrors


def backup(pkgConfig, dotfilePath, backupPath):

    noErrors = True
    pkgName = pkgConfig['pkgName']

    for link in pkgConfig['links']:
        for key, value in link.items():
            sourceFile = homePath + value
            destFile = backupPath + key

            if directory.isfile(sourceFile):
                if not directory.copy_file(sourceFile, destFile, pkgName):
                    noErrors = False
            else:
                if not directory.copy_folder(sourceFile, destFile, pkgName):
                    noErrors = False

    return noErrors


def setup(packageKey, configDict, dotfilePath):
    """
        Setup package directory on dotfile
    """
    # Make a path for the new directory path using the name specified in the
    # config then make the folder using the path.
    pkgConfig = configDict['options'][packageKey]
    pkgName = pkgConfig['pkgName']
    newPackagePath = dotfilePath + pkgConfig['directoryName'] + "/"
    directory.create_folder(newPackagePath, pkgName)

    for link in pkgConfig['links']:
        for key, value in link.items():
            sourceFile = homePath + value
            destFile = newPackagePath + key

            if directory.isfolder(sourceFile):
                directory.copy_folder(sourceFile, destFile, pkgName)
                directory.delete_folder(sourceFile, pkgName)
            elif directory.isfile(sourceFile):
                directory.copy_file(sourceFile, destFile, pkgName)
                directory.delete_file(sourceFile, pkgName)
            else:
                return False

    return True
