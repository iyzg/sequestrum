# Arguments Modules

# Imports
import argparse
import sequestrum.loggingModule as logMod

PARSER = argparse.ArgumentParser()


def getArguments():
    """
        Return the arguments in the form of a tuple
    """

    commandGroup = PARSER.add_mutually_exclusive_group()
    commandGroup.add_argument("-b", "--backup", help="Backup files and tests your config.", action="store_true")
    commandGroup.add_argument("-i", "--install", help="Install packages onto local system. Use all to install all packages.")
    commandGroup.add_argument("-r", "--refresh", help="Refresh your dotfiles based on your config.", action="store_true")
    commandGroup.add_argument("-s", "--setup", help="Setup dotfile directory. Only run this once.", action="store_true")
    commandGroup.add_argument("-u", "--unlink", help="Unlink packages from local system. Use all to unlink all packages.")

    flagGroup = PARSER.add_argument_group()
    flagGroup.add_argument("--verbose", help="Enables verbose logging.", action="store_true")

    args = PARSER.parse_args()

    if not args.verbose:
        logMod.VERBOSE = False

    if args.install is not None:
        return ("Install", args.install)
    elif args.backup:
        return ("Backup", None)
    elif args.setup:
        return ("Setup", None)
    elif args.refresh:
        return ("Refresh", None)
    elif args.unlink is not None:
        return ("Unlink", args.unlink)
