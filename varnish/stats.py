#!/usr/bin/python

import os
import sys
import threading
import time
import signal

import metrics
import varnishstat

class VarnishstatMonitor (threading.Thread):
    '''Collects Varnish statistics using the varnishstat program
    and makes them available to Ganglia via the gmond Python module
    interface.'''

    def __init__ (self, params):
        self.params = params
        self.refresh = int(params.get('RefreshRate', 60))

        self.varnishstat = varnishstat.Varnishstat(params)
        self.discover_metrics()

        self.lock = threading.Lock()
        self.quit = False
        self.quit_c = threading.Condition()

        super(VarnishstatMonitor, self).__init__()

    def discover_metrics(self):
        self.metrics = {}

        for m in self.varnishstat.discover_metrics():
            if m[2] == varnishstat.m_count:
                m_type = metrics.Metric
            else:
                m_type = metrics.RateMetric

            self.metrics[m[0]] = m_type(
                m[0],
                description=m[1],
                groups='varnish',
                time_max=2 * self.refresh)

        # These are metrics we calculate.
        self.metrics['cache_hit_ratio'] = metrics.Metric('cache_hit_ratio',
            value_type='float',
            groups='varnish',
            time_max=2 * self.refresh,
            format='%0.2f')
        self.metrics['cache_hit_pct'] = metrics.Metric('cache_hit_pct',
            value_type='float',
            groups='varnish',
            time_max=2 * self.refresh,
            format='%0.2f')

    def get_descriptors(self):
        return [x.descriptor for x in self.metrics.values()]

    descriptors = property(get_descriptors)

    def update_metrics(self):
        '''Update the in-memory metrics.'''

        for name, value in self.varnishstat.read_metrics():
            if name in self.metrics:
                self.metrics[name].update(value)

        # We need to calculate a few metrics from the raw data.
        try:
            self.metrics['cache_hit_ratio'].update(
                (self.metrics['cache_hit'].value*1.0)/self.metrics['cache_miss'].value)
        except ZeroDivisionError:
            self.metrics['cache_hit_ratio'].update(0)

        try:
            self.metrics['cache_hit_pct'].update(
                (self.metrics['cache_hit'].value*1.0)/self.metrics['client_req'].value * 100)
        except ZeroDivisionError:
            self.metrics['cache_hit_pct'].update(0)

    def run(self):
        '''Loop until somsone calls the stop() method.'''

        while not self.quit:
            self.update_metrics()

            self.quit_c.acquire()
            self.quit_c.wait(self.refresh)
            self.quit_c.release()

    def stop(self):
        '''Stop the monitoring thread.'''

        self.quit = True
        self.quit_c.acquire()
        self.quit_c.notify()
        self.quit_c.release()

        self.join()

if __name__ == '__main__':
    v = VarnishstatMonitor({})

# vim: set ts=4 sw=4 expandtab ai :

