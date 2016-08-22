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
import cmath
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
    def __init__(self, length=None, framerate=None, verbose=False,
                 fade_percentage=None):
        self.length = length
        if not length:
            self.length = defaults.length
        self.framerate = framerate
        if not framerate:
            self.framerate = defaults.framerate
        self.verbose = verbose
        self.fade_percentage = fade_percentage if fade_percentage else 0.02

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
            self.phase = kwargs['phase']
        else:
            self.phase = numpy.random.random() * 2 * math.pi

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

    def _sinusoid_angle(self, frame, frequency):
        """Calculate the sinusoid angle for a given frame and frequency."""
        return 2 * math.pi * frequency * frame / self.framerate

    def _sinusoid_value(self, frame, frequency):
        """Calculate the value of a sinusoid wave at a given frequency."""
        return math.sin(self.phase + self._sinusoid_angle(frame, frequency))

    def sin_constant(self, frequency, *args, **kwargs):
        """Sinusoid wave of constant frequency."""
        self._init(*args, **kwargs)
        frequency = float(frequency)
        fade_frames = self.fade_percentage * self.framecount
        fade_point = self.framecount - fade_frames
        for frame in range(self.framecount):
            value = self._sinusoid_value(frame, frequency)
            if frame > fade_point:  # fade the end of the note
                _old = value
                value *= 1 - (frame - fade_point) / fade_frames
                if frame % 50 == 0:
                    self.dprint('fade from %s to %s' % (_old, value))
            if frame < fade_frames:
                _old = value
                value *= frame / fade_frames
            self.wavedata[frame] = value
        return self.waveform

    def sin_linear(self, start_freq, end_freq, *args, **kwargs):
        """Sinusoid wave of linearly changing frequency."""
        self._init(*args, **kwargs)
        for frame in range(len(self.wavedata)):
            frequency = start_freq + frame * (
                float(end_freq - start_freq) / self.framecount)
            value = self._sinusoid_value(frame, frequency)
            self.wavedata[frame] = value
        return self.waveform


class FFTGenerator(Generator):
    '''Use an Inverse Fourier Transform to create a multifrequency sinusoid.

    The generated sinusoid is a single waveform comprised of multiple
    frequencies that were not generated as their own fundamental waveforms
    first.
    '''
    def __init__(self, length=None, framerate=None, verbose=False):
        self.approx_desired_precision = 10  # Hz
        self.length = length
        if not length:
            self.length = defaults.length
        self.framerate = framerate
        if not framerate:
            self.framerate = defaults.framerate
        self.verbose = verbose

    @property
    def window_size(self):
        """Length of a window size as determined by the desired precision."""
        return int(self.framerate / 2 / self.approx_desired_precision)

    @property
    def new_window(self):
        """Create a new empty array for a window."""
        return numpy.zeros(self.window_size)

    @property
    def frequencies(self):
        """The frequencies mapped to bins in the frequency domain."""
        return fftpack.fftfreq(self.window_size, 1.0 / self.framerate)

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
        self.dprint('using bin %s for freq %s' %
                    (closest_index, requested_freq))
        return closest_index

    def generate(self, frequencies, **kwargs):
        """Generate the requested waveform."""
        super(FFTGenerator, self)._init(**kwargs)
        wavedata = Waveform(numpy.zeros(int(self.framerate * self.length)))
        freq_domain_stub = self.new_window
        for frequency in frequencies:
            ifft_bin = self._get_frequency_bin(frequency)
            freq_domain_stub[ifft_bin] = self.framerate / len(frequencies)
        window = Waveform(normalize(numpy.real(
            fftpack.ifft(freq_domain_stub))))
        for count, frame in enumerate(range(0, self.framecount,
                                            self.window_size)):
            wavedata = wavedata.insert(frame, window)
        self.dprint('{} generated {}, {} length windows'.format(
            self.__class__.__name__, count, self.window_size))
        self.wavedata = wavedata
        return wavedata


