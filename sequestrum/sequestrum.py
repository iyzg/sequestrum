#!/usr/bin/env python3
#
# Sequestrum - Dotfile Manager

# Libraries
import sys
from pathlib import Path
import yaml

homePath = str(Path.home()) + "/"

# Modules
import errors
import directories
import symlink
import arguments
import commands
import logging

# For Later
packages_to_unlink = []

# Creates a new directory. It creates a new folder path using the config
# then creates a new folder using that path. It then loops through each
# link in the links list and **copies** (not symlinking) the original file
# on the source system over to the dotfiles.


def setup_package(package_key, config_dict, dotfile_path):
    """
        Setup package directory on dotfile
    """
    # Make a path for the new directory path using the name specified in the
    # config then make the folder using the path.
    package_config = config_dict['options'][package_key]
    package_name = package_config['package_name']
    new_package_path = dotfile_path + package_config['directoryName'] + "/"
    if directories.is_folder(new_package_path) == False:
        directories.create_folder(new_package_path, package_name)

    for link in package_config['links']:
        for key, value in link.items():
            source_file = homePath + value
            dest_file = new_package_path + key
            
            # Checks
            if directories.is_folder(dest_file):
                continue
            elif directories.is_file(dest_file):
                continue

            # Setup
            if directories.is_folder(source_file):
                symlink.copy_folder(source_file, dest_file)
                directories.delete_folder(source_file)
            elif directories.is_file(source_file):
                symlink.copy_file(source_file, dest_file)
                directories.delete_file(source_file)
            else:
                return False

    return True


# Grabs the directory of the key. For each item in the dotfile directory,
# properly symlink the file to the right place. If the file on the local
# system already exists. Delete the existing file before symlinking to
# prevent issues.


def install_package(package_key, config_dict, dotfile_path):
    """
        Install package to local system
    """
    # Grab dotfile package directory
    package_config = config_dict['options'][package_key]
    directory_path = dotfile_path + package_config['directoryName'] + "/"

    # Loop through files to link
    for link in package_config['links']:
        # Symlink files to local files
        for key, value in link.items():
            source_file = directory_path + key
            dest_file = homePath + value

            if directories.is_folder(dest_file):
                continue
            elif directories.is_file(dest_file):
                continue

            if directories.create_base_folder(dest_file, package_config['package_name']):
                symlink.create_symlink(source_file, dest_file, package_config['package_name'])
            else:
                return False

    return True


def get_packages_to_unlink(package_key, config_dict, dotfile_path):
    """
        Grab packages and put them into a list ( NO DUPES )
    """
    package_config = config_dict['options'][package_key]

    for link in package_config['links']:
        for _, value in link.items():
            fileToGrab = homePath + value

            if fileToGrab not in packages_to_unlink:
                packages_to_unlink.append(fileToGrab)


def unlink_packages():
    """
        Unlink all files in packages_to_unlink
    """
    for path in packages_to_unlink:
        if directories.is_folder(path):
            directories.delete_folder(path)
        elif directories.is_file(path):
            directories.delete_file(path)
        else:
            print(errors.formatError("Sequestrum", "Nothing to unlink!"))

# Goes through all the file locations that need to be empty for the
# symlinking to work and checks to see if they're empty. If they're not,
# it will return false. If it is clean, it'll return true.


def check_install_locations(package_key, config_dict):
    """
        Checks to see if link locations are clean
    """
    for link in config_dict['options'][package_key]['links']:
        for key, value in link.items():
            destPath = homePath + value
            if symlink.symlinkSourceExists(destPath):
                print(errors.formatError(
                    "Safety", "{} already exists.".format(destPath)))
                return False

    return True

# Checks to see if the file locations in the dotfile repository exist. If
# they do, return false. If they don't, return true. This is to prevent
# overwriting of file that may or may not be important to the user.


def checkSourceLocations(package_key, config_dict, dotfile_path):
    """
        Check to see if dotfile locations are clean
    """
    directory_path = dotfile_path + \
        config_dict['options'][package_key]['directoryName'] + "/"

    for link in config_dict['options'][package_key]['links']:
        for key, value in link.items():
            sourcePath = directory_path + key

            if symlink.symlinkSourceExists(sourcePath):
                logging.printFatal("File dosent exists: {}".format(sourcePath))


