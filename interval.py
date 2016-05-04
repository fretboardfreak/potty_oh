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

"""interval.py: A library for converting musical intervals to useful values."""


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


def add_interval_attribute(obj, key, value):
    """The default method for adding interval attributes to a class."""
    setattr(obj, key, value)


def add_interval_attributes_to_class(class_type, add_func=None):
    """Add attributes to class_type for each musical interval."""
    if not add_func:
        add_func = add_interval_attribute

    for key, value in Interval._property_map.items():
        add_func(class_type, key, value)

    for semitone in range(13):
        key = 'semitone%s' % semitone
        add_func(class_type, key, semitone)


# Add interval attributes to the Interval class itself
add_interval_attributes_to_class(Interval)
