#!/usr/bin/python

import os
import sys
import optparse
import varnish.stats

METRIC = '''metric {
    # %(description)s (%(value_type)s)
    # display format: %(format)s
    name = "%(name)s"
    value_threshold = 1.0
}'''

def metric_init(params):
    global MONITOR
    MONITOR = varnish.stats.VarnishstatMonitor(params)
    MONITOR.start()

    return MONITOR.descriptors

def metric_cleanup():
    global MONITOR
    MONITOR.stop()

def parse_args():
    p = optparse.OptionParser()
    p.add_option('-M', '--metrics', action='store_true')
    p.add_option('-o', '--option', action='append', default=[])

    return p.parse_args()

def main():
    opts, args = parse_args()

    params = {}
    for pspec in opts.option:
        k,v = pspec.split('=', 1)
        param[k] = v

    v = varnish.stats.VarnishstatMonitor(params)

    if opts.metrics:
        for d in v.descriptors:
            print METRIC % d

if __name__ == '__main__':
    main()

