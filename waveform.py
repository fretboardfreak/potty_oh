#!/usr/bin/env python
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

"""A Waveform or Signal Generator Library for creating audio waveforms."""

import math

import numpy

VERSION = "0.1"


class Generator(object):
    def __init__(self, length=1.0, framerate=44100, verbose=False):
        self.length = length
        self.framerate = framerate
        self.verbose = verbose

    def _init(self, length=None, framerate=None, verbose=None, **kwargs):
        if length:
            self.length = length
        if framerate:
            self.framerate = framerate
        if verbose:
            self.verbose = verbose

        # framecount = frames/sec * sec
        self.framecount = int(self.framerate * self.length)
        # rectify length to actual framecount
        self.length = float(self.framecount)/self.framerate
        self.dprint('framecount = %s' % self.framecount)
        self.dprint('rectified length = %s' % self.length)
        self.wavedata = numpy.zeros((self.framecount, 1))

    def dprint(self, msg):
        """Conditionally print a debugging message."""
        if self.verbose:
            print(msg)

    def whitenoise(self, *args, **kwargs):
        """Random Gaussian White Noise."""
        self._init(*args, **kwargs)
        self.wavedata = numpy.random.randn(self.framecount, 1)
        return self.wavedata

    def _sinusoid_amplitude(self, frame, frequency):
        """Calculate the amplitude of a sinusoid wave at a given frequency."""
        # avoid divide by zero
        frame = 0.001 if frame is 0 else frame
        return math.sin(frame /
                        ((self.framerate / frequency) / math.pi))

    def sin_constant(self, frequency, *args, **kwargs):
        """Sinusoid wave of constant frequency."""
        self._init(*args, **kwargs)
        frequency = float(frequency)
        for frame in range(self.framecount):
            amplitude = self._sinusoid_amplitude(frame, frequency)
            self.wavedata[frame, 0] = amplitude
        return self.wavedata

    def sin_linear(self, start_freq, end_freq, *args, **kwargs):
        """Sinusoid wave of linearly changing frequency."""
        self._init(*args, **kwargs)
        for frame in range(self.framecount):
            # freq = start_freq + frame * freq_rate
            # freq_rate = total_freq_change / framecount
            frequency = start_freq + frame * (
                float(end_freq - start_freq) / self.framecount)
            amplitude = self._sinusoid_amplitude(frame, frequency)
            self.wavedata[frame, 0] = amplitude
        return self.wavedata


if __name__ == '__main__':
    import common

    DESC = "A Demonstration Program for the Signal Generator."

    def whitenoise(args, generator):
        generator.whitenoise()

    def sin_constant(args, generator):
        generator.sin_constant(args.frequency)

    def sin_linear(args, generator):
        generator.sin_linear(args.frequency/2, args.frequency*2)

    UI_MAP = {'noise': whitenoise, 'constant': sin_constant,
              'linear': sin_linear}

    def main():
        parser = common.get_cmd_line_parser(description=DESC,
                                           version=VERSION)
        parser.add_argument(
            '-t', '--type', help='Type of signal to generate',
            choices=UI_MAP.keys())
        common.ParserArguments.filename(parser)
        common.ParserArguments.length(parser)
        common.ParserArguments.plot(parser)
        common.ParserArguments.frequency(parser)
        common.ParserArguments.set_defaults(parser, filename='signal.wav',
                                            length=1.0, frequency=480,
                                            type='constant')
        args = parser.parse_args()

        sg = Generator(length=args.length, verbose=args.debug)

        UI_MAP[args.type](args, sg)

        if args.plot:
            import plot
            plot.plot_waveform(sg.wavedata, 1, 0, sg.framecount)
        else:
            import wav_file
            wfile = wav_file.WavFile(args.filename, 1, sg.framecount)
            try:
                wfile.write(sg.wavedata)
            finally:
                wfile.close()

        return 0

    common.call_main(main)
