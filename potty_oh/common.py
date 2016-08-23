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


class _Defaults:
    tempo = 100
    framerate = 44100
    channels = 1
    frequency = 440.0
    length = 1.0
    filename = 'signal.wav'
    debug = False
    verbose = False

# Use an instance instead of class type so any changes to the defaults will be
# available in other modules.
defaults = _Defaults()


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
    def modify_argument(parser, arg_name, attribute, new_value):
        """This is probably not safe/advised, but I'm doing it anyway."""
        for action in parser._actions:
            if action.dest == arg_name:
                setattr(action, attribute, new_value)
                return

    @staticmethod
    def set_defaults(parser, filename=None, length=None, plot=None,
                     frequency=None, tempo=None, debug=None, verbose=None,
                     framerate=None, **kwargs):
        if not filename:
            filename = defaults.filename
        if not length:
            length = defaults.length
        if not frequency:
            # TODO: split up pitch module so this doesn't have to be literal
            frequency = defaults.frequency
        if not tempo:
            tempo = defaults.tempo
        if not debug:
            debug = defaults.debug
        if not verbose:
            verbose = defaults.verbose
        if not framerate:
            framerate = defaults.framerate
        parser.set_defaults(filename=filename, length=length,
                            frequency=frequency, debug=debug, tempo=tempo,
                            verbose=verbose, framerate=framerate, **kwargs)
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

    @staticmethod
    def tempo(parser):
        parser.add_argument(
            '-t', '--tempo', type=int,
            help='Tempo to use for the generated signals.')
        return parser

    @staticmethod
    def framerate(parser):
        parser.add_argument(
            '-F', '--framerate', help='framerate to use.', type=int)
        return parser

    @staticmethod
    def best(parser):
        parser.add_argument(
            '--best', action='store_true',
            help=('Use best algorithm implemented so far instead of '
                  'the original one available when the experiment '
                  'was first tried.'))

def dprint(msg):
    """Conditionally print a debug message."""
    if defaults.debug:
        print('debug: %s' % msg)


def vprint(msg):
    """Conditionally print a verbose message."""
    if defaults.verbose:
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
        defaults.debug = True
        setattr(namespace, self.dest, True)


class VerboseAction(DebugAction):
    """Enable the verbose output mechanism."""

    flag = '--verbose'
    help = 'Enable verbose output.'

    def __call__(self, parser, namespace, values, option_string=None):
        print('Enabling verbose output.')
        defaults.verbose = True
        setattr(namespace, self.dest, True)


def call_main(main):
    """Call the main method for the script and handle the exit."""
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except KeyboardInterrupt:
        print('...interrupted by user, exiting.')
        sys.exit(1)
    except Exception as exc:
        if defaults.debug:
            raise
        else:
            print('Unhandled Error:\n{}'.format(exc))
            sys.exit(1)
