#!/usr/bin/env python3
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

"""A basic Signal Generator program."""

from potty_oh import common
from potty_oh.waveform import Generator


def whitenoise(args, generator):
    """Generate some whitenoise."""
    generator.whitenoise()


def sin_constant(args, generator):
    """Generate a constant frequency sinusoid."""
    generator.sin_constant(args.frequency)


def sin_linear(args, generator):
    """Generate a sinusoid with linearly changing frequency."""
    generator.sin_linear(args.frequency / 2, args.frequency * 2)


def main():
    ui_map = {'noise': whitenoise, 'constant': sin_constant,
              'linear': sin_linear}

    parser = common.get_cmd_line_parser(description=__doc__)
    parser.add_argument(
        '-t', '--type', help='Type of signal to generate',
        choices=ui_map.keys())
    common.ParserArguments.filename(parser)
    common.ParserArguments.length(parser)
    common.ParserArguments.plot(parser)
    common.ParserArguments.frequency(parser)
    common.ParserArguments.set_defaults(parser, type='constant')
    args = parser.parse_args()

    sg = Generator(length=args.length, verbose=args.debug)

    ui_map[args.type](args, sg)
    waveform = sg.waveform

    if args.plot:
        import potty_oh.plot as plot
        plot.plot_waveform(waveform.frames, waveform.channels, 0, 4000)
    else:
        from potty_oh.wav_file import wav_file_context
        with wav_file_context(args.filename) as fout:
            fout.write_frames(waveform.frames)

    return 0


if __name__ == "__main__":
    common.call_main(main)
