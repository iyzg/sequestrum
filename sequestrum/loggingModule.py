# Logging module

import sys

def formatOutput(errorType, errorMessage, pkgName=None):
    if pkgName:
        return("[{}:{}] {}".format(errorType, pkgName, errorMessage))
    else:
        return("[{}] {}".format(errorType, errorMessage))


def printFatal(errorMessage, pkgname=None):
    print("\033[1;31mFATAL\033[0m: {} {}".format(errorMessage, pkgName))
    sys.exit()


def printError(errorMessage, pkgName=None):
    print("\033[1;31mERROR\033[0m: {} {}".format(errorMessage, pkgName))


def printWarn(errorMessage, pkgName=None):
    print("\033[1;33mWARN\033[0m: {} {}".format(errorMessage, pkgName))

def printInfo(errorMessage, pkgName=None):
    print("\033[1;32mINFO\033[0m: {} {}".format(errorMessage, pkgName))


def printVerbose(errorMessage, pkgName=None):
    print("\033[1;32mVERBOSE\033[0m: {} {}".format(errorMessage, pkgName))
