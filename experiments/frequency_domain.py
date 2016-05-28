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

"""An experiment to help better understand the frequency domain."""

from math import pi
from numpy import real, imag
from matplotlib import pyplot

from potty_oh.common import get_cmd_line_parser
from potty_oh.common import call_main
from potty_oh.common import ParserArguments
from potty_oh.common import defaults
from potty_oh.signal_generator import Generator
from potty_oh.analysis import do_fft


def main():
    parser = get_cmd_line_parser(description=__doc__)
    parser = ParserArguments.filename(parser)
    parser = ParserArguments.plot(parser)
    parser = ParserArguments.framerate(parser)
    parser = ParserArguments.set_defaults(parser)
    parser.add_argument(
        '--phase', help="Run the experiment with a given phase value.",
        type=float, default=0.0)
    args = parser.parse_args()
    defaults.framerate = args.framerate

    sig_gen = Generator(verbose=args.debug)

    phase = 0 if not hasattr(args, 'phase') else args.phase
    signal = sig_gen.sin_constant(440, length=0.05, phase=phase % (2 * pi))

    freq, power_domain, freq_domain = do_fft(signal)

    try:
        _, subplots = pyplot.subplots(1, 2)
        subplots[0].plot(power_domain)
        subplots[0].set_title('Power Domain')
        subplots[1].plot(freq_domain)
        subplots[1].set_title('Freq Domain')
        pyplot.show()

        _, subplots = pyplot.subplots(1, 2)
        subplots[0].plot(real(freq_domain))
        subplots[0].set_title('Real Freq. Domain')
        subplots[1].plot(imag(freq_domain))
        subplots[1].set_title('Imaginary Freq. Domain')
        pyplot.show()
    finally:
        pyplot.close()

    return 0


if __name__ == "__main__":
    call_main(main)
