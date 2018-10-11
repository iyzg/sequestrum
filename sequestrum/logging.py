# Logging module

from sys import exit


def format_output(error_type, error_message):
    """
        Formats the errors to look standard
    """
    return "[{}] {}".format(error_type, error_message)


def print_fatal(error_message):
    """
        Prints message with FATAL
    """
    print("\033[1;31mFATAL\033[0m {}".format(error_message))
    exit()


def print_error(error_message):
    """
        Prints message with ERROR
    """
    print("\033[1;31mERROR\033[0m {}".format(error_message))


def print_warn(error_message):
    """
        Prints message with WARN
    """
    print("\033[1;33mWARN\033[0m {}".format(error_message))


def print_info(error_message):
    """
        Prints message with INFO
    """
    print("\033[1;32mINFO\033[0m {}".format(error_message))

def print_verbose(error_message):
    """
        Prints message with green color to show success
    """
    print("\033[1;32mVERBOSE\033[0m {}".format(error_message))
