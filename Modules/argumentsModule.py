# Arguments Modules

# Imports
import argparse

def getArguments():
    """
        Return the arguments in the form of a tuple
    """
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()

    group.add_argument("-i", "--install", help="Install packages onto local system. Use all to install all packages.")
    group.add_argument("-s", "--setup", help="Setup dotfile directory.", action="store_true")

    args = parser.parse_args()

    if args.install != None:
        return ("Install", args.install)
    elif args.setup:
        return ("Setup", "all")
