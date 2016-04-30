==========================================
Potty-Oh: Python Audio Programming Toolset
==========================================

:author: Curtis Sand (a.k.a. fret, fretboardfreak)
:date: 160430

**Potty-Oh**: **P**\ython **Audio**

:mirrors:
    - https://github.com/fretboardfreak/potty_oh
    - https://bitbucket.org/fret/potty_oh

Potty-Oh is the result of my exploration into audio waveforms and how to
program various manipulations of audio.

Potty-Oh is a play on the phonetic pronunciation of the terms, "Python Audio".
Libraries already exist with the unclever names pyaudio and paudio so I went
with something just a little different.

License
=======

Potty-Oh uses the Apache Version 2.0 License. Please see ``LICENSE.rst`` for
more information::

    Copyright 2016 Curtis Sand

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

        Unless required by applicable law or agreed to in writing, software
        distributed under the License is distributed on an "AS IS" BASIS,
        WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
        See the License for the specific language governing permissions and
        limitations under the License.


Dependencies
============

*Tested on Fedora 23 and MacOS (Homebrew) only; your mileage may vary.*

``scikits.audiolab`` requires:

- *fedora-23*: libsndfile-devel
- *mac-os*: libsndfile

``matplotlib`` requires:

- *fedora-23*:

  - libpng-devel
  - freetype-devel

.. EOF README
