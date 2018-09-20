#!/usr/bin/env python3
#
# Sequestrum - Dotfile Manager

# Libraries
import sys
from pathlib import Path
import yaml

homePath = str(Path.home()) + "/"

# Modules
import sequestrum.errorsModule as errMod
import sequestrum.directoryModule as dirMod
import sequestrum.symlinkModule as symMod
import sequestrum.argumentsModule as argMod
import sequestrum.commandsModule as comMod
import sequestrum.loggingModule as logMod


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
    if dirMod.isFile(newPackagePath) == False:
        dirMod.createFolder(newPackagePath, pkgName)

    for link in pkgConfig['links']:
        for key, value in link.items():
            sourceFile = homePath + value
            destFile = newPackagePath + key
            
            # Checks
            if dirMod.isFolder(destFile):
                continue
            elif dirmod.isFile(destFile):
                continue

            # Setup
            if dirMod.isFolder(sourceFile):
                symMod.copyFolder(sourceFile, destFile)
                dirMod.deleteFolder(sourceFile)
            elif dirMod.isFile(sourceFile):
                symMod.copyFile(sourceFile, destFile)
                dirMod.deleteFile(sourceFile)
            else:
                return False

    return True


# Grabs the directory of the key. For each item in the dotfile directory,
# properly symlink the file to the right place. If the file on the local
# system already exists. Delete the existing file before symlinking to
# prevent issues.


def installPackage(packageKey, configDict, dotfilePath):
    """
        Install package to local system
    """
    # Grab dotfile package directory
    pkgConfig = configDict['options'][packageKey]
    directoryPath = dotfilePath + pkgConfig['directoryName'] + "/"

    # Loop through files to link
    for link in pkgConfig['links']:
        # Symlink files to local files
        for key, value in link.items():
            sourceFile = directoryPath + key
            destFile = homePath + value

            if dirMod.createBaseFolder(destFile, pkgConfig['pkgName']):
                symMod.createSymlink(sourceFile, destFile, pkgConfig['pkgName'])
            else:
                return False

    return True


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
        else:
            print(errMod.formatError("Sequestrum", "Nothing to unlink!"))

# Goes through all the file locations that need to be empty for the
# symlinking to work and checks to see if they're empty. If they're not,
# it will return false. If it is clean, it'll return true.


def checkInstallLocations(packageKey, configDict):
    """
        Checks to see if link locations are clean
    """
    for link in configDict['options'][packageKey]['links']:
        for key, value in link.items():
            destPath = homePath + value
            if symMod.symlinkSourceExists(destPath):
                print(errMod.formatError(
                    "Safety", "{} already exists.".format(destPath)))
                return False

    return True

# Checks to see if the file locations in the dotfile repository exist. If
# they do, return false. If they don't, return true. This is to prevent
# overwriting of file that may or may not be important to the user.


def checkSourceLocations(packageKey, configDict, dotfilePath):
    """
        Check to see if dotfile locations are clean
    """
    directoryPath = dotfilePath + \
        configDict['options'][packageKey]['directoryName'] + "/"

    for link in configDict['options'][packageKey]['links']:
        for key, value in link.items():
            sourcePath = directoryPath + key

            if symMod.symlinkSourceExists(sourcePath):
                logMod.printFatal("File dosent exists: {}".format(sourcePath))


