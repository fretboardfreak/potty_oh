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

"""A library for manipulating Waveform Objects."""

import math
import numpy

try:
    from itertools import zip_longest
except ImportError:  # python 2...  bleh!
    from itertools import izip_longest as zip_longest

from .common import defaults


def seconds_to_frame(seconds, framerate=None):
    """Given a number of seconds, calculate the equivalent length in frames."""
    if framerate is None:
        framerate = defaults.framerate
    return math.floor(float(framerate) * float(seconds))


def frame_to_seconds(frame, framerate=None):
    """Calculate the time in seconds repreesented by a number of frames."""
    if framerate is None:
        framerate = defaults.framerate
    return float(frame) / float(framerate)


def quarter_note_length(tempo, beats_per_quarter=1):
    """Calculate the length of a quarter note in seconds."""
    return 60.0 / float(tempo) * float(beats_per_quarter)


def mix_down(first, second):
    """Blend two Waveform objects together using a mathematical average.

    Blend two Waveform together using a mathematical average. Mean halves the
    power of each signal. This is equivalent to what the air does in real life.
    This means we need to try and avoid attenuating signals exessively when we
    don't need to.
    """
    first_frameset = first
    if isinstance(first, Waveform):
        first_frameset = first.frames
    second_frameset = second
    if isinstance(second, Waveform):
        second_frameset = second.frames
    result = numpy.zeros(max(len(first_frameset), len(second_frameset)))
    for frame, (lfr, rfr) in enumerate(
            zip_longest(first_frameset, second_frameset, fillvalue=0.0)):
        # see attenuation note in docstring
        if float(lfr) != 0.0 and float(rfr) != 0.0:
            result[frame] = numpy.mean([float(lfr), float(rfr)])
        elif float(lfr) == 0.0:
            result[frame] = rfr
        else:
            result[frame] = lfr
    return Waveform(result)


class Waveform(object):
    """A Container for audio waveforms and associated metadata.

    Supports either Mono or Stereo audio waveforms.
    """
    def __init__(self, wavedata, framerate=None):
        if not framerate:
            framerate = defaults.framerate
        self.framerate = framerate
        self._set_wavedata(wavedata)

    def _verify_channel_count(self, channels):
        if channels < 1 or channels > 2:
            raise ValueError('Waveform only supports 1 or 2 channel audio.')

    def _set_wavedata(self, wavedata):
        """Convert the wavedata into a numpy array of a consistent shape.

        A single array dimension is used for mono waveforms. For stereo
        waveforms a 2D array with the dimensions (framecount, 2) is used.
        """
        tmp = numpy.array(wavedata)
        if len(tmp.shape) == 1:
            self.channels = 1
            self._wavedata = tmp
        elif len(tmp.shape) == 2:
            self.channels = 2
            if tmp.shape[0] < tmp.shape[1]:
                self._verify_channel_count(tmp.shape[0])
                self._wavedata = tmp.transpose()
            else:
                self._verify_channel_count(tmp.shape[1])
                self._wavedata = tmp
        else:
            raise ValueError('Waveform only supports 1 or 2 channel audio.')

    def __repr__(self):
        return "<{}: framerate={}, channels={}, frames=({})>".format(
                self.__class__.__name__, self.framerate, self.channels,
                self.frames.shape)

    @property
    def frames(self):
        return self._wavedata

    @frames.setter
    def frames(self, value):
        self._set_wavedata(value)

    def __len__(self):
        """Return framecount for len() since it must be an integer."""
        return len(self._wavedata)

    @property
    def length(self):
        """Return the length of the waveform in seconds."""
        return float(len(self._wavedata)) / self.framerate

    def mix_down(self, other):
        """Mix this waveform with another."""
        return mix_down(self, other)

    def insert(self, frame, waveform):
        """Insert another waveform into this one at a specific frame."""
        if waveform.channels != 1:
            raise NotImplemented(
                "Don't know how to insert stereo waveforms yet")
        if self.channels != 1:
            raise NotImplemented(
                "Don't know how to insert stereo waveforms yet")
        new = numpy.zeros(max(frame + len(waveform), len(self)))
        for index, frm in enumerate(waveform.frames):
            new[index + frame] = frm
        return self.mix_down(new)
