#!/usr/bin/env python3
#
# Sequestrum - Dotfile Manager

# Libraries
import sys
from pathlib import Path
import yaml

# Modules
import sequestrum.directoryModule as dirMod
import sequestrum.symlinkModule as symMod
import sequestrum.argumentsModule as argMod
import sequestrum.commandsModule as comMod
import sequestrum.loggingModule as logMod
import sequestrum.packageModule as pkgMod

homePath = str(Path.home()) + "/"

# For Later
packagesToUnlink = []

# Creates a new directory. It creates a new folder path using the config
# then creates a new folder using that path. It then loops through each
# link in the links list and **copies** (not symlinking) the original file
# on the source system over to the dotfiles.


def setupPackage(packageKey, configDict, dotfilePath):
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
                dirMod.deleteFolder(sourceFile)
            elif dirMod.isFile(sourceFile):
                dirMod.copyFile(sourceFile, destFile, pkgName)
                dirMod.deleteFile(sourceFile)
            else:
                return False

    return True


# Grabs the directory of the key. For each item in the dotfile directory,
# properly symlink the file to the right place. If the file on the local
# system already exists. Delete the existing file before symlinking to
# prevent issues.

def GetPackagesToUnlink(packageKey, configDict, dotfilePath):
    """
        Grab packages and put them into a list ( NO DUPES )
    """
    pkgConfig = configDict['options'][packageKey]

    for link in pkgConfig['links']:
        for _, value in link.items():
            fileToGrab = homePath + value

            if fileToGrab not in packagesToUnlink:
                packagesToUnlink.append(fileToGrab)


def UnlinkPackages():
    """
        Unlink all files in packagesToUnlink
    """
    for path in packagesToUnlink:
        if dirMod.isFolder(path):
            dirMod.deleteFolder(path)
        elif dirMod.isFile(path):
            dirMod.deleteFile(path)
        # else:
        #    print(errMod.formatError("Sequestrum", "Nothing to unlink!"))

# Goes through all the file locations that need to be empty for the
# symlinking to work and checks to see if they're empty. If they're not,
# it will return false. If it is clean, it'll return true.


def checkInstallLocations(pkgConfig):
    """
        Checks to see if link locations are clean
    """

    noErrors = True

    for link in pkgConfig['links']:
        for _, value in link.items():
            destPath = homePath + value

            if symMod.symlinkSourceExists(destPath):
                logMod.printError("File already exists: {}"
                                  .format(destPath), pkgConfig['pkgName'])
                noErrors = False

    return noErrors

# Checks to see if the file locations in the dotfile repository exist. If
# they do, return false. If they don't, return true. This is to prevent
# overwriting of file that may or may not be important to the user.


def checkSourceLocations(pkgConfig, dotfilePath):
    """
        Check to see if dotfile locations are clean
    """
    directoryPath = dotfilePath + pkgConfig['directoryName'] + "/"

    noErrors = True

    for link in pkgConfig['links']:
        for key, _ in link.items():
            sourcePath = directoryPath + key

            if not symMod.symlinkSourceExists(sourcePath):
                logMod.printError("File dosen't exists: {}"
                                  .format(sourcePath), pkgConfig['pkgName'])
                noErrors = False

    return noErrors


