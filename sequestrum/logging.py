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


def _format_output(level, text, pkg_name=None):
    if pkg_name is not None and pkg_name is not "":
        return("[{}:{}] {}".format(level, pkg_name, text))
    else:
        return("[{}] {}".format(level, text))


def fatal(text, pkg_name=None):
    _format_color(_format_output("FATAL", text, pkg_name), 'red')
    sys.exit(1)


def error(text, pkg_name=None):
    _format_color(_format_output("ERROR", text, pkg_name), 'red')


def warn(text, pkg_name=None):
    _format_color(_format_output("WARN", text, pkg_name), 'yellow')


def info(text, pkg_name=None):
    _format_color(_format_output("INFO", text, pkg_name), 'white')


def success(text, pkg_name=None):
    _format_color(_format_output("INFO", text, pkg_name), 'green')


def debug(text, pkg_name=None):
    if VERBOSE:
        _format_color(_format_output("VERBOSE", text, pkg_name), 'cyan')
