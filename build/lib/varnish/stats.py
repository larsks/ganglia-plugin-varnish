#!/usr/bin/python

import os
import sys
import subprocess
import lxml.etree
import optparse
import threading
import time
import signal

class DeltaDict (dict):
    
    def __setitem__ (self, k, v):
        ov = self.get(k,v)
        dv = v - ov

        super(DeltaDict, self).__setitem__('%s_delta' % k, dv)
        super(DeltaDict, self).__setitem__(k, v)

class VarnishStatMonitor (threading.Thread):
    def __init__ (self, params):
        self._data = DeltaDict()
        self.lock = threading.Lock()

        self.interval = int(params.get('RefreshRate', 60))
        self.quit = False
        self.quit_c = threading.Condition()

        self.generate_descriptors()

        super(VarnishStatMonitor, self).__init__()

    def read_stats(self):
            p = subprocess.Popen(['varnishstat', '-1', '-x'],
                stdout=subprocess.PIPE)
            p.wait()

            doc = lxml.etree.fromstring(p.stdout.read())
            return doc

    def update_metrics(self):
        doc = self.read_stats()

        self.lock.acquire()

        for stat in doc.xpath('/varnishstat/stat'):
            name = stat.xpath('name')[0].text
            value = stat.xpath('value')[0].text
            self._data[name] = int(value)

        self._data['cache_hit_ratio'] = \
            (self._data['cache_hit'] * 1.0) / self._data['cache_miss']
        self._data['cache_hit_pct'] = \
            (self._data['cache_hit'] * 1.0) / self._data['client_req'] * 100

        self.lock.release()

    def run(self):
        while not self.quit:
            self.update_metrics()

            self.quit_c.acquire()
            self.quit_c.wait(self.interval)
            self.quit_c.release()

    def data(self):
        self.lock.acquire()
        x = {}
        for k in self._data.keys():
            x[k] = self._data[k]
        self.lock.release()

        return x

    def stop(self):
        self.quit = True
        self.quit_c.acquire()
        self.quit_c.notify()
        self.quit_c.release()

	self.join()

    def generate_descriptors(self):
        self.descriptors = []

        doc = self.read_stats()
        for stat in doc.xpath('/varnishstat/stat'):
            name = stat.xpath('name')[0].text
            desc = stat.xpath('description')[0].text

            self.descriptors.append({
                'name':         name,
                'description':  desc,
                'call_back':    self.fetch,
                'time_max':     self.interval * 2,
                'value_type':   'uint',
                'slope':        'both',
                'format':       '%u',
                'groups':       'varnish_metrics',
            })

            self.descriptors.append({
                'name':         '%s_delta' % name,
                'description':  '%s (delta)' % desc,
                'call_back':    self.fetch,
                'time_max':     self.interval * 2,
                'value_type':   'uint',
                'slope':        'both',
                'format':       '%u',
                'groups':       'varnish_metrics',
            })

        self.descriptors.append({
                'name':         'cache_hit_ratio',
                'description':  'Cache hit/miss ratio',
                'call_back':    self.fetch,
                'time_max':     self.interval * 2,
                'value_type':   'float',
                'slope':        'both',
                'format':       '%f',
                'groups':       'varnish_metrics',
        })

        self.descriptors.append({
                'name':         'cache_hit_pct',
                'description':  'Cache hit percent',
                'call_back':    self.fetch,
                'time_max':     self.interval * 2,
                'value_type':   'float',
                'slope':        'both',
                'format':       '%f',
                'groups':       'varnish_metrics',
        })

    def fetch(self, name):
        return self.data()[name]

if __name__ == '__main__':
    v = VarnishStatMonitor({})

