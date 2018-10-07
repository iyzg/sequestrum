# Commands Module

# Imports
from subprocess import run
import sequestrum.logging as logging


def run_commands(unparsed_command_list, package_name=None):
    """
        Runs commands passed in
    """

    for command in unparsed_command_list:
        parsed_command = command.split()

        try:
            runner = run(parsed_command)
        except Exception as error:
            logging.print_fatal("Error occured during command \"{}\": {}".format(command, error), package_name)
        else:
            logging.print_verbose("Command \"{}\" finished with exit code: {}".format(command, runner.returncode), package_name)
