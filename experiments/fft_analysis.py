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

"""An experiment to help figure out how to use FFT analysis calculations."""

from potty_oh.common import get_cmd_line_parser
from potty_oh.common import call_main
from potty_oh.common import ParserArguments
from potty_oh.common import defaults
from potty_oh.signal_generator import Generator
from potty_oh.analysis import analyze_window


def main():
    parser = get_cmd_line_parser(description=__doc__)
    parser = ParserArguments.filename(parser)
    parser = ParserArguments.plot(parser)
    parser = ParserArguments.framerate(parser)
    parser = ParserArguments.set_defaults(parser)
    args = parser.parse_args()
    defaults.framerate = args.framerate

    sig_gen = Generator(verbose=args.debug)

    print('1 second waveform at 1000Hz')
    frequency_powers = analyze_window(
        sig_gen.sin_constant(1000))
    print("Frequency Powers found by FFT: ", frequency_powers)

    print('\n0.5 second waveform at 880Hz')
    frequency_powers = analyze_window(
        sig_gen.sin_constant(880, length=0.5))
    print("Frequency Powers found by FFT: ", frequency_powers)

    print('\n0.75 second waveform at 1234Hz')
    frequency_powers = analyze_window(
        sig_gen.sin_constant(1234, length=0.75))
    tmp = list(frequency_powers.items())
    tmp.sort(key=lambda x: x[1], reverse=True)
    print('{} present non-zero frequencies in signal. The most '
          'powerfull frequencies are:\n{}'.format(
              len(frequency_powers), '\n'.join([str(t) for t in tmp[:10]])))

    return 0


if __name__ == "__main__":
    call_main(main)
