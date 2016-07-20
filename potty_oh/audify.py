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

"""A library for turning music21 streams into audio... Audifying."""

from .waveform import Waveform
from .waveform import quarter_note_length
from .waveform import seconds_to_frame
from .signal_generator import Generator


def audify_basic(score, tempo):
    """Audify a music21 score using the basic signal generater."""
    sig_gen = Generator()
    song = Waveform([])
    qnl = quarter_note_length(tempo)

    notes = score.flat.notes
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

    return song
