======================
Potty-Oh: Python Audio
======================

:mirrors:
    - https://github.com/fretboardfreak/potty_oh
    - https://bitbucket.org/fret/potty_oh

Official Project Website: www.fretboardfreak.com/potty_oh

Potty-Oh is the result of my exploration into audio waveforms and how to
program various manipulations of audio. The project consists of the Potty-Oh
python library and a set of experiments using the library.

Potty-Oh is a play on the phonetic pronunciation of the terms, "Python Audio".
Libraries already exist with the unclever names pyaudio and paudio so I went
with something just a little different.

A note on music libraries: I started writing my own library to calculate
musical pitches in various tuning temperaments. The modules are available in
the subpackage ``potty_oh.music``. For more complicated musical concepts I've
opted to use the `music21 <http://web.mit.edu/music21/>`_ library developed by
MIT.

References
==========

Here's a list of links that I've come across that have explained some part of
musical theory or digital audio in a way that was useful.

- https://en.m.wikipedia.org/wiki/Bit_rate#Audio
- http://mathforum.org/library/drmath/view/52312.html
- https://en.m.wikipedia.org/wiki/Music_and_mathematics
- https://en.m.wikipedia.org/wiki/Meantone_temperament
- https://en.m.wikipedia.org/wiki/Quarter-comma_meantone
- https://en.m.wikipedia.org/wiki/Twelfth_root_of_two
- https://en.m.wikipedia.org/wiki/C_(musical_note)
- https://en.m.wikipedia.org/wiki/Piano_key_frequencies
- https://en.m.wikipedia.org/wiki/Scientific_pitch_notation
- https://en.m.wikipedia.org/wiki/Diatonic_scale
- https://en.m.wikipedia.org/wiki/Circle_of_fifths_text_table
- https://en.m.wikipedia.org/wiki/Pythagorean_tuning
- http://zone.ni.com/reference/en-XX/help/372416B-01/svtconcepts/fft_funda/

Dependencies
============

*These instructions tested on Fedora 23 and MacOS (Homebrew) only; your mileage
may vary.*

Potty-Oh is written for Python 3.

System Dependencies
^^^^^^^^^^^^^^^^^^^

Fedora 23 Packages: install with ``sudo dnf install <pkg>, ...``

- python3-devel
- liblas-devel
- lapack-devel
- libsndfile-devel
- libpng-devel
- freetype-devel

MacOS Homebrew Packages: install with ``brew intstall <pkg>, ...``

- libsndfile


Once the system dependencies are resolved, the python package requirements can
be found in ``requirements.txt``. A list of helpful packages for development
are also available in ``dev-requirements.txt``. The python requirements can be
installed using ``pip``::

    pip3 install -r requirements.txt
    pip3 install -r dev-requirements.txt


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


.. EOF README
