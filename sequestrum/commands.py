import sys
from pathlib import Path

from sequestrum import logging
from sequestrum import package
from sequestrum import directory

_HOME_PATH = str(Path.home()) + "/"


# Creates a new directory. It creates a new folder path using the config
# then creates a new folder using that path. It then loops through each
# link in the links list and **copies** (not symlinking) the original file
# on the source system over to the dotfiles.
def setup(args, config):
    # Grab the path of the dotfile directory
    dotfile_path = _HOME_PATH + \
        config['options']['base']['dotfileDirectory'] + "/"
    error_occured = False

    for key, value in config['options'].items():
        if key.endswith("Package"):
            if not package.check_source_locations(value, dotfile_path,
                                                  inverted=True):
                error_occured = True

            if not package.check_install_locations(value, inverted=True):
                error_occured = True

    if error_occured:
        logging.fatal("Could not setup due to config errors.")

    error_occured = False

    for key, value in config['options'].items():
        if key.endswith("Package"):
            if not package.setup(key, config, dotfile_path):
                error_occured = True

    if error_occured:
        logging.fatal(
            "Could not setup due errors. Please see errors above")
    else:
        logging.success("Setup was successfull, running installation ...")
        install(('Install', 'all'), config)


# Install the files from the dotfiles. Symlinks the files from the
# specified packages to the local system files. If the file or folder
# already exists on the local system, delete it then symlink properly to
# avoid errors.
def install(args, config):
    # Grab the path of the dotfile directory
    dotfile_path = _HOME_PATH + \
        config['options']['base']['dotfileDirectory'] + "/"
    full_pkgname = args[1] + "Package"
    error_occured = False

    if full_pkgname == "allPackage":
        for key, value in config['options'].items():
            if key.endswith("Package"):
                if not package.check_source_locations(value, dotfile_path):
                    error_occured = True

                if not package.check_install_locations(value):
                    error_occured = True

        if error_occured:
            logging.fatal("Could not install due errors.")

        error_occured = False

        for key, value in config['options'].items():
            if key.endswith("Package"):
                if not package.install(value, dotfile_path):
                    error_occured = True

        if error_occured:
            logging.warn(
                "Errors occured during installation, please check above")
        else:
            logging.success("Packages got installed successfully!")

    # The option to only install one package instead of all your dotfiles.
    elif full_pkgname in config['options']:

        pkg_config = config['options'][full_pkgname]

        if not package.check_install_locations(pkg_config):
            sys.exit()

        if not package.install(pkg_config, dotfile_path):
            logging.warn(
                "Errors occured during installation, please check above")
        else:
            logging.success("Package got installed successfully!")
    else:
        logging.error("Package {} was not found in config"
                      .format(args[1] + "Package"))


# TODO: Fix
def refresh(args, config):
    logging.fatal("NYI")


# Backs up your local files before you setup your dotfiles. This is also a
# good way to check if your config files aer correct
# If they aren't they won't be backed up to your backup folder
# and throw an error instead.
def backup(args, config):
    # Grab the path of the dotfile directory
    dotfile_path = _HOME_PATH + \
        config['options']['base']['dotfileDirectory'] + "/"
    backup_path = _HOME_PATH + "sequestrum-backup/"

    if directory.isfolder(backup_path):
        logging.fatal("Backup folder {} already exists"
                      .format(backup_path))
    else:
        directory.create_folder(backup_path)

    error_occured = False

    for key, value in config['options'].items():
        if key.endswith("Package"):
            if not package.check_source_locations(value, dotfile_path):
                error_occured = True

    if error_occured:
        logging.fatal("Could not backup due to missing files.")

    error_occured = False

    for key, value in config['options'].items():
        if key.endswith("Package"):
            if not package.backup(value, backup_path):
                error_occured = True

    if error_occured:
        logging.warn(
            "Errors occured during backup, please check above")
    else:
        logging.success("Packages got backuped successfully!")


# Unlink the source files. This doesn't really "unlink",
# instead it actually just deletes the files.
# It collects a list of files to unlink then
# it goes through and unlinks them all.
def unlink(args, config):
    full_pkgname = args[1] + "Package"

    if full_pkgname == "allPackage":

        error_occured = False

        for key, value in config['options'].items():
            if key.endswith("Package"):
                if not package.uninstall(value):
                    error_occured = True
                else:
                    logging.info("Unlinked package sucessfully.",
                                 value['pkgName'])

        if error_occured:
            logging.error("Could not unlink all files.")
        else:
            logging.success("All packages got successfully unlinked.")

    elif full_pkgname in config['options']:
        pkg_config = config['options'][full_pkgname]

        if not package.uninstall(pkg_config):
            logging.error("Could not unlink all files.")
        else:
            logging.success("All packages got successfully unlinked.")

    else:
        logging.error("Package {} was not found in config"
                      .format(args[1] + "Package"))
