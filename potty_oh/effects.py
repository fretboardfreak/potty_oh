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

"""A library various effects that can be applied to arrays of audio data."""

import math
import numpy
from itertools import zip_longest


def mix_down(first, second):
    """Blend two Waveform together using a mathematical average.

    Mean halves the power of each signal. This is equivalent to what the air
    does in real life. This means we need to try and avoid attenuating signals
    exessively when we don't need to.
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
        # see docstring note about signal attenuation w.r.t. math.mean()
        if float(lfr) != 0.0 and float(rfr) != 0.0:
            result[frame] = numpy.mean([float(lfr), float(rfr)])
        elif float(lfr) == 0.0:
            result[frame] = rfr
        else:
            result[frame] = lfr
    return Waveform(result)
