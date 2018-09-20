#!/usr/bin/env python3
#
# Sequestrum - Dotfile Manager

# Libraries
import sys
from pathlib import Path
import yaml

# Modules
import sequestrum.directoryModule as dirMod
import sequestrum.argumentsModule as argMod
import sequestrum.loggingModule as logMod
import sequestrum.packageModule as pkgMod

homePath = str(Path.home()) + "/"

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
                dirMod.deleteFolder(sourceFile, pkgName)
            elif dirMod.isFile(sourceFile):
                dirMod.copyFile(sourceFile, destFile, pkgName)
                dirMod.deleteFile(sourceFile, pkgName)
            else:
                return False

    return True


def main():

    # Grab user inputted arguments from the module
    # and make sure they entered some.
    arguments = argMod.getArguments()

    if arguments is None:
        argMod.PARSER.print_usage()
        sys.exit(0)

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
                    if not pkgMod.checkSourceLocations(value, dotfilePath,
                                                       inverted=True):
                        errorOccured = True

                    if not pkgMod.checkInstallLocations(value, inverted=True):
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
                    if not pkgMod.checkSourceLocations(value, dotfilePath):
                        errorOccured = True

                    if not pkgMod.checkInstallLocations(value):
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
                logMod.printSuccess("Packages got installed successfully!")

        # The option to only install one package instead of all your dotfiles.
        elif arguments[1] in packageList:

            fullPackageName = arguments[1] + "Package"
            pkgConfig = configDict['options'][fullPackageName]

            if not pkgMod.checkInstallLocations(pkgConfig):
                sys.exit()

            if not pkgMod.install(pkgConfig, dotfilePath):
                logMod.printWarn(
                    "Errors occured during installation, please check above")
            else:
                logMod.printSuccess("Package got installed successfully!")
        else:
            logMod.printError("Package {} was not found in config"
                              .format(arguments[1] + "Package"))

    # TODO: Fix
    elif arguments[0] == "Refresh":
        if arguments[1] == "all":
            logMod.printFatal("NYI")

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
                    if not pkgMod.checkSourceLocations(value, dotfilePath):
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
                logMod.printSuccess("Packages got backuped successfully!")

    # Unlink the source files. This doesn't really "unlink",
    # instead it actually just deletes the files.
    # It collects a list of files to unlink then
    # it goes through and unlinks them all.
    elif arguments[0] == "Unlink":
        if arguments[1] == "all":

            errorOccured = False

            for key, value in configDict['options'].items():
                if key.endswith("Package"):
                    if not pkgMod.uninstall(value):
                        errorOccured = True
                    else:
                        logMod.printInfo("Unlinked package sucessfully.",
                                         value['pkgName'])

            if errorOccured:
                logMod.printError("Could not unlink all files.")
            else:
                logMod.printSuccess("All packages got successfully unlinked.")

        elif arguments[1] in packageList:
            pkgConfig = configDict['options'][arguments[1] + "Package"]

            if not pkgMod.uninstall(pkgConfig):
                logMod.printError("Could not unlink all files.")
            else:
                logMod.printSuccess("All packages got successfully unlinked.")

        else:
            logMod.printError("Package {} was not found in config"
                              .format(arguments[1] + "Package"))
    else:
        logMod.printFatal("Invalid Command")


if __name__ == '__main__':
    main()
