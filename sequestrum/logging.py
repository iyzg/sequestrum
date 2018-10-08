# Logging module

import sys
import time

def delay_print(string):
    for character in string:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.07)

    print("\n", end="")


def format_output(error_type, error_message):
        return("[{}] {}".format(error_type, error_message))


def print_fatal(error_message):
    print("\033[1;31mFATAL\033[0m {}".format(error_message))
    sys.exit()


def print_error(error_message):
    print("\033[1;31mERROR\033[0m {}".format(error_message))


def print_warn(error_message):
    print("\033[1;33mWARN\033[0m {}".format(error_message))


def print_info(error_message):
    print("\033[1;32mINFO\033[0m {}".format(error_message))

def print_verbose(error_message):
    print("\033[1;32mVERBOSE\033[0m {}".format(error_message))
