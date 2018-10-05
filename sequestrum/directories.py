# Directory Module

# Libraries
import os
import shutil
import pathlib
import logging


def current_path():
    """
        Returns the current path
    """
    return os.getcwd()


def create_folder(path, package_name):
    """
        Creates a folder
    """
    try:
        os.makedirs(path)
    except OSError as error:
        logging.print_error("Could not create folder \"{}\" due to following error: {}".format(path, error), package_name)
    else:
        logging.print_verbose("Folder doesn't exist and was created: {}".format(path), package_name)


def create_base_folder(path, package_name):
    """
        Create base directory if needed
    """

    basePath = pathlib.Path(path).parent

    # Check if the base folder is a file
    if basePath.exists():
        # Check if the parent is a file or if its a symlink
        if basePath.is_file() or basePath.is_symlink():
            logging.print_error("Base directory is a file or link: {}".format(basePath), package_name)
            return False
        # If not, it must be a directory, so we are ok
        else:
            return True

    # Create path and parents (or ignore if folder already exists)
    try:
        basePath.mkdir(parents=True, exist_ok=True)
    except Exception as error:
        logging.print_error("Could not create parent folder \"{}\" due to following error: {}".format(basePath, error), package_name)
        return False
    else:
        logging.print_verbose("Parent folder dosent exist and was created: {}".format(basePath), package_name)

    return True


def delete_folder(path):
    """
        Deletes a folder
    """

    basePath = pathlib.Path(path)

    if not basePath.exists():
        print("Sequestrum: Folder already deleted!")
        return

    try:
        if basePath.is_symlink():
            basePath.unlink()
        else:
            shutil.rmtree(basePath)
    except OSError as error:
        print("Sequestrum: Deletion of folder failed: {}".format(error))
    else:
        print("Sequestrum: Deleted successfully!")


def delete_file(path):
    """
        Deletes file
    """
    try:
        os.remove(path)
    except OSError:
        print("REmoving of file failed")
    else:
        print("Successfully removed file")


def is_folder(path):
    """
        Checks to see if path is a folder
    """
    try:
        if os.path.isdir(path):
            return True
        else:
            return False
    except OSError:
        print("Sequestum: Folder checking failed")


def is_file(path):
    """
        Checks to see if path is a file
    """

    try:
        if os.path.isfile(path):
            return True
        else:
            return False
    except OSError:
        print("Sequestrum: File check failed")


def grab_package_names(path):
    """
        Grabs package names from config
    """
    package_list = []
    for name in os.listdir(path):
        if os.path.isdir(path):
            package_list.append(name)

    return package_list
