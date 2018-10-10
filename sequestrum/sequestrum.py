# Libraries
from pathlib import Path
import sys
from time import sleep
import yaml

# Modules
import sequestrum.directories as directories
import sequestrum.symlink as symlink
import sequestrum.arguments as arguments
import sequestrum.options as options
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
    new_package_path = dotfile_path + package_config['directoryName'] + "/"
    if directories.is_folder(new_package_path) is False:
        directories.create_folder(new_package_path)

    for link in package_config['links']:
        for key, value in link.items():
            source_file = HOME_PATH + value
            dest_file = new_package_path + key

            # Checks
            if directories.is_folder(dest_file):
                logging.print_warn("Folder exists, skipping: {}".format(dest_file))
                continue
            elif directories.is_file(dest_file):
                logging.print_warn("File exists, skipping: {}".format(dest_file))
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
                logging.print_warn("Folder exists, skipping: {}".format(dest_file))
                continue
            elif directories.is_file(dest_file):
                logging.print_warn("File exists, skipping: {}".format(dest_file))
                continue

            if directories.create_base_folder(dest_file):
                symlink.create_symlink(source_file, dest_file)
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
            logging.print_error("Nothing to unlink")

# Goes through all the file locations that need to be empty for the
# symlinking to work and checks to see if they're empty. If they're not,
# it will return false. If it is clean, it'll return true.


def check_localfile_locations(package_key, config_dict, mode=None):
    """
        Checks local file locations
    """
    
    if mode is None:
        logging.print_fatal("No mode provided to check")

    for link in config_dict['options'][package_key]['links']:
        for key, value in link.items():
            destPath = HOME_PATH + value
            
            if mode == "Clean":
                if symlink.symlink_source_exists(destPath):
                    logging.print_fatal("Local file location occupied: {}".format(destPath))
                    return False
            elif mode == "Dirty":
                if not symlink.symlink_source_exists(destPath):
                    logging.print_fatal("Local file location empty: {}".format(destPath))
                    return False

    return True

# Checks to see if the file locations in the dotfile repository exist. If
# they do, return false. If they don't, return true. This is to prevent
# overwriting of file that may or may not be important to the user.


def check_dotfile_locations(package_key, config_dict, dotfile_path, mode=None):
    """
        Checks dotfile locations
    """

    if mode is None:
        logging.print_fatal("No mode provided to check")

    directory_path = dotfile_path + \
        config_dict['options'][package_key]['directoryName'] + "/"

    for link in config_dict['options'][package_key]['links']:
        for key, value in link.items():
            sourcePath = directory_path + key
            
            if mode == "Clean":
                if symlink.symlink_source_exists(sourcePath):
                    logging.print_fatal("Dotfile location occupied: {}".format(sourcePath))
                    return False
            if mode == "Dirty":
                if not symlink.symlink_source_exists(sourcePath):
                    logging.print_fatal("Dotfile location empty: {}".format(sourcePath))
                    return False
    
    return True
    


def main():
    # Grab user inputted args from the module and make sure they entered some.
    args = arguments.get_arguments()

    if args is None:
        logging.print_error("Must pass arguments")
        sys.exit()

    config_file = None
    config_dict = {}
    package_list = []

    try:
        config_file = open("config.yaml", "r")
    except:
        logging.print_error("No configuration found")
        sys.exit()

    config_dict = yaml.load(config_file)

    # Grab list of directories from the config.
    for key, value in config_dict['options'].items():
        if key.endswith("Package"):
            friendly_name = key[:-7]
            config_dict['options'][key]['package_name'] = friendly_name
            package_list.append(friendly_name)

    # Error checking for proper config
    if "base" not in config_dict['options']:
        logging.print_fatal(
            "Invalid config file, a base package needs to be defined")
    elif "dotfileDirectory" not in config_dict['options']['base']:
        logging.print_fatal("Missing dotfileDirectory in base package")

    # Grab the path of the dotfile directory
    dotfile_path = HOME_PATH + \
        config_dict['options']['base']['dotfileDirectory'] + "/"

    # Install the files from the dotfiles. Symlinks the files from the
    # specified packages to the local system files. If the file or folder
    # already exists on the local system, delete it then symlink properly to
    # avoid errors.
    if args[0] == "Install":
        # Install all packages
        if args[1] == "all":
            for key, value in config_dict['options'].items():
                if key.endswith("Package"):
                    check_dotfile_locations(key, config_dict, dotfile_path, "Dirty")

            for key, value in config_dict['options'].items():
                if key.endswith("Package"):
                    if "commandsBefore" in value:
                        options.run_commands(
                            config_dict['options'][key]['commandsBefore'], config_dict['options'][key]['package_name'])
                    install_package(key, config_dict, dotfile_path)
                    if "commandsAfter" in value:
                        options.run_commands(
                            config_dict['options'][key]['commandsAfter'], config_dict['options'][key]['package_name'])

            logging.print_info("Complete installation complete")

        # The option to only install one package instead of all your dotfiles.
        elif args[1] in package_list:
            for key, value in config_dict['options'].items():
                if key == args[1] + "Package":
                    check_dotfile_locations(key, config_dict, dotfile_path, "Dirty")

            for key, value in config_dict['options'].items():
                if key == args[1] + "Package":
                    if "commandsBefore" in value:
                        options.run_commands(
                            config_dict['options'][key]["commandsBefore"])
                    install_package(key, config_dict, dotfile_path)
                    if "commandsAfter" in value:
                        options.run_commands(
                            config_dict['options'][key]["commandsAfter"])

            logging.print_info("{} installation complete".format(args[1]))
        else:
            logging.print_error("Invalid Package")

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
                        options.run_commands(
                            config_dict['options'][key]["commandsBefore"])
                    setup_package(key, config_dict, dotfile_path)
                    if "commandsAfter" in value:
                        options.run_commands(
                            config_dict['options'][key]["commandsAfter"])

            logging.print_info("Dotfile refresh complete")
        else:
            logging.print_error("Error 102 Please report to GH")

    # Unlink the source files. This doesn't really "unlink", instead it actually just
    # deletes the files. It collects a list of files to unlink then it goes through and
    # unlinks them all.
    # TODO: Add safety to make sure both the files exist
    elif args[0] == "Unlink":
        if args[1] == "all":
            for key, value in config_dict['options'].items():
                if key.endswith("Package"):
                    get_packages_to_unlink(key, config_dict, dotfile_path)
            unlink_packages()
            logging.print_info("Completele unlink complete")
        elif args[1] in package_list:
            for key, value in config_dict['options'].items():
                if key == args[1] + "Package":
                    get_packages_to_unlink(key, config_dict, dotfile_path)
            unlink_packages()
            logging.print_info("{} unlink complete".format(args[1]))
        else:
            logging.print_error("Invalid Package")

    else:
        logging.print_error("Invalid Command")


if __name__ == '__main__':
    main()
