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

"""A demonstration of tuning temperament across the 12 semitones.

The 12 semitones of a musical scale are played in each of the implemented
temperaments.  Musical temperament refers to the ratios used to determine the
frequency of each note.
"""

import itertools

from potty_oh.common import get_cmd_line_parser
from potty_oh.common import ParserArguments
from potty_oh.common import call_main
from potty_oh.waveform import Generator
from potty_oh.wav_file import wav_file_context
from potty_oh.music.temperament import Temperament
from potty_oh.music.pitch import Key
from potty_oh.music.interval import Interval


def main():
    parser = get_cmd_line_parser(description=__doc__)
    ParserArguments.filename(parser)
    ParserArguments.length(parser)
    ParserArguments.modify_argument(parser, 'length', 'help',
                                    'Length per pitch clip.')
    ParserArguments.set_defaults(parser, length=0.75)
    args = parser.parse_args()

    sg = Generator(length=args.length / 2.0, verbose=args.debug)

    with wav_file_context(args.filename) as fout:
        for tone, temperament in itertools.product(
                range(Interval.max() + 1), Temperament.iter()):
            key = Key(temperament=temperament)
            waveform = sg.sin_constant(key.interval(tone))
            fout.write_frames(waveform.frames)

    return 0


if __name__ == "__main__":
    call_main(main)
