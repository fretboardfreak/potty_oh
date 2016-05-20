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

"""A test for what happens when two waveforms are averaged together."""

from potty_oh import common
from potty_oh.wav_file import wav_file_context
from potty_oh.waveform import mix_down
from potty_oh.signal_generator import Generator
from potty_oh.music.pitch import Key
from potty_oh.music.interval import Interval


def main():
    parser = common.get_cmd_line_parser(description=__doc__)
    common.ParserArguments.filename(parser)
    common.ParserArguments.length(parser)
    common.ParserArguments.framerate(parser)
    common.ParserArguments.set_defaults(parser, type='constant',
                                        length=2.0)
    args = parser.parse_args()
    common.defaults.framerate = args.framerate

    sg = Generator(length=args.length, verbose=args.debug)

    key = Key()
    unison = sg.sin_constant(key.interval(Interval.unison))
    maj_third = sg.sin_constant(key.interval(Interval.major_third))
    min_third = sg.sin_constant(key.interval(Interval.minor_third))
    fifth = sg.sin_constant(key.interval(Interval.fifth))

    powerchord = unison.mix_down(fifth)

    maj_triad = powerchord.mix_down(maj_third)
    min_triad = mix_down(powerchord, min_third)

    with wav_file_context(args.filename) as fout:
        fout.write_frames(powerchord.frames)
        fout.write_frames(maj_triad.frames)
        fout.write_frames(min_triad.frames)

    return 0


if __name__ == "__main__":
    common.call_main(main)
