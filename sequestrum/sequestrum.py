import sys
import yaml

from sequestrum import arguments
from sequestrum import logging
from sequestrum import commands


def main():

    # Grab user inputted arguments from the module
    # and make sure they entered some.
    args = arguments.get_arguments()

    if args is None:
        arguments.PARSER.print_usage()
        sys.exit(1)

    try:
        configFile = open("config.yaml", "r")
    except Exception as error:
        logging.fatal("Could not open any configuration file: {}"
                      .format(error))

    configDict = yaml.load(configFile)

    # Internally use pkg name without suffix
    for key, _ in configDict['options'].items():
        if key.endswith("Package"):
            configDict['options'][key]['pkgName'] = key[:-7]

    # We need to have a base package
    if "base" not in configDict['options']:
        logging.fatal(
            "Invalid config file, a base package needs to be defined")

    # TODO(nawuko): This looks ugly,
    # maybe use dictionary mapping?
    if args[0] == "Setup":
        commands.setup(args, configDict)
    elif args[0] == "Install":
        commands.install(args, configDict)
    elif args[0] == "Refresh":
        commands.refresh(args, configDict)
    elif args[0] == "Backup":
        commands.backup(args, configDict)
    elif args[0] == "Unlink":
        commands.unlink(args, configDict)
    else:
        arguments.PARSER.print_usage()
        sys.exit(1)


if __name__ == '__main__':
    main()
