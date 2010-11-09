prefix		= /usr
exec_prefix	= $(prefix)
libdir		= $(prefix)/lib
sysconfdir	= /etc


ifdef DESTDIR
INSTALL_ARGS = --root=$(DESTDIR)
endif

all:
	python setup.py build

install: all
	python setup.py install $(INSTALL_ARGS)
	#
	install -d -m 755 $(DESTDIR)$(libdir)/ganglia/python-modules
	install -m 755 lib/varnishstats.py \
		$(DESTDIR)$(libdir)/ganglia/python-modules
	#
	install -d -m 755 $(DESTDIR)$(sysconfdir)/ganglia/conf.d
	install -m 755 varnishstats.pyconf \
		$(DESTDIR)$(sysconfdir)/ganglia/conf.d/varnishstats.pyconf.sample

