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

"""A progression of the first FFT Experiment.

The first FFT Experiment was performing the FFT on the entire waveform. This
results in a single spectrogram snapshot for the entire time period represented
by the array analyzed. This experiment uses a windowing function to analize
smaller sections of a signal to show the spectrogram of shorter sections of a
signal.
"""

from potty_oh.common import get_cmd_line_parser
from potty_oh.common import call_main
from potty_oh.common import defaults
from potty_oh.common import ParserArguments
from potty_oh.signal_generator import Generator
from potty_oh.waveform import Waveform
from potty_oh.waveform import seconds_to_frame
from potty_oh.wav_file import wav_file_context
import potty_oh.plot as plot
from potty_oh.analysis import analyze_whole_waveform


def main():
    parser = get_cmd_line_parser(description=__doc__)
    parser = ParserArguments.filename(parser)
    parser = ParserArguments.plot(parser)
    parser = ParserArguments.framerate(parser)
    parser = ParserArguments.set_defaults(parser)
    args = parser.parse_args()
    defaults.framerate = args.framerate

    sig_gen = Generator(verbose=args.debug)

    print('0.2 second waveform at 1000Hz and 0.2 seconds at 440Hz '
          '(starting 0.1 second in)')
    signal = Waveform([])
    signal = signal.insert(0, sig_gen.sin_constant(1000, length=0.2))
    signal = signal.insert(seconds_to_frame(0.1),
                           sig_gen.sin_constant(440, length=0.2))

    if args.plot:
        plot.plot_waveform(signal.frames, 1, 0, 4000)
    else:
        with wav_file_context('signal.wav') as fout:
            fout.write_frames(signal.frames)

    spectrum = analyze_whole_waveform(signal)
    print("Frequency Powers found by STFT: ")
    timeslices = [(time, spec) for time, spec in spectrum.items()]
    timeslices.sort(key=lambda x: x[0])
    for timeslice in timeslices:
        print(timeslice)

    return 0


if __name__ == "__main__":
    call_main(main)
