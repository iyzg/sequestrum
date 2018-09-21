#!/usr/bin/env python3
#
# Sequestrum - Dotfile Manager

# Libraries
import sys
import yaml

# Modules
import sequestrum.argumentsModule as argMod
import sequestrum.loggingModule as logMod
import sequestrum.commandsModule as cmdMod


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

    # Internally use pkg name without suffix
    for key, _ in configDict['options'].items():
        if key.endswith("Package"):
            configDict['options'][key]['pkgName'] = key[:-7]

    # We need to have a base package
    if "base" not in configDict['options']:
        logMod.printFatal(
            "Invalid config file, a base package needs to be defined")

    # TODO(nawuko): This looks ugly, 
    # maybe use dictionary mapping?
    if arguments[0] == "Setup":
        cmdMod.commandSetup(arguments, configDict)
    elif arguments[0] == "Install":
        cmdMod.commandInstall(arguments, configDict)
    elif arguments[0] == "Refresh":
        cmdMod.commandRefresh(arguments, configDict)
    elif arguments[0] == "Backup":
        cmdMod.commandBackup(arguments, configDict)
    elif arguments[0] == "Unlink":
        cmdMod.commandUnlink(arguments, configDict)
    else:
        logMod.printFatal("Invalid Command")


if __name__ == '__main__':
    main()
