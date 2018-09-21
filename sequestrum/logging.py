# Logging module
import os
import sys

VERBOSE = True
_COLORS = dict(
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
_COLOR_RESET = '\033[0m'


def _format_color(text, color=None):
    if os.getenv('ANSI_COLORS_DISABLED') is None:
        fmt_str = '\033[%dm%s'
        if color is not None:
            text = fmt_str % (_COLORS[color], text)

        text += _COLOR_RESET
    print(text)


def _format_output(errorType, errorMessage, pkgName=None):
    if pkgName is not None and pkgName is not "":
        return("[{}:{}] {}".format(errorType, pkgName, errorMessage))
    else:
        return("[{}] {}".format(errorType, errorMessage))


def fatal(errorMessage, pkgName=None):
    _format_color(_format_output("FATAL", errorMessage, pkgName), 'red')
    sys.exit(1)


def error(errorMessage, pkgName=None):
    _format_color(_format_output("ERROR", errorMessage, pkgName), 'red')


def warn(errorMessage, pkgName=None):
    _format_color(_format_output("WARN", errorMessage, pkgName), 'yellow')


def info(errorMessage, pkgName=None):
    _format_color(_format_output("INFO", errorMessage, pkgName), 'white')


def success(errorMessage, pkgName=None):
    _format_color(_format_output("INFO", errorMessage, pkgName), 'green')


def debug(errorMessage, pkgName=None):
    if VERBOSE:
        _format_color(_format_output("VERBOSE", errorMessage, pkgName), 'cyan')
