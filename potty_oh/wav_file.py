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

"""wav.py : library for handling wav format sound files."""

from contextlib import contextmanager
from pysndfile import construct_format, PySndfile


def wav_format_code(encoding=None):
    """Calculate the format code for 'pcm16' encoded 'wav' files."""
    if not encoding:
        encoding = 'pcm16'
    return construct_format('wav', encoding)


def open(filename, mode=None, format=None, channels=1,
         framerate=44100):
    """Factory method to generate PySndfile objects with wav file defaults."""
    if not mode:
        mode = 'w'
    if not format:
        fmt = wav_format_code()
    return PySndfile(filename, mode, fmt, channels, framerate)


@contextmanager
def wav_file_context(*args, **kwargs):
    """Context manager for cleaning up wav file resources."""
    sndfile = open(*args, **kwargs)
    yield sndfile