def main():

    # Grab user inputted arguments from the module and make sure they entered some.
    arguments = arguments.getArguments()

    if arguments is None:
        print(errors.formatError("Arguments", "Must pass arguments"))
        sys.exit()

    try:
        configFile = open("config.yaml", "r")
    except:
        print(errors.formatError("Core", "No configuration found."))
        sys.exit()

    config_dict = yaml.load(configFile)
    packageList = []

    # Grab list of directories from the config.
    for key, value in config_dict['options'].items():
        if key.endswith("Package"):
            friendlyName = key[:-7]
            config_dict['options'][key]['package_name'] = friendlyName
            packageList.append(friendlyName)

    # We need to have a base package
    if "base" not in config_dict['options']:
        logging.printFatal(
            "Invalid config file, a base package needs to be defined")

    # Grab the path of the dotfile directory
    dotfile_path = homePath + \
        config_dict['options']['base']['dotfileDirectory'] + "/"

    # Setups up the dotfiles accordingly to the config. This should only be
    # ran once to setup your dotfiles with the right directories. After this,
    # users should use the update argument to update their dotfiles with new
    # packages.
    if arguments[0] == "Setup":
        if arguments[1] == "all":
            for key, value in config_dict['options'].items():
                if key.endswith("Package"):
                    if not checkSourceLocations(key, config_dict, dotfile_path):
                        print(errors.formatError("Sequestrum", "Dotfile Path Missing"))
                        sys.exit()

                    if not check_install_locations(key, config_dict):
                        print(errors.formatError("Sequestrum", "Home Path Occupied"))
                        sys.exit()

            for key, value in config_dict['options'].items():
                if key.endswith("Package"):
                    if "commandsBefore" in value:
                        commands.runCommands(
                            config_dict['options'][key]["commandsBefore"])
                    setup_package(key, config_dict, dotfile_path)
                    if "commandsAfter" in value:
                        commands.runCommands(
                            config_dict['options'][key]["commandsAfter"])
        else:
            print(errors.formatError("Sequestrum",
                                     "uwu Another Impossible Safety Net owo"))

    # Install the files from the dotfiles. Symlinks the files from the
    # specified packages to the local system files. If the file or folder
    # already exists on the local system, delete it then symlink properly to
    # avoid errors.
    elif arguments[0] == "Install":
        # Install all packages
        if arguments[1] == "all":
            for key, value in config_dict['options'].items():
                if key.endswith("Package"):
                    if not check_install_locations(key, config_dict):
                        sys.exit()

            for key, value in config_dict['options'].items():
                if key.endswith("Package"):
                    if "commandsBefore" in value:
                        commands.runCommands(
                            config_dict['options'][key]['commandsBefore'], config_dict['options'][key]['package_name'])
                    install_package(key, config_dict, dotfile_path)
                    if "commandsAfter" in value:
                        commands.runCommands(
                            config_dict['options'][key]['commandsAfter'], config_dict['options'][key]['package_name'])

            logging.printInfo("We are done!")

        # The option to only install one package instead of all your dotfiles.
        elif arguments[1] in packageList:
            for key, value in config_dict['options'].items():
                if key == arguments[1] + "Package":
                    if not check_install_locations(key, config_dict):
                        sys.exit()

            for key, value in config_dict['options'].items():
                if key == arguments[1] + "Package":
                    if "commandsBefore" in value:
                        commands.runCommands(
                            config_dict['options'][key]["commandsBefore"])
                    install_package(key, config_dict, dotfile_path)
                    if "commandsAfter" in value:
                        commands.runCommands(
                            config_dict['options'][key]["commandsAfter"])
        else:
            print(errors.formatError("Sequstrum", "Invalid Package."))

    elif arguments[0] == "Refresh":
        if arguments[1] == "all":
            dotfilePackageList = directories.grabPackageNames(dotfile_path)
            for key, value in config_dict['options'].items():
                if key.endswith("Package"):
                    if "commandsBefore" in value:
                        commands.runCommands(
                            config_dict['options'][key]["commandsBefore"])
                    setup_package(key, config_dict, dotfile_path)
                    install_package(key, config_dict, dotfile_path)
                    if "commandsAfter" in value:
                        commands.runCommands(
                            config_dict['options'][key]["commandsAfter"])
        else:
            print(errors.formatError("Sequestrum", "Source code compromised."))

    # Unlink the source files. This doesn't really "unlink", instead it actually just
    # deletes the files. It collects a list of files to unlink then it goes through and
    # unlinks them all.
    elif arguments[0] == "Unlink":
        if arguments[1] == "all":
            for key, value in config_dict['options'].items():
                if key.endswith("Package"):
                    get_packages_to_unlink(key, config_dict, dotfile_path)
            unlink_packages()
        elif arguments[1] in packageList:
            for key, value in config_dict['options'].items():
                if key == arguments[1] + "Package":
                    get_packages_to_unlink(key, config_dict, dotfile_path)
            unlink_packages()
        else:
            print(errors.formatError("Sequestrum", "Invalid Package."))
    else:
        print(errors.formatError("Sequestrum", "Invalid Command"))


if __name__ == '__main__':
    main()
