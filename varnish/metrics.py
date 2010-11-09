#!/usr/bin/python

import time

DEFAULT = {
        'time_max'      : 120,
        'value_type'    : 'uint',
        'slope'         : 'both',
        'format'        : '%u',
        }

def firstDefined(*args):
    '''There must be a better way of doing this...'''
    for i in args:
        if i is not None:
            return i
    return None

class Metric (object):
    def __init__ (self, name, initval=None, description=None, time_max=None,
            value_type=None, slope=None, format=None, groups=None):
        self.name = name
        self.description = firstDefined(description, name)
        self.time_max = firstDefined(time_max, DEFAULT['time_max'])
        self.value_type = firstDefined(value_type, DEFAULT['value_type'])
        self.slope = firstDefined(slope, DEFAULT['slope'])
        self.format = firstDefined(format, DEFAULT['format'])
        self.groups = firstDefined(groups, '')
        
        # Set initial value.
        self._value = firstDefined(initval, 0)

    def get_descriptor (self):
        return {
                'name':         self.name,
                'description':  self.description,
                'call_back':    self.get_value,
                'time_max':     self.time_max,
                'value_type':   self.value_type,
                'slope':        self.slope,
                'format':       self.format,
                'groups':       self.groups,
                }

    def get_value (self):
        return self._value

    def update(self, v):
        self._value = v

    def refresh(self):
        pass

    value       = property(get_value)
    descriptor  = property(get_descriptor)

class DeltaMetric (Metric):
    '''The value of this metric is the delta between the current and
    previous values.'''
    def __init__(self, name, **kwargs):
        super(DeltaMetric, self).__init__(name, **kwargs)
        self._previous = self._value
        self._value = 0

    def update(self, v):
        self._value = v - self._previous
        self._previous = v

    def refresh(self):
        self.update(self._previous)

class RateMetric (Metric):
    '''The value of this metric is the delta over time between the current
    and previous values.'''
    def __init__(self, name, **kwargs):
        super(RateMetric, self).__init__(name, **kwargs)
        self._time = time.time()
        self._previous = self._value

    def update(self, v):
        now = time.time()
        self._value = (v - self._previous * 1.0)/(now - self._time)
        self._previous = v
        self._time = now

    def refresh(self):
        self.update(self._previous)

