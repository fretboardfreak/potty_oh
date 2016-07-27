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

"""An experiment to help determine the best way to use music21 objects.

The music21 libaries have a lot of purposes beyond what I need so for now I
think all I need is to know how to access the note pitches and their positions
and durations within the work. From those three bits of info I can then
construct a waveform representing that music given a tempo to define the length
of a quarter note.
"""

import numpy

from music21 import corpus

from potty_oh.common import get_cmd_line_parser
from potty_oh.common import call_main
from potty_oh.common import ParserArguments
from potty_oh.common import defaults
from potty_oh.wav_file import wav_file_context
from potty_oh.waveform import Waveform
from potty_oh.waveform import seconds_to_frame
from potty_oh.waveform import quarter_note_length
from potty_oh.signal_generator import Generator
from potty_oh.audify import audify_to_file


def main():
    parser = get_cmd_line_parser(description=__doc__)
    ParserArguments.filename(parser)
    ParserArguments.tempo(parser)
    ParserArguments.framerate(parser)
    ParserArguments.set_defaults(parser)
    ParserArguments.best(parser)
    args = parser.parse_args()
    defaults.framerate = args.framerate

    print('Generating Signal:')
    sig_gen = Generator()
    song = Waveform([])
    qnl = quarter_note_length(args.tempo)

    # work = corpus.parse(numpy.random.choice(corpus.getComposer('bach')))
    work = corpus.parse(numpy.random.choice(corpus.getCorePaths()))
    notes = work.flat.notes
    if args.best:
        audify_to_file(notes, args.tempo, args.filename, args.verbose)
        return 0

    note_count = len(notes)
    try:
        for count, note in enumerate(notes):
            print('{}/{}: {} [{}]: {} {}'.format(
                count, note_count, note.offset, note.duration.quarterLength,
                note.pitch, note.pitch.frequency))
            note_length = qnl * note.quarterLength
            start = seconds_to_frame(qnl * note.offset)
            print('  inserting {} seconds into frame {}'.format(
                note_length, start))
            song = song.insert(
                start, sig_gen.sin_constant(note.pitch.frequency,
                                            length=note_length))
    except KeyboardInterrupt:
        print('Stopping song generating here...')

    print('Writing Song {} to file {}...'.format(
        work.corpusFilepath, args.filename))
    with wav_file_context(args.filename) as fout:
        fout.write_frames(song.frames)

    return 0


if __name__ == "__main__":
    call_main(main)
