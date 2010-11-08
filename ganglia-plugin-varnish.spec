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

%description
Publish Varnish cache metrics to Gmond.

%prep
%setup -q

%build
%configure
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc

