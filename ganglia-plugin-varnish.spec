%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:		ganglia-plugin-varnish
Version:	1
Release:	1%{?dist}
Summary:	Ganglia metric plugin for Varnish.

Group:		SEAS/IRCS
License:	BSD
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

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
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root=$RPM_BUILD_ROOT

install -m 755 -d $RPM_BUILD_ROOT%{_libdir}/ganglia/python_modules/
install -m 755 lib/varnish.py $RPM_BUILD_ROOT%{_libdir}/ganglia/python_modules/
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/ganglia/conf.d/
install -m 644 varnish.pyconf $RPM_BUILD_ROOT%{_sysconfdir}/ganglia/conf.d/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README.rst

%{_sysconfdir}/ganglia/conf.d/varnish.pyconf
%{_libdir}/ganglia/python_modules/varnish.py

%{python_sitelib}/varnish/


