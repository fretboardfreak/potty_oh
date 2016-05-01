# Copyright 2016 Curtis Sand
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

"""common.py : helpful code that can be reused."""

import sys
import argparse


DEBUG = False
VERBOSE = False


def get_cmd_line_parser(version=None, *args, **kwargs):
    """Initialize a useful argument parser that can be reused."""
    parser = argparse.ArgumentParser(*args, **kwargs)
    if version:
        parser.add_argument(
            '--version', help='Print the version and exit.', action='version',
            version='%(prog)s {}'.format(version))
    DebugAction.add_parser_argument(parser)
    VerboseAction.add_parser_argument(parser)

    return parser


class ParserArguments(object):
    @staticmethod
    def set_defaults(parser, filename=None, length=None, plot=None,
                     frequency=None, debug=DEBUG, verbose=VERBOSE, **kwargs):
        parser.set_defaults(filename=filename, length=length,
                            frequency=frequency, debug=debug,
                            verbose=verbose, **kwargs)
        return parser

    @staticmethod
    def filename(parser):
        parser.add_argument(
            '--filename',
            help='File to write the generated waveform to.')
        return parser

    @staticmethod
    def length(parser):
        parser.add_argument(
            '-l', '--length', type=float,
            help='Length in seconds of the generated wav.')
        return parser

    @staticmethod
    def plot(parser):
        parser.add_argument(
            '-p', '--plot', help='Plot the waveform instead. '
            'Warning: Use a small length (e.g. 0.05) or the plot '
            'will be massive.', action='store_true')
        return parser

    @staticmethod
    def frequency(parser):
        parser.add_argument(
            '-f', '--frequency', help='Frequency to use.', type=float)
        return parser


def dprint(msg):
    """Conditionally print a debug message."""
    if DEBUG:
        print(msg)


def vprint(msg):
    """Conditionally print a verbose message."""
    if VERBOSE:
        print(msg)


class DebugAction(argparse.Action):
    """Enable the debugging output mechanism."""

    flag = '--debug'
    help = 'Enable debugging output.'

    @classmethod
    def add_parser_argument(cls, parser):
        parser.add_argument(cls.flag, help=cls.help, action=cls)

    def __init__(self, option_strings, dest, **kwargs):
        super(DebugAction, self).__init__(option_strings, dest, nargs=0,
                                          default=False, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print('Enabling debugging output.')
        global DEBUG
        DEBUG = True
        setattr(namespace, self.dest, True)


class VerboseAction(DebugAction):
    """Enable the verbose output mechanism."""

    flag = '--verbose'
    help = 'Enable verbose output.'

    def __call__(self, parser, namespace, values, option_string=None):
        print('Enabling verbose output.')
        global VERBOSE
        VERBOSE = True
        setattr(namespace, self.dest, True)


def call_main(main):
    """Call the main method for the script and handle the exit."""
    try:
        sys.exit(main())
    except SystemExit:
        sys.exit(0)
    except KeyboardInterrupt:
        print('...interrupted by user, exiting.')
        sys.exit(1)
    except Exception as exc:
        if DEBUG:
            raise
        else:
            print('Unhandled Error:\n{}'.format(exc))
            sys.exit(1)
