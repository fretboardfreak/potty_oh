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

import common
from temperament import Temperament
from interval import Interval


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
        common.dprint('semitone %s, octave %s :' % (semitone, octave))
        index = semitone % Interval.max()
        common.dprint('  interval: %s' % (Interval.name(index)))
        octave += semitone // Interval.max()
        common.dprint('  octave: %s' % octave)

        # octaves are always 'root * 2' so use
        # 'root * pow(2, octave)' for new root.
        octave_root = (self.root_frequency *
                       (pow(self.temperament.octave, octave)))
        common.dprint("  octave root: %s" % octave_root)
        common.dprint('  interval ratio: %s' % self.temperament[index])
        result = octave_root * self.temperament[index]
        common.dprint('  note freq: %s' % result)
        return result


if __name__ == "__main__":
    import waveform
    import wav_file

    DOC = ("A demonstration of various musical notes and tunings. The 12 "
           "semitones of a musical scale are played in each temperament. "
           "Musical temperament refers to the ratios used to determine the "
           "frequency of each note.")

    def main():
        parser = common.get_cmd_line_parser(description=DOC)
        common.ParserArguments.filename(parser)
        common.ParserArguments.length(parser)
        common.ParserArguments.modify_argument(parser, 'length', 'help',
                                               'Length per pitch clip.')
        common.ParserArguments.plot(parser)
        common.ParserArguments.set_defaults(parser, length=0.75)
        args = parser.parse_args()

        sg = waveform.Generator(length=args.length / 2.0, verbose=args.debug)

        if args.plot:
            raise NotImplemented()
        else:
            with wav_file.wav_file_context(args.filename) as fout:
                key = Key()
                for tone in range(Interval.max() + 1):
                    fout.write_frames(sg.sin_constant(key.interval(tone)))

        return 0

    common.call_main(main)
