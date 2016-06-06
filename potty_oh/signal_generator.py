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

"""A library of Audio Signal Generators for making digital noises."""

import math
import numpy
from scipy import fftpack

from .common import defaults
from .waveform import Waveform
from .effects import normalize


class Generator(object):
    """A Basic Signal Generator.

    Each signal produced is generated independently of previously generated
    signals.
    """
    def __init__(self, length=None, framerate=None, verbose=False):
        self.length = length
        if not length:
            self.length = defaults.length
        self.framerate = framerate
        if not framerate:
            self.framerate = defaults.framerate
        self.verbose = verbose

    def _init(self, length=None, framerate=None, verbose=None, **kwargs):
        if length:
            self.length = length
        if framerate:
            self.framerate = framerate
        if verbose:
            self.verbose = verbose

        # framecount = frames / sec * sec
        self.framecount = int(self.framerate * self.length)
        # rectify length to actual framecount
        self.length = float(self.framecount) / self.framerate
        self.dprint('generating %s frames' % self.framecount)
        self.wavedata = numpy.zeros(self.framecount)
        if 'phase' in kwargs:
            self.random_phase_shift = kwargs['phase']
        else:
            self.random_phase_shift = numpy.random.random() * 2 * math.pi

    @property
    def waveform(self):
        return Waveform(self.wavedata, self.framerate)

    def dprint(self, msg):
        """Conditionally print a debugging message."""
        if self.verbose:
            print(msg)

    def whitenoise(self, *args, **kwargs):
        """Random Gaussian White Noise."""
        self._init(*args, **kwargs)
        self.wavedata = numpy.random.randn(self.framecount)
        return self.wavedata

    def _sinusoid_amplitude(self, frame, frequency):
        """Calculate the amplitude of a sinusoid wave at a given frequency."""
        return math.sin(
            self.random_phase_shift +
            frame / ((self.framerate / frequency) / math.pi))

    def sin_constant(self, frequency, *args, **kwargs):
        """Sinusoid wave of constant frequency."""
        self._init(*args, **kwargs)
        frequency = float(frequency)
        for frame in range(len(self.wavedata)):
            amplitude = self._sinusoid_amplitude(frame, frequency)
            self.wavedata[frame] = amplitude
        return self.waveform

    def sin_linear(self, start_freq, end_freq, *args, **kwargs):
        """Sinusoid wave of linearly changing frequency."""
        self._init(*args, **kwargs)
        for frame in range(len(self.wavedata)):
            # freq = start_freq + frame * freq_rate
            # freq_rate = total_freq_change / framecount
            frequency = start_freq + frame * (
                float(end_freq - start_freq) / self.framecount)
            amplitude = self._sinusoid_amplitude(frame, frequency)
            self.wavedata[frame] = amplitude
        return self.waveform


class FFTGenerator(Generator):
    '''
    '''
    def __init__(self, length=None, framerate=None, verbose=False):
        self.approx_desired_precision = 10
        self.length = length
        if not length:
            self.length = defaults.length
        self.framerate = framerate
        if not framerate:
            self.framerate = defaults.framerate
        self.verbose = verbose

    @property
    def window_size(self):
        return int(self.framerate / 2 / self.approx_desired_precision)

    @property
    def frequencies(self):
        return fftpack.fftfreq(int(self.window_size / 2),
                               1.0 / self.framerate)

    def _get_frequency_bin(self, requested_freq):
        """Find the FFT bin corresponding closest to requested frequency."""
        diff = 20000  # Need large value, 20KHz is high enough
        closest_index = None
        for index, freq in enumerate(self.frequencies):
            if freq < 0:
                continue
            tmp_diff = abs(requested_freq - freq)
            if tmp_diff < diff:
                diff = tmp_diff
                closest_index = index
        return closest_index

    def single_frequency(self, frequency, **kwargs):
        super(FFTGenerator, self)._init(**kwargs)
        # TODO: this is only generating a short waveform, something is still
        #       not quite right here...
        ifft_bin = self._get_frequency_bin(frequency)
        self.wavedata[ifft_bin] = self.framerate
        return fftpack.ifft(self.wavedata)

    def multi_frequency(self, frequencies, **kwargs):
        super(FFTGenerator, self)._init(**kwargs)
        # TODO: this is only generating a short waveform, something is still
        #       not quite right here...
        for frequency in frequencies:
            ifft_bin = self._get_frequency_bin(frequency)
            self.wavedata[ifft_bin] = self.framerate
        self.wavedata = normalize(numpy.real(fftpack.ifft(self.wavedata)))
        return self.waveform
