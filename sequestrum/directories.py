# Directory Module

# Libraries
import os
import shutil
import pathlib
import sequestrum.logging as logging


def current_path():
    """
        Returns the current path
    """
    return os.getcwd()


def create_folder(path):
    """
        Creates a folder
    """
    try:
        os.makedirs(path)
    except OSError as error:
        logging.print_error("Could not create folder \"{}\" due to following error: {}".format(path, error))
    else:
        logging.print_verbose("Folder doesn't exist and was created: {}".format(path))


def create_base_folder(path):
    """
        Create base directory if needed
    """

    basePath = pathlib.Path(path).parent

    # Check if the base folder is a file
    if basePath.exists():
        # Check if the parent is a file or if its a symlink
        if basePath.is_file() or basePath.is_symlink():
            logging.print_error("Base directory is a file or link: {}".format(basePath))
            return False
        # If not, it must be a directory, so we are ok
        else:
            return True

    # Create path and parents (or ignore if folder already exists)
    try:
        basePath.mkdir(parents=True, exist_ok=True)
    except Exception as error:
        logging.print_error("Could not create parent folder \"{}\" due to following error: {}".format(basePath, error))
        return False
    else:
        logging.print_verbose("Parent folder dosent exist and was created: {}".format(basePath))

    return True


def delete_folder(path):
    """
        Deletes a folder
    """

    basePath = pathlib.Path(path)

    if not basePath.exists():
        logging.print_error("Folder doesn't exist: {}".format(path))
        return

    try:
        if basePath.is_symlink():
            basePath.unlink()
        else:
            shutil.rmtree(basePath)
    except OSError as error:
        logging.print_error("Folder Deletion/Unsymlink Failed: {}".format(error))
    else:
        logging.print_verbose("Folder Deleted Successfully: {}".format(path))


def delete_file(path):
    """
        Deletes file
    """
    try:
        os.remove(path)
    except OSError as error:
        logging.print_error("File Deletion Failed: {}".format(path))
    else:
        logging.print_verbose("File Successfully Deleted: {}".format(path))


def is_folder(path):
    """
        Checks to see if path is a folder
    """
    try:
        if os.path.isdir(path):
            return True
        else:
            return False
    except OSError as error:
        logging.print_error("Path doesn't exist: {}".format(path))


def is_file(path):
    """
        Checks to see if path is a file
    """

    try:
        if os.path.isfile(path):
            return True
        else:
            return False
    except OSError as error:
        logging.print_error("Path doesn't exist: {}".format(path))

def grab_package_names(path):
    """
        Grabs package names from config
    """
    package_list = []
    for name in os.listdir(path):
        if os.path.isdir(path):
            package_list.append(name)

    return package_list
