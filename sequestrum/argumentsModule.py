# Arguments Modules

# Imports
import argparse
import sequestrum.loggingModule as logMod


def getArguments():
    """
        Return the arguments in the form of a tuple
    """
    parser = argparse.ArgumentParser()

    commandGroup = parser.add_mutually_exclusive_group()
    commandGroup.add_argument("-b", "--backup", help="Backup files and tests your config.", action="store_true")
    commandGroup.add_argument("-i", "--install", help="Install packages onto local system. Use all to install all packages.")
    commandGroup.add_argument("-r", "--refresh", help="Refresh your dotfiles based on your config.", action="store_true")
    commandGroup.add_argument("-s", "--setup", help="Setup dotfile directory. Only run this once.", action="store_true")
    commandGroup.add_argument("-u", "--unlink", help="Unlink packages from local system. Use all to unlink all packages.")
    
    flagGroup = parser.add_argument_group()
    flagGroup.add_argument("--verbose", help="Enables verbose logging.", action="store_true")

    args = parser.parse_args()

    if not args.verbose:
        logMod.VERBOSE = False

    if args.install is not None:
        return ("Install", args.install)
    elif args.backup:
        return ("Backup", "all")
    elif args.setup:
        return ("Setup", "all")
    elif args.refresh:
        return ("Refresh", "all")
    elif args.unlink is not None:
        return ("Unlink", args.unlink)
