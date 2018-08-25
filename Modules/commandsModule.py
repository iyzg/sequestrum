# Commands Module

# Imports
from subprocess import run

# Functions
# Run Commands


def runCommands(unparsedCommandList):
    """
        Runs commands passed in
    """
    for command in unparsedCommandList:
        parsedCommand = command.split()
        run(parsedCommand)
