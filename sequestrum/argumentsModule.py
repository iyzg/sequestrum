# Arguments Modules

# Imports
import argparse

def getArguments():
    """
        Return the arguments in the form of a tuple
    """
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()

    group.add_argument("-b", "--backup", help="Backup files and tests your config.", action="store_true")
    group.add_argument("-i", "--install", help="Install packages onto local system. Use all to install all packages.")
    group.add_argument("-r", "--refresh", help="Refresh your dotfiles based on your config.", action="store_true")
    group.add_argument("-s", "--setup", help="Setup dotfile directory. Only run this once.", action="store_true")
    group.add_argument("-u", "--unlink", help="Unlink packages from local system. Use all to unlink all packages.")

    args = parser.parse_args()

    if args.install != None:
        return ("Install", args.install)
    elif args.backup:
        return ("Backup", "all")
    elif args.setup:
        return ("Setup", "all")
    elif args.refresh:
        return ("Refresh", "all")
    elif args.unlink != None:
        return ("Unlink", args.unlink)