def main():

    # Grab user inputted arguments from the module
    # and make sure they entered some.
    arguments = argMod.getArguments()

    if arguments is None:
        logMod.printFatal("Must pass arguments")

    try:
        configFile = open("config.yaml", "r")
    except Exception as error:
        logMod.printFatal("Could not open any configuration file: {}"
                          .format(error))

    configDict = yaml.load(configFile)
    packageList = []

    # Grab list of directories from the config.
    for key, value in configDict['options'].items():
        if key.endswith("Package"):
            pkgName = key[:-7]
            configDict['options'][key]['pkgName'] = pkgName
            packageList.append(pkgName)

    # We need to have a base package
    if "base" not in configDict['options']:
        logMod.printFatal(
            "Invalid config file, a base package needs to be defined")

    # Grab the path of the dotfile directory
    dotfilePath = homePath + \
        configDict['options']['base']['dotfileDirectory'] + "/"

    # Setups up the dotfiles accordingly to the config. This should only be
    # ran once to setup your dotfiles with the right directories. After this,
    # users should use the update argument to update their dotfiles with new
    # packages.
    if arguments[0] == "Setup":
        if arguments[1] == "all":

            errorOccured = False

            for key, value in configDict['options'].items():
                if key.endswith("Package"):
                    if not checkSourceLocations(value, dotfilePath):
                        errorOccured = True

                    if not checkInstallLocations(value):
                        errorOccured = True

            if errorOccured:
                logMod.printFatal("Could not setup due errors.")

            errorOccured = False

            for key, value in configDict['options'].items():
                if key.endswith("Package"):
                    if pkgMod.runCommands(value, after=False):
                        if setupPackage(key, configDict, dotfilePath):
                            pkgMod.runCommands(value, after=True)

    # Install the files from the dotfiles. Symlinks the files from the
    # specified packages to the local system files. If the file or folder
    # already exists on the local system, delete it then symlink properly to
    # avoid errors.
    elif arguments[0] == "Install":
        # Install all packages
        if arguments[1] == "all":

            errorOccured = False

            for key, value in configDict['options'].items():
                if key.endswith("Package"):
                    if not checkSourceLocations(value, dotfilePath):
                        errorOccured = True

                    if not checkInstallLocations(value):
                        errorOccured = True

            if errorOccured:
                logMod.printFatal("Could not install due errors.")

            errorOccured = False

            for key, value in configDict['options'].items():
                if key.endswith("Package"):
                    if not pkgMod.install(value, dotfilePath):
                        errorOccured = True

            if errorOccured:
                logMod.printWarn(
                    "Errors occured during installation, please check above")
            else:
                logMod.printInfo("Packages got installed successfully!")

        # The option to only install one package instead of all your dotfiles.
        elif arguments[1] in packageList:

            fullPackageName = arguments[1] + "Package"
            pkgConfig = configDict['options'].items()[fullPackageName]

            if not checkInstallLocations(pkgConfig):
                sys.exit()

            if not pkgMod.install(pkgConfig, dotfilePath):
                logMod.printWarn(
                    "Errors occured during installation, please check above")
            else:
                logMod.printInfo("Package got installed successfully!")
        else:
            logMod.printError(
                "Package {} was not found in config".format(fullPackageName))

    # TODO: Fix
    elif arguments[0] == "Refresh":
        if arguments[1] == "all":
            dotfilePackageList = dirMod.grabPackageNames(dotfilePath)
            for key, value in configDict['options'].items():
                if key.endswith("Package"):
                    if key[:-7] not in dotfilePackageList:
                        if "commandsBefore" in value:
                            comMod.runCommands(
                                configDict['options'][key]["commandsBefore"])
                        # InstallPackage(key, configDict, dotfilePath)
                        if "commandsAfter" in value:
                            comMod.runCommands(
                                configDict['options'][key]["commandsAfter"])

    # Backs up your local files before you setup your dotfiles. This is also a
    # good way to check if your config files aer correct
    # If they aren't they won't be backed up to your backup folder
    # and throw an error instead.
    elif arguments[0] == "Backup":
        if arguments[1] == "all":
            backupPath = homePath + "sequestrum-backup/"

            if dirMod.isFolder(backupPath):
                logMod.printFatal("Backup folder {} already exists"
                                  .format(backupPath))
            else:
                dirMod.createFolder(backupPath)

            errorOccured = False

            for key, value in configDict['options'].items():
                if key.endswith("Package"):
                    if not checkSourceLocations(value, dotfilePath):
                        errorOccured = True

            if errorOccured:
                logMod.printFatal("Could not backup due to missing files.")

            errorOccured = False

            for key, value in configDict['options'].items():
                if key.endswith("Package"):
                    if not pkgMod.backup(value, dotfilePath, backupPath):
                        errorOccured = True

            if errorOccured:
                logMod.printWarn(
                    "Errors occured during backup, please check above")
            else:
                logMod.printInfo("Packages got backuped successfully!")

    # Unlink the source files. This doesn't really "unlink",
    # instead it actually just deletes the files.
    # It collects a list of files to unlink then
    # it goes through and unlinks them all.
    elif arguments[0] == "Unlink":
        if arguments[1] == "all":
            for key, value in configDict['options'].items():
                if key.endswith("Package"):
                    GetPackagesToUnlink(key, configDict, dotfilePath)
            UnlinkPackages()
        elif arguments[1] in packageList:
            for key, value in configDict['options'].items():
                if key == arguments[1] + "Package":
                    GetPackagesToUnlink(key, configDict, dotfilePath)
            UnlinkPackages()
        else:
            logMod.printFatal("Invalid Package.")
    else:
        logMod.printFatal("Invalid Command")


if __name__ == '__main__':
    main()
