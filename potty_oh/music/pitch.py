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

"""
pitch.py: tools for calculating pitch frequencies.

:TODO: piano key representation (1-80)
"""

from potty_oh.common import dprint

from .temperament import Temperament
from .interval import Interval


class ReferenceFrequencies(object):
    """A collection of reference frequencies """
    scientific_middle_c = 256

    concert_a4 = 440
    middle_c = 261.626


class Key(object):
    """An object for calculating the note frequencies of musical keys."""

    def __init__(self, root_frequency=ReferenceFrequencies.concert_a4,
                 root_name=None,
                 temperament=Temperament.even):
        self.root_frequency = float(root_frequency)
        self.root_name = root_name
        self.temperament = temperament

    def interval(self, semitone, octave=0):
        """Get the frequency of a given interval relative to the root."""
        dprint('semitone %s, octave %s :' % (semitone, octave))
        index = semitone % Interval.max()
        dprint('  interval: %s' % (Interval.name(index)))
        octave += semitone // Interval.max()
        dprint('  octave: %s' % octave)

        # octaves are always 'root * 2' so use
        # 'root * pow(2, octave)' for new root.
        octave_root = (self.root_frequency *
                       (pow(self.temperament.octave, octave)))
        dprint("  octave root: %s" % octave_root)
        dprint('  interval ratio: %s' % self.temperament[index])
        result = octave_root * self.temperament[index]
        dprint('  note freq: %s' % result)
        return result
