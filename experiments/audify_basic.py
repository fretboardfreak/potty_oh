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

"""Explore how how to audify a music21 score using "potty_oh.audify"."""

from itertools import cycle
import random

from music21 import scale
from music21.note import Note
from music21.stream import Stream
from music21.pitch import Pitch

from potty_oh.common import get_cmd_line_parser
from potty_oh.common import call_main
from potty_oh.common import ParserArguments
from potty_oh.common import defaults
from potty_oh.wav_file import wav_file_context
from potty_oh.audify import audify_basic


def main():
    parser = get_cmd_line_parser(description=__doc__)
    ParserArguments.filename(parser)
    ParserArguments.tempo(parser)
    ParserArguments.framerate(parser)
    ParserArguments.set_defaults(parser)
    args = parser.parse_args()
    defaults.framerate = args.framerate

    song = Stream()

    roots = 'ABCDEFG'
    scales = [scale.MajorScale, scale.MinorScale,
              scale.WholeToneScale, scale.ChromaticScale]

    print('Choosing a random scale from Major, Minor, Whole Tone, Chromatic.')
    rscale = random.choice(scales)(Pitch(random.choice(roots)))
    print('Using: %s' % rscale.name)

    print('Generating a score...')
    random_note_count = 50
    random_note_speeds = [0.25, 0.5]
    print('100 Random 1/8th and 1/16th notes in rapid succession...')
    for i in range(random_note_count):
        note = Note(random.choice(rscale.pitches))
        note.duration.quarterLength = random.choice(random_note_speeds)
        song.append(note)

    scale_practice_count = 4
    print('Do the scale up and down a few times... maybe %s' %
          scale_practice_count)
    rev = rscale.pitches[:]
    rev.reverse()
    updown_scale = rscale.pitches[:]
    updown_scale.extend(rev[1:-1])
    print('updown scale: %s' % updown_scale)
    for count, pitch in enumerate(cycle(updown_scale)):
        print(' note %s, %s' % (count, pitch))
        song.append(Note(pitch))
        if count >= scale_practice_count * len(updown_scale):
            break

    print('Composition finished:')
    song.show('txt')

    print('Audifying the song...')
    wave = audify_basic(song, args.tempo)

    print('Writing Song to file {}...'.format(args.filename))
    with wav_file_context(args.filename) as fout:
        fout.write_frames(wave.frames)

    return 0


if __name__ == "__main__":
    call_main(main)
