import sys
from pathlib import Path

from sequestrum import logging
from sequestrum import package
from sequestrum import directory

homePath = str(Path.home()) + "/"


# Creates a new directory. It creates a new folder path using the config
# then creates a new folder using that path. It then loops through each
# link in the links list and **copies** (not symlinking) the original file
# on the source system over to the dotfiles.
def setup(arguments, configDict):
    # Grab the path of the dotfile directory
    dotfilePath = homePath + \
        configDict['options']['base']['dotfileDirectory'] + "/"
    errorOccured = False

    for key, value in configDict['options'].items():
        if key.endswith("Package"):
            if not package.check_source_locations(value, dotfilePath,
                                                  inverted=True):
                errorOccured = True

            if not package.check_install_locations(value, inverted=True):
                errorOccured = True

    if errorOccured:
        logging.fatal("Could not setup due to config errors.")

    errorOccured = False

    for key, value in configDict['options'].items():
        if key.endswith("Package"):
            if not package.setup(key, configDict, dotfilePath):
                errorOccured = True

    if errorOccured:
        logging.fatal(
            "Could not setup due errors. Please see errors above")
    else:
        logging.success("Setup was successfull, running installation ...")
        install(('Install', 'all'), configDict)


# Install the files from the dotfiles. Symlinks the files from the
# specified packages to the local system files. If the file or folder
# already exists on the local system, delete it then symlink properly to
# avoid errors.
def install(arguments, configDict):
    # Grab the path of the dotfile directory
    dotfilePath = homePath + \
        configDict['options']['base']['dotfileDirectory'] + "/"
    fullPackageName = arguments[1] + "Package"
    errorOccured = False

    if fullPackageName == "allPackage":
        for key, value in configDict['options'].items():
            if key.endswith("Package"):
                if not package.check_source_locations(value, dotfilePath):
                    errorOccured = True

                if not package.check_install_locations(value):
                    errorOccured = True

        if errorOccured:
            logging.fatal("Could not install due errors.")

        errorOccured = False

        for key, value in configDict['options'].items():
            if key.endswith("Package"):
                if not package.install(value, dotfilePath):
                    errorOccured = True

        if errorOccured:
            logging.warn(
                "Errors occured during installation, please check above")
        else:
            logging.success("Packages got installed successfully!")

    # The option to only install one package instead of all your dotfiles.
    elif fullPackageName in configDict['options']:

        pkgConfig = configDict['options'][fullPackageName]

        if not package.check_install_locations(pkgConfig):
            sys.exit()

        if not package.install(pkgConfig, dotfilePath):
            logging.warn(
                "Errors occured during installation, please check above")
        else:
            logging.success("Package got installed successfully!")
    else:
        logging.error("Package {} was not found in config"
                      .format(arguments[1] + "Package"))


# TODO: Fix
def refresh(arguments, configDict):
    logging.fatal("NYI")


# Backs up your local files before you setup your dotfiles. This is also a
# good way to check if your config files aer correct
# If they aren't they won't be backed up to your backup folder
# and throw an error instead.
def backup(arguments, configDict):
    # Grab the path of the dotfile directory
    dotfilePath = homePath + \
        configDict['options']['base']['dotfileDirectory'] + "/"
    backupPath = homePath + "sequestrum-backup/"

    if directory.isfolder(backupPath):
        logging.fatal("Backup folder {} already exists"
                      .format(backupPath))
    else:
        directory.create_folder(backupPath)

    errorOccured = False

    for key, value in configDict['options'].items():
        if key.endswith("Package"):
            if not package.check_source_locations(value, dotfilePath):
                errorOccured = True

    if errorOccured:
        logging.fatal("Could not backup due to missing files.")

    errorOccured = False

    for key, value in configDict['options'].items():
        if key.endswith("Package"):
            if not package.backup(value, dotfilePath, backupPath):
                errorOccured = True

    if errorOccured:
        logging.warn(
            "Errors occured during backup, please check above")
    else:
        logging.success("Packages got backuped successfully!")


# Unlink the source files. This doesn't really "unlink",
# instead it actually just deletes the files.
# It collects a list of files to unlink then
# it goes through and unlinks them all.
def unlink(arguments, configDict):
    fullPackageName = arguments[1] + "Package"

    if fullPackageName == "allPackage":

        errorOccured = False

        for key, value in configDict['options'].items():
            if key.endswith("Package"):
                if not package.uninstall(value):
                    errorOccured = True
                else:
                    logging.info("Unlinked package sucessfully.",
                                 value['pkgName'])

        if errorOccured:
            logging.error("Could not unlink all files.")
        else:
            logging.success("All packages got successfully unlinked.")

    elif fullPackageName in configDict['options']:
        pkgConfig = configDict['options'][fullPackageName]

        if not package.uninstall(pkgConfig):
            logging.error("Could not unlink all files.")
        else:
            logging.success("All packages got successfully unlinked.")

    else:
        logging.error("Package {} was not found in config"
                      .format(arguments[1] + "Package"))
