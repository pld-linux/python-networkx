#
# Conditional build:
%bcond_with	doc	# Sphinx documentation, TODO: fix this
%bcond_with	tests	# unit tests (2 failures)

%define		module	networkx
Summary:	High-productivity software for complex networks
Summary(pl.UTF-8):	Efektywne operacje na skomplikowanych grafach
Name:		python-%{module}
Version:	2.2
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/networkx/
Source0:	https://pypi.python.org/packages/source/n/networkx/%{module}-%{version}.zip
# Source0-md5:	82608a3686fb3e61f20cf13bfd3c1b4a
URL:		http://networkx.github.io/index.html
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-decorator >= 4.3
BuildRequires:	python-nose >= 0.10.1
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	unzip
%if %{with doc}
BuildRequires:	python-nb2plots
BuildRequires:	python-sphinx-gallery
BuildRequires:	python-texext
BuildRequires:	sphinx-pdg-2 >= 1.3
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python language software package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.

%description -l pl.UTF-8
Pakiet oprogramowania do tworzenia, manipulacji i badania struktury
dynamiki i funkcji złożonych sieci.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%py_build %{?with_tests:test}

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py_install

%py_postclean

install -d $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python}|'

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{module}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CONTRIBUTORS.rst LICENSE.txt README.rst
%{py_sitescriptdir}/networkx
%{py_sitescriptdir}/networkx-%{version}-py*.egg-info
%{_examplesdir}/python-%{module}-%{version}

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
