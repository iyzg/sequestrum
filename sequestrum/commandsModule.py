import sys
from pathlib import Path

import sequestrum.loggingModule as logMod
import sequestrum.packageModule as pkgMod
import sequestrum.directoryModule as dirMod

homePath = str(Path.home()) + "/"


# Creates a new directory. It creates a new folder path using the config
# then creates a new folder using that path. It then loops through each
# link in the links list and **copies** (not symlinking) the original file
# on the source system over to the dotfiles.
def commandSetup(arguments, configDict):
    # Grab the path of the dotfile directory
    dotfilePath = homePath + \
        configDict['options']['base']['dotfileDirectory'] + "/"
    errorOccured = False

    for key, value in configDict['options'].items():
        if key.endswith("Package"):
            if not pkgMod.checkSourceLocations(value, dotfilePath,
                                               inverted=True):
                errorOccured = True

            if not pkgMod.checkInstallLocations(value, inverted=True):
                errorOccured = True

    if errorOccured:
        logMod.printFatal("Could not setup due to config errors.")

    errorOccured = False

    for key, value in configDict['options'].items():
        if key.endswith("Package"):
            if not pkgMod.setup(key, configDict, dotfilePath):
                errorOccured = True

    if errorOccured:
        logMod.printFatal(
            "Could not setup due errors. Please see errors above")
    else:
        logMod.printSuccess("Setup was successfull, running installation ...")
        commandInstall(('Install', 'all'), configDict)


# Install the files from the dotfiles. Symlinks the files from the
# specified packages to the local system files. If the file or folder
# already exists on the local system, delete it then symlink properly to
# avoid errors.
def commandInstall(arguments, configDict):
    # Grab the path of the dotfile directory
    dotfilePath = homePath + \
        configDict['options']['base']['dotfileDirectory'] + "/"
    fullPackageName = arguments[1] + "Package"
    errorOccured = False

    if fullPackageName == "allPackage":
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
    elif fullPackageName in configDict['options']:

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
def commandRefresh(arguments, configDict):
    logMod.printFatal("NYI")


# Backs up your local files before you setup your dotfiles. This is also a
# good way to check if your config files aer correct
# If they aren't they won't be backed up to your backup folder
# and throw an error instead.
def commandBackup(arguments, configDict):
    # Grab the path of the dotfile directory
    dotfilePath = homePath + \
        configDict['options']['base']['dotfileDirectory'] + "/"
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
def commandUnlink(arguments, configDict):
    fullPackageName = arguments[1] + "Package"

    if fullPackageName == "allPackage":

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

    elif fullPackageName in configDict['options']:
        pkgConfig = configDict['options'][fullPackageName]

        if not pkgMod.uninstall(pkgConfig):
            logMod.printError("Could not unlink all files.")
        else:
            logMod.printSuccess("All packages got successfully unlinked.")

    else:
        logMod.printError("Package {} was not found in config"
                          .format(arguments[1] + "Package"))