class ContinuousGenerator(Generator):
    """Generate and accumulate a continuous signal accross multiple notes.

    For the description below,
        LengthA="lenth_of_note - (1/2 * transition_length)"
    and
        LengthB="length_of_note - transition_length".

    For the first note generate a constant note of length LengthA.

    For subsequent notes generate a linear signal from the freq. of the first
    note to that of the second of the set transition length, followed by a
    constant note of length LengthB.

    If the keyword "end=True" is used then the constant portion of the length
    should only be LengthA. ::

        |         |            |            |
        {------}\ | LengthB    | LengthA    |
        |        \|            |            |
        | LengthA |\           |/{----------}
        |         | \{-------}/|            |

    Note: Due to the fact that this generator currently ignores the phase of
    the sinusoid being generated, when the frequency is modulated during a
    transition period there are some unfortunate problems. When the frequency
    of the waveform shifts we need to compensate by adding a phase shift so
    that we are using the same phase angle of a sinusoid of a new frequency.
    Since we ignore phase though, both frequency and phase shift and we end up
    seeing an antialiased waveform of an apparent frequency much higher than
    either of the two frequencies being transitioned between.

    TODO: See if I can figure out the appropriate phase calculation to anchor
    the phase angle of the sinusoid as the frequency shifts during the
    transition period.

    """
    def __init__(self, length=None, framerate=None, verbose=False):
        super(ContinuousGenerator, self).__init__(length, framerate, verbose)
        self.phase = 0  # don't do any random phase shifting
        self.frequency = 0.001  # avoid divide by zero
        self.end = False
        self.start = True
        self.last_frame = 0
        self.wavedata = numpy.zeros(1)
        self.transition_length = int(self.framerate * 0.1)
        if self.transition_length % 2 != 0:  # need even length transition
            self.transition_length += 1

    @property
    def _constant_length(self):
        adjustment = self.transition_length
        if len(self.wavedata) <= 1 or self.end:
            adjustment /= 2
        return int(self.framecount - adjustment)

    def _init(self, frequency=None, length=None, verbose=None, end=None,
              **kwargs):
        if frequency:
            self.last_frequency = self.frequency
            self.frequency = frequency
        if length:
            self.length = length
        if verbose:
            self.verbose = verbose
        if end:
            self.end = end

        # framecount = frames / sec * sec
        self.framecount = int(self.framerate * self.length)
        # rectify length to actual framecount
        self.length = float(self.framecount) / self.framerate

    def _prep_wavedata(self, transition=False):
        # save the frame where the next note starts
        adjustment = self.transition_length
        if not transition:
            adjustment = self._constant_length
        new_block = numpy.zeros(adjustment)
        self.wavedata = numpy.concatenate((self.wavedata, new_block))

    def _constant(self):
        """Append sinusoid wave of constant frequency to wavedata."""
        self.dprint('constant freq from frame %s to %s' %
                    (self.last_frame,
                     self.last_frame + self._constant_length))
        frequency = float(self.frequency)
        for frame in range(self.last_frame,
                           self.last_frame + self._constant_length):
            value = self._sinusoid_value(frame, frequency)
            print('const frame %s at value %s at %s' % (
                frame, value, frequency))
            self.wavedata[frame] = value
        self.last_frame = frame

    def _transition(self):
        """Append sinusoid wave of linearly changing frequency to wavedata."""
        self.dprint('transition from frame %s to %s' %
                    (self.last_frame,
                     self.last_frame + self.transition_length))
        for frame in range(self.last_frame,
                           self.last_frame + self.transition_length):
            modifier = ((frame - self.last_frame) *
                        float(self.frequency - self.last_frequency) /
                        self.transition_length)
            frequency = (self.last_frequency + modifier)
            value = self._sinusoid_value(frame, frequency)
            print('transition frame %s at %s value %s: mod %s' % (
                frame, frequency, value, modifier))
            self.wavedata[frame] = value
        self.last_frame = frame

    def generate(self, frequency, length, end=False, *args, **kwargs):
        self._init(frequency=frequency, length=length, end=end,
                   *args, **kwargs)
        self.dprint('generating %s new frames at %s' % (self.framecount,
                                                        frequency))
        if self.start:
            self.dprint('Starting initial frequency in the signal...')
            self._prep_wavedata()
            self._constant()
            self.dprint('signal is now %s long' % len(self.wavedata))
            self.start = False
        else:
            self.dprint('Adding transition... %s to %s' % (
                self.last_frequency, self.frequency))
            self._prep_wavedata(transition=True)
            self._transition()
            self.dprint('  transition now %s long' % len(self.wavedata))
            self.dprint('Adding the %s note...' % self.frequency)
            self._prep_wavedata()
            self._constant()
            self.dprint('signal is now %s long' % len(self.wavedata))


