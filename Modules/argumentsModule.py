#!/usr/bin/python
#
# Arguments Module

# Libraries
import sys

arguments = len(sys.argv) - 1

def getArguments():
    """
        Returns arguments
    """
    numberOfArguments = len(sys.argv) - 1

    if numberOfArguments == 1:
        return (sys.argv[1], "all")
    elif numberOfArguments == 2:
        return (sys.argv[1], sys.argv[2])
    else:
        print("Pass Arguments F0ol.")
        sys.exit()
        return None
