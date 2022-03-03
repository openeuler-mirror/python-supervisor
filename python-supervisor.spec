%global _empty_manifest_terminate_build 0
Name:		python-supervisor
Version:	4.2.2
Release:	2
Summary:	A system for controlling process state under UNIX
License:	BSD and MIT
URL:		http://supervisord.org/
Source0:	https://files.pythonhosted.org/packages/d3/7f/c780b7471ba0ff4548967a9f7a8b0bfce222c3a496c3dfad0164172222b0/supervisor-4.2.2.tar.gz
Source1:	supervisord.service
Source2:	supervisord.conf
Source3:	supervisor.logrotate
Source4:	supervisor.tmpfiles
BuildArch:	noarch

Requires:	python3-pytest
Requires:	python3-pytest-cov

%description
Supervisor is a client/server system that allows its users to
control a number of processes on UNIX-like operating systems.

%package -n python3-supervisor
Summary:	A system for controlling process state under UNIX
BuildRequires:	systemd
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
Provides:	python-supervisor
Provides:	supervisor
Recommends:	logrotate
%description -n python3-supervisor
Supervisor is a client/server system that allows its users to
control a number of processes on UNIX-like operating systems.

%package help
Summary:	Development documents and examples for supervisor
Provides:	python3-supervisor-doc
%description help
Supervisor is a client/server system that allows its users to
control a number of processes on UNIX-like operating systems.

%prep
%autosetup -n supervisor-4.2.2

%build
%py3_build

%install
%py3_install

mkdir -p %{buildroot}/%{_sysconfdir}/supervisord.d
mkdir -p %{buildroot}/%{_sysconfdir}/logrotate.d/
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}/%{_localstatedir}/log/%{name}
mkdir -p %{buildroot}/%{_rundir}/%{name}
chmod 755 %{buildroot}/%{_localstatedir}/log/%{name}
install -p -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/supervisord.service
install -p -m 644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/supervisord.conf
install -p -m 644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/logrotate.d/supervisor
install -D -p -m 0644 %{SOURCE4} %{buildroot}%{_tmpfilesdir}/%{name}.conf
sed -i s'/^#!.*//' $( find %{buildroot}/%{python3_sitelib}/supervisor/ -type f)

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

%post
%systemd_post %{name}d.service

%preun
%systemd_preun %{name}d.service

%postun
%systemd_postun %{name}d.service

%files -n python3-supervisor -f filelist.lst
%dir %{python3_sitelib}/*
%license COPYRIGHT.txt LICENSES.txt
%dir %{_localstatedir}/log/%{name}
%{_unitdir}/supervisord.service
%{_tmpfilesdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/supervisord.conf
%dir %{_sysconfdir}/supervisord.d
%dir %{_rundir}/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/supervisor

%files help -f doclist.lst
%{_docdir}/*

%changelog
* Thu Mar 03 2022 Lv Genggeng <lvgenggeng@uniontech.com> - 4.2.2-2
- add service and conf file

* Tue Sep 07 2021 Python_Bot <Python_Bot@openeuler.org> - 4.2.2-1
- Package Spec generated
