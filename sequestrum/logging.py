# Logging module

import sys
import time

def delay_print(string):
    for character in string:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.07)

    print("\n", end="")


def format_output(error_type, error_message, package_name=None):
    if package_name:
        return("[{}:{}] {}".format(error_type, package_name, error_message))
    else:
        return("[{}] {}".format(error_type, error_message))


def print_fatal(error_message, package_name=None):
    print("\033[1;31mFATAL\033[0m: {} {}".format(error_message, package_name))
    sys.exit()


def print_error(error_message, package_name=None):
    print("\033[1;31mERROR\033[0m: {} {}".format(error_message, package_name))


def print_warn(error_message, package_name=None):
    print("\033[1;33mWARN\033[0m: {} {}".format(error_message, package_name))


def print_info(error_message, package_name=None):
    print("\033[1;32mINFO\033[0m: {} {}".format(error_message, package_name))

def print_verbose(error_message, package_name=None):
    print("\033[1;32mVERBOSE\033[0m: {} {}".format(error_message, package_name))
