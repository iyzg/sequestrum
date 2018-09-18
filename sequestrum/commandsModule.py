# Commands Module

# Imports
from subprocess import run
import sequestrum.loggingModule as logMod

# Functions
# Run Commands


def runCommands(unparsedCommandList, pkgName = None):
    """
        Runs commands passed in
    """

    for command in unparsedCommandList:
        parsedCommand = command.split()

        try:
            runner = run(parsedCommand)
        except Exception as error:
            logMod.printFatal(
                "Error occured during command \"{}\": {}".format(command, error), pkgName)
        else:
            logMod.printVerbose("Command \"{}\" finished with exit code: {}".format(
                command, runner.returncode), pkgName)