class PhasorGenerator(object):
    """Generate a sinusoid by simulating a phasor in the imaginary plane.

    By creating an imaginary number using python's polar coordinates methods we
    can simulate a phasor vector in the imaginary plane. By rotating the vector
    around the origin and taking the projection of the vector onto the real
    axis we can generate a sinusoid.

    # Anchoring Phase while stepping frequency

    # get value for first frame at first frequency
    phasor = cmath.rect(amplitude, 2 * math.pi * frame * frequency / framerate)
    phasor_argument = cmath.atan(phasor.imag / phasor.real)

    sinusoid_value = phasor.real

    # get phase for second frequency
    tmp_phasor = cmath.rect(
        amplitude, 2 * math.pi * frame * new_frequency / framerate)
    tmp_phase_arg = cmath.atan(tmp_phasor.imag / tmp_phasor.real)
    phase_correction = phasor_argument.real - tmp_phase_arg.real

    # check phase correction
    test_phasor = cmath.rect(
        amplitude, (2 * math.pi * frame * new_frequency /
                    framerate) + phase_correction)
    if sinusoid_value != test_phasor.real:
        # recalculate test_phasor with "phase_correction += math.pi"
        if new_test_phasor.real != sinusoid_value:
            raise Exception("something is wrong")

    # get value for next frame at new frequency
    new_phasor = cmath.rect(
        amplitude, (2 * math.pi * (frame + 1) * new_frequency /
                    framerate) + phase_correction)


    """
    def __init__(self, length=None, framerate=None, verbose=False):
        self.length = length
        if not length:
            self.length = defaults.length
        self.framerate = framerate
        if not framerate:
            self.framerate = defaults.framerate
        self.verbose = verbose
        self.wavedata = numpy.zeros(1)
        self.last_frame = -1
        self.last_phase = 0
        self.last_frequency = 0
        self.frequency = 0
        self.phase = 0
        self.amplitude = 1  # assumed to be constant for now
        self.cmp_precision = 1e-07

    @property
    def waveform(self):
        return Waveform(self.wavedata, self.framerate)

    def _prep_wavedata(self):
        new_block = numpy.zeros(self.length)
        self.wavedata = numpy.concatenate((self.wavedata, new_block))

    def dprint(self, msg):
        """Conditionally print a debugging message."""
        if self.verbose:
            print(msg)

    def _time(self, frame):
        """Convert wavedata frame units to seconds.

        Unit Conversion:
            seconds = frame / (frame / second) = second * frame / frame
        """
        return frame / self.framerate

    def _angle(self, frame, frequency, phase):
        """Calculate sinusoid angle in radians."""
        return 2 * math.pi * frequency * self._time(frame) + phase

    def _phasor(self, frame, frequency, phase)):
        """Generate a phasor in the imaginary plane for the given point."""
        return cmath.rect(self.amplitude,
                          self._angle(frame, frequency, phase))

    def _phasor_argument(self, phasor):
        """Calculate the phasor argument.

        The phasor argument can be used to calculate the appropriate phase
        correction when transitioning between frequencies.
        """
        return cmath.atan(phasor.imag / phasor.real)

    def _calculate_phase_correction(self):
        """Calculate a new phase correction value for the new frequency."""
        # phasor for new frequency at the last frame
        new_phasor = self._phasor(self.last_frame, self.frequency,
                                  self.last_phase)
        new_phasor_arg = self._phasor_argument(new_phasor).real
        phase_correction = self.last_phase - new_phasor_arg

        corrected_phasor = self._phasor(self.last_frame, self.frequency,
                                        phase_correction)
        # Check whether we have the correct solution or if we need another half
        # period for the phase correction to match up
        if not math.isclose(self.wavedata[self.last_frame],
                            corrected_phasor.real,
                            rel_tol=self.cmp_precision):
            phase_correction += math.pi
            corrected_phasor = self._phasor(self.last_frame, self.frequency,
                                            phase_correction)
            if not math.isclose(self.wavedata[self.last_frame],
                                corrected_phasor.real,
                                rel_tol=self.cmp_precision):
                raise Exception('Something is wrong, the correction does not '
                                'match up.')
        self.phase = phase_correction

    def _generate(self):
        """Continue generating the sinusoid at the current frequency."""
        for frame in range(self.last_frame + 1,
                           self.last_frame + self.framecount + 1)
            phasor = self._phasor(frame, self.frequency, self.phase)
            self.wavedata[frame] = phasor.real

    def generate(self, frequency, length=None):
        """Generate a new note and append it to the wavedata container."""
        self.frequency = frequency
        if length:
            self.length = length
            # framecount = frames / sec * sec
            self.framecount = int(self.framerate * self.length)
            # rectify length to actual framecount
            self.length = float(self.framecount) / self.framerate
        if (self.frequency != self.last_frequency
                and not len(self.wavedata) <= 1):
            self._calculate_phase_correction()
        self._generate()
