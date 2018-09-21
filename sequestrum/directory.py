import os
import shutil
import pathlib

from sequestrum import logging


def create_folder(path, pkg_name=None):
    """
        Creates a folder
    """
    try:
        os.makedirs(path)
    except OSError as error:
        logging.error(
            "Could not create folder \"{}\" due to following error: {}"
            .format(path, error), pkg_name)
    else:
        logging.debug(
            "Folder dosent exist and was created: {}".format(path), pkg_name)


def create_parent_folder(path, pkg_name):
    """
        Create Base directory if needed
    """
    parent_path = pathlib.Path(path).parent

    # Check if the base folder is a file
    if parent_path.exists():
        # Check if the parent is a file or if its a symlink
        if parent_path.is_file() or parent_path.is_symlink():
            logging.error(
                "Base directory is a file or link: {}"
                .format(parent_path), pkg_name)
            return False
        # If not, it must be a directory, so we are ok
        else:
            return True

    # Create path and parents (or ignore if folder already exists)
    try:
        parent_path.mkdir(parents=True, exist_ok=True)
    except Exception as error:
        logging.error(
            "Could not create parent folder \"{}\" due to following error: {}"
            .format(parent_path, error), pkg_name)
        return False
    else:
        logging.debug(
            "Parent folder dosent exist and was created: {}"
            .format(parent_path), pkg_name)

    return True


def copy_file(source, destination, pkg_name):
    """
        Copys file from source to destination
    """
    try:
        shutil.copyfile(source, destination)
    except OSError as error:
        logging.error("Unable to copy file: {}"
                      .format(error), pkg_name)
        return False
    else:
        logging.debug("Copy file {} -> {}"
                      .format(source, destination), pkg_name)
        return True


def copy_folder(source, destination, pkg_name):
    """
        Copies frolder from source to destination
    """
    try:
        shutil.copytree(source, destination)
    except OSError as error:
        logging.error("Unable to copy directory: {}"
                      .format(error), pkg_name)
        return False
    else:
        logging.debug("Copy folder {} -> {}"
                      .format(source, destination), pkg_name)
        return True


def delete_folder(path, pkg_name):
    """
        Deletes a folder
    """
    base_path = pathlib.Path(path)

    # We don't need todo anything
    if not base_path.exists():
        logging.debug("Cannot delete folder since it was not found: {}"
                      .format(base_path), pkg_name)
        return True

    try:
        if base_path.is_symlink():
            base_path.unlink()
        else:
            shutil.rmtree(base_path)
    except OSError as error:
        logging.error("Deletion of folder failed: {}"
                      .format(error), pkg_name)
        return False

    logging.debug("Deleted folder: {}".format(base_path), pkg_name)
    return True


def delete_file(path, pkg_name):
    """
        Deletes file
    """
    base_path = pathlib.Path(path)

    # We don't need todo anything
    if not base_path.exists():
        logging.debug("Cannot delete file since it was not found: {}"
                      .format(base_path), pkg_name)
        return True

    try:
        base_path.unlink()
    except OSError as error:
        logging.error("Deletion of file failed: {}"
                      .format(error), pkg_name)
        return False

    logging.debug("Deleted file: {}".format(base_path), pkg_name)
    return True


def isfolder(path):
    """
        Checks to see if path is a folder
    """
    try:
        if os.path.isdir(path):
            return True
    except OSError as error:
        logging.error("Error during isfolder check: {}".format(error))

    return False


def isfile(path):
    """
        Checks to see if path is a file
    """
    try:
        if os.path.isfile(path):
            return True
    except OSError as error:
        logging.error("Error during isfile check: {}".format(error))

    return False
