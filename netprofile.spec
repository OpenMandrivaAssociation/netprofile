Name: netprofile
Summary: Manage network profiles
Version: 0.10
Release: %mkrel 3
Source: %{name}-%{version}.tar.bz2
License: GPL
Group: System/Base
BuildArchitectures: noarch
BuildRoot: %{_tmppath}/%{name}-buildroot
Requires: initscripts >= 7.06-13mdk
Requires: diffutils
URL: http://www.mandrivalinux.com/

%description
Manage network profiles

%prep

%setup -q

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std INITDIR=%_initrddir

%clean
rm -rf $RPM_BUILD_ROOT

%post

if [ ! -d /etc/netprofile/profiles/default ]; then
  /sbin/save-netprofile default
fi

%files
%defattr(-,root,root) 
%doc ChangeLog
/sbin/*
%dir /etc/netprofile
%dir /etc/netprofile/profiles
%config(noreplace) /etc/netprofile/list
%config(noreplace) /etc/bash_completion.d/netprofile
/etc/sysconfig/network-scripts/ifup.d/netprofile


