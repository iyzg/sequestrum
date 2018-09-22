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
        config_dict = yaml.load(open("config.yaml", "r"))
    except Exception as error:
        logging.fatal("Could not open any configuration file: {}"
                      .format(error))

    # Internally use pkg name without suffix
    for key, _ in config_dict['options'].items():
        if key.endswith("Package"):
            config_dict['options'][key]['pkgName'] = key[:-7]

    # We need to have a base package
    if "base" not in config_dict['options']:
        logging.fatal(
            "Invalid config file, a base package needs to be defined")

    # TODO(nawuko): This looks ugly,
    # maybe use dictionary mapping?
    if args[0] == "Setup":
        commands.setup(args, config_dict)
    elif args[0] == "Install":
        commands.install(args, config_dict)
    elif args[0] == "Refresh":
        commands.refresh(args, config_dict)
    elif args[0] == "Backup":
        commands.backup(args, config_dict)
    elif args[0] == "Unlink":
        commands.unlink(args, config_dict)
    else:
        arguments.PARSER.print_usage()
        sys.exit(1)


if __name__ == '__main__':
    main()
