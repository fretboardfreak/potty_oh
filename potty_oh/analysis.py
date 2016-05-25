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

"""analysis.py: A library of tools for performing signal analysis tasks."""

from math import sqrt
from numpy import round, zeros
from scipy import fftpack, hanning

from potty_oh.waveform import Waveform


def analyze_whole_waveform(waveform):
    """
    niquist_freq = framerate / 2
    precision = niquist_freq / window_size

    Want precision to be within 5% of target pitches or "5 cent".
    (+-600Hz @ 12KHz to +-10Hz @ 220Hz)

    window_size = framerate / 2 / precision

    Gives window sizes in the range of:
    - 400 Frames at 8K Frames/sec
    - 2205 Frames at 44.1K Frames/sec
    """
    desired_precision = 10  # Hz
    window_size = int(waveform.framerate / 2.0 / desired_precision)
    hanning_window = hanning(window_size)
    spectrum = {}
    for start_frame in range(0, len(waveform.frames), len(hanning_window)):
        window = zeros(len(hanning_window))
        for frame in range(len(window)):
            window[frame] = (hanning_window[frame] *
                             waveform.frames[start_frame + frame])
        spectrum[start_frame] = analyze_window(Waveform(window))
    return spectrum


def analyze_window(waveform):
    """Perform FFT frequency analysis against the given waveform.
    """
    frequency_coefficients = fftpack.fft(waveform.frames)
    power_coefficients = [sqrt(pow(x.real, 2) + pow(x.imag, 2))
                          for x in frequency_coefficients]
    bins = int(len(power_coefficients)/2)
    power_domain = round(power_coefficients[:bins])
    frequency_domain = frequency_coefficients[:bins]
    frequencies = fftpack.fftfreq(len(frequency_domain),
                                  1.0 / waveform.framerate)
    powers = {freq: (strength, coef)
              for freq, strength, coef in zip(frequencies, power_domain,
                                              frequency_domain)
              if strength != 0.0}
    return powers
