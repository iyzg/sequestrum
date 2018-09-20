# Logging module

import sys


def formatOutput(errorType, errorMessage, pkgName=None):
    if pkgName is not None and pkgName is not "":
        return("[{}:{}] {}".format(errorType, pkgName, errorMessage))
    else:
        return("[{}] {}".format(errorType, errorMessage))


def printFatal(errorMessage, pkgName=None):
    print(formatOutput("FATAL", errorMessage, pkgName))
    sys.exit()


def printError(errorMessage, pkgName=None):
    print(formatOutput("ERROR", errorMessage, pkgName))


def printWarn(errorMessage, pkgName=None):
    print(formatOutput("WARN", errorMessage, pkgName))


def printInfo(errorMessage, pkgName=None):
    print(formatOutput("INFO", errorMessage, pkgName))


def printVerbose(errorMessage, pkgName=None):
    print(formatOutput("VERBOSE", errorMessage, pkgName))
