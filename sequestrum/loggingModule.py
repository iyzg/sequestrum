# Logging module

import sys
from termcolor import cprint


def formatOutput(errorType, errorMessage, pkgName=None):
    if pkgName is not None and pkgName is not "":
        return("[{}:{}] {}".format(errorType, pkgName, errorMessage))
    else:
        return("[{}] {}".format(errorType, errorMessage))


def printFatal(errorMessage, pkgName=None):
    cprint(formatOutput("FATAL", errorMessage, pkgName), 'red')
    sys.exit()


def printError(errorMessage, pkgName=None):
    cprint(formatOutput("ERROR", errorMessage, pkgName), 'red')


def printWarn(errorMessage, pkgName=None):
    cprint(formatOutput("WARN", errorMessage, pkgName), 'yellow')


def printInfo(errorMessage, pkgName=None):
    cprint(formatOutput("INFO", errorMessage, pkgName), 'green')


def printVerbose(errorMessage, pkgName=None):
    cprint(formatOutput("VERBOSE", errorMessage, pkgName), 'green')
