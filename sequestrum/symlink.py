import os

from sequestrum import logging


def create(source_path, dest_path, pkg_name=None):
    """
        Creates symlink from source to destination
    """
    try:
        os.symlink(source_path, dest_path)
    except OSError as error:
        logging.error("Unable to create symlink: {}"
                      .format(error), pkg_name)
        return False
    else:
        logging.debug("Linking {} <-> {}"
                      .format(source_path, dest_path), pkg_name)
        return True


def source_exists(source_path):
    """
        Checks to see if symlink source exists
    """
    # Check if file exists
    if not os.path.exists(source_path):
        return False

    # We cannot link symlinks
    if os.path.islink(source_path):
        return False

    return True
