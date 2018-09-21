# Directory Module

# Libraries
import os
import shutil
import pathlib

from sequestrum import logging


def create_folder(path, pkgName=None):
    """
        Creates a folder
    """
    try:
        os.makedirs(path)
    except OSError as error:
        logging.error(
            "Could not create folder \"{}\" due to following error: {}"
            .format(path, error), pkgName)
    else:
        logging.debug(
            "Folder dosent exist and was created: {}".format(path), pkgName)


def create_parent_folder(path, pkgName):
    """
        Create Base directory if needed
    """
    basePath = pathlib.Path(path).parent

    # Check if the base folder is a file
    if basePath.exists():
        # Check if the parent is a file or if its a symlink
        if basePath.is_file() or basePath.is_symlink():
            logging.error(
                "Base directory is a file or link: {}"
                .format(basePath), pkgName)
            return False
        # If not, it must be a directory, so we are ok
        else:
            return True

    # Create path and parents (or ignore if folder already exists)
    try:
        basePath.mkdir(parents=True, exist_ok=True)
    except Exception as error:
        logging.error(
            "Could not create parent folder \"{}\" due to following error: {}"
            .format(basePath, error), pkgName)
        return False
    else:
        logging.debug(
            "Parent folder dosent exist and was created: {}"
            .format(basePath), pkgName)

    return True


def copy_file(source, destination, pkgName):
    """
        Copys file from source to destination
    """
    try:
        shutil.copyfile(source, destination)
    except OSError as error:
        logging.error("Unable to copy file: {}"
                      .format(error), pkgName)
        return False
    else:
        logging.debug("Copy file {} -> {}"
                      .format(source, destination), pkgName)
        return True


def copy_folder(source, destination, pkgName):
    """
        Copies frolder from source to destination
    """
    try:
        shutil.copytree(source, destination)
    except OSError as error:
        logging.error("Unable to copy directory: {}"
                      .format(error), pkgName)
        return False
    else:
        logging.debug("Copy folder {} -> {}"
                      .format(source, destination), pkgName)
        return True


# Delete Folder


def delete_folder(path, pkgName):
    """
        Deletes a folder
    """

    basePath = pathlib.Path(path)

    # We don't need todo anything
    if not basePath.exists():
        logging.debug("Cannot delete folder since it was not found: {}"
                      .format(basePath), pkgName)
        return True

    try:
        if basePath.is_symlink():
            basePath.unlink()
        else:
            shutil.rmtree(basePath)
    except OSError as error:
        logging.error("Deletion of folder failed: {}"
                      .format(error), pkgName)
        return False

    logging.debug("Deleted folder: {}".format(basePath), pkgName)
    return True

# Delete File


def delete_file(path, pkgName):
    """
        Deletes file
    """
    basePath = pathlib.Path(path)

    # We don't need todo anything
    if not basePath.exists():
        logging.debug("Cannot delete file since it was not found: {}"
                      .format(basePath), pkgName)
        return True

    try:
        basePath.unlink()
    except OSError as error:
        logging.error("Deletion of file failed: {}"
                      .format(error), pkgName)
        return False

    logging.debug("Deleted file: {}".format(basePath), pkgName)
    return True


def isfolder(path):
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


def isfile(path):
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
