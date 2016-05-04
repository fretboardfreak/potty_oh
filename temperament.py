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

"""temperament.py: a library of musical tuning temperaments from history."""

from interval import Interval, add_interval_attributes_to_class


class TemperamentType(list):
    """A list of interval ratios to represent musical tuning temperament."""
    def __init__(self, multipliers):
        if len(multipliers) != Interval.max() + 1:
            raise TypeError('%s multipliers are required, %s received.' %
                            (Interval.max(), len(multipliers)))
        super(TemperamentType, self).__init__(multipliers)

    @staticmethod
    def set_interval_property(cls, name, value):
        """Set an interval property on the temprement list."""

        def method(cls):
            return cls[getattr(Interval, name)]

        setattr(cls, name, property(method))


add_interval_attributes_to_class(TemperamentType,
                                 TemperamentType.set_interval_property)


class EvenTemperament(TemperamentType):
    """The modern temperament: based on 12 equally spaced tones per octave."""
    def __init__(self):
        multipliers = [pow(2, float(i) / 12.0)
                       for i in range(Interval.max() + 1)]
        super(EvenTemperament, self).__init__(multipliers)


class Temperament(object):
    """A collection of some tuning temperaments used throughout history.

    Other Temperaments to add:

    - quarter-comma mean tone tempered
    - third-comma mean tone tempered
    """
    even = EvenTemperament()
    modern = even

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
