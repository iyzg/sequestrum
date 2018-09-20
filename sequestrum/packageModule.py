from subprocess import run

import sequestrum.loggingModule as logMod
import sequestrum.symlinkModule as symMod
import sequestrum.commandsModule as comMod
import sequestrum.directoryModule as dirMod

from pathlib import Path
homePath = str(Path.home()) + "/"


def runCommands(pkgConfig, after):

    unparsedCommands = None

    # Use commandsBefore list when after is false
    if "commandsBefore" in pkgConfig and not after:
        unparsedCommands = pkgConfig['commandsBefore']

    # Use commandsAfter list when after is true
    if "commandsAfter" in pkgConfig and after:
        unparsedCommands = pkgConfig['commandsAfter']

    # Check if we have something todo
    if unparsedCommands is None:
        return True

    for command in unparsedCommands:
        parsedCommand = command.split()

        try:
            runner = run(parsedCommand)
        except Exception as error:
            logMod.printError(
                "Error occured during command \"{}\": {}".format(command, error), pkgConfig['pkgName'])
            return False
        else:
            logMod.printVerbose("Command \"{}\" finished with exit code: {}".format(
                command, runner.returncode), pkgConfig['pkgName'])

    return True


def symlinkPackage(pkgConfig, dotfilePath):
    """
        Symlink package to local system
    """
    # Grab dotfile package directory
    directoryPath = dotfilePath + pkgConfig['directoryName'] + "/"

    # Loop through files to link
    for link in pkgConfig['links']:
        # Symlink files to local files
        for key, value in link.items():
            sourceFile = directoryPath + key
            destFile = homePath + value

            # Create base folder if it dosent exist
            if dirMod.createBaseFolder(destFile, pkgConfig['pkgName']):
                # Create symlink, if it fails return false
                if not symMod.createSymlink(sourceFile, destFile, pkgConfig['pkgName']):
                    return False
            else:
                return False

    return True


def installPackage(pkgConfig, dotfilePath):
    if not runCommands(pkgConfig, after=False):
        logMod.printError(
            "Abort installation of package due to \"commandsBefore\" Errors", pkgConfig['pkgName'])
        return False

    if not symlinkPackage(pkgConfig, dotfilePath):
        logMod.printError(
            "Abort installation of package due to Symlink Errors", pkgConfig['pkgName'])
        return False

    if not runCommands(pkgConfig, after=True):
        logMod.printError(
            "Abort installation of package due to \"commandsAfter\" Errors", pkgConfig['pkgName'])
        return False
    else:
        logMod.printInfo("Package was installed successfully",
                         pkgConfig['pkgName'])
