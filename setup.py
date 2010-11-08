import os
from setuptools import setup, find_packages

def read_spec_file(fname):
    for line in open(fname):
        if line.startswith('Version:'):
            version=line.strip().split(None, 1)[1]
            return version

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='firewall-compiler',
        version=read_spec_file('ganglia-plugin-varnish.spec'),
        description='Ganglia gmond plugin for Varnish',
        long_description=read('README.rst'),
        author='Lars Kellogg-Stedman',
        author_email='lars@seas.harvard.edu',
        packages=['varnish'],
        )

