# Logging module
import os
import sys

VERBOSE = True
COLORS = dict(
    list(zip([
        'grey',
        'red',
        'green',
        'yellow',
        'blue',
        'magenta',
        'cyan',
        'white',
    ],
        list(range(30, 38))
    ))
)
COLOR_RESET = '\033[0m'


def printColor(text, color=None):
    if os.getenv('ANSI_COLORS_DISABLED') is None:
        fmt_str = '\033[%dm%s'
        if color is not None:
            text = fmt_str % (COLORS[color], text)

        text += COLOR_RESET
    print(text)


def formatOutput(errorType, errorMessage, pkgName=None):
    if pkgName is not None and pkgName is not "":
        return("[{}:{}] {}".format(errorType, pkgName, errorMessage))
    else:
        return("[{}] {}".format(errorType, errorMessage))


def printFatal(errorMessage, pkgName=None):
    printColor(formatOutput("FATAL", errorMessage, pkgName), 'red')
    sys.exit(1)


def printError(errorMessage, pkgName=None):
    printColor(formatOutput("ERROR", errorMessage, pkgName), 'red')


def printWarn(errorMessage, pkgName=None):
    printColor(formatOutput("WARN", errorMessage, pkgName), 'yellow')


def printInfo(errorMessage, pkgName=None):
    printColor(formatOutput("INFO", errorMessage, pkgName), 'white')


def printSuccess(errorMessage, pkgName=None):
    printColor(formatOutput("INFO", errorMessage, pkgName), 'green')


def printVerbose(errorMessage, pkgName=None):
    if VERBOSE:
        printColor(formatOutput("VERBOSE", errorMessage, pkgName), 'cyan')
