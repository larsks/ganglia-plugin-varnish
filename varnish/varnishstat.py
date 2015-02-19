import subprocess
import lxml.etree

import metrics

m_count = 0
m_rate  = 1

forced_metrics = {
        'uptime'        : m_count,
        'n_vcl'         : m_count,
        'n_vcl_avail'   : m_count,
        'n_vcl_discard' : m_count,
        }

class Varnishstat (object):
    def __init__(self, params):
        self.vspath = params.get('VarnishstatPath', 'varnishstat')

    def discover_metrics(self):
        '''This gets a list of the available metrics from Varnish.  It
        attempts to guess the metric type by the presence or absence of the
        "average" field.  You can override this guess in the
        ``forced_metrics`` dictionary.'''

        m = []

        p = subprocess.Popen([self.vspath, '-1'],
            stdout=subprocess.PIPE)

        for line in iter(p.stdout.readline, b''):
            name, val, avg, desc = line.strip().split(None, 3)
            if name in forced_metrics:
                m.append((name, desc, forced_metrics[name]))
            elif avg == '.':
                m.append((name, desc, m_count))
            else:
                m.append((name, desc, m_rate))

        p.communicate()

        return m

    def read_metrics(self):
        '''Read XML output from varnishstat and parse it 
        with lxml.etree.'''

        p = subprocess.Popen([self.vspath, '-1', '-x'],
            stdout=subprocess.PIPE)
        output = p.communicate()[0]

        doc = lxml.etree.fromstring(output)
        for stat in doc.xpath('/varnishstat/stat'):
            name = stat.xpath('name')[0].text
            value = stat.xpath('value')[0].text
            yield(name, int(value))

if __name__ == '__main__':

    v = VarnishStat()

# vim: set ts=4 sw=4 expandtab ai :

