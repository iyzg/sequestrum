# Libraries
from pathlib import Path
import sys
from time import sleep
import yaml

# Modules
import sequestrum.errors as errors
import sequestrum.directories as directories
import sequestrum.symlink as symlink
import sequestrum.arguments as arguments
import sequestrum.commands as commands
import sequestrum.logging as logging

# For Later
packages_to_unlink = []

# Global constants
HOME_PATH = str(Path.home()) + "/"


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
    if directories.is_folder(new_package_path) is False:
        directories.create_folder(new_package_path, package_name)

    for link in package_config['links']:
        for key, value in link.items():
            source_file = HOME_PATH + value
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
            dest_file = HOME_PATH + value

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
            fileToGrab = HOME_PATH + value

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
            print(errors.format_error("Sequestrum", "Nothing to unlink!"))

# Goes through all the file locations that need to be empty for the
# symlinking to work and checks to see if they're empty. If they're not,
# it will return false. If it is clean, it'll return true.


def check_install_locations(package_key, config_dict):
    """
        Checks to see if link locations are clean
    """

    for link in config_dict['options'][package_key]['links']:
        for key, value in link.items():
            destPath = HOME_PATH + value

            if symlink.symlink_source_exists(destPath):
                print(errors.format_error(
                    "Safety", "{} already exists.".format(destPath)))
                return False

    return True

# Checks to see if the file locations in the dotfile repository exist. If
# they do, return false. If they don't, return true. This is to prevent
# overwriting of file that may or may not be important to the user.


def check_source_locations(package_key, config_dict, dotfile_path):
    """
        Check to see if dotfile locations are clean
    """

    directory_path = dotfile_path + \
        config_dict['options'][package_key]['directoryName'] + "/"

    for link in config_dict['options'][package_key]['links']:
        for key, value in link.items():
            sourcePath = directory_path + key

            if symlink.symlink_source_exists(sourcePath):
                logging.print_fatal("File dosent exists: {}".format(sourcePath))


def main():
    # Grab user inputted args from the module and make sure they entered some.
    args = arguments.get_arguments()

    if args is None:
        print(errors.format_error("Arguments", "Must pass args"))
        sys.exit()

    config_file = None
    config_dict = {}
    package_list = []

    try:
        config_file = open("config.yaml", "r")
    except:
        print(errors.format_error("Core", "No configuration found."))
        sys.exit()

    config_dict = yaml.load(config_file)

    # Grab list of directories from the config.
    for key, value in config_dict['options'].items():
        if key.endswith("Package"):
            friendly_name = key[:-7]
            config_dict['options'][key]['package_name'] = friendly_name
            package_list.append(friendly_name)

    # We need to have a base package
    if "base" not in config_dict['options']:
        logging.print_fatal(
            "Invalid config file, a base package needs to be defined")

    # Grab the path of the dotfile directory
    dotfile_path = HOME_PATH + \
        config_dict['options']['base']['dotfileDirectory'] + "/"

    # Setups up the dotfiles accordingly to the config. This should only be
    # ran once to setup your dotfiles with the right directories. After this,
    # users should use the update argument to update their dotfiles with new
    # packages.
    if args[0] == "Setup":
        if args[1] == "all":
            for key, value in config_dict['options'].items():
                if key.endswith("Package"):
                    if not check_source_locations(key, config_dict, dotfile_path):
                        print(errors.format_error("Sequestrum", "Dotfile Path Missing"))
                        sys.exit()

                    if not check_install_locations(key, config_dict):
                        print(errors.format_error("Sequestrum", "Home Path Occupied"))
                        sys.exit()

            for key, value in config_dict['options'].items():
                if key.endswith("Package"):
                    if "commandsBefore" in value:
                        commands.run_commands(
                            config_dict['options'][key]["commandsBefore"])
                    setup_package(key, config_dict, dotfile_path)
                    if "commandsAfter" in value:
                        commands.run_commands(
                            config_dict['options'][key]["commandsAfter"])
        else:
            print(errors.format_error("Sequestrum",
                                      "uwu Another Impossible Safety Net owo"))

    # Install the files from the dotfiles. Symlinks the files from the
    # specified packages to the local system files. If the file or folder
    # already exists on the local system, delete it then symlink properly to
    # avoid errors.
    elif args[0] == "Install":
        # Install all packages
        if args[1] == "all":
            for key, value in config_dict['options'].items():
                if key.endswith("Package"):
                    if not check_install_locations(key, config_dict):
                        sys.exit()

            for key, value in config_dict['options'].items():
                if key.endswith("Package"):
                    if "commandsBefore" in value:
                        commands.run_commands(
                            config_dict['options'][key]['commandsBefore'], config_dict['options'][key]['package_name'])
                    install_package(key, config_dict, dotfile_path)
                    if "commandsAfter" in value:
                        commands.run_commands(
                            config_dict['options'][key]['commandsAfter'], config_dict['options'][key]['package_name'])

            logging.print_info("We are done!")

        # The option to only install one package instead of all your dotfiles.
        elif args[1] in package_list:
            for key, value in config_dict['options'].items():
                if key == args[1] + "Package":
                    if not check_install_locations(key, config_dict):
                        sys.exit()

            for key, value in config_dict['options'].items():
                if key == args[1] + "Package":
                    if "commandsBefore" in value:
                        commands.run_commands(
                            config_dict['options'][key]["commandsBefore"])
                    install_package(key, config_dict, dotfile_path)
                    if "commandsAfter" in value:
                        commands.run_commands(
                            config_dict['options'][key]["commandsAfter"])
        else:
            print(errors.format_error("Sequstrum", "Invalid Package."))

    # Refresh
    # -------
    # Refreshs the symlinks with the current file. This is so users don't have to manually
    # move files around and can instead manage their dotfiles in one file.
    # TODO: Remove files with warning if they are gone from the config
    elif args[0] == "Refresh":
        if args[1] == "all":
            for key, value in config_dict['options'].items():
                if key.endswith("Package"):
                    if "commandsBefore" in value:
                        commands.run_commands(
                            config_dict['options'][key]["commandsBefore"])
                    setup_package(key, config_dict, dotfile_path)
                    install_package(key, config_dict, dotfile_path)
                    if "commandsAfter" in value:
                        commands.run_commands(
                            config_dict['options'][key]["commandsAfter"])
        else:
            print(errors.format_error("Sequestrum", "Source code compromised."))

    # Unlink the source files. This doesn't really "unlink", instead it actually just
    # deletes the files. It collects a list of files to unlink then it goes through and
    # unlinks them all.
    elif args[0] == "Unlink":
        if args[1] == "all":
            for key, value in config_dict['options'].items():
                if key.endswith("Package"):
                    get_packages_to_unlink(key, config_dict, dotfile_path)
            unlink_packages()
        elif args[1] in package_list:
            for key, value in config_dict['options'].items():
                if key == args[1] + "Package":
                    get_packages_to_unlink(key, config_dict, dotfile_path)
            unlink_packages()
        else:
            print(errors.format_error("Sequestrum", "Invalid Package."))

    else:
        print(errors.format_error("Sequestrum", "Invalid Command"))


if __name__ == '__main__':
    main()
