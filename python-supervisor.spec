%global _empty_manifest_terminate_build 0
Name:		python-supervisor
Version:	4.2.2
Release:	1
Summary:	A system for controlling process state under UNIX
License:	BSD-derived (http://www.repoze.org/LICENSE.txt)
URL:		http://supervisord.org/
Source0:	https://files.pythonhosted.org/packages/d3/7f/c780b7471ba0ff4548967a9f7a8b0bfce222c3a496c3dfad0164172222b0/supervisor-4.2.2.tar.gz
BuildArch:	noarch

Requires:	python3-pytest
Requires:	python3-pytest-cov

%description
Supervisor is a client/server system that allows its users to control a number of processes on UNIX-like operating systems.

%package -n python3-supervisor
Summary:	A system for controlling process state under UNIX
Provides:	python-supervisor
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
%description -n python3-supervisor
Supervisor is a client/server system that allows its users to control a number of processes on UNIX-like operating systems.

%package help
Summary:	Development documents and examples for supervisor
Provides:	python3-supervisor-doc
%description help
Supervisor is a client/server system that allows its users to control a number of processes on UNIX-like operating systems.

%prep
%autosetup -n supervisor-4.2.2

%build
%py3_build

%install
%py3_install
install -d -m755 %{buildroot}/%{_pkgdocdir}
if [ -d doc ]; then cp -arf doc %{buildroot}/%{_pkgdocdir}; fi
if [ -d docs ]; then cp -arf docs %{buildroot}/%{_pkgdocdir}; fi
if [ -d example ]; then cp -arf example %{buildroot}/%{_pkgdocdir}; fi
if [ -d examples ]; then cp -arf examples %{buildroot}/%{_pkgdocdir}; fi
pushd %{buildroot}
if [ -d usr/lib ]; then
	find usr/lib -type f -printf "/%h/%f\n" >> filelist.lst
fi
if [ -d usr/lib64 ]; then
	find usr/lib64 -type f -printf "/%h/%f\n" >> filelist.lst
fi
if [ -d usr/bin ]; then
	find usr/bin -type f -printf "/%h/%f\n" >> filelist.lst
fi
if [ -d usr/sbin ]; then
	find usr/sbin -type f -printf "/%h/%f\n" >> filelist.lst
fi
touch doclist.lst
if [ -d usr/share/man ]; then
	find usr/share/man -type f -printf "/%h/%f.gz\n" >> doclist.lst
fi
popd
mv %{buildroot}/filelist.lst .
mv %{buildroot}/doclist.lst .

%files -n python3-supervisor -f filelist.lst
%dir %{python3_sitelib}/*

%files help -f doclist.lst
%{_docdir}/*

%changelog
* Tue Sep 07 2021 Python_Bot <Python_Bot@openeuler.org> - 4.2.2-1
- Package Spec generated
