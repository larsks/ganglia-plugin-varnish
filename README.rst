================================
Varnish plugin for Ganglia Gmond
================================

This is a Python plugin for gmond_ that collects statistics from Varnish_.

Installation
============

You will need to have Ganglia's gmond installed, and you will need the
optional Python module support. Under RHEL5/CentOS, the necessary packages
are:

- ganglia-gmond-3.1.7-1
- ganglia-gmond-modules-python-3.1.7-1

To install everything by hand::

  # make install

You may also build an RPM from this package for installation onto
RedHat-ish systems.

Configuration
=============

The makefile install a sample configuration file as
``varnish_plugin.pyconf.sample``.  This may not represent all of the
metrics available from Varnish.  To generate a configuration showing all
available metrics, run::

  /usr/lib/ganglia/python_modules/varnish_plugin.py -M

Note that varnish must be running in order for this to work.  The module
also supports two configuration parameters:

- RefreshRate -- how often to refresh the metrics.  This is the basic
  period for which deltas are calculated.  Default: 60 seconds.

- VarnishstatPath -- Path to ``varnishstat`` executable.  This defaults to
  simply ``varnishstat``, but if it can't be found in ``$PATH`` you can
  provide an explicit path here.

Metrics
=======

This module exposes all of the metrics available from Varnish.  It attempts
to correctly identify the metric type (rate vs. counter) from the output of
``varnishstat``, but this method may not be entirely accurate.  At the
moment it is not possible to override the type determined by these
heuristics.

Support
=======

Please post question/comments/suggestions to the issue tracker:

  https://github.com/larsks/ganglia-plugin-varnish/issues

Author
======

Lars Kellogg-Stedman <lars@oddbit.com>

.. _gmond: http://ganglia.sourceforge.net/
.. _varnish: http://www.varnish-cache.org/