def main():

    # Grab user inputted arguments from the module and make sure they entered some.
    arguments = argMod.getArguments()

    if arguments is None:
        print(errMod.formatError("Arguments", "Must pass arguments"))
        sys.exit()

    try:
        configFile = open("config.yaml", "r")
    except:
        print(errMod.formatError("Core", "No configuration found."))
        sys.exit()

    configDict = yaml.load(configFile)
    packageList = []

    # Grab list of directories from the config.
    for key, value in configDict['options'].items():
        if key.endswith("Package"):
            friendlyName = key[:-7]
            configDict['options'][key]['pkgName'] = friendlyName
            packageList.append(friendlyName)

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
            for key, value in configDict['options'].items():
                if key.endswith("Package"):
                    if not checkSourceLocations(key, configDict, dotfilePath):
                        print(errMod.formatError("Sequestrum", "Dotfile Path Missing"))
                        sys.exit()

                    if not checkInstallLocations(key, configDict):
                        print(errMod.formatError("Sequestrum", "Home Path Occupied"))
                        sys.exit()

            for key, value in configDict['options'].items():
                if key.endswith("Package"):
                    if "commandsBefore" in value:
                        comMod.runCommands(
                            configDict['options'][key]["commandsBefore"])
                    setupPackage(key, configDict, dotfilePath)
                    if "commandsAfter" in value:
                        comMod.runCommands(
                            configDict['options'][key]["commandsAfter"])
        else:
            print(errMod.formatError("Sequestrum",
                                     "uwu Another Impossible Safety Net owo"))

    # Install the files from the dotfiles. Symlinks the files from the
    # specified packages to the local system files. If the file or folder
    # already exists on the local system, delete it then symlink properly to
    # avoid errors.
    elif arguments[0] == "Install":
        # Install all packages
        if arguments[1] == "all":
            for key, value in configDict['options'].items():
                if key.endswith("Package"):
                    if not checkInstallLocations(key, configDict):
                        sys.exit()

            for key, value in configDict['options'].items():
                if key.endswith("Package"):
                    if "commandsBefore" in value:
                        comMod.runCommands(
                            configDict['options'][key]['commandsBefore'], configDict['options'][key]['pkgName'])
                    installPackage(key, configDict, dotfilePath)
                    if "commandsAfter" in value:
                        comMod.runCommands(
                            configDict['options'][key]['commandsAfter'], configDict['options'][key]['pkgName'])

            logMod.printInfo("We are done!")

        # The option to only install one package instead of all your dotfiles.
        elif arguments[1] in packageList:
            for key, value in configDict['options'].items():
                if key == arguments[1] + "Package":
                    if not checkInstallLocations(key, configDict):
                        sys.exit()

            for key, value in configDict['options'].items():
                if key == arguments[1] + "Package":
                    if "commandsBefore" in value:
                        comMod.runCommands(
                            configDict['options'][key]["commandsBefore"])
                    installPackage(key, configDict, dotfilePath)
                    if "commandsAfter" in value:
                        comMod.runCommands(
                            configDict['options'][key]["commandsAfter"])
        else:
            print(errMod.formatError("Sequstrum", "Invalid Package."))

    # TODO: Fix
    elif arguments[0] == "Refresh":
        if arguments[1] == "all":
            dotfilePackageList = dirMod.grabPackageNames(dotfilePath)
            for key, value in configDict['options'].items():
                if key.endswith("Package"):
                    if "commandsBefore" in value:
                        comMod.runCommands(
                            configDict['options'][key]["commandsBefore"])
                    setupPackage(key, configDict, dotfilePath)
                    installPackage(key, configDict, dotfilePath)
                    if "commandsAfter" in value:
                        comMod.runCommands(
                            configDict['options'][key]["commandsAfter"])
        else:
            print(errMod.formatError("Sequestrum", "Source code compromised."))

    # Backs up your local files before you setup your dotfiles. This is also a
    # good way to check if your config files aer correct. If they aren't they won't
    # be backed up to your backup folder and throw an error instead.
    elif arguments[0] == "Backup":
        if arguments[1] == "all":
            backupPath = homePath + "sequestrum-backup/"
            if dirMod.isFolder(backupPath):
                print(errMod.formatError("Backup", "{} Exists".format(backupPath)))
                sys.exit()
            else:
                dirMod.createFolder(backupPath)
            for key, value in configDict['options'].items():
                if key.endswith("Package"):
                    for link in configDict['options'][key]['links']:
                        for key, value in link.items():
                            sourceFile = homePath + value
                            destFile = backupPath + key

                            if dirMod.isFile(sourceFile):
                                symMod.copyFile(sourceFile, destFile)
                            else:
                                print(errMod.formatError(
                                    "Backup", "{} doesn't exist."))
                                sys.exit()
            print(errMod.formatError("Backup", "All files backed up"))
        else:
            print(errMod.formatError("Sequestrum", "Source code compromised."))

    # Unlink the source files. This doesn't really "unlink", instead it actually just
    # deletes the files. It collects a list of files to unlink then it goes through and
    # unlinks them all.
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
            print(errMod.formatError("Sequestrum", "Invalid Package."))
    else:
        print(errMod.formatError("Sequestrum", "Invalid Command"))


if __name__ == '__main__':
