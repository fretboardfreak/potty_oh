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

"""Test how convolution might be used to 'mix down' audio signals.

The idea is to somehow generate a single sinusoid that is a continuous
waveform containing all of the frequencies in the separate original tracks.
Convolution is supposed to show the overlap of two given signals. The question
is, does correlating two audio signals in this way result in something useful?

When you run the plot you may notice that the original "main track" waveform
is different when compared to the convolved waveform even when the harmony
note is not playing. I was unable to remove this distortion when using
convolve to associate the main track and the harmony. Even though you cannot
hear this change in the signal this test generates it's not necessarily a
desireable change.

Overall this provides a better result than a plain mathmatical average of the
waveforms but it still causes distortions to the entire waveform.
"""

import scipy
from matplotlib import pyplot

from potty_oh import common
from potty_oh.signal_generator import FFTGenerator
from potty_oh.waveform import Waveform
from potty_oh.waveform import seconds_to_frame
from potty_oh.waveform import frame_to_seconds
from potty_oh.effects import normalize


def main():
    parser = common.get_cmd_line_parser(description=__doc__)
    common.ParserArguments.filename(parser)
    common.ParserArguments.plot(parser)
    common.ParserArguments.set_defaults(parser, type='constant')
    args = parser.parse_args()

    sg = FFTGenerator(framerate=args.framerate,
                      verbose=args.debug)

    if args.plot:
        length = 0.05
    else:
        length = 2.0
    main_freqs = [440.0, 660.0]  # Hz
    harmony_freqs = [550.0]  # Hz (major third)

    main_track = sg.generate(main_freqs, length=length * 3)
    print("440 and 660HZ main track is %s seconds or %s frames" %
          (length * 3, len(main_track)))

    harmony_note = sg.generate(harmony_freqs, length=length)
    print("%sHz Harmony is audible for %s seconds or %s frames" %
          (harmony_freqs, length, len(harmony_note)))

    print("Insert the harmony note at the right place a zeroed track.")
    note_frames = seconds_to_frame(length)
    harmony_track = Waveform(scipy.zeros(len(main_track)))
    for index in range(note_frames, note_frames * 2):
        harmony_track._wavedata[index] = (
                harmony_note._wavedata[index - note_frames - 1])

    preprocessed_harmony_track = Waveform(harmony_track._wavedata.copy())
    for index, frame in enumerate(preprocessed_harmony_track.frames):
        preprocessed_harmony_track._wavedata[index] = 0.5 - (0.5 * frame)

    convolution_data = scipy.convolve(main_track.frames,
                                      preprocessed_harmony_track.frames,
                                      mode="full")
    print("Convolution (including mirrored data) is %s seconds or %s frames" %
          (frame_to_seconds(len(convolution_data), framerate=sg.framerate),
           len(convolution_data)))

    print("Normalizing Convolution Amplitude")
    convolution = Waveform(normalize(
        convolution_data[:int(len(convolution_data)/2)]))

    if args.plot:
        _, subplots = pyplot.subplots(4, 1)
        subplots[0].plot(main_track.frames)
        subplots[0].set_title('Main Track 440.0 and 660.0 Hz - Root and Fifth')
        subplots[1].plot(harmony_track.frames)
        subplots[1].set_title('Harmony Major Third (550.0 Hz)')
        subplots[2].plot(preprocessed_harmony_track.frames)
        subplots[2].set_title('Preprocessed Harmony Track')
        subplots[3].plot(convolution.frames)
        subplots[3].set_title('Convolved track of the two waveforms.')
        pyplot.show()
    else:
        from potty_oh.wav_file import wav_file_context
        with wav_file_context(args.filename) as fout:
            fout.write_frames(convolution.frames)

    return 0


if __name__ == "__main__":
    common.call_main(main)
