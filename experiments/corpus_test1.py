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


def main():
    parser = get_cmd_line_parser(description=__doc__)
    parser.parse_args()

    work_path = numpy.random.choice(corpus.getComposer('bach'))
    work = corpus.parse(work_path)
    for note in work.flat.notes:
        print('{} [{}]: {} {}'.format(note.offset, note.duration.quarterLength,
                                      note.pitch, note.frequency))
    return 0


if __name__ == "__main__":
    call_main(main)
