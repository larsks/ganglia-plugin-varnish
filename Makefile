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
	install -d -m 755 $(DESTDIR)$(libdir)/ganglia/python_modules
	install -m 755 lib/varnish_plugin.py \
		$(DESTDIR)$(libdir)/ganglia/python_modules
	#
	install -d -m 755 $(DESTDIR)$(sysconfdir)/ganglia/conf.d
	install -m 644 varnish_plugin.pyconf \
		$(DESTDIR)$(sysconfdir)/ganglia/conf.d/varnish_plugin.pyconf.sample

