#!/usr/bin/env python
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

"""
pitch.py: tools for calculating pitch frequencies.

:TODO: piano key representation (1-80)
"""

import common


class Interval(object):
    """A mapping of interval types to one of the twelve semitones in a key."""
    _intervals = {
        'unison': 0, 'minor_second': 1, 'major_second': 2, 'minor_third': 3,
        'major_third': 4, 'fourth': 5, 'augmented_fourth': 6, 'fifth': 7,
        'minor_sixth': 8, 'major_sixth': 9, 'minor_seventh': 10,
        'major_seventh': 11, 'octave': 12}

    # Should alias 'seventh' be a minor seventh instead? flat 7 is often the
    # intended meaning of "seventh". Or is it just the Minor Domininant 7th
    # chord that use a flat 7?
    _aliases = {
        'second': 2, 'third': 4, 'diminished_fifth': 6,
        'sixth': 9, 'seventh': 11}

    # name -> semitones
    _property_map = _intervals.copy()
    # alias -> semitones
    _property_map.update(_aliases)

    # semitones -> name
    _semitone_map = dict((value, key)
                         for key, value in _intervals.items())

    @classmethod
    def name(cls, interval):
        """Get the string name of an interval."""
        return cls._semitone_map[interval]

    @classmethod
    def max(cls):
        """The highest interval or semitone in an octave."""
        return len(cls._intervals.items()) - 1

    @classmethod
    def min(cls):
        """For completeness."""
        return 0


class TemperamentType(list):
    """A list of interval ratios to represent musical tuning temperament."""
    def __init__(self, multipliers):
        if len(multipliers) != Interval.max() + 1:
            raise TypeError('%s multipliers are required, %s received.' %
                            (Interval.max(), len(multipliers)))
        super(TemperamentType, self).__init__(multipliers)

    @classmethod
    def set_interval_property(cls, name):
        """Set an interval property on the temprement list."""

        def method(cls):
            return cls[getattr(Interval, name)]

        setattr(cls, name, property(method))


# add attributes to the Interval and TemperamentType classes
for key, value in Interval._property_map.items():
    setattr(Interval, key, value)
    TemperamentType.set_interval_property(key)
for semitone in range(13):
    key = 'semitone%s' % semitone
    setattr(Interval, key, semitone)
    TemperamentType.set_interval_property(key)
# clean up after myself
del(key)
del(value)
del(semitone)


class EvenTemperament(TemperamentType):
    """The modern temperament: based on 12 equally spaced tones per octave."""
    def __init__(self):
        multipliers = [pow(2, float(i) / 12.0)
                       for i in range(Interval.max() + 1)]
        super(EvenTemperament, self).__init__(multipliers)


class Temperament(object):
    """A collection of some tuning temperaments used throughout history.

    Other Temperaments to add:

    - equal tempered/12th root tempered (freq=root*pow(2, (semitones/12)))
    - quarter-comma mean tone tempered
    - third-comma mean tone tempered
    """
    even = EvenTemperament()

    pythagorean = TemperamentType(
        [1.0, 256.0/243.0, 9.0/8.0, 32.0/27.0, 81.0/64.0,
         4.0/3.0, 729.0/512.0, 3.0/2.0, 128.0/81.0, 27.0/16.0,
         16.0/9.0, 243.0/128.0, 2.0])

    just = TemperamentType(
        [1.0, 25.0/24.0, 9.0/8.0, 6.0/5.0, 5.0/4.0,
         4.0/3.0, 45.0/32.0, 3.0/2.0, 8.0/5.0, 5.0/3.0,
         9.0/5.0, 15.0/8.0, 2.0])

    @classmethod
    def iter(cls, *args, **kwarsg):
        """Iterate over the set of temperaments."""
        return iter([cls.even, cls.pythagorean, cls.just])


class ReferenceFrequencies(object):
    """A collection of reference frequencies """
    scientific_middle_c = 256

    concert_a4 = 440
    middle_c = 261.626


class Key(object):
    """An object for calculating the note frequencies of musical keys."""

    def __init__(self, root_frequency=ReferenceFrequencies.middle_c,
                 root_name=None,
                 temperament=Temperament.even):
        self.root_frequency = float(root_frequency)
        self.root_name = root_name
        self.temperament = temperament

    def interval(self, semitone, octave=0):
        """Get the frequency of a given interval relative to the root."""
        common.dprint('semitone %s, octave %s :' % (semitone, octave))
        # mod by 'Interval.max() - 1' b/c there are 2 roots in a temperament
        index = semitone % (Interval.max() - 1)
        common.dprint('  interval: %s' % (Interval.name(index)))
        common.dprint('  root ratio: %s' % self.temperament[index])
        octave += semitone // (Interval.max() - 1)
        octave_root = (self.root_frequency *
                       (self.temperament.octave * (octave + 1)))
        common.dprint("  octave root: %s" % octave_root)
        result = octave_root * self.temperament[index]
        common.dprint('  note freq: %s' % result)
        return result


if __name__ == "__main__":
    import waveform
    import wav_file

    DOC = "A demonstration of various musical notes and tunings."

    def main():
        parser = common.get_cmd_line_parser(description=DOC)
        common.ParserArguments.filename(parser)
        common.ParserArguments.length(parser)
        common.ParserArguments.modify_argument(parser, 'length', 'help',
                                               'Length per pitch clip.')
        common.ParserArguments.plot(parser)
        common.ParserArguments.set_defaults(parser, filename='signal.wav',
                                            length=0.75)
        args = parser.parse_args()

        sg = waveform.Generator(length=args.length / 2.0, verbose=args.debug)

        if args.plot:
            raise NotImplemented()
        else:
            even = Key()
            pyth = Key(temperament=Temperament.pythagorean)
            just = Key(temperament=Temperament.just)
            with wav_file.WavFile(args.filename, 1, sg.framerate) as fout:
                for tone in range(Interval.max() + 1):
                    fout.write(sg.sin_constant(even.interval(tone)))
                    fout.write(sg.sin_constant(pyth.interval(tone)))
                    fout.write(sg.sin_constant(just.interval(tone)))

        return 0

    common.call_main(main)
