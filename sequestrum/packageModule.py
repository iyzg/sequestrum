from subprocess import run

import sequestrum.loggingModule as logMod
import sequestrum.symlinkModule as symMod
# import sequestrum.commandsModule as comMod
import sequestrum.directoryModule as dirMod

from pathlib import Path
homePath = str(Path.home()) + "/"


def checkLocation(pkgConfig, path, useSource=True, inverted=False):
    """
        Checks to see if link locations are clean
    """

    noErrors = True

    for link in pkgConfig['links']:
        for key, value in link.items():
            destLink = key if useSource else value
            direction = "Source" if useSource else "Dest"
            destPath = path + destLink
            pkgName = pkgConfig['pkgName']

            exists = symMod.symlinkSourceExists(destPath)

            if symMod.symlinkSourceExists(destPath) and not inverted:
                logMod.printError("{} file already exists: {}"
                                  .format(direction, destPath), pkgName)
                noErrors = False
            elif not exists and inverted:
                logMod.printError("{} file dosen't exists: {}"
                                  .format(direction, destPath), pkgName)
                noErrors = False

    return noErrors


def checkInstallLocations(pkgConfig, inverted=False):
    """
        Checks to see if link locations are clean
    """

    return checkLocation(pkgConfig, homePath, False, inverted)


def checkSourceLocations(pkgConfig, dotfilePath, inverted=False):
    """
        Check to see if dotfile locations are clean
    """
    directoryPath = dotfilePath + pkgConfig['directoryName'] + "/"
    return checkLocation(pkgConfig, directoryPath, True, not inverted)


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
                "Error occured during command \"{}\": {}"
                .format(command, error), pkgConfig['pkgName'])
            return False
        else:
            logMod.printVerbose(
                "Command \"{}\" finished with exit code: {}"
                .format(command, runner.returncode), pkgConfig['pkgName'])

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
            pkgName = pkgConfig['pkgName']

            # Create base folder if it dosent exist
            if dirMod.createBaseFolder(destFile, pkgName):
                # Create symlink, if it fails return false
                if not symMod.createSymlink(sourceFile, destFile, pkgName):
                    return False
            else:
                return False

    return True


def install(pkgConfig, dotfilePath):
    if not runCommands(pkgConfig, after=False):
        logMod.printError(
            "Abort installation of package due to \"commandsBefore\" Errors",
            pkgConfig['pkgName'])
        return False

    if not symlinkPackage(pkgConfig, dotfilePath):
        logMod.printError(
            "Abort installation of package due to Symlink Errors",
            pkgConfig['pkgName'])
        return False

    if not runCommands(pkgConfig, after=True):
        logMod.printError(
            "Abort installation of package due to \"commandsAfter\" Errors",
            pkgConfig['pkgName'])
        return False

    logMod.printInfo("Package was installed successfully",
                     pkgConfig['pkgName'])
    return True


def uninstall(pkgConfig):

    noErrors = True
    filesToUnlink = []
    pkgName = pkgConfig['pkgName']

    for link in pkgConfig['links']:
        for _, value in link.items():
            symlinkFile = homePath + value

            if symlinkFile not in filesToUnlink:
                filesToUnlink.append(symlinkFile)

    for symlinkFile in filesToUnlink:
        if dirMod.isFolder(symlinkFile):
            if not dirMod.deleteFolder(symlinkFile, pkgName):
                noErrors = False
        elif dirMod.isFile(symlinkFile):
            if not dirMod.deleteFile(symlinkFile, pkgName):
                noErrors = False

    return noErrors


def backup(pkgConfig, dotfilePath, backupPath):

    noErrors = True
    pkgName = pkgConfig['pkgName']

    for link in pkgConfig['links']:
        for key, value in link.items():
            sourceFile = homePath + value
            destFile = backupPath + key

            if dirMod.isFile(sourceFile):
                if not dirMod.copyFile(sourceFile, destFile, pkgName):
                    noErrors = False
            else:
                if not dirMod.copyFolder(sourceFile, destFile, pkgName):
                    noErrors = False

    return noErrors


def setup(packageKey, configDict, dotfilePath):
    """
        Setup package directory on dotfile
    """
    # Make a path for the new directory path using the name specified in the
    # config then make the folder using the path.
    pkgConfig = configDict['options'][packageKey]
    pkgName = pkgConfig['pkgName']
    newPackagePath = dotfilePath + pkgConfig['directoryName'] + "/"
    dirMod.createFolder(newPackagePath, pkgName)

    for link in pkgConfig['links']:
        for key, value in link.items():
            sourceFile = homePath + value
            destFile = newPackagePath + key

            if dirMod.isFolder(sourceFile):
                dirMod.copyFolder(sourceFile, destFile, pkgName)
                dirMod.deleteFolder(sourceFile, pkgName)
            elif dirMod.isFile(sourceFile):
                dirMod.copyFile(sourceFile, destFile, pkgName)
                dirMod.deleteFile(sourceFile, pkgName)
            else:
                return False

    return True
