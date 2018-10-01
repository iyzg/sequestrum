# Commands Module

# Imports
import sequestrum.loggingmodule as logmod
from subprocess import run

def runCommands(unparsed_command_list, pkgName = None):
    """
        Runs commands passed in
    """

    for command in unparsed_command_list:
        parsed_command = command.split()

        try:
            runner = run(parsed_command)
        except Exception as error:
            logMod.printFatal(
                "Error occured during command \"{}\": {}".format(command, error), pkgName)
        else:
            logMod.printVerbose("Command \"{}\" finished with exit code: {}".format(
                command, runner.returncode), pkgName)
