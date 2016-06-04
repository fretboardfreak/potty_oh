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

"""effects.py: a library of effects to apply to waveforms."""

from matplotlib import pyplot

from .waveform import Waveform


def normalize(waveform):
    if isinstance(waveform, Waveform):
        wavedata = waveform.frames
    else:
        wavedata = waveform
    peak = max(wavedata)
    wavedata *= 1.0 / peak
    return wavedata
