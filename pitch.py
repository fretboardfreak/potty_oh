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

"""
pitch.py: tools for calculating pitch frequencies.

Ideas and theories to explore:

- qualities (8 total) vs intervals (12 total)

#. pythagorean diatonic tuning: [9/8, 5/4, 4/3, 3/2, 5/3, 15/8, 2]
#. just intonation tuning: [9/8, 81/64, 4/3, 3/2, 27/16, 243/128, 2]
#. meantone (quarter-comma) tempered
#. mean (third-comma) tempered
#. equal tempered (12fth root) [2^(x/12), ...]
#. piano key representation (1-80)
"""

import string


class PitchError(Exception):
    pass


class ReferenceFrequencies(object):
    scientific_middle_c = 256

    concert_a4 = 440
    middle_c = 261.626


class TemperamentError(PitchError):
    pass


class Temperament(list):
    def __init__(self, multipliers):
        if len(multipliers) != 7:
            raise TemperamentError('Need 7 multipliers.')
        super(Temperament, self).__init__(multipliers)


PythagoreanTemperament = Temperament([9.0/8.0, 5.0/4.0, 4.0/3.0,
                                      3.0/2.0, 5.0/3.0, 15.0/8.0, 2.0])
JustTemperament = Temperament([9.0/8.0, 5.0/4.0, 4.0/3.0, 3.0/2.0,
                               5.0/3.0, 15.0/8.0, 2.0])


class Diatonic(object):

    max_quality = 8  # next octave
    min_quality = 1  # unison

    def __init__(self, root_frequency=440.0, root_name="A",
                 temperament=PythagoreanTemperament):
        self.root_frequency = float(root_frequency)
        self.root_name = root_name
        self.temperament = temperament

    def quality(self, quality, octave=4):
        if isinstance(quality, int):
            octave_root = self.root_frequency * pow(self.temperament[-1],
                                                    (octave - 4))
            print("octave root: %s" % octave_root)
            index = (quality - 1) % 7
            print('temperament index: %s' % index)
            result = octave_root * self.temperament[index]
            print('note freq: %s' % result)
            return result
        else:
            raise NotImplemented('Letter based note qualities coming soon.')



if __name__ == "__main__":
    import common
    import waveform
    import wav_file

    DOC="A demonstration of various musical notes and tunings."

    def main():
        parser = common.get_cmd_line_parser(description=DOC)
        common.ParserArguments.filename(parser)
        common.ParserArguments.length(parser)
        common.ParserArguments.modify_argument(parser, 'length', 'help',
                                               'Length per pitch clip.')
        common.ParserArguments.plot(parser)
        common.ParserArguments.set_defaults(parser, filename='signal.wav',
                                            length=1.0)
        args = parser.parse_args()

        sg = waveform.Generator(length=args.length, verbose=args.debug)

        if args.plot:
            raise NotImplemented()
        else:
            notes = pitch.Diatonic()
            with wav_file.WavFile(args.filename, 1, sg.framerate) as fout:
                for quality in range(pitch.Diatonic.min_quality,
                                     pitch.Diatonic.max_quality):
                    fout.write(sg.sin_constant(notes.quality(quality)))
                fout.write(sg.sin_constant(notes.quality(1, 5)))

        return 0

    common.call_main(main)
