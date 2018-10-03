# Logging module

import sys
from termcolor import cprint


def format_output(error_type, error_message, package_name=None):
    if package_name is not None and package_name is not "":
        return("[{}:{}] {}".format(error_type, package_name, error_message))
    else:
        return("[{}] {}".format(error_type, error_message))


def print_fatal(error_message, package_name=None):
    cprint(format_output("FATAL", error_message, package_name), 'red')
    sys.exit()


def print_error(error_message, package_name=None):
    cprint(format_output("ERROR", error_message, package_name), 'red')


def print_warn(error_message, package_name=None):
    cprint(format_output("WARN", error_message, package_name), 'yellow')


def print_info(error_message, package_name=None):
    cprint(format_output("INFO", error_message, package_name), 'green')


def print_verbose(error_message, package_name=None):
    cprint(format_output("VERBOSE", error_message, package_name), 'green')
