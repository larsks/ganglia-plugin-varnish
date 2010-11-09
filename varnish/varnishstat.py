import subprocess
import lxml.etree

import metrics

class Varnishstat (object):
    def __init__(self, params):
        self.vspath = params.get('VarnishstatPath', 'varnishstat')

    def discover_metrics(self):
        m = []

        p = subprocess.Popen([self.vspath, '-1'],
            stdout=subprocess.PIPE)
        p.wait()

        for line in p.stdout:
            name, val, avg, desc = line.strip().split(None, 3)
            if avg == '.':
                m.append((name, desc, 'count'))
            else:
                m.append((name, desc, 'rate'))

        return m

    def read_metrics(self):
        '''Read XML output from varnishstat and parse it 
        with lxml.etree.'''

        p = subprocess.Popen([self.vspath, '-1', '-x'],
            stdout=subprocess.PIPE)
        p.wait()

        doc = lxml.etree.fromstring(p.stdout.read())
        for stat in doc.xpath('/varnishstat/stat'):
            name = stat.xpath('name')[0].text
            value = stat.xpath('value')[0].text
            yield(name, int(value))

if __name__ == '__main__':

    v = VarnishStat()

# vim: set ts=4 sw=4 expandtab ai :

