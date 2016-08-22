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

"""A script to convert a piece from the music21 corpus into audio."""

import numpy
from music21 import corpus

from potty_oh.common import get_cmd_line_parser
from potty_oh.common import call_main
from potty_oh.common import ParserArguments
from potty_oh.common import defaults
from potty_oh.wav_file import wav_file_context
from potty_oh.audify import audify


def main():
    parser = get_cmd_line_parser(description=__doc__)
    ParserArguments.filename(parser)
    ParserArguments.tempo(parser)
    ParserArguments.framerate(parser)
    ParserArguments.set_defaults(parser)
    args = parser.parse_args()
    defaults.framerate = args.framerate

    print('Generating Signal:')
    work = corpus.parse(numpy.random.choice(corpus.getCorePaths()))
    notes = work.flat.notes
    waveform = audify(notes, args.tempo, args.verbose)

    print('Writing Song {} to file {}...'.format(
        work.corpusFilepath, args.filename))
    with wav_file_context(args.filename) as fout:
        fout.write_frames(waveform.frames)

    return 0


if __name__ == "__main__":
    call_main(main)
