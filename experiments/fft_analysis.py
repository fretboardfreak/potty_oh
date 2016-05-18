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

from math import sqrt
from numpy import round
from scipy import fft

from potty_oh.common import get_cmd_line_parser
from potty_oh.common import call_main
from potty_oh.signal_generator import Generator


def analyze_waveform(waveform):
    power_coefficients = [sqrt(pow(x.real, 2) + pow(x.imag, 2))
                          for x in fft(waveform.frames)]
    bins = int(len(power_coefficients)/2)
    power_domain = round(power_coefficients[:bins])

    niq_freq = waveform.framerate / 2.0  # max representable frequency
    precision = niq_freq / bins  # step in Hz per FFT bin
    print('{} samples at a framerate of {} samp/sec:\n  max_freq {}, '
          'precision {}'.format(len(waveform.frames), waveform.framerate,
                                niq_freq, precision))

    powers = {(waveform.framerate * (index / niq_freq) * precision): strength
              for index, strength in enumerate(power_domain)
              if strength != 0.0}
    return powers


def main():
    parser = get_cmd_line_parser(description=__doc__)
    args = parser.parse_args()

    sig_gen = Generator(verbose=args.debug)

    print('1 second waveform at 1000Hz')
    frequency_powers = analyze_waveform(sig_gen.sin_constant(1000))
    print("Frequency Powers found by FFT: ", frequency_powers)

    print('\n0.5 second waveform at 880Hz')
    frequency_powers = analyze_waveform(sig_gen.sin_constant(880, length=0.5))
    print("Frequency Powers found by FFT: ", frequency_powers)

    print('\n0.25 second waveform at 2000Hz')
    frequency_powers = analyze_waveform(
        sig_gen.sin_constant(2000, length=0.25))
    print("Frequency Powers found by FFT: ", frequency_powers)

    return 0


if __name__ == "__main__":
    call_main(main)
