%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:		ganglia-plugin-varnish
Version:	1
Release:	4%{?dist}
Summary:	Ganglia metric plugin for Varnish.

Group:		System Environment/Base
License:	BSD
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch
BuildRequires:	python-setuptools
Requires:	python-setuptools
Requires:	ganglia-gmond-modules-python
Requires:	ganglia-gmond
Requires:	varnish

%description
Publish Varnish cache metrics to Gmond.

%prep
%setup -q

%build
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT libdir=${_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README.rst

%{_sysconfdir}/ganglia/conf.d/varnishstats.pyconf
%{_libdir}/ganglia/python_modules/varnishstats.py*

%{python_sitelib}/varnish/
%{python_sitelib}/ganglia_plugin_varnish*.egg-info

