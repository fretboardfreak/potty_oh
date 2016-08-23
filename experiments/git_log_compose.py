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

"""Compose a song out of a git repository."""

import os
import subprocess
import random

from collections import OrderedDict
from music21.stream import Stream
from music21.note import Note
from music21.scale import MajorScale

from potty_oh.common import get_cmd_line_parser
from potty_oh.common import call_main
from potty_oh.common import ParserArguments
from potty_oh.common import defaults
from potty_oh.common import dprint
from potty_oh.common import vprint
from potty_oh.wav_file import wav_file_context
from potty_oh.audify import audify


def main():
    parser = get_cmd_line_parser(description=__doc__)
    ParserArguments.filename(parser)
    ParserArguments.tempo(parser)
    ParserArguments.framerate(parser)
    parser.add_argument('-r', '--repo', help='The git repository to use.')
    ParserArguments.set_defaults(parser)
    args = parser.parse_args()
    defaults.framerate = args.framerate

    repo_data = scrape_repository_data(args.repo)
    song = compose_repository_song(repo_data)

    notes = song.flat.notes
    waveform = audify(notes, args.tempo, args.verbose)
    with wav_file_context(args.filename) as fout:
        fout.write_frames(waveform.frames)
    return 0


def scrape_repository_data(repository):
    vprint('Scraping filenames modified in each commit in the '
           'Git Repository...')
    git_cmd = ['git', '--git-dir', os.path.join(repository, ".git"),
               '--work-tree', repository]
    sha_output = subprocess.check_output(
        git_cmd + ['log', '--pretty=format:"%h"'], universal_newlines=True)
    shas = sha_output.replace('"', '').split('\n')
    shas.reverse()
    dprint('Found %s shas. First %s, Last %s' % (len(shas), shas[0], shas[-1]))

    repo_data = OrderedDict()
    for sha in shas:
        file_output = subprocess.check_output(
            git_cmd + ['show', '--pretty=format:""', '--name-only', sha],
            universal_newlines=True)
        repo_data[sha] = [f for f in file_output.replace('"', '').split('\n')
                          if f != '']
    dprint('repo_data: %s' % repo_data)
    return repo_data


def compose_repository_song(repo_data):
    vprint('Composing a song using the data from your Git Repository...')
    song = Stream()

    scale = MajorScale('%s4' % random.choice('ABCDEFG'))
    print('Using Scale: %s' % scale)
    clips, phrases = phrasify(repo_data, scale)

    for sha in repo_data:
        for clip in phrases[hash(sha)]:
            for note in clips[clip]:
                song.append(note)

    return song


def phrasify(repo_data, scale):
    """
    Convert the repo data into a bunch of musical phrase patterns and clips.

    For each commit, create a phrase clip out of each unique sha or filepath
    part (i.e. "/home/user/bin" becomes ['home', 'user', 'bin']). Each phrase
    clip is a short sequence notes.

    Also for each commit create a pattern with each modified file creating a
    musical phrase of clips.

    """
    clips = {}
    phrases = {}
    for sha in repo_data:
        sha_hash = hash(sha)
        clips[sha_hash] = convert_string_to_notes(sha, scale)
        phrase = [sha_hash]
        for filename in repo_data[sha]:
            for fpart in filename.split('/'):
                if fpart == "" or hash(fpart) in clips:
                    continue
                fpart_hash = hash(fpart)
                clips[fpart_hash] = convert_string_to_notes(fpart, scale)
                phrase.append(fpart_hash)
        phrases[sha_hash] = phrase
    return clips, phrases


def convert_string_to_notes(string, scale):
    print('converting: %s' % string)
    return [Note(scale.pitchFromDegree(char),
                 quarterLength=get_random_note_length())
            for char in bytearray(string, 'UTF-8')]


def get_random_note_length():
    """Return a note length in quarter note units."""
    tmp = random.choice([0, 0, 0, 0, 1, 2])
    tmp += random.choice([0, 0, 0, 0, 1/2, 1/4])
    if tmp == 0:
        tmp += random.choice([1, 1/2])
    return tmp


if __name__ == "__main__":
    call_main(main)
