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


def source_exists(source_path, ignore_symlinks=True):
    """
        Checks to see if symlink source exists
    """
    # Check if file exists
    if not os.path.lexists(source_path):
        return False

    # We cannot link symlinks
    if ignore_symlinks and os.path.islink(source_path):
        return False

    return True


def is_link(source_path):
    """
        Checks to see if the source_path is a symlink
    """
    if not os.path.lexists(source_path):
        return False

    return os.path.islink(source_path)


def get_dest(source_path):
    """
        Returns the destination of a symlink
    """
    if not is_link(source_path):
        return None

    return os.path.realpath(source_path)
