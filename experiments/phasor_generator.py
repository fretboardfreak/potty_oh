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

"""A Continuous Signal Generator program."""

from potty_oh import common
from potty_oh.signal_generator import PhasorGenerator


def main():
    parser = common.get_cmd_line_parser(description=__doc__)
    common.ParserArguments.filename(parser)
    common.ParserArguments.plot(parser)
    common.ParserArguments.length(parser)
    common.ParserArguments.set_defaults(parser, type='constant')

    default_freqs = [300, 800]
    parser.add_argument(
        '-f', '--frequencies', action='append', dest='freqs', type=float,
        default=[], help="Specify the frequencies to use. Defaults to "
                         "%s." % default_freqs)
    args = parser.parse_args()

    freqs = default_freqs
    if len(args.freqs) > 0:
        freqs = args.freqs

    sg = PhasorGenerator(framerate=args.framerate, length=args.length,
                         verbose=args.debug)
    for freq in freqs[:-1]:
        sg.generate(freq, args.length)
    sg.generate(freqs[-1], args.length)
    waveform = sg.waveform

    if args.plot:
        import potty_oh.plot as plot
        plot.plot_waveform(waveform.frames, waveform.channels, 0,
                           len(waveform))
    else:
        from potty_oh.wav_file import wav_file_context
        with wav_file_context(args.filename) as fout:
            fout.write_frames(waveform.frames)

    return 0


if __name__ == "__main__":
    common.call_main(main)
